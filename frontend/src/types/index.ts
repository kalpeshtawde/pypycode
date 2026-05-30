export interface TestCase {
  serialNumber: number;
  function: string;
  input: string;
  expectedOutput: string;
}

export interface Problem {
  id: number;
  slug: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  description: string;
  starterCode: string;
  examples: { input: string; output: string; explanation?: string }[];
  testCases?: TestCase[];
  tags: string[];
  createdAt: string;
}

export interface Submission {
  id: number;
  status: "pending" | "running" | "accepted" | "wrong_answer" | "time_limit" | "runtime_error";
  passedTests: number;
  totalTests: number;
  runtimeMs: number | null;
  memoryKb: number | null;
  errorOutput: string | null;
  createdAt: string;
}

export interface LeaderboardEntry {
  rank: number;
  username: string;
  solved: number;
}

export interface User {
  id: string;
  username: string;
  email: string;
  firstName?: string | null;
  lastName?: string | null;
  screenName?: string | null;
}

export interface ProfileStats {
  totalSubmissions: number;
  acceptedSubmissions: number;
  solvedProblems: number;
  acceptanceRate: number;
}

export interface ProfileActivity {
  submissionId: string;
  problemId: string;
  problemSlug: string;
  problemTitle: string;
  status: string;
  passedTests: number | null;
  totalTests: number | null;
  runtimeMs: number | null;
  memoryKb: number | null;
  createdAt: string;
}

export interface UserProfile {
  id: string;
  username: string;
  email: string;
  firstName: string | null;
  lastName: string | null;
  screenName: string | null;
  isAdmin: boolean;
  createdAt: string | null;
  stats: ProfileStats;
  activity: ProfileActivity[];
}

export interface FeatureFlag {
  id: string;
  name: string;
  enabled: boolean;
  createdAt: string | null;
  updatedAt: string | null;
}

export interface BillingTrialStatus {
  isActive: boolean;
  used: boolean;
  daysRemaining: number;
  startedAt: string | null;
  endsAt: string | null;
}

export interface BillingSubscriptionSnapshot {
  id: string;
  status: string;
  stripeProductId: string;
  stripePriceId?: string | null;
  stripeCustomerId?: string | null;
  stripeSubscriptionId?: string | null;
  amountCents: number;
  currency: string;
  interval: string;
  currentPeriodStart?: string | null;
  currentPeriodEnd?: string | null;
  cancelAtPeriodEnd: boolean;
  canceledAt?: string | null;
  createdAt?: string | null;
  updatedAt?: string | null;
}

export interface BillingAccessStatus {
  accessStatus: "none" | "trialing" | "trial_expired" | "subscribed";
  subscriptionStatus: string;
  trial: BillingTrialStatus;
  subscription: BillingSubscriptionSnapshot | null;
}

export interface Project {
  id: string;
  name: string;
  isDefault: boolean;
  createdAt: string | null;
  // AI-authored metadata (null for hand-created projects).
  goal?: string | null;
  strategy?: string | null;
  level?: string | null;
  explanation?: string | null;
  aiMetadata?: Record<string, unknown> | null;
}
