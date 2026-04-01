import { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Editor from "@monaco-editor/react";
import ReactMarkdown from "react-markdown";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";
import type { Problem, Submission } from "../types";

const STATUS_LABEL: Record<string, string> = {
  pending: "Queued…",
  running: "Running…",
  accepted: "Accepted",
  wrong_answer: "Wrong Answer",
  time_limit: "Time Limit Exceeded",
  runtime_error: "Runtime Error",
};

export default function ProblemPage() {
  const { slug } = useParams<{ slug: string }>();
  const { token } = useAuthStore();
  const navigate = useNavigate();

  const [problem, setProblem] = useState<Problem | null>(null);
  const [code, setCode] = useState("");
  const [submission, setSubmission] = useState<Submission | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [activeTab, setActiveTab] = useState<"description" | "submissions">("description");

  useEffect(() => {
    if (!slug) return;
    api.get<Problem>(`/problems/${slug}`).then((p) => {
      setProblem(p);
      setCode(p.starterCode);
    });
  }, [slug]);

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

  const handleSubmit = async () => {
    if (!token) { navigate("/auth"); return; }
    if (!problem) return;
    setSubmitting(true);
    setSubmission(null);
    try {
      const { id } = await api.post<{ id: number }>(
        "/submissions/",
        { problemSlug: problem.slug, code },
        token
      );
      setSubmission({ id, status: "pending", passedTests: 0, totalTests: 0, runtimeMs: null, memoryKb: null, errorOutput: null, createdAt: new Date().toISOString() });
      poll(id);
    } catch (e: unknown) {
      setSubmitting(false);
      alert(e instanceof Error ? e.message : "Submission failed");
    }
  };

  if (!problem) {
    return <div className="flex items-center justify-center h-64 text-slate-600 font-mono">Loading…</div>;
  }

  const statusOk = submission?.status === "accepted";
  const statusDone = submission && !["pending", "running"].includes(submission.status);

  return (
    <div className="flex h-[calc(100vh-64px)]">
      {/* Left: Problem panel */}
      <div className="w-[42%] flex flex-col border-r border-surface-border overflow-hidden">
        {/* Tabs */}
        <div className="flex border-b border-surface-border shrink-0">
          {(["description", "submissions"] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-5 py-3 text-sm font-body capitalize transition-colors border-b-2 ${
                activeTab === tab
                  ? "border-accent text-white"
                  : "border-transparent text-slate-500 hover:text-slate-300"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="overflow-y-auto flex-1 p-6">
          {activeTab === "description" ? (
            <>
              {/* Title + badge */}
              <div className="flex items-start gap-3 mb-6">
                <div>
                  <h1 className="font-display text-2xl font-semibold text-white mb-2">{problem.title}</h1>
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className={`badge-${problem.difficulty}`}>{problem.difficulty}</span>
                    {problem.tags.map((t) => (
                      <span key={t} className="text-xs px-2 py-0.5 rounded-full bg-navy-800
                                               text-slate-500 font-mono border border-surface-border">
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Description */}
              <div className="prose prose-invert prose-sm max-w-none
                              prose-p:text-slate-400 prose-p:leading-relaxed
                              prose-strong:text-slate-200 prose-code:text-accent
                              prose-code:bg-navy-800 prose-code:px-1 prose-code:rounded
                              prose-code:text-sm prose-code:font-mono prose-code:before:content-none prose-code:after:content-none">
                <ReactMarkdown>{problem.description}</ReactMarkdown>
              </div>

              {/* Examples */}
              <div className="mt-8 space-y-4">
                <h3 className="font-display text-sm font-semibold text-slate-300 uppercase tracking-widest">Examples</h3>
                {problem.examples.map((ex, i) => (
                  <div key={i} className="bg-navy-900 rounded-lg p-4 border border-surface-border space-y-2 text-sm font-mono">
                    <div><span className="text-slate-500">Input: </span><span className="text-slate-300">{ex.input}</span></div>
                    <div><span className="text-slate-500">Output: </span><span className="text-accent">{ex.output}</span></div>
                    {ex.explanation && <div className="text-slate-500 text-xs pt-1">{ex.explanation}</div>}
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="text-center py-16 text-slate-600 font-mono text-sm">
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
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Editor toolbar */}
        <div className="flex items-center justify-between px-4 py-2 border-b border-surface-border shrink-0 bg-navy-900">
          <span className="text-xs font-mono text-slate-500">Python 3.12</span>
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className={`btn-primary text-sm py-1.5 px-5 ${submitting ? "opacity-60 cursor-not-allowed" : ""}`}
          >
            {submitting ? (
              <span className="flex items-center gap-2">
                <svg className="w-3 h-3 animate-spin-slow" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="32" strokeDashoffset="12" />
                </svg>
                Running…
              </span>
            ) : "Submit"}
          </button>
        </div>

        {/* Monaco Editor */}
        <div className="flex-1 overflow-hidden">
          <Editor
            height="100%"
            defaultLanguage="python"
            value={code}
            onChange={(v) => setCode(v ?? "")}
            theme="vs-dark"
            options={{
              fontSize: 14,
              fontFamily: "'JetBrains Mono', monospace",
              fontLigatures: true,
              minimap: { enabled: false },
              lineNumbers: "on",
              scrollBeyondLastLine: false,
              padding: { top: 16, bottom: 16 },
              renderLineHighlight: "gutter",
              cursorStyle: "line",
              tabSize: 4,
            }}
          />
        </div>

        {/* Result panel */}
        {submission && (
          <div className={`shrink-0 border-t border-surface-border p-4 text-sm
                          ${statusOk ? "bg-emerald-950/30" : statusDone ? "bg-red-950/20" : "bg-navy-900"}`}>
            <div className="flex items-center gap-3 mb-2">
              <span className={`font-semibold font-mono status-${submission.status}`}>
                {statusOk ? "✓ " : statusDone ? "✗ " : ""}{STATUS_LABEL[submission.status] ?? submission.status}
              </span>
              {statusDone && (
                <span className="text-slate-500 font-mono text-xs">
                  {submission.passedTests}/{submission.totalTests} tests passed
                  {submission.runtimeMs ? ` · ${Math.round(submission.runtimeMs)}ms` : ""}
                </span>
              )}
            </div>
            {submission.errorOutput && (
              <pre className="text-xs font-mono text-red-400 bg-red-950/20 rounded-lg p-3 overflow-auto max-h-32 whitespace-pre-wrap">
                {submission.errorOutput}
              </pre>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
