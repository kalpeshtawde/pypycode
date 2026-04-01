import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../utils/api";

const FEATURES = [
  { icon: "⚡", title: "Python-only", desc: "Every problem crafted for Python. No Java detours." },
  { icon: "🔒", title: "Sandboxed execution", desc: "Your code runs in an isolated Docker container, safely." },
  { icon: "📊", title: "Real-time results", desc: "Instant feedback: pass/fail, runtime, and error traces." },
  { icon: "🏆", title: "Leaderboard", desc: "Compete globally. Rise through the ranks." },
];

const SNIPPETS = [
  "def solution(nums, target):",
  "    seen = {}",
  "    for i, n in enumerate(nums):",
  '        if target - n in seen:',
  "            return [seen[target-n], i]",
  "        seen[n] = i",
];

export default function HomePage() {
  const [count, setCount] = useState<number | null>(null);

  useEffect(() => {
    api.get<{ id: number }[]>("/problems/").then((p) => setCount(p.length)).catch(() => {});
  }, []);

  return (
    <div className="relative overflow-hidden">
      {/* Gradient orbs */}
      <div className="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 w-[700px] h-[500px]
                      bg-accent/5 rounded-full blur-[120px]" />
      <div className="pointer-events-none absolute top-80 -right-40 w-[400px] h-[400px]
                      bg-blue-500/5 rounded-full blur-[100px]" />

      {/* Hero */}
      <section className="relative max-w-7xl mx-auto px-6 pt-28 pb-24 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-accent/20
                        bg-accent/5 text-accent text-xs font-mono mb-8 animate-fade-up">
          <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
          Python challenges, nothing else
        </div>

        <h1 className="font-display text-5xl sm:text-7xl font-semibold leading-[1.05] tracking-tight
                       text-white mb-6 animate-fade-up [animation-delay:100ms] opacity-0 [animation-fill-mode:forwards]">
          Write Python.
          <br />
          <em className="not-italic text-accent">Ship solutions.</em>
        </h1>

        <p className="max-w-xl mx-auto text-slate-400 text-lg leading-relaxed mb-10
                      animate-fade-up [animation-delay:200ms] opacity-0 [animation-fill-mode:forwards]">
          A focused coding platform for Python developers. Solve real algorithmic
          problems, get instant sandboxed feedback, and climb the leaderboard.
        </p>

        <div className="flex items-center justify-center gap-4
                        animate-fade-up [animation-delay:300ms] opacity-0 [animation-fill-mode:forwards]">
          <Link to="/problems" className="btn-primary text-base px-7 py-3">
            Start solving →
          </Link>
          <Link to="/leaderboard" className="btn-ghost text-base px-7 py-3">
            Leaderboard
          </Link>
        </div>

        {count !== null && (
          <p className="mt-6 text-slate-600 text-sm font-mono
                        animate-fade-up [animation-delay:400ms] opacity-0 [animation-fill-mode:forwards]">
            {count} problems available
          </p>
        )}
      </section>

      {/* Code preview */}
      <section className="max-w-2xl mx-auto px-6 mb-24">
        <div className="card overflow-hidden shadow-2xl shadow-black/40">
          <div className="flex items-center gap-1.5 px-4 py-3 border-b border-surface-border bg-navy-900">
            <span className="w-3 h-3 rounded-full bg-red-500/60" />
            <span className="w-3 h-3 rounded-full bg-amber-500/60" />
            <span className="w-3 h-3 rounded-full bg-emerald-500/60" />
            <span className="ml-3 text-xs font-mono text-slate-500">two_sum.py</span>
          </div>
          <div className="p-6">
            <pre className="font-mono text-sm leading-7 overflow-x-auto">
              {SNIPPETS.map((line, i) => (
                <div key={i}
                  className="animate-fade-up opacity-0 [animation-fill-mode:forwards]"
                  style={{ animationDelay: `${500 + i * 80}ms` }}>
                  <span className="select-none text-slate-600 mr-4 w-4 inline-block text-right">{i + 1}</span>
                  <span className={
                    line.startsWith("def ") ? "text-blue-400" :
                    line.includes("return") ? "text-accent" :
                    line.includes("#") ? "text-slate-500" :
                    line.includes('"') ? "text-amber-300" :
                    "text-slate-300"
                  }>{line}</span>
                </div>
              ))}
            </pre>
            <div className="mt-4 pt-4 border-t border-surface-border flex items-center gap-3">
              <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
              <span className="text-xs font-mono text-emerald-400">✓ All 3 test cases passed — 12ms</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-6 pb-24">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {FEATURES.map((f, i) => (
            <div key={i} className="card p-6 hover:border-accent/20 transition-colors duration-300">
              <div className="text-2xl mb-3">{f.icon}</div>
              <h3 className="font-display text-base font-semibold text-white mb-1">{f.title}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
