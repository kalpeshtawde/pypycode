import { Link } from "react-router-dom";
import { useEffect, useMemo, useState, type ReactNode } from "react";
import { api } from "../utils/api";
import { useSEO } from "../hooks/useSEO";
import {
  getDefaultMetadata,
  createOrganizationStructuredData,
  createWebSiteStructuredData,
} from "../utils/seo";

const FEATURES = [
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5" aria-hidden="true">
        <path d="M13 2L4 14h6l-1 8 9-12h-6l1-8Z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    title: "Python-only",
    desc: "Every problem crafted for Python. No Java detours.",
    to: "/problems",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5" aria-hidden="true">
        <rect x="4" y="10" width="16" height="10" rx="2.5" stroke="currentColor" strokeWidth="1.8" />
        <path d="M8 10V7a4 4 0 118 0v3" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        <circle cx="12" cy="15" r="1.25" fill="currentColor" />
      </svg>
    ),
    title: "Sandboxed execution",
    desc: "Your code runs in an isolated Docker container, safely.",
    to: "/about",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5" aria-hidden="true">
        <path d="M4 18V6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M8 18v-4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M12 18V9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M16 18V5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M20 18v-7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      </svg>
    ),
    title: "Real-time results",
    desc: "Instant feedback: pass/fail, runtime, and error traces.",
    to: "/problems",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5" aria-hidden="true">
        <path d="M8 20h8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M12 16v4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M7 5h10v2a5 5 0 01-10 0V5Z" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
        <path d="M7 7H5a2.5 2.5 0 010-5h2" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M17 7h2a2.5 2.5 0 000-5h-2" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      </svg>
    ),
    title: "Leaderboard",
    desc: "Compete globally. Rise through the ranks.",
    to: "/leaderboard",
  },
] as const satisfies ReadonlyArray<{ icon: ReactNode; title: string; desc: string; to: string }>;

const SNIPPETS = [
  "def solution(nums, target):",
  "    seen = {}",
  "    for i, n in enumerate(nums):",
  '        if target - n in seen:',
  "            return [seen[target-n], i]",
  "        seen[n] = i",
];

const STEPS = [
  {
    n: "1",
    title: "Pick a problem",
    desc: "Filter by difficulty or topic — arrays, trees, graphs, DP, and more.",
  },
  {
    n: "2",
    title: "Write Python",
    desc: "Code in the browser editor with instant run-and-test feedback.",
  },
  {
    n: "3",
    title: "Level up",
    desc: "Track solved problems and climb the global leaderboard.",
  },
] as const;

const FADE = "motion-safe:animate-fade-up motion-safe:opacity-0 [animation-fill-mode:forwards]";

function snippetLineClass(line: string) {
  if (line.startsWith("def ")) return "text-emerald-700 dark:text-emerald-400";
  if (line.includes("return")) return "text-teal-600 dark:text-teal-400";
  if (line.includes("#")) return "text-slate-500 dark:text-slate-400";
  if (line.includes('"')) return "text-amber-600 dark:text-amber-400";
  return "text-slate-800 dark:text-slate-200";
}

