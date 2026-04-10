import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";
import type { BillingAccessStatus, UserProfile } from "../types";

export default function ProfilePage() {
  const { token, setAuth, logout } = useAuthStore();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [billingStatus, setBillingStatus] = useState<BillingAccessStatus | null>(null);
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    screenName: "",
  });
  const [screenNameAvailability, setScreenNameAvailability] = useState<{
    checking: boolean;
    available: boolean | null;
    message: string;
  }>({ checking: false, available: null, message: "" });

  useEffect(() => {
    if (!token) {
      navigate("/auth");
      return;
    }

    api
      .get<UserProfile>("/auth/profile", token)
      .then((res) => {
        setProfile(res);
        setFormData({
          firstName: res.firstName || "",
          lastName: res.lastName || "",
          screenName: (res.screenName || "").replace(/^@/, ""),
        });
      })
      .catch((err: unknown) => {
        const msg = err instanceof Error ? err.message : "Failed to load profile";
        setError(msg);
        if (msg.toLowerCase().includes("unauthorized")) {
          logout();
          navigate("/auth");
        }
      })
      .finally(() => setLoading(false));

    api
      .get<BillingAccessStatus>("/billing/access-status", token)
      .then((res) => setBillingStatus(res))
      .catch(() => setBillingStatus(null));
  }, [token, navigate, logout]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  useEffect(() => {
    if (!profile) return;

    const raw = formData.screenName.trim();
    if (!raw) {
      setScreenNameAvailability({ checking: false, available: null, message: "" });
      return;
    }

    const timer = setTimeout(async () => {
      setScreenNameAvailability({ checking: true, available: null, message: "" });
      try {
        const res = await api.get<{ available: boolean; screenName: string; error?: string }>(
          `/auth/screen-name-availability?screenName=${encodeURIComponent(raw)}&excludeUserId=${encodeURIComponent(profile.id)}`,
          token
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
  }, [formData.screenName, profile, token]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !profile) return;

    if (screenNameAvailability.available === false) {
      setError(screenNameAvailability.message || "Screen name is not available");
      return;
    }

    setSaving(true);
    setError("");
    setSuccess("");

    try {
      const updated = await api.post<{
        id: string;
        username: string;
        email: string;
        firstName: string | null;
        lastName: string | null;
        screenName: string | null;
      }>("/auth/profile", formData, token);

      setProfile((prev) =>
        prev
          ? {
              ...prev,
              firstName: updated.firstName,
              lastName: updated.lastName,
              screenName: updated.screenName,
            }
          : prev
      );

      setFormData({
        firstName: updated.firstName || "",
        lastName: updated.lastName || "",
        screenName: (updated.screenName || "").replace(/^@/, ""),
      });

      setAuth(token, {
        id: updated.id,
        username: updated.username,
        email: updated.email,
        firstName: updated.firstName,
        lastName: updated.lastName,
        screenName: updated.screenName,
      });

      setSuccess("Profile updated successfully.");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to update profile");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[calc(100vh-64px)] flex items-center justify-center">
        <p className="text-slate-600 font-mono text-sm">Loading profile...</p>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-6">
        <p className="text-red-600 font-mono text-sm">{error || "Profile not found"}</p>
      </div>
    );
  }

  return (
    <div className="min-h-[calc(100vh-64px)] bg-gradient-to-b from-slate-50 via-white to-slate-50 px-6 py-12">
      <div className="max-w-5xl mx-auto space-y-8">
        <div>
          <h1 className="font-display text-4xl font-semibold text-slate-900">My Profile</h1>
          <p className="text-slate-600 mt-2">View your details, stats, and recent activity.</p>
        </div>

        <div className="grid md:grid-cols-4 gap-4">
          <StatCard label="Solved Problems" value={profile.stats.solvedProblems} />
          <StatCard label="Total Submissions" value={profile.stats.totalSubmissions} />
          <StatCard label="Accepted" value={profile.stats.acceptedSubmissions} />
          <StatCard label="Acceptance Rate" value={`${profile.stats.acceptanceRate}%`} />
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          <section className="lg:col-span-1 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-slate-900 font-semibold mb-4">Profile Details</h2>
            <form className="space-y-4" onSubmit={handleSave}>
              <div>
                <label className="block text-sm text-slate-600 mb-1">Email</label>
                <input
                  value={profile.email}
                  disabled
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-slate-100 text-slate-600 text-sm"
                />
              </div>

              <div>
                <label className="block text-sm text-slate-600 mb-1">First Name</label>
                <input
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 bg-slate-50 text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm text-slate-600 mb-1">Last Name</label>
                <input
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 bg-slate-50 text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm text-slate-600 mb-1">Screen Name</label>
                <input
                  name="screenName"
                  value={formData.screenName}
                  onChange={handleChange}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 bg-slate-50 text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              {screenNameAvailability.message && screenNameAvailability.available === false && (
                <p className="text-xs text-red-600">
                  {screenNameAvailability.message}
                </p>
              )}

              {error && <p className="text-red-600 text-sm">{error}</p>}
              {success && <p className="text-emerald-600 text-sm">{success}</p>}

              <button
                type="submit"
                disabled={saving || screenNameAvailability.checking || screenNameAvailability.available === false}
                className="w-full bg-emerald-600 hover:bg-emerald-700 disabled:opacity-60 text-white font-medium py-2 rounded-lg transition-colors"
              >
                {saving ? "Saving..." : "Save Changes"}
              </button>
            </form>

            <div className="mt-8 border-t border-slate-200 pt-6">
              <h3 className="text-slate-900 font-semibold mb-3">Subscription status</h3>
              {!billingStatus && <p className="text-slate-500 text-sm">Unable to load billing status.</p>}
              {billingStatus && (
                <div className="space-y-2 text-sm text-slate-700">
                  <p>
                    Access: <span className="font-semibold capitalize">{billingStatus.accessStatus.replace("_", " ")}</span>
                  </p>

                  {billingStatus.accessStatus === "trialing" && billingStatus.trial.endsAt && (
                    <p>
                      Trial ends: <span className="font-semibold">{new Date(billingStatus.trial.endsAt).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })}</span>
                    </p>
                  )}

                  {billingStatus.accessStatus === "subscribed" && billingStatus.subscription?.currentPeriodEnd && (
                    <p>
                      Renews on: <span className="font-semibold">{new Date(billingStatus.subscription.currentPeriodEnd).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })}</span>
                    </p>
                  )}

                  {billingStatus.accessStatus === "trial_expired" && billingStatus.trial.used && (
                    <div className="text-amber-700">
                      <p className="font-semibold">Trial consumed</p>
                      <p className="text-sm">Your 15-day free trial has been used. Subscribe annually to continue accessing all problems.</p>
                    </div>
                  )}

                  {billingStatus.accessStatus === "none" && !billingStatus.trial.used && (
                    <p className="text-slate-500">No active subscription. Start a trial or subscribe to access all problems.</p>
                  )}
                </div>
              )}
            </div>
          </section>

          <section className="lg:col-span-2 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-slate-900 font-semibold mb-4">Recent Activity</h2>

            {profile.activity.length === 0 ? (
              <p className="text-slate-500 text-sm">No submissions yet. Start solving problems to see activity.</p>
            ) : (
              <div className="space-y-3">
                {profile.activity.map((a) => (
                  <div
                    key={a.submissionId}
                    className="border border-slate-200 rounded-lg p-4 flex items-center justify-between gap-4"
                  >
                    <div>
                      <Link to={`/problems/${a.problemSlug}`} className="text-slate-900 font-medium hover:text-emerald-700">
                        {a.problemTitle}
                      </Link>
                      <p className="text-xs text-slate-500 mt-1">
                        {new Date(a.createdAt).toLocaleString()} • {a.runtimeMs ?? "-"} ms
                      </p>
                    </div>
                    <span className={`text-xs font-mono px-2 py-1 rounded ${statusClass(a.status)}`}>
                      {a.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <p className="text-xs uppercase tracking-wide text-slate-500 font-mono">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-slate-900">{value}</p>
    </div>
  );
}

function statusClass(status: string) {
  if (status === "accepted") return "bg-emerald-100 text-emerald-700";
  if (status === "runtime_error" || status === "wrong_answer") return "bg-red-100 text-red-700";
  if (status === "running" || status === "pending") return "bg-amber-100 text-amber-700";
  return "bg-slate-100 text-slate-700";
}
