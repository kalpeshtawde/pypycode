import { useEffect, useState, useCallback, useMemo, useRef } from "react";
import { useParams, useNavigate, useSearchParams, useLocation } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";
import CodeMirrorEditor from "../components/CodeMirrorEditor";
import type { Problem, Project, Submission, TestCase } from "../types";

const STATUS_LABEL: Record<string, string> = {
  pending: "Queued…",
  running: "Running…",
  accepted: "Accepted",
  wrong_answer: "Wrong Answer",
  time_limit: "Time Limit Exceeded",
  runtime_error: "Runtime Error",
};

type TestCaseRow = {
  index: number;
  passed: boolean;
  input?: string;
  expected?: string;
  got?: string;
  message?: string;
};

function buildTestCaseRows(submission: Submission, testCases?: TestCase[]): TestCaseRow[] {
  const total = Math.max(submission.totalTests || 0, 0);
  if (!total) return [];
  
  // Create map of serialNumber -> input for lookup
  const inputByIndex = new Map<number, string>();
  if (testCases) {
    for (const tc of testCases) {
      inputByIndex.set(tc.serialNumber + 1, tc.input); // +1 because test rows are 1-indexed
    }
  }

  const failedByIndex = new Map<number, Omit<TestCaseRow, "index" | "passed">>();
  // Extract only the Errors: section for parsing (ignore the Output: section)
  const errorsSection = submission.errorOutput?.match(/Errors:\n([\s\S]*)$/i);
  const rawDetails = errorsSection ? errorsSection[1].trim() : "";
  const lines = rawDetails.split("\n");
  let currentIndex: number | null = null;
  let currentChunk: string[] = [];

  const commitChunk = () => {
    if (currentIndex == null) return;
    const chunk = currentChunk.join("\n").trim();
    if (!chunk) return;

    const expectedGotMatch = chunk.match(/^expected\s+(.+),\s*got\s+(.+)$/is);
    if (expectedGotMatch) {
      failedByIndex.set(currentIndex, {
        expected: expectedGotMatch[1].trim(),
        got: expectedGotMatch[2].trim(),
      });
      return;
    }

    failedByIndex.set(currentIndex, { message: chunk });
  };

  for (const line of lines) {
    const testStart = line.match(/^Test\s+(\d+):\s*(.*)$/i);
    if (testStart) {
      commitChunk();
      currentIndex = Number(testStart[1]);
      currentChunk = [testStart[2] || ""];
      continue;
    }

    if (currentIndex != null) {
      currentChunk.push(line);
    }
  }
  commitChunk();

  const rows: TestCaseRow[] = [];
  for (let index = 1; index <= total; index += 1) {
    const parsedFailure = failedByIndex.get(index);
    // A test is failed only if the sandbox explicitly reported it in the error string
    const passed = !parsedFailure;

    rows.push({
      index,
      passed,
      input: inputByIndex.get(index),
      expected: parsedFailure?.expected,
      got: parsedFailure?.got,
      message: parsedFailure?.message,
    });
  }

  return rows;
}

function extractOutputTail(errorOutput: string | null | undefined, maxLines: number = 10): string | null {
  if (!errorOutput) return null;

  // Extract only the Output: section, stopping before Errors: or end of string
  const match = errorOutput.match(/Output:\n([\s\S]*?)(?=\nErrors:|$)/i);
  if (!match) return null;

  const content = match[1].trim();
  if (!content) return null;

  const lines = content
    .split("\n")
    .map((line) => line.trimEnd())
    .filter((line) => line.length > 0);

  if (!lines.length) return null;
  return lines.slice(-maxLines).join("\n");
}

