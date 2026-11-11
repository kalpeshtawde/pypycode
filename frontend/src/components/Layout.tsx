import { Outlet, NavLink, useLocation, useNavigate } from "react-router-dom";
import { useAuthStore } from "../hooks/useAuth";
import { useThemeStore } from "../hooks/useTheme";
import { useEffect, useState } from "react";
import { api } from "../utils/api";
import type { BillingAccessStatus } from "../types";
import Footer from "./Footer";

export default function Layout() {
  const { token, user, setAuth, logout } = useAuthStore();
  const { theme, toggleTheme } = useThemeStore();
  const navigate = useNavigate();
  const location = useLocation();
  const authRedirectPath = `${location.pathname}${location.search}`;
  const authLink = `/auth?redirect=${encodeURIComponent(authRedirectPath)}`;
  const [accessStatus, setAccessStatus] = useState<BillingAccessStatus | null>(null);
  const [loadingAccessStatus, setLoadingAccessStatus] = useState(false);
  const [billingEnabled, setBillingEnabled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    setMobileOpen(false);
  }, [location.pathname]);

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
    api
      .get<{ enabled: boolean }>("/feature-flags/check/Billing")
      .then((res) => setBillingEnabled(res.enabled))
      .catch(() => setBillingEnabled(false));
  }, []);

  useEffect(() => {
    if (!token || loadingAccessStatus || !accessStatus) {
      return;
    }

    // If billing is disabled, skip the pricing redirect flow
    if (!billingEnabled) {
      return;
    }

    const hasAccess = accessStatus.accessStatus === "subscribed" || accessStatus.accessStatus === "trialing";
    const isPublicPath = location.pathname === "/auth" || location.pathname === "/pricing" || location.pathname === "/problems";
    const isProblemDetail = location.pathname.startsWith("/problems/") && location.pathname !== "/problems/";
    if (!hasAccess && !isPublicPath && isProblemDetail) {
      navigate(`/pricing?required=1&redirect=${encodeURIComponent(authRedirectPath)}`, { replace: true });
    }
  }, [token, loadingAccessStatus, accessStatus, location.pathname, authRedirectPath, navigate, billingEnabled]);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-900">
      {/* Navbar */}
      <header 
        className="sticky top-0 z-50 border-b px-4 sm:px-6 lg:px-10"
        style={{
          background: 'var(--header-bg)',
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          borderBottomColor: 'var(--border-default)',
          height: '64px'
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
            background: var(--logo-bg);
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
            color: #34D399;
            position: absolute;
            left: 5px;
            top: 50%;
            transform: translateY(-50%);
            line-height: 1;
          }
          
          .logo-cursor {
            width: 5px;
            height: 9px;
            background: #34D399;
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
            align-items: baseline;
          }
          
          .logo-blue {
            color: #059669;
            font-size: 19px;
            font-weight: 800;
          }
          
          .logo-dark {
            color: var(--text-primary);
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
            <span className="logo-wordmark hidden min-[400px]:inline-flex">
              <span className="logo-blue">PyPy</span>
              <span className="logo-dark">Code</span>
            </span>
          </NavLink>

          {/* Links */}
          <div className="hidden md:flex items-center gap-6 lg:gap-8 md:ml-6 lg:ml-12">
            <style>{`
              .nav-link {
                font-weight: 600;
                font-size: 15px;
                color: var(--text-muted);
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
                background-color: var(--accent-text);
                transition: width 200ms ease;
              }
              .nav-link:hover {
                color: var(--text-primary);
              }
              .nav-link:hover::after {
                width: 100%;
              }
              .nav-link.active {
                color: var(--accent-text);
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
            {billingEnabled && (
              <NavLink 
                to="/pricing" 
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              >
                Pricing
              </NavLink>
            )}
            <NavLink 
              to="/contact" 
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              Contact
            </NavLink>
          </div>

          {/* Auth */}
          <div className="flex items-center gap-2 sm:gap-3 ml-auto">
            <button
              onClick={toggleTheme}
              aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
              title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
              className="flex items-center justify-center w-8 h-8 sm:w-9 sm:h-9 rounded-full border border-slate-200 dark:border-slate-700
                         bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300
                         hover:border-slate-300 dark:hover:border-slate-600 hover:text-slate-900 dark:hover:text-slate-100
                         transition-all duration-200 cursor-pointer shrink-0"
            >
              {theme === "dark" ? (
                <svg viewBox="0 0 24 24" fill="none" className="w-[18px] h-[18px]" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <circle cx="12" cy="12" r="4" />
                  <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" />
                </svg>
              ) : (
                <svg viewBox="0 0 24 24" fill="none" className="w-[18px] h-[18px]" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
                </svg>
              )}
            </button>
            {user ? (
              <>
                {/* Avatar Circle */}
                <NavLink
                  to="/profile"
                  aria-label="Profile"
                  className="shrink-0"
                  style={{
                    width: '34px',
                    height: '34px',
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #059669, #10B981)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontWeight: 700,
                    fontSize: '14px'
                  }}
                >
                  {user.username.charAt(0).toUpperCase()}
                </NavLink>
                <NavLink
                  to="/profile"
                  className={({ isActive }) => `nav-link hidden md:inline-block ${isActive ? 'active' : ''}`}
                >
                  Profile
                </NavLink>
                <button 
                  onClick={() => { logout(); navigate("/"); }}
                  className="text-xs sm:text-[13px] font-semibold tracking-[0.2px] rounded-full px-2.5 sm:px-3.5 py-2 whitespace-nowrap cursor-pointer transition-all duration-200
                             bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700
                             text-slate-600 dark:text-slate-300 shadow-[0_1px_2px_rgba(15,23,42,0.04)] dark:shadow-none
                             hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-500/10 hover:border-red-200 dark:hover:border-red-500/30
                             hover:shadow-[0_4px_10px_rgba(220,38,38,0.12)] dark:hover:shadow-none
                             focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500/30 shrink-0"
                >
                  Sign out
                </button>
              </>
            ) : (
              <NavLink to={authLink} className="btn-primary text-sm py-2 px-4 sm:px-5 whitespace-nowrap shrink-0">
                Sign in
              </NavLink>
            )}
            <button
              onClick={() => setMobileOpen((open) => !open)}
              aria-label={mobileOpen ? "Close menu" : "Open menu"}
              aria-expanded={mobileOpen}
              className="md:hidden flex items-center justify-center w-8 h-8 rounded-full border border-slate-200 dark:border-slate-700
                         bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300
                         hover:border-slate-300 dark:hover:border-slate-600 hover:text-slate-900 dark:hover:text-slate-100
                         transition-all duration-200 cursor-pointer shrink-0"
            >
              {mobileOpen ? (
                <svg viewBox="0 0 24 24" fill="none" className="w-4 h-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
                  <path d="M6 6l12 12M18 6L6 18" />
                </svg>
              ) : (
                <svg viewBox="0 0 24 24" fill="none" className="w-4 h-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
                  <path d="M4 7h16M4 12h16M4 17h16" />
                </svg>
              )}
            </button>
          </div>
        </nav>

        {/* Mobile menu */}
        {mobileOpen && (
          <div
            className="md:hidden absolute left-0 right-0 top-full border-b border-slate-200 dark:border-slate-700
                       bg-white dark:bg-slate-800 shadow-lg shadow-slate-900/5 dark:shadow-black/30"
          >
            <nav className="flex flex-col px-4 py-2">
              {[
                { to: "/problems", label: "Problems" },
                { to: "/leaderboard", label: "Leaderboard" },
                ...(billingEnabled ? [{ to: "/pricing", label: "Pricing" }] : []),
                { to: "/contact", label: "Contact" },
                ...(user ? [{ to: "/profile", label: "Profile" }] : []),
              ].map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `py-3 text-[15px] font-semibold border-b border-slate-100 dark:border-slate-700 last:border-0 ${
                      isActive ? "text-emerald-600 dark:text-emerald-400" : "text-slate-600 dark:text-slate-300"
                    }`
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>
          </div>
        )}
      </header>

      {accessStatus?.accessStatus === "trialing" && billingEnabled && (
        <div className="w-full px-4 py-2 bg-amber-50 dark:bg-amber-500/10 border-b border-amber-200 dark:border-amber-500/25">
          <div className="max-w-5xl mx-auto flex items-center justify-center gap-2">
            <svg className="h-3.5 w-3.5 text-amber-500 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span className="text-xs font-medium text-amber-700 dark:text-amber-300">
              {accessStatus.trial.daysRemaining} day{accessStatus.trial.daysRemaining === 1 ? "" : "s"} remaining in your trial
            </span>
            <a href="/pricing" className="text-xs font-semibold text-amber-800 dark:text-amber-300 underline underline-offset-2 hover:text-amber-900 dark:hover:text-amber-200 transition-colors">
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
