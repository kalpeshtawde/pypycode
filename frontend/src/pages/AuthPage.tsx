import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

export default function AuthPage() {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleGoogleSuccess = async (credentialResponse: any) => {
    setError("");
    setLoading(true);
    try {
      const res = await api.post<{ token: string; username: string; is_new: boolean }>(
        "/auth/google",
        { token: credentialResponse.credential }
      );
      const me = await api.get<{ id: number; username: string; email: string }>(
        "/auth/me",
        res.token
      );
      setAuth(res.token, me);
      navigate("/problems");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleError = () => {
    setError("Google authentication failed. Please try again.");
  };

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-6 py-16 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
        {/* Background glow */}
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-emerald-500/8 rounded-full blur-[120px]" />
          <div className="absolute bottom-0 right-0 w-80 h-80 bg-blue-500/5 rounded-full blur-[100px]" />
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
              Welcome to PyPyCode
            </h1>
            <p className="text-slate-400 text-sm text-center mb-8">
              Sign in with your Google account to start solving Python problems
            </p>

            <div className="flex justify-center mb-6">
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={handleGoogleError}
                text="signin_with"
                theme="dark"
              />
            </div>

            {error && (
              <div className="bg-red-950/30 border border-red-900/40 rounded-lg px-4 py-2.5
                              text-sm text-red-300 font-mono text-center">
                {error}
              </div>
            )}

            {loading && (
              <div className="text-center text-slate-400 text-sm font-mono">
                Signing in…
              </div>
            )}
          </div>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}
