import { Outlet, NavLink, useLocation, useNavigate } from "react-router-dom";
import { useAuthStore } from "../hooks/useAuth";
import { useEffect, useState } from "react";
import { api } from "../utils/api";
import type { BillingAccessStatus } from "../types";
import Footer from "./Footer";

export default function Layout() {
  const { token, user, setAuth, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const authRedirectPath = `${location.pathname}${location.search}`;
  const authLink = `/auth?redirect=${encodeURIComponent(authRedirectPath)}`;
  const [accessStatus, setAccessStatus] = useState<BillingAccessStatus | null>(null);
  const [loadingAccessStatus, setLoadingAccessStatus] = useState(false);

  useEffect(() => {
    if (token && !user) {
      api.get<{ id: string; username: string; email: string; firstName?: string | null; lastName?: string | null; screenName?: string | null }>("/auth/me", token)
        .then((u) => setAuth(token, u))
        .catch(() => logout());
    }
  }, [token]);

  useEffect(() => {
    if (!token) {
      setAccessStatus(null);
      return;
    }

    setLoadingAccessStatus(true);
    api
      .get<BillingAccessStatus>("/billing/access-status", token)
      .then((status) => setAccessStatus(status))
      .catch(() => setAccessStatus(null))
      .finally(() => setLoadingAccessStatus(false));
  }, [token, location.pathname]);

  useEffect(() => {
    if (!token || loadingAccessStatus || !accessStatus) {
      return;
    }

    const hasAccess = accessStatus.accessStatus === "subscribed" || accessStatus.accessStatus === "trialing";
    const isPublicPath = location.pathname === "/auth" || location.pathname === "/pricing" || location.pathname === "/problems";
    const isProblemDetail = location.pathname.startsWith("/problems/") && location.pathname !== "/problems/";
    if (!hasAccess && !isPublicPath && isProblemDetail) {
      navigate(`/pricing?required=1&redirect=${encodeURIComponent(authRedirectPath)}`, { replace: true });
    }
  }, [token, loadingAccessStatus, accessStatus, location.pathname, authRedirectPath, navigate]);

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
        <style>{`
          @import url('https://fonts.googleapis.com/css2?family=Reddit+Sans:wght@700;800&display=swap');
          
          @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
          }
          
          .logo-icon {
            width: 32px;
            height: 32px;
            border-radius: 7px;
            background: #0F172A;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            position: relative;
          }
          
          .logo-prompt {
            font-family: "Reddit Sans", monospace;
            font-size: 14px;
            font-weight: 700;
            color: #1A6BFF;
            position: absolute;
            left: 5px;
            top: 50%;
            transform: translateY(-50%);
            line-height: 1;
          }
          
          .logo-cursor {
            width: 5px;
            height: 9px;
            background: #6366F1;
            border-radius: 1px;
            position: absolute;
            right: 6px;
            top: 50%;
            transform: translateY(-50%);
            animation: blink 1.2s ease-in-out infinite;
          }
          
          .logo-wordmark {
            font-size: 19px;
            font-weight: 800;
            line-height: 1;
            letter-spacing: -0.3px;
            display: inline-flex;
            align-items: baseline;
          }
          
          .logo-blue {
            color: #1A6BFF;
            font-size: 19px;
            font-weight: 800;
          }
          
          .logo-dark {
            color: #0F172A;
            font-size: 19px;
            font-weight: 800;
          }
        `}</style>
        
        <nav className="h-full flex items-center justify-between">
          {/* Logo */}
          <NavLink 
            to="/" 
            style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '10px', 
              textDecoration: 'none', 
              cursor: 'pointer' 
            }}
          >
            {/* Icon */}
            <div className="logo-icon">
              <span className="logo-prompt">&gt;_</span>
              <div className="logo-cursor"></div>
            </div>
            
            {/* Wordmark */}
            <span className="logo-wordmark">
              <span className="logo-blue">PyPy</span>
              <span className="logo-dark">Code</span>
            </span>
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
            <NavLink 
              to="/pricing" 
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              Pricing
            </NavLink>
            <NavLink 
              to="/contact" 
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              Contact
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
                <NavLink
                  to="/profile"
                  className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                >
                  Profile
                </NavLink>
                <button 
                  onClick={() => { logout(); navigate("/"); }}
                  style={{
                    fontWeight: 600,
                    fontSize: '13px',
                    letterSpacing: '0.2px',
                    color: '#475569',
                    background: '#FFFFFF',
                    border: '1px solid #E2E8F0',
                    borderRadius: '999px',
                    padding: '8px 14px',
                    cursor: 'pointer',
                    transition: 'all 180ms ease',
                    boxShadow: '0 1px 2px rgba(15,23,42,0.04)'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.color = '#DC2626';
                    e.currentTarget.style.background = '#FEF2F2';
                    e.currentTarget.style.borderColor = '#FECACA';
                    e.currentTarget.style.boxShadow = '0 4px 10px rgba(220,38,38,0.12)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.color = '#475569';
                    e.currentTarget.style.background = '#FFFFFF';
                    e.currentTarget.style.borderColor = '#E2E8F0';
                    e.currentTarget.style.boxShadow = '0 1px 2px rgba(15,23,42,0.04)';
                  }}
                  onFocus={(e) => {
                    e.currentTarget.style.outline = 'none';
                    e.currentTarget.style.boxShadow = '0 0 0 3px rgba(220,38,38,0.2)';
                  }}
                  onBlur={(e) => {
                    e.currentTarget.style.boxShadow = '0 1px 2px rgba(15,23,42,0.04)';
                  }}
                >
                  Sign out
                </button>
              </>
            ) : (
              <NavLink to={authLink} className="btn-primary text-sm py-2 px-5">
                Sign in
              </NavLink>
            )}
          </div>
        </nav>
      </header>

      {accessStatus?.accessStatus === "trialing" && (
        <div className="w-full px-4 py-2 bg-amber-50 border-b border-amber-200">
          <div className="max-w-5xl mx-auto flex items-center justify-center gap-2">
            <svg className="h-3.5 w-3.5 text-amber-500 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span className="text-xs font-medium text-amber-700">
              {accessStatus.trial.daysRemaining} day{accessStatus.trial.daysRemaining === 1 ? "" : "s"} remaining in your trial
            </span>
            <a href="/pricing" className="text-xs font-semibold text-amber-800 underline underline-offset-2 hover:text-amber-900 transition-colors">
              Upgrade now
            </a>
          </div>
        </div>
      )}

      {/* Page content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}
