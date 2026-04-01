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
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-6 py-16">
      {/* Background glow */}
      <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
        <div className="w-96 h-96 bg-accent/5 rounded-full blur-[120px]" />
      </div>

      <div className="relative w-full max-w-sm">
        {/* Logo mark */}
        <div className="flex justify-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-accent/10 border border-accent/20
                          flex items-center justify-center">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M3 3h6v6H3zM11 3h6v6h-6zM3 11h6v6H3zM11 11h6v6h-6z" fill="#4ade80"/>
            </svg>
          </div>
        </div>

        <div className="card p-8">
          <h1 className="font-display text-2xl font-semibold text-white text-center mb-1">
            {mode === "login" ? "Welcome back" : "Create account"}
          </h1>
          <p className="text-slate-500 text-sm text-center mb-8">
            {mode === "login"
              ? "Sign in to track your progress"
              : "Start solving Python problems today"}
          </p>

          {/* Mode toggle */}
          <div className="flex bg-navy-900 rounded-lg p-1 mb-6">
            {(["login", "register"] as Mode[]).map((m) => (
              <button
                key={m}
                onClick={() => { setMode(m); setError(""); }}
                className={`flex-1 py-1.5 text-sm rounded-md capitalize transition-all ${
                  mode === m
                    ? "bg-surface text-white border border-surface-border"
                    : "text-slate-500 hover:text-slate-300"
                }`}
              >
                {m === "login" ? "Sign in" : "Register"}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === "register" && (
              <div>
                <label className="block text-xs font-mono text-slate-500 mb-1.5 uppercase tracking-wider">
                  Username
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  minLength={3}
                  placeholder="pythonista"
                  className="w-full bg-navy-900 border border-surface-border rounded-lg px-4 py-2.5
                             text-sm text-white placeholder-slate-600 font-body
                             focus:outline-none focus:border-accent/40 focus:ring-1 focus:ring-accent/20
                             transition-colors"
                />
              </div>
            )}

            <div>
              <label className="block text-xs font-mono text-slate-500 mb-1.5 uppercase tracking-wider">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
                className="w-full bg-navy-900 border border-surface-border rounded-lg px-4 py-2.5
                           text-sm text-white placeholder-slate-600 font-body
                           focus:outline-none focus:border-accent/40 focus:ring-1 focus:ring-accent/20
                           transition-colors"
              />
            </div>

            <div>
              <label className="block text-xs font-mono text-slate-500 mb-1.5 uppercase tracking-wider">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
                placeholder="••••••••"
                className="w-full bg-navy-900 border border-surface-border rounded-lg px-4 py-2.5
                           text-sm text-white placeholder-slate-600 font-body
                           focus:outline-none focus:border-accent/40 focus:ring-1 focus:ring-accent/20
                           transition-colors"
              />
            </div>

            {error && (
              <div className="bg-red-950/40 border border-red-900/50 rounded-lg px-4 py-2.5
                              text-sm text-red-400 font-mono">
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
            <p className="mt-4 text-center text-xs text-slate-600">
              Demo account:{" "}
              <button
                onClick={() => { setEmail("demo@pypycode.dev"); setPassword("demo1234"); }}
                className="text-accent hover:underline font-mono"
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
