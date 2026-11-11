import { useEffect, useState } from "react";
import { api } from "../utils/api";
import { useSEO } from "../hooks/useSEO";
import { getLeaderboardMetadata } from "../utils/seo";
import type { LeaderboardEntry } from "../types";

const MEDALS = ["🥇", "🥈", "🥉"];

export default function LeaderboardPage() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  
  useSEO(getLeaderboardMetadata());

  useEffect(() => {
    api.get<LeaderboardEntry[]>("/leaderboard/")
      .then(setEntries)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-[calc(100vh-64px)] bg-gradient-to-b from-slate-50 dark:from-slate-900 via-white dark:via-slate-900 to-slate-50 dark:to-slate-900">
      {/* Background glow */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-emerald-500/5 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 right-0 w-80 h-80 bg-blue-500/3 rounded-full blur-[100px]" />
      </div>

      <div className="relative max-w-3xl mx-auto px-6 py-16">
        <div className="mb-12">
          <h1 className="font-display text-5xl font-semibold text-slate-900 dark:text-slate-100 mb-2">Leaderboard</h1>
          <p className="text-slate-600 dark:text-slate-400 text-lg">Top Python problem solvers.</p>
        </div>

        <div className="rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 overflow-hidden shadow-lg shadow-slate-200/50 dark:shadow-black/30">
          <div className="grid grid-cols-[3rem_1fr_auto] text-xs font-mono text-slate-600 dark:text-slate-400
                          uppercase tracking-widest px-6 py-4 border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900">
            <span>Rank</span>
            <span>Username</span>
            <span>Solved</span>
          </div>

          {loading ? (
            <div className="py-24 text-center text-slate-500 dark:text-slate-400 font-mono text-sm">Loading…</div>
          ) : entries.length === 0 ? (
            <div className="py-24 text-center text-slate-500 dark:text-slate-400 font-mono text-sm">
              No submissions yet. Be the first! 🐍
            </div>
          ) : (
            entries.map((e) => (
              <div
                key={e.rank}
                className={`grid grid-cols-[3rem_1fr_auto] items-center px-6 py-4
                            border-b border-slate-100 dark:border-slate-700 last:border-0 transition-all duration-200
                            ${e.rank <= 3 
                              ? "bg-gradient-to-r from-emerald-50 to-transparent hover:from-emerald-100 dark:from-emerald-500/10 dark:hover:from-emerald-500/15" 
                              : "hover:bg-slate-50 dark:hover:bg-slate-800"}`}
              >
                <span className="text-lg font-semibold">
                  {e.rank <= 3 ? MEDALS[e.rank - 1] : (
                    <span className="text-slate-400 font-mono text-xs font-medium">{e.rank}</span>
                  )}
                </span>
                <div className="flex items-center">
                  <span className={`font-body text-sm transition-colors ${e.rank <= 3 ? "text-slate-900 dark:text-slate-100 font-semibold" : "text-slate-700 dark:text-slate-300"}`}>
                    {e.username}
                  </span>
                </div>
                <span className="font-mono text-sm font-semibold">
                  <span className={e.rank <= 3 ? "text-emerald-600 dark:text-emerald-400" : "text-slate-600 dark:text-slate-400"}>
                    {e.solved}
                  </span>
                  <span className="text-slate-400 ml-2 text-xs font-normal">solved</span>
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
