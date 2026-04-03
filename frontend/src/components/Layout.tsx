import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useAuthStore } from "../hooks/useAuth";
import { useEffect } from "react";
import { api } from "../utils/api";
import Footer from "./Footer";

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

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      {/* Navbar */}
      <header 
        className="sticky top-0 z-50 border-b"
        style={{
          background: 'rgba(241, 245, 249, 0.85)',
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          borderBottomColor: '#E2E8F0',
          height: '64px',
          padding: '0 40px'
        }}
      >
        <nav className="h-full flex items-center justify-between">
          {/* Logo */}
          <NavLink to="/" className="shrink-0" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {/* 2×2 Grid Icon */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '2px',
              width: '16px',
              height: '16px'
            }}>
              <div style={{ width: '7px', height: '7px', backgroundColor: '#1A6BFF', borderRadius: '2px' }} />
              <div style={{ width: '7px', height: '7px', backgroundColor: '#6366F1', borderRadius: '2px' }} />
              <div style={{ width: '7px', height: '7px', backgroundColor: '#6366F1', borderRadius: '2px' }} />
              <div style={{ width: '7px', height: '7px', backgroundColor: '#1A6BFF', borderRadius: '2px' }} />
            </div>

            {/* Wordmark */}
            <div style={{ display: 'flex', gap: '0px' }}>
              <span style={{ fontSize: '19px', fontWeight: 800, color: '#1A6BFF' }}>
                PyPy
              </span>
              <span style={{ fontSize: '19px', fontWeight: 800, color: '#0F172A' }}>
                Code
              </span>
            </div>
          </NavLink>

          {/* Links */}
          <div className="flex items-center gap-8 ml-12">
            <style>{`
              .nav-link {
                font-weight: 600;
                font-size: 15px;
                color: #64748B;
                text-decoration: none;
                position: relative;
                transition: color 200ms ease;
              }
              .nav-link::after {
                content: '';
                position: absolute;
                bottom: -4px;
                left: 0;
                width: 0;
                height: 2px;
                background-color: #1A6BFF;
                transition: width 200ms ease;
              }
              .nav-link:hover {
                color: #0F172A;
              }
              .nav-link:hover::after {
                width: 100%;
              }
              .nav-link.active {
                color: #1A6BFF;
              }
              .nav-link.active::after {
                width: 100%;
              }
            `}</style>
            <NavLink 
              to="/problems" 
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              Problems
            </NavLink>
            <NavLink 
              to="/leaderboard" 
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              Leaderboard
            </NavLink>
          </div>

          {/* Auth */}
          <div className="flex items-center gap-3 ml-auto">
            {user ? (
              <>
                {/* Avatar Circle */}
                <div
                  style={{
                    width: '34px',
                    height: '34px',
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #1A6BFF, #6366F1)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontWeight: 700,
                    fontSize: '14px'
                  }}
                >
                  {user.username.charAt(0).toUpperCase()}
                </div>
                <button 
                  onClick={() => { logout(); navigate("/"); }}
                  style={{
                    fontWeight: 500,
                    fontSize: '14px',
                    color: '#64748B',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    transition: 'color 200ms ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.color = '#0F172A'}
                  onMouseLeave={(e) => e.currentTarget.style.color = '#64748B'}
                >
                  Sign out
                </button>
              </>
            ) : (
              <NavLink to="/auth" className="btn-primary text-sm py-2 px-5">
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
      <Footer />
    </div>
  );
}
