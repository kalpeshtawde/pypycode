import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";
import { useSEO } from "../hooks/useSEO";
import type { AdminUser, AdminUsersResponse, AdminUsersSummary } from "../types";

type SortField = "created_at" | "username" | "email" | "solved" | "submissions" | "last_activity";

const PER_PAGE = 25;

const EMPTY_SUMMARY: AdminUsersSummary = {
  totalUsers: 0,
  newThisWeek: 0,
  activeTrials: 0,
  activeSubscriptions: 0,
};

function formatDate(value: string | null | undefined) {
  if (!value) return "—";
  return new Date(value).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

function formatMoney(cents: number, currency: string) {
  return new Intl.NumberFormat(undefined, {
    style: "currency",
    currency: (currency || "usd").toUpperCase(),
    maximumFractionDigits: cents % 100 === 0 ? 0 : 2,
  }).format(cents / 100);
}

type Tone = "emerald" | "amber" | "red" | "blue" | "indigo" | "slate";

const TONE_CLASS: Record<Tone, string> = {
  emerald: "bg-emerald-50 dark:bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-500/30",
  amber: "bg-amber-50 dark:bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-500/30",
  red: "bg-red-50 dark:bg-red-500/10 text-red-700 dark:text-red-400 border-red-200 dark:border-red-500/30",
  blue: "bg-blue-50 dark:bg-blue-500/10 text-blue-700 dark:text-blue-400 border-blue-200 dark:border-blue-500/30",
  indigo: "bg-indigo-50 dark:bg-indigo-500/10 text-indigo-700 dark:text-indigo-400 border-indigo-200 dark:border-indigo-500/30",
  slate: "bg-slate-100 dark:bg-slate-700/50 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-600",
};

function planBadge(user: AdminUser): { label: string; tone: Tone } {
  const sub = user.subscription;

  if (sub) {
    const interval = sub.interval === "year" ? "Annual" : sub.interval === "month" ? "Monthly" : sub.interval;
    const amount = formatMoney(sub.amountCents, sub.currency);
    const periodEnd = formatDate(sub.currentPeriodEnd);
    const base = `${interval} · ${amount}`;

    if (sub.cancelAtPeriodEnd) {
      return { label: `${base} · cancels ${periodEnd}`, tone: "amber" };
    }
    if (sub.status === "active" || sub.status === "trialing") {
      return { label: `${base} · renews ${periodEnd}`, tone: "emerald" };
    }
    return { label: `${base} · ${sub.status.replace(/_/g, " ")}`, tone: "red" };
  }

  if (user.isAdmin) return { label: "Admin access", tone: "indigo" };
  if (user.trial.isActive) return { label: `Trial · ${user.trial.daysRemaining}d left`, tone: "blue" };
  if (user.trial.used) return { label: "Trial consumed", tone: "slate" };
  return { label: "No plan", tone: "slate" };
}

function displayName(user: AdminUser) {
  const full = [user.firstName, user.lastName].filter(Boolean).join(" ");
  return full || user.username;
}

export default function AdminUsersPage() {
  const { token } = useAuthStore();
  const [data, setData] = useState<AdminUsersResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [page, setPage] = useState(1);
  const [sort, setSort] = useState<SortField>("created_at");
  const [order, setOrder] = useState<"asc" | "desc">("desc");
  const [selected, setSelected] = useState<AdminUser | null>(null);

  useSEO(
    useMemo(
      () => ({
        title: "Users — Admin | PyPyCode",
        description: "Admin user directory.",
        robots: "noindex, nofollow",
      }),
      []
    )
  );

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query.trim());
      setPage(1);
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  const load = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams({
        page: String(page),
        per_page: String(PER_PAGE),
        sort,
        order,
      });
      if (debouncedQuery) params.set("q", debouncedQuery);
      const res = await api.get<AdminUsersResponse>(`/admin/users?${params.toString()}`, token);
      setData(res);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load users");
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [token, page, sort, order, debouncedQuery]);

  useEffect(() => {
    load();
  }, [load]);

  const summary = data?.summary ?? EMPTY_SUMMARY;
  const pagination = data?.pagination;
  const users = data?.users ?? [];

  const toggleSort = (field: SortField) => {
    if (sort === field) {
      setOrder((current) => (current === "asc" ? "desc" : "asc"));
    } else {
      setSort(field);
      setOrder(field === "created_at" || field === "last_activity" ? "desc" : "asc");
    }
    setPage(1);
  };

  const sortIndicator = (field: SortField) => (sort === field ? (order === "asc" ? "↑" : "↓") : "");

  return (
    <div className="min-h-[calc(100vh-64px)] bg-gradient-to-b from-slate-50 via-white to-slate-50 dark:from-slate-900 dark:via-slate-900 dark:to-slate-900 px-4 sm:px-6 py-8 sm:py-12">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-wrap items-end justify-between gap-3 mb-6">
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-emerald-600 dark:text-emerald-400 mb-1">
              Admin
            </p>
            <h1 className="font-display text-3xl sm:text-4xl font-semibold text-slate-900 dark:text-slate-100">
              Users
            </h1>
            <p className="text-slate-600 dark:text-slate-400 mt-1 text-sm">
              Everyone who has signed up, their usage and their subscription.
            </p>
          </div>
          <button
            onClick={load}
            disabled={loading}
            className="inline-flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-600 px-3.5 py-2 text-sm font-medium text-slate-700 dark:text-slate-300
                       hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors disabled:opacity-50"
          >
            <svg className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fillRule="evenodd" d="M15.312 11.424a5.5 5.5 0 0 1-9.201 2.466l-.312-.311h4.274a.75.75 0 0 0 0-1.5H2.99a.75.75 0 0 0-.75.75v4.242a.75.75 0 0 0 1.5 0v-2.43l.31.31a7 7 0 0 0 11.712-3.138.75.75 0 0 0-1.449-.39ZM4.974 5.954a5.5 5.5 0 0 1 9.2-2.466l.31.31h-4.268a.75.75 0 0 0 0 1.5h7.286a.75.75 0 0 0 .75-.75V.712a.75.75 0 0 0-1.5 0v2.43l-.31-.31a7 7 0 0 0-11.712 3.138.75.75 0 0 0 1.45.391Z" clipRule="evenodd" />
            </svg>
            Refresh
          </button>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
          <SummaryCard label="Total users" value={summary.totalUsers} />
          <SummaryCard label="New this week" value={summary.newThisWeek} />
          <SummaryCard label="Active trials" value={summary.activeTrials} />
          <SummaryCard label="Paid subscriptions" value={summary.activeSubscriptions} />
        </div>

        <div className="flex items-center gap-2 mb-3">
          <div className="relative w-full sm:max-w-sm">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fillRule="evenodd" d="M9 3.5a5.5 5.5 0 1 0 3.43 9.79l3.14 3.14a.75.75 0 1 0 1.06-1.06l-3.14-3.14A5.5 5.5 0 0 0 9 3.5ZM5 9a4 4 0 1 1 8 0 4 4 0 0 1-8 0Z" clipRule="evenodd" />
            </svg>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search name, username, email…"
              className="w-full rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 pl-9 pr-3 py-2 text-sm
                         text-slate-800 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500
                         focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
          </div>
        </div>

        {error && (
          <div className="mb-4 rounded-lg border border-red-200 dark:border-red-500/30 bg-red-50 dark:bg-red-500/10 px-4 py-3 text-sm text-red-700 dark:text-red-400">
            {error}
          </div>
        )}

        <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-sm overflow-x-auto">
          <div
            className="grid items-center gap-4 px-4 sm:px-6 py-3 border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/60
                       text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400"
            style={{ gridTemplateColumns: "minmax(200px,1.1fr) minmax(200px,1.3fr) 230px 90px 120px 110px", minWidth: "900px" }}
          >
            <SortHeader label="User" active={sort === "username"} indicator={sortIndicator("username")} onClick={() => toggleSort("username")} />
            <SortHeader label="Email" active={sort === "email"} indicator={sortIndicator("email")} onClick={() => toggleSort("email")} />
            <span>Plan</span>
            <span>Role</span>
            <SortHeader label="Activity" active={sort === "last_activity"} indicator={sortIndicator("last_activity")} onClick={() => toggleSort("last_activity")} />
            <SortHeader label="Joined" active={sort === "created_at"} indicator={sortIndicator("created_at")} onClick={() => toggleSort("created_at")} />
          </div>

          {loading && !data ? (
            <div className="py-16 text-center text-sm font-mono text-slate-500 dark:text-slate-400">Loading users…</div>
          ) : users.length === 0 ? (
            <div className="py-16 text-center text-sm text-slate-500 dark:text-slate-400">
              {debouncedQuery ? "No users match that search." : "No users yet."}
            </div>
          ) : (
            users.map((user) => {
              const badge = planBadge(user);
              return (
                <button
                  key={user.id}
                  onClick={() => setSelected(user)}
                  className="w-full text-left grid items-center gap-4 px-4 sm:px-6 py-3 border-b border-slate-100 dark:border-slate-700/70 last:border-0
                             hover:bg-slate-50 dark:hover:bg-slate-700/40 transition-colors"
                  style={{ gridTemplateColumns: "minmax(200px,1.1fr) minmax(200px,1.3fr) 230px 90px 120px 110px", minWidth: "900px" }}
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <span className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-emerald-500 to-emerald-600 text-xs font-bold text-white">
                      {(user.screenName || user.username || "?").replace(/^@/, "").charAt(0).toUpperCase()}
                    </span>
                    <span className="min-w-0">
                      <span className="block truncate text-sm font-medium text-slate-900 dark:text-slate-100">
                        {displayName(user)}
                      </span>
                      <span className="block truncate text-xs text-slate-500 dark:text-slate-400">
                        {user.screenName || `@${user.username}`}
                        {user.provider === "google" && <span className="ml-1.5 text-[10px] uppercase tracking-wide text-slate-400 dark:text-slate-500">google</span>}
                      </span>
                    </span>
                  </div>

                  <span className="truncate text-sm text-slate-700 dark:text-slate-300">{user.email}</span>

                  <span>
                    <span className={`inline-flex max-w-full items-center truncate rounded-full border px-2 py-0.5 text-[11px] font-medium ${TONE_CLASS[badge.tone]}`}>
                      {badge.label}
                    </span>
                  </span>

                  <span className={`text-xs font-medium ${user.isAdmin ? "text-indigo-600 dark:text-indigo-400" : "text-slate-500 dark:text-slate-400"}`}>
                    {user.isAdmin ? "Admin" : "User"}
                  </span>

                  <span className="text-xs text-slate-600 dark:text-slate-400">
                    <span className="font-mono">{user.solved}</span> solved · <span className="font-mono">{user.submissions}</span> subs
                    <span className="block text-[11px] text-slate-400 dark:text-slate-500">{formatDate(user.lastActivityAt)}</span>
                  </span>

                  <span className="text-xs text-slate-600 dark:text-slate-400">{formatDate(user.createdAt)}</span>
                </button>
              );
            })
          )}
        </div>

        {pagination && pagination.totalPages > 1 && (
          <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-sm">
            <p className="text-slate-600 dark:text-slate-400">
              Page {pagination.page} of {pagination.totalPages} · {pagination.total} users
            </p>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(p - 1, 1))}
                disabled={pagination.page <= 1 || loading}
                className="rounded-lg border border-slate-300 dark:border-slate-600 px-3 py-1.5 text-sm text-slate-700 dark:text-slate-300
                           hover:bg-slate-100 dark:hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              >
                Previous
              </button>
              <button
                onClick={() => setPage((p) => Math.min(p + 1, pagination.totalPages))}
                disabled={pagination.page >= pagination.totalPages || loading}
                className="rounded-lg border border-slate-300 dark:border-slate-600 px-3 py-1.5 text-sm text-slate-700 dark:text-slate-300
                           hover:bg-slate-100 dark:hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>

      {selected && <UserDrawer user={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}

function SummaryCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-4 shadow-sm">
      <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">{label}</p>
      <p className="mt-1.5 text-2xl font-semibold text-slate-900 dark:text-slate-100">{value}</p>
    </div>
  );
}

