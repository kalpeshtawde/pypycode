import { useEffect, useState, type ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";
import type { User } from "../types";

export default function RequireAdmin({ children }: { children: ReactNode }) {
  const { token, setAuth } = useAuthStore();
  const [state, setState] = useState<"checking" | "allowed" | "denied">("checking");

  useEffect(() => {
    if (!token) {
      setState("denied");
      return;
    }

    let cancelled = false;
    setState("checking");
    api
      .get<User>("/auth/me", token)
      .then((user) => {
        if (cancelled) return;
        setAuth(token, user);
        setState(user.isAdmin ? "allowed" : "denied");
      })
      .catch(() => {
        if (!cancelled) setState("denied");
      });

    return () => {
      cancelled = true;
    };
  }, [token, setAuth]);

  if (state === "checking") {
    return (
      <div className="min-h-[calc(100vh-64px)] flex items-center justify-center">
        <p className="text-slate-600 dark:text-slate-400 font-mono text-sm">Checking access…</p>
      </div>
    );
  }

  if (state === "denied") {
    return <Navigate to={token ? "/" : "/auth"} replace />;
  }

  return <>{children}</>;
}