export default function ProblemPage() {
  const { slug } = useParams<{ slug: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const { token } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const authLink = `/auth?redirect=${encodeURIComponent(`${location.pathname}${location.search}`)}`;

  const [problem, setProblem] = useState<Problem | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<string>(
    () => searchParams.get("projectId") ?? ""
  );
  const [code, setCode] = useState("");
  const codeLoadedRef = useRef(false);
  const saveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [submission, setSubmission] = useState<Submission | null>(null);
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [lastSuccessfulRunCode, setLastSuccessfulRunCode] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"description" | "submissions">("description");
  const [fontSize, setFontSize] = useState(15);
  const [vimMode, setVimMode] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [expandedTest, setExpandedTest] = useState<number | null>(null);
  const [isFavorite, setIsFavorite] = useState(false);
  const [isCheckingFavorite, setIsCheckingFavorite] = useState(false);

  useEffect(() => {
    if (!slug) return;
    codeLoadedRef.current = false;
    api.get<Problem>(`/problems/${slug}`).then((p) => {
      setProblem(p);
      // Load saved code from localStorage, or fall back to starter code
      const savedCode = localStorage.getItem(`pypycode:code:${p.slug}`);
      setCode(savedCode || p.starterCode);
      codeLoadedRef.current = true;
    });
  }, [slug]);

  useEffect(() => {
    if (!problem?.id || !token) {
      setIsFavorite(false);
      return;
    }
    setIsCheckingFavorite(true);
    api.get<{ isFavorite: boolean }>(`/favorites/check/${problem.id}`, token)
      .then((data) => setIsFavorite(data.isFavorite))
      .catch(() => setIsFavorite(false))
      .finally(() => setIsCheckingFavorite(false));
  }, [problem?.id, token]);

  useEffect(() => {
    if (!token) {
      setProjects([]);
      setSelectedProjectId("");
      return;
    }

    api.get<Project[]>("/projects/", token)
      .then((data) => {
        const sorted = [...data].sort((a, b) => {
          if (a.isDefault === b.isDefault) {
            return a.name.localeCompare(b.name);
          }
          return a.isDefault ? -1 : 1;
        });
        setProjects(sorted);
        setSelectedProjectId((current) => {
          if (current && sorted.some((project) => project.id === current)) {
            return current;
          }
          const fromUrl = searchParams.get("projectId") ?? "";
          if (fromUrl && sorted.some((project) => project.id === fromUrl)) {
            return fromUrl;
          }
          const defaultProject = sorted.find((project) => project.isDefault) ?? sorted[0];
          return defaultProject?.id ?? "";
        });
      })
      .catch(() => {
        setProjects([]);
      });
  }, [token, searchParams]);

  useEffect(() => {
    const params = new URLSearchParams(searchParams);
    if (selectedProjectId) {
      params.set("projectId", selectedProjectId);
    } else {
      params.delete("projectId");
    }
    if (params.toString() !== searchParams.toString()) {
      setSearchParams(params, { replace: true });
    }
  }, [selectedProjectId, searchParams, setSearchParams]);

  useEffect(() => {
    if (!slug || !problem) return;
    if (!token) {
      setSubmission(null);
      // Only reset code if we haven't loaded from localStorage yet
      if (!codeLoadedRef.current) {
        setCode(problem.starterCode);
      }
      return;
    }

    const suffix = selectedProjectId
      ? `?projectId=${encodeURIComponent(selectedProjectId)}`
      : "";
    api.get<Array<{ id: number; status: string; passedTests: number; totalTests: number; runtimeMs: number | null; memoryKb: number | null; code: string; createdAt: string }>>(
      `/submissions/problem/${slug}${suffix}`,
      token
    )
      .then((submissions) => {
        if (submissions.length > 0) {
          const latestSubmission = submissions[0];
          setSubmission({
            id: latestSubmission.id,
            status: latestSubmission.status as any,
            passedTests: latestSubmission.passedTests,
            totalTests: latestSubmission.totalTests,
            runtimeMs: latestSubmission.runtimeMs,
            memoryKb: latestSubmission.memoryKb,
            errorOutput: null,
            createdAt: latestSubmission.createdAt,
          });
          setCode(latestSubmission.code);
          setLastSuccessfulRunCode(null);
          return;
        }

        setSubmission(null);
        if (!codeLoadedRef.current) {
          setCode(problem.starterCode);
        }
        setLastSuccessfulRunCode(null);
      })
      .catch(() => {
        setSubmission(null);
        if (!codeLoadedRef.current) {
          setCode(problem.starterCode);
        }
        setLastSuccessfulRunCode(null);
      });
  }, [slug, token, selectedProjectId, problem]);

  const poll = useCallback((id: number) => {
    const interval = setInterval(async () => {
      try {
        const sub = await api.get<Submission>(`/submissions/${id}`, token);
        setSubmission(sub);
        if (sub.status !== "pending" && sub.status !== "running") {
          clearInterval(interval);
          setSubmitting(false);
        }
      } catch {
        clearInterval(interval);
        setSubmitting(false);
      }
    }, 1200);
    return () => clearInterval(interval);
  }, [token]);

  const handleRun = async () => {
    if (!token) { navigate(authLink); return; }
    if (!problem) return;
    setRunning(true);
    setSubmission(null);
    setLastSuccessfulRunCode(null);
    try {
      const result = await api.post<{
        status: Submission["status"];
        passedTests: number;
        totalTests: number;
        runtimeMs: number | null;
        memoryKb: number | null;
        errorOutput: string | null;
      }>(
        "/submissions/run",
        { problemSlug: problem.slug, code, projectId: selectedProjectId || undefined },
        token
      );

      setSubmission({
        id: 0,
        status: result.status,
        passedTests: result.passedTests,
        totalTests: result.totalTests,
        runtimeMs: result.runtimeMs,
        memoryKb: result.memoryKb,
        errorOutput: result.errorOutput,
        createdAt: new Date().toISOString(),
      });

      if (result.status === "accepted") {
        setLastSuccessfulRunCode(code);
      }
    } catch (e: unknown) {
      alert(e instanceof Error ? e.message : "Run failed");
    } finally {
      setRunning(false);
    }
  };

  const handleSubmit = async () => {
    if (!token) { navigate(authLink); return; }
    if (!problem) return;
    if (lastSuccessfulRunCode !== code) return;
    setSubmitting(true);
    setSubmission(null);
    try {
      const { id } = await api.post<{ id: number }>(
        "/submissions/",
        { problemSlug: problem.slug, code, projectId: selectedProjectId || undefined },
        token
      );
      setSubmission({ id, status: "pending", passedTests: 0, totalTests: 0, runtimeMs: null, memoryKb: null, errorOutput: null, createdAt: new Date().toISOString() });
      poll(id);
    } catch (e: unknown) {
      setSubmitting(false);
      alert(e instanceof Error ? e.message : "Submission failed");
    }
  };

  const handleToggleFavorite = async () => {
    if (!token) { navigate(authLink); return; }
    if (!problem || isCheckingFavorite) return;

    try {
      if (isFavorite) {
        await api.delete(`/favorites/${problem.id}`, token);
        setIsFavorite(false);
        setToastMessage("Removed from favorites");
      } else {
        await api.post("/favorites/", { problemId: problem.id }, token);
        setIsFavorite(true);
        setToastMessage("Added to favorites");
      }
      setTimeout(() => setToastMessage(null), 2500);
    } catch (e: unknown) {
      setToastMessage(e instanceof Error ? e.message : "Failed to update favorite");
      setTimeout(() => setToastMessage(null), 2500);
    }
  };

  const testRows = useMemo(() => (submission ? buildTestCaseRows(submission, problem?.testCases) : []), [submission, problem?.testCases]);
  const outputTail = useMemo(() => extractOutputTail(submission?.errorOutput), [submission?.errorOutput]);

  useEffect(() => {
    setExpandedTest(null);
  }, [submission?.id, submission?.status, submission?.createdAt]);

  if (!problem) {
    return <div className="flex items-center justify-center h-64 text-slate-600 font-mono">Loading…</div>;
  }

  const statusOk = submission?.status === "accepted";
  const statusDone = submission && !["pending", "running"].includes(submission.status);
  const canSubmit = !running && !submitting && !!lastSuccessfulRunCode && lastSuccessfulRunCode === code;

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] bg-slate-50 relative overflow-hidden">
      <div className="fixed top-16 left-0 right-0 flex items-center justify-between border-b border-slate-200 bg-slate-50 px-4 py-3 z-40">
        <div className="flex items-center">
          {(["description", "submissions"] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-5 py-2.5 text-sm font-body capitalize transition-colors border-b-2 ${
                activeTab === tab
                  ? "border-accent text-slate-900"
                  : "border-transparent text-slate-600 hover:text-slate-900"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <select
            value={selectedProjectId}
            onChange={(e) => setSelectedProjectId(e.target.value)}
            disabled={!token || projects.length === 0 || submitting}
            className="px-3 py-1.5 text-sm font-mono border border-emerald-200 rounded-lg bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 disabled:bg-slate-100 disabled:text-slate-400 min-w-[190px]"
          >
            {!token && <option value="">Sign in to select project</option>}
            {token && projects.length === 0 && <option value="">No projects</option>}
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>

          <button
            onClick={handleRun}
            disabled={running || submitting}
            className={`btn-primary text-sm py-1.5 px-4 flex items-center gap-1.5 ${(running || submitting) ? "opacity-60 cursor-not-allowed" : ""}`}
          >
            <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path d="M6 4.75A.75.75 0 0 1 7.19 4.14l7.5 5.25a.75.75 0 0 1 0 1.22l-7.5 5.25A.75.75 0 0 1 6 15.25v-10.5Z" />
            </svg>
            {running ? "Running..." : "Run"}
          </button>

          <button
            onClick={handleSubmit}
            disabled={!canSubmit}
            className={`text-sm py-1.5 px-5 rounded-lg bg-indigo-600 text-white transition-colors ${canSubmit ? "hover:bg-indigo-700" : "opacity-60 cursor-not-allowed"}`}
          >
            {submitting ? (
              <span className="flex items-center gap-2">
                <svg className="w-3 h-3 animate-spin-slow" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="32" strokeDashoffset="12" />
                </svg>
                Submitting...
              </span>
            ) : "Submit"}
          </button>
        </div>
      </div>

      <div className="flex flex-1 min-h-0 pt-[62px]">
      {/* Left: Problem panel */}
      <div className="w-[42%] flex flex-col border-r border-slate-200 overflow-hidden bg-slate-50">
        <div className="overflow-y-auto flex-1 p-6">
          {activeTab === "description" ? (
            <>
              {/* Title + badge */}
              <div className="mb-8">
                <div className="flex items-center gap-3 mb-4">
                  <h1 className="text-5xl font-black text-slate-900" style={{ fontSize: '42px', fontWeight: 900, letterSpacing: '-0.02em' }}>
                    {problem.title}
                  </h1>
                  <button
                    onClick={handleToggleFavorite}
                    disabled={!token || isCheckingFavorite}
                    className={`p-2 rounded-full transition-all duration-200 ${
                      !token
                        ? "opacity-40 cursor-not-allowed"
                        : "hover:bg-slate-100 active:scale-95 cursor-pointer"
                    }`}
                    title={!token ? "Sign in to add favorites" : (isFavorite ? "Remove from favorites" : "Add to favorites")}
                  >
                    {isCheckingFavorite ? (
                      <svg className="w-8 h-8 animate-spin text-slate-400" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" strokeDasharray="32" strokeDashoffset="12" />
                      </svg>
                    ) : (
                      <svg
                        className={`w-8 h-8 transition-all duration-200 ${
                          isFavorite ? "fill-yellow-400 stroke-yellow-500" : "fill-none stroke-slate-400 hover:stroke-slate-600"
                        }`}
                        viewBox="0 0 24 24"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                      </svg>
                    )}
                  </button>
                </div>
                <div className="flex items-center gap-3 flex-wrap">
                  <span 
                    className="inline-flex items-center px-3.5 py-1.5 rounded-full text-white font-bold text-sm"
                    style={{
                      background: 'linear-gradient(135deg, #34D399, #10B981)',
                      boxShadow: '0 2px 8px rgba(16, 185, 129, 0.3)',
                      fontSize: '13px',
                      fontWeight: 700,
                      padding: '5px 14px'
                    }}
                  >
                    ✦ {problem.difficulty.charAt(0).toUpperCase() + problem.difficulty.slice(1)}
                  </span>
                  {problem.tags.map((t) => (
                    <span 
                      key={t} 
                      className="inline-flex px-3 py-1.5 rounded-full text-sm font-semibold"
                      style={{
                        backgroundColor: '#EEF3FF',
                        color: '#1A6BFF',
                        fontSize: '12px',
                        fontWeight: 600,
                        padding: '5px 13px',
                        border: '1px solid rgba(26, 107, 255, 0.18)'
                      }}
                    >
                      {t}
                    </span>
                  ))}
                </div>
              </div>

              {/* Problem Statement */}
              <div style={{ marginBottom: '32px' }}>
                <div className="flex items-center gap-2.5" style={{ marginBottom: '16px' }}>
                  <div 
                    style={{
                      width: '3px',
                      height: '20px',
                      backgroundColor: '#10B981',
                      borderRadius: '2px'
                    }}
                  />
                  <h2 style={{
                    fontWeight: 700,
                    fontSize: '18px',
                    color: '#0F172A',
                    margin: 0
                  }}>
                    Problem Statement
                  </h2>
                </div>
                <div 
                  className="prose prose-sm max-w-none prose-p:before:content-none prose-p:after:content-none"
                  style={{
                    fontSize: '17px',
                    lineHeight: '1.8',
                    color: '#475569',
                    backgroundColor: '#F8FAFC',
                    padding: '20px',
                    borderRadius: '12px',
                    border: '1px solid #E2E8F0'
                  }}
                >
                  <style>{`
                    .prose p {
                      font-size: 17px !important;
                      line-height: 1.8 !important;
                      color: #475569 !important;
                      margin-bottom: 12px !important;
                    }
                    .prose p:last-child {
                      margin-bottom: 0 !important;
                    }
                    .prose strong {
                      color: #0F172A !important;
                      font-weight: 600 !important;
                    }
                    .prose code {
                      background-color: #EEF3FF !important;
                      color: #1A6BFF !important;
                      font-weight: 600 !important;
                      border-radius: 5px !important;
                      padding: 2px 7px !important;
                      border: 1px solid rgba(26, 107, 255, 0.15) !important;
                      font-family: inherit !important;
                    }
                    .prose code::before {
                      content: '' !important;
                    }
                    .prose code::after {
                      content: '' !important;
                    }
                  `}</style>
                  <ReactMarkdown>
                    {problem.description.split('\n').reduce((acc: string, line: string, idx: number, arr: string[]) => {
                      const constraintIdx = arr.findIndex((l: string) => l.toLowerCase().includes('constraint'));
                      if (constraintIdx !== -1 && idx >= constraintIdx) return acc;
                      return acc + (acc && line ? '\n' : '') + line;
                    }, '')}
                  </ReactMarkdown>
                </div>
              </div>

              {/* Constraints */}
              {(() => {
                const lines = problem.description.split('\n');
                const constraintsStartIdx = lines.findIndex((line: string) => line.toLowerCase().includes('constraint'));
                
                let constraintLines: string[] = [];
                if (constraintsStartIdx !== -1) {
                  for (let i = constraintsStartIdx + 1; i < lines.length; i++) {
                    const line = lines[i];
                    if (line.trim() === '') continue;
                    if (line.match(/^#+\s/)) break;
                    constraintLines.push(line);
                  }
                }
                
                const constraints = constraintLines
                  .filter((line: string) => line.trim() && (line.includes('`') || line.startsWith('•') || line.startsWith('-')))
                  .map((line: string) => {
                    const match = line.match(/`([^`]+)`/g);
                    return match ? match.map((m: string) => m.replace(/`/g, '')) : [line.replace(/^[•\-]\s*/, '').trim()];
                  })
                  .flat()
                  .filter((c: string, i: number, arr: string[]) => arr.indexOf(c) === i);

                return constraints.length > 0 ? (
                  <div style={{ marginBottom: '32px' }}>
                    <div className="flex items-center gap-2.5" style={{ marginBottom: '16px' }}>
                      <div 
                        style={{
                          width: '3px',
                          height: '20px',
                          backgroundColor: '#F59E0B',
                          borderRadius: '2px'
                        }}
                      />
                      <h2 style={{
                        fontWeight: 700,
                        fontSize: '18px',
                        color: '#0F172A',
                        margin: 0
                      }}>
                        Constraints
                      </h2>
                    </div>
                    <div style={{
                      backgroundColor: '#FFFBEB',
                      border: '1px solid #FEE3B1',
                      borderRadius: '12px',
                      padding: '20px',
                      display: 'grid',
                      gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                      gap: '12px'
                    }}>
                      {constraints.map((constraint: string, i: number) => (
                        <div 
                          key={i}
                          style={{
                            backgroundColor: 'white',
                            border: '1px solid #FCD34D',
                            borderRadius: '8px',
                            padding: '12px 14px',
                            fontSize: '14px',
                            color: '#475569',
                            fontFamily: 'monospace',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px'
                          }}
                        >
                          <span style={{ color: '#F59E0B', fontWeight: 700 }}>•</span>
                          <span>{constraint}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : null;
              })()}

              {/* Examples */}
              <div className="mt-10 space-y-6">
                <div className="flex items-center gap-2.5" style={{ marginBottom: '24px' }}>
                  <div 
                    style={{
                      width: '3px',
                      height: '18px',
                      backgroundColor: '#1A6BFF',
                      borderRadius: '2px'
                    }}
                  />
                  <h3 style={{
                    fontWeight: 700,
                    fontSize: '16px',
                    color: '#0F172A',
                    margin: 0
                  }}>
                    Examples
                  </h3>
                </div>

                {problem.examples.map((ex, i) => (
                  <div 
                    key={i} 
                    style={{
                      backgroundColor: 'white',
                      borderRadius: '16px',
                      border: '1px solid #E2E8F0',
                      boxShadow: '0 4px 24px rgba(15, 23, 42, 0.07)',
                      padding: '22px'
                    }}
                  >
                    {/* Example number circle and label */}
                    <div className="flex items-center gap-3 mb-5">
                      <div
                        style={{
                          width: '34px',
                          height: '34px',
                          borderRadius: '50%',
                          background: `linear-gradient(135deg, #1A6BFF, #6366F1)`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                          fontWeight: 800,
                          fontSize: '16px'
                        }}
                      >
                        {i + 1}
                      </div>
                      <span style={{
                        fontWeight: 600,
                        fontSize: '13px',
                        color: '#94A3B8'
                      }}>
                        Example
                      </span>
                    </div>

                    {/* Input section */}
                    <div style={{ marginBottom: '16px' }}>
                      <div style={{
                        textTransform: 'uppercase',
                        letterSpacing: '0.08em',
                        fontSize: '11px',
                        color: '#94A3B8',
                        fontWeight: 600,
                        marginBottom: '8px'
                      }}>
                        Input
                      </div>
                      <div style={{
                        backgroundColor: '#EEF3FF',
                        borderLeft: '3px solid #1A6BFF',
                        borderRadius: '10px',
                        padding: '12px 16px',
                        fontSize: '14px',
                        color: '#0F172A',
                        fontFamily: 'inherit',
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word'
                      }}>
                        {ex.input}
                      </div>
                    </div>

                    {/* Output section */}
                    <div style={{ marginBottom: ex.explanation ? '16px' : 0 }}>
                      <div style={{
                        textTransform: 'uppercase',
                        letterSpacing: '0.08em',
                        fontSize: '11px',
                        color: '#94A3B8',
                        fontWeight: 600,
                        marginBottom: '8px'
                      }}>
                        Output
                      </div>
                      <div style={{
                        backgroundColor: '#ECFDF5',
                        borderLeft: '3px solid #10B981',
                        borderRadius: '10px',
                        padding: '12px 16px',
                        fontSize: '14px',
                        color: '#0F172A',
                        fontFamily: 'inherit',
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word'
                      }}>
                        {ex.output}
                      </div>
                    </div>

                    {/* Explanation */}
                    {ex.explanation && (
                      <div style={{
                        fontStyle: 'italic',
                        fontSize: '13px',
                        color: '#94A3B8',
                        marginTop: '12px',
                        paddingTop: '12px',
                        borderTop: '1px solid #E2E8F0'
                      }}>
                        <span style={{ color: '#1A6BFF' }}>✦ </span>
                        {ex.explanation}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="text-center py-16 text-slate-500 font-mono text-sm">
              {!token ? (
                <p>Sign in to see your submissions.</p>
              ) : (
                <p>No submissions yet for this problem.</p>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Right: Editor + output */}
      <div className="flex-1 flex flex-col overflow-hidden bg-slate-50">
        {/* Editor toolbar */}
        <div 
          className="shrink-0 flex items-center border-b"
          style={{
            height: '44px',
            backgroundColor: '#F8FAFC',
            borderBottomColor: '#E2E8F0',
            padding: '0 20px',
            gap: '20px'
          }}
        >
          <style>{`
            .font-size-slider {
              width: 100px;
              height: 4px;
              background: #E2E8F0;
              border-radius: 999px;
              outline: none;
              -webkit-appearance: none;
              appearance: none;
            }
            .font-size-slider::-webkit-slider-thumb {
              -webkit-appearance: none;
              appearance: none;
              width: 14px;
              height: 14px;
              background: #1A6BFF;
              border-radius: 50%;
              cursor: pointer;
            }
            .font-size-slider::-moz-range-thumb {
              width: 14px;
              height: 14px;
              background: #1A6BFF;
              border-radius: 50%;
              cursor: pointer;
              border: none;
            }
            .vim-toggle-track {
              width: 36px;
              height: 20px;
              border-radius: 999px;
              background: #E2E8F0;
              cursor: pointer;
              transition: background 200ms ease;
              position: relative;
              display: inline-flex;
              align-items: center;
            }
            .vim-toggle-track.active {
              background: #1A6BFF;
            }
            .vim-toggle-thumb {
              width: 16px;
              height: 16px;
              background: white;
              border-radius: 50%;
              box-shadow: 0 1px 3px rgba(0,0,0,0.15);
              position: absolute;
              left: 2px;
              transition: left 200ms ease;
            }
            .vim-toggle-track.active .vim-toggle-thumb {
              left: 18px;
            }
          `}</style>

          {/* Font Size Slider */}
          <div className="flex items-center gap-2">
            <label style={{ fontSize: '12px', fontWeight: 600, color: '#64748B' }}>
              Font Size
            </label>
            <input
              type="range"
              min="12"
              max="24"
              step="1"
              value={fontSize}
              onChange={(e) => setFontSize(Number(e.target.value))}
              className="font-size-slider"
            />
            <div
              style={{
                backgroundColor: '#EEF3FF',
                color: '#1A6BFF',
                fontWeight: 600,
                fontSize: '11px',
                padding: '2px 7px',
                borderRadius: '999px',
                minWidth: '35px',
                textAlign: 'center'
              }}
            >
              {fontSize}px
            </div>
          </div>

          {/* Divider */}
          <div style={{
            width: '1px',
            height: '20px',
            backgroundColor: '#E2E8F0',
            margin: '0 4px'
          }} />

          {/* Vim Mode Toggle */}
          <div className="flex items-center gap-2">
            <label style={{ fontSize: '12px', fontWeight: 600, color: '#64748B' }}>
              Vim
            </label>
            <button
              onClick={() => {
                setVimMode(!vimMode);
                const message = !vimMode ? 'Vim mode enabled' : 'Vim mode disabled';
                setToastMessage(message);
                setTimeout(() => setToastMessage(null), 2500);
              }}
              className={`vim-toggle-track ${vimMode ? 'active' : ''}`}
              title="Toggle Vim mode"
            >
              <div className="vim-toggle-thumb" />
            </button>
            {vimMode && (
              <div
                style={{
                  backgroundColor: '#1A6BFF',
                  color: 'white',
                  fontSize: '10px',
                  fontWeight: 700,
                  padding: '2px 6px',
                  borderRadius: '4px'
                }}
              >
                VIM
              </div>
            )}
          </div>
        </div>

        {/* CodeMirror Editor */}
        <div className="flex-1 overflow-auto bg-slate-50">
          <CodeMirrorEditor
            value={code}
            onChange={(newCode) => {
              setCode(newCode);
              // Debounce localStorage save to avoid typing lag
              if (problem?.slug) {
                if (saveTimeoutRef.current) {
                  clearTimeout(saveTimeoutRef.current);
                }
                saveTimeoutRef.current = setTimeout(() => {
                  localStorage.setItem(`pypycode:code:${problem.slug}`, newCode);
                }, 500);
              }
            }}
            fontSize={fontSize}
            vimMode={vimMode}
          />
        </div>

        {/* Result panel */}
        {submission && (
          <div className="shrink-0 border-t border-slate-200 bg-slate-50 text-sm max-h-[45vh] overflow-y-auto">
            <div className="flex items-center justify-between gap-3 px-4 py-3 border-b border-slate-200 bg-white/75">
              <div className="flex items-center gap-3 min-w-0">
                <span
                  className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold font-mono border ${
                    statusOk
                      ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                      : statusDone
                        ? "bg-red-50 text-red-700 border-red-200"
                        : "bg-slate-100 text-slate-700 border-slate-200"
                  }`}
                >
                  {statusOk ? "✓" : statusDone ? "✗" : "•"}&nbsp;
                  {STATUS_LABEL[submission.status] ?? submission.status}
                </span>
                <span className="text-slate-600 font-mono text-xs">
                  {submission.passedTests}/{submission.totalTests} tests passed
                </span>
              </div>
              <span className="text-slate-500 font-mono text-xs whitespace-nowrap">
                {submission.runtimeMs != null ? `${Math.round(submission.runtimeMs)}ms` : "—"}
              </span>
            </div>

            {statusDone && testRows.length > 0 ? (
              <div className="px-4 py-3 space-y-2 max-h-72 overflow-auto">
                {testRows.map((row) => {
                  const isExpanded = expandedTest === row.index;
                  return (
                    <div
                      key={row.index}
                      className={`rounded-lg border ${row.passed ? "border-emerald-100 bg-emerald-50/45" : "border-red-100 bg-red-50/45"}`}
                    >
                      <button
                        type="button"
                        onClick={() => setExpandedTest((current) => (current === row.index ? null : row.index))}
                        className="w-full flex items-center justify-between px-3 py-2.5 text-left"
                      >
                        <div className="flex items-center gap-2.5">
                          <span className={`text-sm font-bold ${row.passed ? "text-emerald-600" : "text-red-600"}`}>
                            {row.passed ? "✓" : "✗"}
                          </span>
                          <span className="text-sm font-mono text-slate-700">Test {row.index}</span>
                        </div>
                        <span
                          className="text-slate-400 text-xs"
                          style={{
                            transform: isExpanded ? "rotate(180deg)" : "rotate(0deg)",
                            transition: "transform 180ms ease",
                          }}
                        >
                          ▼
                        </span>
                      </button>

                      <div
                        style={{
                          maxHeight: isExpanded ? "500px" : "0px",
                          opacity: isExpanded ? 1 : 0,
                          overflow: "hidden",
                          transition: "max-height 300ms ease, opacity 180ms ease",
                        }}
                      >
                        <div className="px-3 pb-3 pt-1 space-y-2 border-t border-slate-200/70">
                          {row.input && (
                            <div>
                              <div className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 mb-1">Input:</div>
                              <pre className="text-xs font-mono text-slate-700 bg-slate-100 border border-slate-200 rounded-md px-2.5 py-2 overflow-auto whitespace-pre-wrap">
                                {row.input}
                              </pre>
                            </div>
                          )}
                          {row.expected !== undefined && (
                            <div>
                              <div className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 mb-1">Expected:</div>
                              <pre className="text-xs font-mono text-slate-700 bg-slate-100 border border-slate-200 rounded-md px-2.5 py-2 overflow-auto whitespace-pre-wrap">
                                {row.expected}
                              </pre>
                            </div>
                          )}
                          <div>
                            <div className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 mb-1">
                              {row.got !== undefined ? "Got:" : "Details:"}
                            </div>
                            <pre className="text-xs font-mono text-slate-700 bg-slate-100 border border-slate-200 rounded-md px-2.5 py-2 overflow-auto whitespace-pre-wrap">
                              {row.got ?? row.message ?? "Passed"}
                            </pre>
                          </div>
                          {!row.passed && outputTail && (
                            <div>
                              <div className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 mb-1">
                                Output (last lines):
                              </div>
                              <pre className="text-xs font-mono text-slate-700 bg-slate-100 border border-slate-200 rounded-md px-2.5 py-2 overflow-auto whitespace-pre-wrap">
                                {outputTail}
                              </pre>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : submission.errorOutput ? (
              <div className="px-4 py-3">
                <pre className="text-xs font-mono text-red-700 bg-red-50 border border-red-100 rounded-lg p-3 overflow-auto max-h-32 whitespace-pre-wrap">
                  {submission.errorOutput}
                </pre>
              </div>
            ) : (
              <div className="px-4 py-3 text-xs font-mono text-slate-500">Running tests...</div>
            )}
          </div>
        )}
      </div>
      </div>

      {/* Toast Notification */}
      {toastMessage && (
        <div
          style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            backgroundColor: '#0F172A',
            color: 'white',
            padding: '10px 18px',
            borderRadius: '10px',
            fontSize: '13px',
            animation: 'slideUp 300ms ease forwards',
            zIndex: 1000
          }}
        >
          <style>{`
            @keyframes slideUp {
              from {
                transform: translateY(20px);
                opacity: 0;
              }
              to {
                transform: translateY(0);
                opacity: 1;
              }
            }
          `}</style>
          {toastMessage}
        </div>
      )}
    </div>
  );
}
