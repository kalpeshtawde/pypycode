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
    <div className="min-h-[calc(100vh-64px)] bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Background glow */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-emerald-500/8 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 right-0 w-80 h-80 bg-blue-500/5 rounded-full blur-[100px]" />
      </div>

      <div className="relative max-w-3xl mx-auto px-6 py-16">
        <div className="mb-12">
          <h1 className="font-display text-5xl font-semibold text-white mb-2">Leaderboard</h1>
          <p className="text-slate-300 text-lg">Top Python problem solvers.</p>
        </div>

        <div className="rounded-lg border border-slate-700/60 bg-gradient-to-br from-slate-800/40 to-slate-900/40 overflow-hidden backdrop-blur-sm shadow-2xl shadow-slate-900/50">
          <div className="grid grid-cols-[3rem_1fr_auto] text-xs font-mono text-slate-400
                          uppercase tracking-widest px-6 py-4 border-b border-slate-700/50 bg-slate-800/50">
            <span>Rank</span>
            <span>Username</span>
            <span>Solved</span>
          </div>

          {loading ? (
            <div className="py-24 text-center text-slate-400 font-mono text-sm">Loading…</div>
          ) : entries.length === 0 ? (
            <div className="py-24 text-center text-slate-400 font-mono text-sm">
              No submissions yet. Be the first! 🐍
            </div>
          ) : (
            entries.map((e) => (
              <div
                key={e.rank}
                className={`grid grid-cols-[3rem_1fr_auto] items-center px-6 py-4
                            border-b border-slate-700/30 last:border-0 transition-all duration-200
                            ${e.rank <= 3 
                              ? "bg-gradient-to-r from-emerald-500/10 to-transparent hover:from-emerald-500/15" 
                              : "hover:bg-slate-700/20"}`}
              >
                <span className="text-lg font-semibold">
                  {e.rank <= 3 ? MEDALS[e.rank - 1] : (
                    <span className="text-slate-500 font-mono text-xs font-medium">{e.rank}</span>
                  )}
                </span>
                <div className="flex items-center gap-3">
                  <span className={`w-8 h-8 rounded-full border-2 flex items-center justify-center text-xs font-mono font-bold transition-all
                                   ${e.rank <= 3 
                                     ? "bg-emerald-500/20 border-emerald-500/50 text-emerald-300" 
                                     : "bg-slate-700/50 border-slate-600/50 text-slate-300"}`}>
                    {e.username[0].toUpperCase()}
                  </span>
                  <span className={`font-body text-sm transition-colors ${e.rank <= 3 ? "text-white font-semibold" : "text-slate-300"}`}>
                    {e.username}
                  </span>
                </div>
                <span className="font-mono text-sm font-semibold">
                  <span className={e.rank <= 3 ? "text-emerald-400" : "text-slate-300"}>
                    {e.solved}
                  </span>
                  <span className="text-slate-500 ml-2 text-xs font-normal">solved</span>
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
