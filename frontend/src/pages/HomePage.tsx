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
    api
      .get<{ problems: { id: string }[]; pagination?: { total?: number } }>("/problems/")
      .then((res) => {
        const total = res.pagination?.total;
        setCount(typeof total === "number" ? total : res.problems.length);
      })
      .catch(() => {});
  }, []);

  return (
    <div className="relative overflow-hidden bg-gradient-to-b from-slate-50 via-white to-slate-50">
      {/* Gradient orbs */}
      <div className="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 w-[700px] h-[500px]
                      bg-emerald-500/5 rounded-full blur-[120px]" />
      <div className="pointer-events-none absolute top-80 -right-40 w-[400px] h-[400px]
                      bg-blue-500/3 rounded-full blur-[100px]" />
      <div className="pointer-events-none absolute bottom-0 -left-40 w-[500px] h-[500px]
                      bg-purple-500/3 rounded-full blur-[120px]" />

      {/* Hero */}
      <section className="relative max-w-7xl mx-auto px-6 pt-28 pb-24 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-emerald-200
                        bg-emerald-50 text-emerald-700 text-xs font-mono mb-8 animate-fade-up">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse" />
          Python challenges, nothing else
        </div>

        <h1 className="font-display text-5xl sm:text-7xl font-semibold leading-[1.05] tracking-tight
                       text-slate-900 mb-6 animate-fade-up [animation-delay:100ms] opacity-0 [animation-fill-mode:forwards]">
          Write Python.
          <br />
          <em className="not-italic bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">Ship solutions.</em>
        </h1>

        <p className="max-w-xl mx-auto text-slate-600 text-lg leading-relaxed mb-10
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
          <p className="mt-6 text-slate-500 text-sm font-mono
                        animate-fade-up [animation-delay:400ms] opacity-0 [animation-fill-mode:forwards]">
            {count} problems available
          </p>
        )}
      </section>

      {/* Code preview */}
      <section className="max-w-2xl mx-auto px-6 mb-24">
        <div className="overflow-hidden rounded-lg border border-slate-200 shadow-lg shadow-slate-200/50 bg-white">
          <div className="flex items-center gap-1.5 px-4 py-3 border-b border-slate-200 bg-slate-50">
            <span className="w-3 h-3 rounded-full bg-red-500" />
            <span className="w-3 h-3 rounded-full bg-amber-500" />
            <span className="w-3 h-3 rounded-full bg-emerald-500" />
            <span className="ml-3 text-xs font-mono text-slate-600 font-medium">two_sum.py</span>
          </div>
          <div className="p-6">
            <pre className="font-mono text-sm leading-7 overflow-x-auto">
              {SNIPPETS.map((line, i) => (
                <div key={i}
                  className="animate-fade-up opacity-0 [animation-fill-mode:forwards]"
                  style={{ animationDelay: `${500 + i * 80}ms` }}>
                  <span className="select-none text-slate-400 mr-4 w-4 inline-block text-right">{i + 1}</span>
                  <span className={
                    line.startsWith("def ") ? "text-blue-600" :
                    line.includes("return") ? "text-emerald-600" :
                    line.includes("#") ? "text-slate-500" :
                    line.includes('"') ? "text-amber-600" :
                    "text-slate-800"
                  }>{line}</span>
                </div>
              ))}
            </pre>
            <div className="mt-4 pt-4 border-t border-slate-200 flex items-center gap-3">
              <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse" />
              <span className="text-xs font-mono text-emerald-700 font-medium">✓ All 3 test cases passed — 12ms</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-6 pb-24">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {FEATURES.map((f, i) => (
            <div key={i} className="group relative overflow-hidden rounded-lg border border-slate-200 bg-white p-6 transition-all duration-300 hover:border-emerald-300 hover:shadow-lg hover:shadow-emerald-200/50">
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-50/0 to-emerald-50/0 group-hover:from-emerald-50 group-hover:to-emerald-50/50 transition-all duration-300" />
              <div className="relative">
                <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">{f.icon}</div>
                <h3 className="font-display text-base font-semibold text-slate-900 mb-2 group-hover:text-emerald-700 transition-colors duration-300">{f.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed group-hover:text-slate-700 transition-colors duration-300">{f.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
