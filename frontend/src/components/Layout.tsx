import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useAuthStore } from "../hooks/useAuth";
import { useEffect } from "react";
import { api } from "../utils/api";

export default function Layout() {
  const { token, user, setAuth, logout } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (token && !user) {
      api.get<{ id: number; username: string; email: string }>("/auth/me", token)
        .then((u) => setAuth(token, u))
        .catch(() => logout());
    }
  }, [token]);

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `text-sm font-body transition-colors duration-150 ${
      isActive ? "text-accent" : "text-slate-400 hover:text-white"
    }`;

  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar */}
      <header className="sticky top-0 z-50 border-b border-surface-border bg-navy-950/80 backdrop-blur-xl">
        <nav className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between gap-8">
          {/* Logo */}
          <NavLink to="/" className="flex items-center gap-2 shrink-0">
            <span className="w-7 h-7 rounded-md bg-accent flex items-center justify-center">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M2 2h4v4H2zM8 2h4v4H8zM2 8h4v4H2zM8 8h4v4H8z" fill="#0b1424"/>
              </svg>
            </span>
            <span className="font-display text-lg font-semibold tracking-tight text-white">
              PyPy<span className="text-accent">Code</span>
            </span>
          </NavLink>

          {/* Links */}
          <div className="flex items-center gap-8">
            <NavLink to="/problems" className={linkClass}>Problems</NavLink>
            <NavLink to="/leaderboard" className={linkClass}>Leaderboard</NavLink>
          </div>

          {/* Auth */}
          <div className="flex items-center gap-3 ml-auto">
            {user ? (
              <>
                <span className="text-sm text-slate-400 hidden sm:block">
                  <span className="text-accent font-mono">@</span>{user.username}
                </span>
                <button onClick={() => { logout(); navigate("/"); }} className="btn-ghost text-xs py-1.5 px-3">
                  Sign out
                </button>
              </>
            ) : (
              <NavLink to="/auth" className="btn-primary text-xs py-1.5 px-4">
                Sign in
              </NavLink>
            )}
          </div>
        </nav>
      </header>

      {/* Page content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-surface-border py-8 px-6 text-center">
        <p className="text-slate-600 text-xs font-body">
          PyPyCode — Python-only coding challenges. Built with Flask + React.
        </p>
      </footer>
    </div>
  );
}
