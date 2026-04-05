import { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";
import CodeMirrorEditor from "../components/CodeMirrorEditor";
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
  const [fontSize, setFontSize] = useState(15);
  const [vimMode, setVimMode] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    api.get<Problem>(`/problems/${slug}`).then((p) => {
      setProblem(p);
      setCode(p.starterCode);
    });
  }, [slug]);

  useEffect(() => {
    if (!slug || !token) return;
    api.get<Array<{ id: number; status: string; passedTests: number; totalTests: number; runtimeMs: number | null; memoryKb: number | null; code: string; createdAt: string }>>(
      `/submissions/problem/${slug}`,
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
        }
      })
      .catch(() => {});
  }, [slug, token]);

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
    <div className="flex h-[calc(100vh-64px)] bg-slate-50 relative">
      {/* Left: Problem panel */}
      <div className="w-[42%] flex flex-col border-r border-slate-200 overflow-hidden bg-slate-50">
        {/* Tabs */}
        <div className="flex border-b border-slate-200 shrink-0 bg-slate-50">
          {(["description", "submissions"] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-5 py-3 text-sm font-body capitalize transition-colors border-b-2 ${
                activeTab === tab
                  ? "border-accent text-slate-900"
                  : "border-transparent text-slate-600 hover:text-slate-900"
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
              <div className="mb-8">
                <h1 className="text-5xl font-black text-slate-900 mb-4" style={{ fontSize: '42px', fontWeight: 900, letterSpacing: '-0.02em' }}>
                  {problem.title}
                </h1>
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
        {/* Editor header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-200 shrink-0 bg-slate-50">
          <span className="text-xs font-mono text-slate-600">Python 3.12</span>
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
        <div className="flex-1 overflow-hidden bg-slate-50">
          <CodeMirrorEditor
            value={code}
            onChange={setCode}
            fontSize={fontSize}
            vimMode={vimMode}
          />
        </div>

        {/* Result panel */}
        {submission && (
          <div className={`shrink-0 border-t border-slate-200 p-4 text-sm
                          ${statusOk ? "bg-emerald-50" : statusDone ? "bg-yellow-50" : "bg-slate-50"}`}>
            <div className="flex items-center gap-3 mb-2">
              {statusOk && (
                <span className="text-emerald-600 font-bold text-lg">✓</span>
              )}
              <span className={`font-semibold font-mono ${statusOk ? "text-emerald-600" : statusDone ? "text-yellow-600" : "text-slate-600"}`}>
                {STATUS_LABEL[submission.status] ?? submission.status}
              </span>
              {statusDone && (
                <span className="text-slate-600 font-mono text-xs">
                  {submission.passedTests}/{submission.totalTests} tests passed
                  {submission.runtimeMs ? ` · ${Math.round(submission.runtimeMs)}ms` : ""}
                </span>
              )}
            </div>
            {submission.errorOutput && (
              <pre className="text-xs font-mono text-red-700 bg-red-50 rounded-lg p-3 overflow-auto max-h-32 whitespace-pre-wrap">
                {submission.errorOutput}
              </pre>
            )}
          </div>
        )}
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
