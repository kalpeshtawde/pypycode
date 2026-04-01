import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../utils/api";
import type { Problem } from "../types";

const DIFFS = ["all", "easy", "medium", "hard"] as const;

export default function ProblemsPage() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [filter, setFilter] = useState<typeof DIFFS[number]>("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const q = filter !== "all" ? `?difficulty=${filter}` : "";
    api.get<Problem[]>(`/problems/${q}`)
      .then(setProblems)
      .finally(() => setLoading(false));
  }, [filter]);

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      {/* Header */}
      <div className="mb-10">
        <h1 className="font-display text-4xl font-semibold text-white mb-2">Problems</h1>
        <p className="text-slate-500">Python-only. Solve them all.</p>
      </div>

      {/* Filter tabs */}
      <div className="flex items-center gap-2 mb-8">
        {DIFFS.map((d) => (
          <button
            key={d}
            onClick={() => setFilter(d)}
            className={`px-4 py-1.5 rounded-lg text-sm font-mono capitalize transition-all ${
              filter === d
                ? "bg-surface border border-accent/30 text-accent"
                : "text-slate-500 hover:text-slate-300"
            }`}
          >
            {d}
          </button>
        ))}
        <span className="ml-auto text-xs font-mono text-slate-600">
          {problems.length} problem{problems.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* Table */}
      <div className="card overflow-hidden">
        <div className="grid grid-cols-[3rem_1fr_auto_auto] text-xs font-mono text-slate-600
                        uppercase tracking-widest px-5 py-3 border-b border-surface-border">
          <span>#</span>
          <span>Title</span>
          <span>Tags</span>
          <span>Difficulty</span>
        </div>

        {loading ? (
          <div className="py-24 text-center text-slate-600 font-mono text-sm">Loading…</div>
        ) : problems.length === 0 ? (
          <div className="py-24 text-center text-slate-600 font-mono text-sm">No problems found.</div>
        ) : (
          problems.map((p, i) => (
            <Link
              key={p.id}
              to={`/problems/${p.slug}`}
              className="grid grid-cols-[3rem_1fr_auto_auto] items-center px-5 py-4
                         border-b border-surface-border last:border-0
                         hover:bg-surface-raised transition-colors duration-150 group"
            >
              <span className="text-xs font-mono text-slate-600">{i + 1}</span>
              <span className="font-body text-slate-200 group-hover:text-white transition-colors">
                {p.title}
              </span>
              <div className="flex gap-1.5 flex-wrap mr-6">
                {(p.tags || []).slice(0, 2).map((t) => (
                  <span key={t} className="text-xs px-2 py-0.5 rounded-full bg-navy-800
                                           text-slate-500 font-mono border border-surface-border">
                    {t}
                  </span>
                ))}
              </div>
              <span className={`badge-${p.difficulty}`}>{p.difficulty}</span>
            </Link>
          ))
        )}
      </div>
    </div>
  );
}
