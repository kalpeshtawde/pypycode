import { useState, useEffect, useMemo } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

export default function AuthPage() {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [googleToken, setGoogleToken] = useState<string | null>(null);
  const [showProfileForm, setShowProfileForm] = useState(false);
  const [profileData, setProfileData] = useState({
    firstName: "",
    lastName: "",
    screenName: "",
  });
  const [screenNameAvailability, setScreenNameAvailability] = useState<{
    checking: boolean;
    available: boolean | null;
    message: string;
  }>({ checking: false, available: null, message: "" });
  const { setAuth, token } = useAuthStore();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const redirectPath = useMemo(() => {
    const redirect = searchParams.get("redirect");
    if (!redirect) return "/problems";
    if (!redirect.startsWith("/") || redirect.startsWith("//")) return "/problems";
    if (redirect.startsWith("/problems/")) return redirect;
    return "/problems";
  }, [searchParams]);

  // Check if user is already authenticated
  useEffect(() => {
    if (token) {
      navigate(redirectPath, { replace: true });
    } else {
      setIsCheckingAuth(false);
    }
  }, [token, navigate, redirectPath]);

  useEffect(() => {
    if (!showProfileForm) return;

    const raw = profileData.screenName.trim();
    if (!raw) {
      setScreenNameAvailability({ checking: false, available: null, message: "" });
      return;
    }

    const timer = setTimeout(async () => {
      setScreenNameAvailability({ checking: true, available: null, message: "" });
      try {
        const res = await api.get<{ available: boolean; screenName: string; error?: string }>(
          `/auth/screen-name-availability?screenName=${encodeURIComponent(raw)}`
        );
        setScreenNameAvailability({
          checking: false,
          available: res.available,
          message: res.available ? "" : res.error || `${res.screenName} is not available`,
        });
      } catch {
        setScreenNameAvailability({ checking: false, available: null, message: "Unable to check availability" });
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [profileData.screenName, showProfileForm]);

  const handleGoogleSuccess = async (credentialResponse: any) => {
    setError("");
    setLoading(true);
    setGoogleToken(credentialResponse.credential);
    
    try {
      // First, try to authenticate without profile data
      const res = await api.post<{
        token?: string;
        username?: string;
        is_new: boolean;
        requiresProfileSetup?: boolean;
        firstName?: string;
        lastName?: string;
        screenName?: string;
        error?: string;
      }>(
        "/auth/google",
        { token: credentialResponse.credential }
      );
      
      // If profile setup is required, show profile form
      if (res.requiresProfileSetup || res.is_new) {
        setProfileData({
          firstName: res.firstName || "",
          lastName: res.lastName || "",
          screenName: res.screenName || "",
        });
        setShowProfileForm(true);
        setLoading(false);
        return;
      }

      if (!res.token) {
        setError("Authentication failed");
        setLoading(false);
        return;
      }
      
      // Existing user - log them in
      const me = await api.get<{ id: string; username: string; email: string }>(
        "/auth/me",
        res.token
      );
      setAuth(res.token, me);
      setSuccess(true);
      
      setTimeout(() => {
        navigate(redirectPath, { replace: true });
      }, 1500);
    } catch (err: unknown) {
      // If error is about missing profile data, show form
      const errorMsg = err instanceof Error ? err.message : "Authentication failed";
      if (errorMsg.includes("First name") || errorMsg.includes("screen name")) {
        setShowProfileForm(true);
        setLoading(false);
      } else {
        setError(errorMsg);
        setLoading(false);
      }
    }
  };

  const handleGoogleError = () => {
    setError("Google authentication failed. Please try again.");
    setLoading(false);
  };

  const handleProfileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfileData(prev => ({ ...prev, [name]: value }));
  };

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    if (screenNameAvailability.available === false) {
      setError(screenNameAvailability.message || "Screen name is not available");
      setLoading(false);
      return;
    }

    if (!googleToken) {
      setError("Google token missing. Please try again.");
      setLoading(false);
      return;
    }

    try {
      const res = await api.post<{
        token: string;
        username: string;
        screenName: string;
        firstName: string;
        lastName: string;
        is_new: boolean;
      }>("/auth/google", {
        token: googleToken,
        ...profileData,
      });

      const me = await api.get<{
        id: string;
        username: string;
        email: string;
        firstName: string;
        lastName: string;
        screenName: string;
      }>("/auth/me", res.token);

      setAuth(res.token, me);
      setSuccess(true);

      setTimeout(() => {
        navigate(redirectPath, { replace: true });
      }, 1500);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Profile setup failed");
      setLoading(false);
    }
  };

  // Show loading spinner while checking authentication
if (isCheckingAuth) {
  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-6 py-16 bg-gradient-to-b from-slate-50 via-white to-slate-50">
      <div className="flex flex-col items-center gap-4">
        <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-600 text-sm font-mono">Checking authentication...</p>
      </div>
    </div>
  );
}

return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Reddit+Sans:wght@700;800&display=swap');
        
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }
        
        .auth-logo-icon {
          width: 64px;
          height: 64px;
          border-radius: 14px;
          background: #0F172A;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
          position: relative;
          box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        .auth-logo-prompt {
          font-family: "Reddit Sans", monospace;
          font-size: 28px;
          font-weight: 700;
          color: #1A6BFF;
          position: absolute;
          left: 10px;
          top: 50%;
          transform: translateY(-50%);
          line-height: 1;
        }
        
        .auth-logo-cursor {
          width: 10px;
          height: 18px;
          background: #6366F1;
          border-radius: 2px;
          position: absolute;
          right: 12px;
          top: 50%;
          transform: translateY(-50%);
          animation: blink 1.2s ease-in-out infinite;
        }
        
        .auth-logo-wordmark {
          font-size: 32px;
          font-weight: 800;
          line-height: 1;
          letter-spacing: -0.5px;
          display: inline-flex;
          align-items: baseline;
        }
        
        .auth-logo-blue {
          color: #059669;
          font-size: 32px;
          font-weight: 800;
        }
        
        .auth-logo-dark {
          color: #0F172A;
          font-size: 32px;
          font-weight: 800;
        }
      `}</style>
      <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-6 py-16 bg-gradient-to-b from-slate-50 via-white to-slate-50">
        {/* Background glow */}
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-emerald-500/5 rounded-full blur-[120px]" />
          <div className="absolute bottom-0 right-0 w-80 h-80 bg-blue-500/3 rounded-full blur-[100px]" />
        </div>

        <div className="relative w-full max-w-md">
          {/* Big Animated Logo */}
          <div className="flex justify-center mb-12">
            <div className="flex items-center gap-6">
              {/* Icon */}
              <div className="auth-logo-icon">
                <span className="auth-logo-prompt">&gt;_</span>
                <div className="auth-logo-cursor"></div>
              </div>
              
              {/* Wordmark */}
              <div className="flex flex-col">
                <span className="auth-logo-wordmark">
                  <span className="auth-logo-blue">PyPy</span>
                  <span className="auth-logo-dark">Code</span>
                </span>
                <span className="text-slate-500 text-sm">Python Challenges</span>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white/80 backdrop-blur-sm shadow-xl p-8 transition-all duration-300">
            <h1 className="font-display text-3xl font-bold text-slate-900 text-center mb-2">
              {showProfileForm ? "Complete Your Profile" : "Welcome to PyPyCode"}
            </h1>
            <p className="text-slate-600 text-sm text-center mb-8">
              {showProfileForm
                ? "Tell us a bit about yourself to get started"
                : "Sign in with your Google account to start solving Python problems"}
            </p>

            {/* Success State */}
            {success && (
              <div className="mb-6 p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
                <div className="flex items-center justify-center gap-2">
                  <svg className="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <p className="text-emerald-300 text-sm font-medium">Authentication successful!</p>
                </div>
                <p className="text-emerald-400 text-xs text-center mt-1">Redirecting...</p>
              </div>
            )}

            {/* Profile Form for New Users */}
            {showProfileForm && !success && (
              <form onSubmit={handleProfileSubmit} className="space-y-4 mb-6">
                <div className="grid grid-cols-2 gap-3">
                  <input
                    type="text"
                    name="firstName"
                    placeholder="First Name"
                    value={profileData.firstName}
                    onChange={handleProfileInputChange}
                    required
                    className="px-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-slate-900 text-sm placeholder-slate-500"
                  />
                  <input
                    type="text"
                    name="lastName"
                    placeholder="Last Name"
                    value={profileData.lastName}
                    onChange={handleProfileInputChange}
                    required
                    className="px-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-slate-900 text-sm placeholder-slate-500"
                  />
                </div>
                <input
                  type="text"
                  name="screenName"
                  placeholder="Screen Name (e.g., codeninja, firstName_lastName)"
                  value={profileData.screenName}
                  onChange={handleProfileInputChange}
                  required
                  className="w-full px-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-slate-900 text-sm placeholder-slate-500"
                />
                {screenNameAvailability.message && screenNameAvailability.available === false && (
                  <p className="text-xs text-red-600">
                    {screenNameAvailability.message}
                  </p>
                )}
                <button
                  type="submit"
                  disabled={loading || screenNameAvailability.checking || screenNameAvailability.available === false}
                  className="w-full bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-medium py-2 rounded-lg transition-colors"
                >
                  {loading ? "Setting up..." : "Complete Setup"}
                </button>
              </form>
            )}

            {/* Google Login Button */}
            {!success && !showProfileForm && (
              <div className="flex justify-center mb-6">
                <div className={`transition-all duration-300 ${loading ? 'opacity-50 pointer-events-none scale-95' : 'hover:scale-105'}`}>
                  <GoogleLogin
                    onSuccess={handleGoogleSuccess}
                    onError={handleGoogleError}
                    text="signin_with"
                    theme="outline"
                    shape="pill"
                    width="300"
                  />
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && !success && (
              <div className="mb-6 bg-red-50 border border-red-200 rounded-lg px-4 py-3
                              text-sm text-red-700 font-mono text-center animate-fade-in">
                <div className="flex items-center justify-center gap-2">
                  <svg className="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {error}
                </div>
              </div>
            )}

            {/* Loading State */}
            {loading && !success && (
              <div className="flex flex-col items-center gap-3 py-4">
                <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-slate-600 text-sm font-mono">Authenticating...</p>
              </div>
            )}

            {/* Additional Info */}
            {!success && !loading && (
              <div className="mt-6 pt-6 border-t border-slate-200">
                <p className="text-slate-500 text-xs text-center">
                  By signing in, you agree to our{" "}
                  <a href="/terms" className="text-emerald-600 hover:text-emerald-700 transition-colors font-medium">
                    Terms
                  </a>{" "}
                  and{" "}
                  <a href="/privacy" className="text-emerald-600 hover:text-emerald-700 transition-colors font-medium">
                    Privacy Policy
                  </a>
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}
