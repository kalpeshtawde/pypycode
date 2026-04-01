import { useEffect, useState } from "react";
import { api } from "../utils/api";
import type { LeaderboardEntry } from "../types";

const MEDALS = ["🥇", "🥈", "🥉"];

export default function LeaderboardPage() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<LeaderboardEntry[]>("/leaderboard/")
      .then(setEntries)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-3xl mx-auto px-6 py-16">
      <div className="mb-10">
        <h1 className="font-display text-4xl font-semibold text-white mb-2">Leaderboard</h1>
        <p className="text-slate-500">Top Python problem solvers.</p>
      </div>

      <div className="card overflow-hidden">
        <div className="grid grid-cols-[3rem_1fr_auto] text-xs font-mono text-slate-600
                        uppercase tracking-widest px-5 py-3 border-b border-surface-border">
          <span>Rank</span>
          <span>Username</span>
          <span>Solved</span>
        </div>

        {loading ? (
          <div className="py-24 text-center text-slate-600 font-mono text-sm">Loading…</div>
        ) : entries.length === 0 ? (
          <div className="py-24 text-center text-slate-600 font-mono text-sm">
            No submissions yet. Be the first! 🐍
          </div>
        ) : (
          entries.map((e) => (
            <div
              key={e.rank}
              className={`grid grid-cols-[3rem_1fr_auto] items-center px-5 py-4
                          border-b border-surface-border last:border-0
                          ${e.rank <= 3 ? "bg-accent/[0.03]" : ""}`}
            >
              <span className="text-base">
                {e.rank <= 3 ? MEDALS[e.rank - 1] : (
                  <span className="text-slate-600 font-mono text-xs">{e.rank}</span>
                )}
              </span>
              <div className="flex items-center gap-2">
                <span className="w-7 h-7 rounded-full bg-navy-700 border border-surface-border
                                 flex items-center justify-center text-xs font-mono text-slate-400">
                  {e.username[0].toUpperCase()}
                </span>
                <span className={`font-body ${e.rank <= 3 ? "text-white font-medium" : "text-slate-300"}`}>
                  {e.username}
                </span>
              </div>
              <span className="font-mono text-accent text-sm font-medium">
                {e.solved}
                <span className="text-slate-600 ml-1 text-xs">solved</span>
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
