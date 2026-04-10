import { useEffect, useMemo, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { useAuthStore } from "../hooks/useAuth";
import type { BillingAccessStatus, BillingSubscriptionSnapshot } from "../types";
import { api } from "../utils/api";

interface PricingResponse {
  plan: string;
  productId: string;
  amountCents: number;
  amountDisplay: string;
  currency: string;
  interval: string;
  trialDays: number;
}

const FEATURES = [
  "Unlimited access to all coding problems",
  "Full leaderboard participation",
  "Unlimited submissions and runs",
  "Priority access to new releases",
];

export default function PricingPage() {
  const { token, user } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const authLink = `/auth?redirect=${encodeURIComponent(location.pathname + location.search)}`;

  const [pricing, setPricing] = useState<PricingResponse | null>(null);
  const [accessStatus, setAccessStatus] = useState<BillingAccessStatus | null>(null);
  const [subscription, setSubscription] = useState<BillingSubscriptionSnapshot | null>(null);
  const [loadingPricing, setLoadingPricing] = useState(true);
  const [loadingAccessStatus, setLoadingAccessStatus] = useState(false);
  const [trialLoading, setTrialLoading] = useState(false);
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const [error, setError] = useState("");

  const searchParams = useMemo(() => new URLSearchParams(location.search), [location.search]);
  const isSuccess = searchParams.get("success") === "1";
  const isCanceled = searchParams.get("canceled") === "1";
  const isRequired = searchParams.get("required") === "1";
  const redirectAfterUnlock = searchParams.get("redirect") || "/problems";

  useEffect(() => {
    api
      .get<PricingResponse>("/billing/pricing")
      .then((res) => setPricing(res))
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : "Unable to load pricing");
      })
      .finally(() => setLoadingPricing(false));
  }, []);

  useEffect(() => {
    if (!token) {
      setAccessStatus(null);
      return;
    }

    setLoadingAccessStatus(true);
    api
      .get<BillingAccessStatus>("/billing/access-status", token)
      .then((res) => setAccessStatus(res))
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : "Unable to check trial eligibility");
      })
      .finally(() => setLoadingAccessStatus(false));

    // Fetch subscription details on successful payment return
    if (isSuccess && token) {
      api
        .get<{ subscription: BillingSubscriptionSnapshot }>("/billing/subscription", token)
        .then((res) => setSubscription(res.subscription))
        .catch(() => {}); // Silently ignore - subscription may not be synced yet
    }
  }, [token, isSuccess]);

  const safeRedirectAfterUnlock = useMemo(() => {
    if (!redirectAfterUnlock.startsWith("/") || redirectAfterUnlock.startsWith("//")) {
      return "/problems";
    }
    return redirectAfterUnlock;
  }, [redirectAfterUnlock]);

  const handleSubscribe = async () => {
    if (!token) return;

    setCheckoutLoading(true);
    setError("");

    try {
      const response = await api.post<{ url: string; sessionId: string }>(
        "/billing/checkout-session",
        { redirect: safeRedirectAfterUnlock },
        token
      );
      window.location.href = response.url;
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unable to create Stripe checkout session");
      setCheckoutLoading(false);
    }
  };

  const handleStartTrial = async () => {
    if (!token) return;

    setTrialLoading(true);
    setError("");

    try {
      const response = await api.post<BillingAccessStatus>("/billing/start-trial", {}, token);
      setAccessStatus(response);
      navigate("/problems", { replace: true });
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unable to start trial");
    } finally {
      setTrialLoading(false);
    }
  };

  const hasSubscriptionAccess = accessStatus?.accessStatus === "subscribed";
  const canStartTrial = !!token && !!accessStatus && !accessStatus.trial.used && !hasSubscriptionAccess;

  return (
    <div className="min-h-[calc(100vh-64px)] bg-gradient-to-b from-slate-50 via-white to-emerald-50/30 py-16 px-6">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="font-display text-4xl sm:text-5xl font-bold text-slate-900 tracking-tight mb-4">
            Annual Access Plan
          </h1>
          <p className="text-slate-600 text-lg max-w-2xl mx-auto">
            One simple subscription for full PyPyCode access. No feature gates, no tiers.
          </p>
        </div>

        {isSuccess && (
          <div className="mb-8 rounded-2xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-white p-8 text-center shadow-sm">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100">
              <svg className="h-8 w-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="font-display text-2xl font-bold text-slate-900 mb-2">
              Payment Successful!
            </h2>
            <p className="text-slate-600 mb-6">
              Your annual subscription has been activated. You now have full access to all PyPyCode features.
            </p>
            {subscription?.currentPeriodEnd && (
              <div className="mb-6 inline-block rounded-xl bg-white border border-emerald-100 px-6 py-4 text-left shadow-sm">
                <div className="text-sm text-slate-500 mb-1">Subscription renews on</div>
                <div className="font-semibold text-slate-900 text-lg">
                  {new Date(subscription.currentPeriodEnd).toLocaleDateString(undefined, {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </div>
              </div>
            )}
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <button
                onClick={() => navigate(safeRedirectAfterUnlock)}
                className="btn-primary text-base px-8 py-3"
              >
                Continue to Problems
              </button>
              <Link
                to="/profile"
                className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-6 py-3 text-slate-700 font-medium hover:bg-slate-50 transition-colors"
              >
                View Subscription in Profile
              </Link>
            </div>
          </div>
        )}

        {isCanceled && (
          <div className="mb-6 rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 text-amber-800 text-sm text-center">
            Checkout canceled. You can start again anytime.
          </div>
        )}

        {isRequired && (
          <div className="mb-6 rounded-lg border border-blue-300 bg-blue-50 px-4 py-3 text-blue-800 text-sm text-center">
            Pick a plan to continue: start your {pricing?.trialDays ?? 15}-day trial or subscribe annually.
          </div>
        )}

        {error && (
          <div className="mb-6 rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-red-700 text-sm text-center">
            {error}
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-6 items-stretch">
          <div className="rounded-2xl border border-slate-200 bg-white/95 shadow-sm p-8">
            <p className="inline-block rounded-full bg-blue-100 text-blue-700 text-xs font-semibold tracking-wide px-3 py-1 mb-4">
              FREE TRIAL
            </p>

            <h2 className="font-display text-3xl font-bold text-slate-900 mb-2">
              {loadingPricing ? "15-day trial" : `${pricing?.trialDays ?? 15}-day trial`}
            </h2>

            <p className="text-slate-600 mb-6">Start with full access for free. No payment required to begin.</p>

            <ul className="space-y-3 mb-8">
              <li className="flex items-center gap-3 text-slate-700">
                <span className="w-5 h-5 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold">
                  ✓
                </span>
                Full access to all problems and submissions
              </li>
              <li className="flex items-center gap-3 text-slate-700">
                <span className="w-5 h-5 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold">
                  ✓
                </span>
                Trial countdown visible in your account
              </li>
            </ul>

            {!token && (
              <Link to={authLink} className="btn-primary inline-flex text-base px-8 py-3">
                Sign in to start trial
              </Link>
            )}

            {token && loadingAccessStatus && <p className="text-slate-500 text-sm">Checking eligibility...</p>}

            {token && !loadingAccessStatus && !accessStatus && (
              <p className="text-slate-600 text-sm">Unable to load trial eligibility right now. Please refresh.</p>
            )}

            {token && !loadingAccessStatus && !!accessStatus && canStartTrial && (
              <button
                onClick={handleStartTrial}
                disabled={trialLoading}
                className="btn-primary text-base px-8 py-3 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                {trialLoading ? "Starting trial..." : "Start free trial"}
              </button>
            )}

            {token && !loadingAccessStatus && !!accessStatus && !canStartTrial && (
              <p className="text-slate-600 text-sm">
                {hasSubscriptionAccess
                  ? "You already have an active subscription."
                  : accessStatus?.accessStatus === "trialing"
                  ? "Trial activated. You have full access to all problems."
                  : accessStatus?.trial.used
                  ? "Trial already used for this account."
                  : "Trial is not available right now."}
              </p>
            )}
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white shadow-xl shadow-slate-200/50 p-8">
            <p className="inline-block rounded-full bg-emerald-100 text-emerald-700 text-xs font-semibold tracking-wide px-3 py-1 mb-4">
              ALL ACCESS
            </p>

            <div className="flex items-end gap-2 mb-2">
              <span className="text-5xl font-display font-bold text-slate-900">
                {loadingPricing ? "..." : pricing?.amountDisplay ?? "$30"}
              </span>
              <span className="text-slate-500 mb-2">/ year</span>
            </div>

            <p className="text-slate-600 mb-6">
              Full platform subscription billed annually. Includes every current and future coding feature.
            </p>

            <ul className="space-y-3 mb-8">
              {FEATURES.map((feature) => (
                <li key={feature} className="flex items-center gap-3 text-slate-700">
                  <span className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center text-xs font-bold">
                    ✓
                  </span>
                  {feature}
                </li>
              ))}
            </ul>

            {token ? (
              <button
                onClick={handleSubscribe}
                disabled={checkoutLoading || loadingPricing || !!hasSubscriptionAccess}
                className="btn-primary text-base px-8 py-3 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                {hasSubscriptionAccess
                  ? "Subscription Active"
                  : checkoutLoading
                  ? "Redirecting to Stripe..."
                  : "Subscribe with Stripe"}
              </button>
            ) : (
              <Link to={authLink} className="btn-primary inline-flex text-base px-8 py-3">
                Sign in to subscribe
              </Link>
            )}
          </div>
        </div>

        <p className="mt-10 text-center text-xs text-slate-500">
          Signed in as {user?.email ?? "guest"} · Stripe product {pricing?.productId ?? "prod_UIjX4gboLVPWDq"}
        </p>
      </div>
    </div>
  );
}