export default function HomePage() {
  const [count, setCount] = useState<number | null>(null);
  const [price, setPrice] = useState<string>("$30");
  const [trialDays, setTrialDays] = useState<number>(15);
  const [typedChars, setTypedChars] = useState(0);

  const fullSnippet = useMemo(() => SNIPPETS.join("\n"), []);
  const typingDone = typedChars >= fullSnippet.length;

  const homeSeoMetadata = useMemo(() => getDefaultMetadata(), []);
  const homeStructuredData = useMemo(
    () => [createWebSiteStructuredData(), createOrganizationStructuredData()],
    []
  );
  useSEO(homeSeoMetadata, homeStructuredData);

  useEffect(() => {
    api
      .get<{ problems: { id: string }[]; pagination?: { total?: number } }>("/problems/")
      .then((res) => {
        const total = res.pagination?.total;
        setCount(typeof total === "number" ? total : res.problems.length);
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    api
      .get<{ amountDisplay?: string; trialDays?: number }>("/billing/pricing")
      .then((res) => {
        if (res.amountDisplay) setPrice(res.amountDisplay);
        if (typeof res.trialDays === "number") setTrialDays(res.trialDays);
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setTypedChars(fullSnippet.length);
      return;
    }
    let i = 0;
    const id = setInterval(() => {
      i += 3;
      setTypedChars(i);
      if (i >= fullSnippet.length) clearInterval(id);
    }, 24);
    return () => clearInterval(id);
  }, [fullSnippet]);

  const typedLines = fullSnippet.slice(0, typedChars).split("\n");

  return (
    <div className="relative overflow-hidden bg-gradient-to-b from-slate-50 dark:from-slate-900 via-white dark:via-slate-900 to-slate-50 dark:to-slate-900">
      {/* Gradient orb */}
      <div className="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 w-[700px] h-[500px]
                      bg-emerald-500/8 rounded-full blur-[120px]" />

      {/* Hero */}
      <section className="relative max-w-7xl mx-auto px-6 pt-24 pb-16 text-center">
        <p className={`inline-flex items-center gap-2 rounded-full border border-emerald-200 dark:border-emerald-500/30 bg-emerald-50 dark:bg-emerald-500/10
                      px-4 py-1.5 text-sm font-medium text-emerald-700 dark:text-emerald-400 mb-8 ${FADE}`}
           style={{ animationDelay: "50ms" }}>
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-600" />
          Python-only coding challenges
        </p>

        <h1 className={`font-display text-5xl sm:text-7xl font-semibold leading-[1.05] tracking-tight
                       text-slate-900 dark:text-slate-100 mb-6 ${FADE}`}
            style={{ animationDelay: "100ms" }}>
          Write Python.
          <br />
          <em className="not-italic bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">Ship solutions.</em>
        </h1>

        <p className={`max-w-xl mx-auto text-slate-600 dark:text-slate-400 text-lg leading-relaxed mb-10 ${FADE}`}
           style={{ animationDelay: "200ms" }}>
          A focused coding platform for Python developers. Solve real algorithmic
          problems, get instant sandboxed feedback, and climb the leaderboard.
        </p>

        <div className={`flex items-center justify-center gap-4 ${FADE}`}
             style={{ animationDelay: "300ms" }}>
          <Link to="/problems" className="btn-primary text-base px-7 py-3">
            Start solving →
          </Link>
          <Link to="/pricing" className="btn-ghost text-base px-7 py-3">
            See pricing
          </Link>
        </div>

        <div className={`mt-10 flex flex-wrap items-center justify-center gap-x-8 gap-y-3 ${FADE}`}
             style={{ animationDelay: "400ms" }}>
          <div className="flex items-baseline gap-2">
            <span className="font-display text-xl font-semibold text-slate-900 dark:text-slate-100">
              {count !== null ? `${count}+` : "—"}
            </span>
            <span className="text-sm text-slate-500 dark:text-slate-400">curated problems</span>
          </div>
          <span className="hidden sm:block w-px h-5 bg-slate-200 dark:bg-slate-700" />
          <div className="flex items-baseline gap-2">
            <span className="font-display text-xl font-semibold text-slate-900 dark:text-slate-100">{price}<span className="text-sm font-normal text-slate-500 dark:text-slate-400">/year</span></span>
            <span className="text-sm text-slate-500 dark:text-slate-400">full access</span>
          </div>
          <span className="hidden sm:block w-px h-5 bg-slate-200 dark:bg-slate-700" />
          <div className="flex items-baseline gap-2">
            <span className="font-display text-xl font-semibold text-slate-900 dark:text-slate-100">{trialDays} days</span>
            <span className="text-sm text-slate-500 dark:text-slate-400">free trial</span>
          </div>
        </div>
      </section>

      {/* Code preview */}
      <section className="max-w-2xl mx-auto px-6 mb-24">
        <div className="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-700 shadow-lg shadow-slate-200/50 dark:shadow-black/30 bg-white dark:bg-slate-800">
          <div className="flex items-center gap-1.5 px-4 py-3 border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900">
            <span className="w-3 h-3 rounded-full bg-red-500" />
            <span className="w-3 h-3 rounded-full bg-amber-500" />
            <span className="w-3 h-3 rounded-full bg-emerald-500" />
            <span className="ml-3 text-xs font-mono text-slate-600 dark:text-slate-400 font-medium">two_sum.py</span>
          </div>
          <div className="p-6">
            <pre className="font-mono text-sm leading-7 overflow-x-auto min-h-[168px]">
              {typedLines.map((line, i) => (
                <div key={i}>
                  <span className="select-none text-slate-400 mr-4 w-4 inline-block text-right">{i + 1}</span>
                  <span className={snippetLineClass(line)}>{line}</span>
                  {i === typedLines.length - 1 && !typingDone && (
                    <span className="inline-block w-2 h-4 ml-0.5 align-middle bg-emerald-600 animate-pulse" />
                  )}
                </div>
              ))}
            </pre>
            <div className={`mt-4 pt-4 border-t border-slate-200 dark:border-slate-700 flex items-center gap-3 transition-opacity duration-500 ${typingDone ? "opacity-100" : "opacity-0"}`}>
              <span className="w-2 h-2 rounded-full bg-emerald-600" />
              <span className="text-xs font-mono text-emerald-700 dark:text-emerald-400 font-medium">✓ All 3 test cases passed — 12ms</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-6 pb-24">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {FEATURES.map((f, i) => (
            <Link key={i} to={f.to} className="group relative isolate overflow-hidden rounded-2xl border border-slate-200/80 dark:border-slate-700 bg-white/95 dark:bg-slate-800/95 p-6 backdrop-blur-sm transition-all duration-300 motion-safe:hover:-translate-y-1 hover:border-emerald-300/70 hover:shadow-xl hover:shadow-emerald-200/40 dark:hover:border-emerald-500/40 dark:hover:shadow-emerald-500/10">
              <div className="absolute inset-0 -z-10 bg-gradient-to-br from-white via-emerald-50/30 to-teal-50/40 dark:from-slate-800 dark:via-emerald-500/5 dark:to-teal-500/5 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
              <div className="absolute -right-10 -top-10 h-24 w-24 rounded-full bg-emerald-300/15 blur-2xl transition-all duration-300 group-hover:bg-emerald-300/25" />
              <div className="relative">
                <div className="mb-5 inline-flex h-11 w-11 items-center justify-center rounded-xl border border-emerald-200/70 dark:border-emerald-500/30 bg-emerald-50 dark:bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 shadow-sm shadow-emerald-100 dark:shadow-none transition-all duration-300 motion-safe:group-hover:scale-105 group-hover:bg-white dark:group-hover:bg-emerald-500/15 group-hover:text-emerald-600 dark:group-hover:text-emerald-300">
                  {f.icon}
                </div>
                <h3 className="font-display text-base font-semibold text-slate-900 dark:text-slate-100 mb-2.5 tracking-tight group-hover:text-emerald-700 dark:group-hover:text-emerald-400 transition-colors duration-300">{f.title}</h3>
                <p className="text-slate-600 dark:text-slate-400 text-sm leading-relaxed group-hover:text-slate-700 dark:group-hover:text-slate-300 transition-colors duration-300">{f.desc}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="max-w-5xl mx-auto px-6 pb-24">
        <h2 className="font-display text-3xl sm:text-4xl font-semibold tracking-tight text-slate-900 dark:text-slate-100 text-center mb-12">
          How it works
        </h2>
        <div className="grid sm:grid-cols-3 gap-8">
          {STEPS.map((s) => (
            <div key={s.n} className="text-center">
              <div className="mx-auto mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-emerald-600 text-white font-display font-semibold">
                {s.n}
              </div>
              <h3 className="font-display text-lg font-semibold text-slate-900 dark:text-slate-100 mb-2">{s.title}</h3>
              <p className="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Final CTA */}
      <section className="max-w-5xl mx-auto px-6 pb-24">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-700 via-emerald-600 to-teal-700 px-8 py-14 text-center shadow-xl shadow-emerald-200/60">
          <div className="pointer-events-none absolute -top-20 left-1/2 -translate-x-1/2 w-[500px] h-[300px] bg-white/10 rounded-full blur-[80px]" />
          <h2 className="relative font-display text-3xl sm:text-4xl font-semibold tracking-tight text-white mb-4">
            Ready to write Python?
          </h2>
          <p className="relative max-w-lg mx-auto text-emerald-50/90 leading-relaxed mb-8">
            Everything unlocked for {price}/year — a fraction of what LeetCode Premium charges.
            Start with a {trialDays}-day free trial.
          </p>
          <div className="relative flex items-center justify-center gap-4">
            <Link to="/pricing" className="inline-flex items-center gap-2 px-7 py-3 rounded-lg bg-white text-emerald-800 font-medium text-base hover:bg-emerald-50 active:scale-95 transition-all duration-150">
              Start free trial →
            </Link>
            <Link to="/problems" className="inline-flex items-center gap-2 px-7 py-3 rounded-lg border border-emerald-300/60 text-emerald-50 font-medium text-base hover:bg-white/10 transition-all duration-150">
              Browse problems
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
