import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";

type Mode = "login" | "register";

export default function AuthPage() {
  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "register") {
        const res = await api.post<{ token: string; username: string }>(
          "/auth/register",
          { username, email, password }
        );
        const me = await api.get<{ id: number; username: string; email: string }>(
          "/auth/me",
          res.token
        );
        setAuth(res.token, me);
      } else {
        const res = await api.post<{ token: string; username: string }>(
          "/auth/login",
          { email, password }
        );
        const me = await api.get<{ id: number; username: string; email: string }>(
          "/auth/me",
          res.token
        );
        setAuth(res.token, me);
      }
      navigate("/problems");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-6 py-16 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Background glow */}
      <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
        <div className="w-96 h-96 bg-emerald-500/8 rounded-full blur-[120px]" />
        <div className="absolute top-0 right-0 w-80 h-80 bg-blue-500/5 rounded-full blur-[100px]" />
      </div>

      <div className="relative w-full max-w-sm">
        {/* Logo mark */}
        <div className="flex justify-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30
                          flex items-center justify-center hover:border-emerald-500/50 transition-colors">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M3 3h6v6H3zM11 3h6v6h-6zM3 11h6v6H3zM11 11h6v6h-6z" fill="#10B981"/>
            </svg>
          </div>
        </div>

        <div className="rounded-lg border border-slate-700/60 bg-gradient-to-br from-slate-800/40 to-slate-900/40 p-8 backdrop-blur-sm shadow-2xl shadow-slate-900/50">
          <h1 className="font-display text-2xl font-semibold text-white text-center mb-1">
            {mode === "login" ? "Welcome back" : "Create account"}
          </h1>
          <p className="text-slate-400 text-sm text-center mb-8">
            {mode === "login"
              ? "Sign in to track your progress"
              : "Start solving Python problems today"}
          </p>

          {/* Mode toggle */}
          <div className="flex bg-slate-800/50 rounded-lg p-1 mb-6 border border-slate-700/50">
            {(["login", "register"] as Mode[]).map((m) => (
              <button
                key={m}
                onClick={() => { setMode(m); setError(""); }}
                className={`flex-1 py-1.5 text-sm rounded-md capitalize transition-all ${
                  mode === m
                    ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                    : "text-slate-400 hover:text-slate-300"
                }`}
              >
                {m === "login" ? "Sign in" : "Register"}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === "register" && (
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1.5 uppercase tracking-wider">
                  Username
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  minLength={3}
                  placeholder="pythonista"
                  className="w-full bg-slate-800/50 border border-slate-700/60 rounded-lg px-4 py-2.5
                             text-sm text-white placeholder-slate-500 font-body
                             focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/20
                             transition-colors"
                />
              </div>
            )}

            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1.5 uppercase tracking-wider">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
                className="w-full bg-slate-800/50 border border-slate-700/60 rounded-lg px-4 py-2.5
                           text-sm text-white placeholder-slate-500 font-body
                           focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/20
                           transition-colors"
              />
            </div>

            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1.5 uppercase tracking-wider">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
                placeholder="••••••••"
                className="w-full bg-slate-800/50 border border-slate-700/60 rounded-lg px-4 py-2.5
                           text-sm text-white placeholder-slate-500 font-body
                           focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/20
                           transition-colors"
              />
            </div>

            {error && (
              <div className="bg-red-950/30 border border-red-900/40 rounded-lg px-4 py-2.5
                              text-sm text-red-300 font-mono">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className={`w-full btn-primary justify-center py-2.5 mt-2 ${
                loading ? "opacity-60 cursor-not-allowed" : ""
              }`}
            >
              {loading ? "Please wait…" : mode === "login" ? "Sign in" : "Create account"}
            </button>
          </form>

          {mode === "login" && (
            <p className="mt-4 text-center text-xs text-slate-500">
              Demo account:{" "}
              <button
                onClick={() => { setEmail("demo@pypycode.dev"); setPassword("demo1234"); }}
                className="text-emerald-400 hover:text-emerald-300 hover:underline font-mono transition-colors"
              >
                demo@pypycode.dev
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