function SortHeader({
  label,
  active,
  indicator,
  onClick,
}: {
  label: string;
  active: boolean;
  indicator: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-1 text-left uppercase tracking-wider transition-colors ${
        active ? "text-slate-900 dark:text-slate-200" : "hover:text-slate-700 dark:hover:text-slate-200"
      }`}
    >
      {label}
      <span className="text-[10px]">{indicator}</span>
    </button>
  );
}

function UserDrawer({ user, onClose }: { user: AdminUser; onClose: () => void }) {
  const badge = planBadge(user);
  const sub = user.subscription;

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <div className="absolute inset-0 bg-slate-900/40 dark:bg-black/50" onClick={onClose} />
      <aside className="relative h-full w-full sm:w-[440px] overflow-y-auto bg-white dark:bg-slate-800 border-l border-slate-200 dark:border-slate-700 shadow-2xl">
        <div className="sticky top-0 flex items-center justify-between gap-3 border-b border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-5 py-4">
          <div className="min-w-0">
            <p className="truncate font-semibold text-slate-900 dark:text-slate-100">{displayName(user)}</p>
            <p className="truncate text-xs text-slate-500 dark:text-slate-400">{user.email}</p>
          </div>
          <button
            onClick={onClose}
            aria-label="Close"
            className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full border border-slate-200 dark:border-slate-600
                       text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors"
          >
            <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <path d="M6 6l12 12M18 6L6 18" />
            </svg>
          </button>
        </div>

        <div className="p-5 space-y-5">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">Plan</p>
            <span className={`inline-flex rounded-full border px-2.5 py-1 text-xs font-medium ${TONE_CLASS[badge.tone]}`}>
              {badge.label}
            </span>
          </div>

          <dl className="space-y-2 text-sm">
            <Row label="Access" value={user.accessStatus.replace(/_/g, " ")} />
            <Row label="Subscription status" value={sub?.status ?? user.subscriptionStatus} />
            <Row label="Provider" value={user.provider === "google" ? "Google" : "Email / password"} />
            <Row label="Role" value={user.isAdmin ? "Admin" : "User"} />
            <Row label="Solved" value={String(user.solved)} />
            <Row label="Submissions" value={String(user.submissions)} />
            <Row label="Last activity" value={formatDate(user.lastActivityAt)} />
            <Row label="Signed up" value={formatDate(user.createdAt)} />
            <Row label="Trial used" value={user.trial.used ? "Yes" : "No"} />
            {user.trial.endsAt && <Row label="Trial ends" value={formatDate(user.trial.endsAt)} />}
          </dl>

          {sub && (
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">Billing</p>
              <dl className="space-y-2 text-sm">
                <Row label="Amount" value={`${formatMoney(sub.amountCents, sub.currency)} / ${sub.interval}`} />
                <Row label="Renews" value={formatDate(sub.currentPeriodEnd)} />
                <Row label="Cancels at period end" value={sub.cancelAtPeriodEnd ? "Yes" : "No"} />
                {sub.canceledAt && <Row label="Canceled" value={formatDate(sub.canceledAt)} />}
              </dl>
              <div className="mt-3 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700 p-3 space-y-1.5">
                <StripeRow label="customer" value={sub.stripeCustomerId} />
                <StripeRow label="subscription" value={sub.stripeSubscriptionId} />
                <StripeRow label="price" value={sub.stripePriceId} />
                <StripeRow label="product" value={sub.stripeProductId} />
              </div>
            </div>
          )}
        </div>
      </aside>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-start justify-between gap-4">
      <dt className="text-slate-500 dark:text-slate-400">{label}</dt>
      <dd className="text-right font-medium text-slate-900 dark:text-slate-100 capitalize">{value}</dd>
    </div>
  );
}

function StripeRow({ label, value }: { label: string; value?: string | null }) {
  return (
    <div className="flex items-start justify-between gap-3 text-[11px] font-mono">
      <span className="text-slate-500 dark:text-slate-400">{label}</span>
      <span className="text-right break-all text-slate-700 dark:text-slate-300">{value || "—"}</span>
    </div>
  );
}
