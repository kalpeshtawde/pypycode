export interface Problem {
  id: number;
  slug: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  description: string;
  starterCode: string;
  examples: { input: string; output: string; explanation?: string }[];
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
  createdAt: string | null;
  stats: ProfileStats;
  activity: ProfileActivity[];
}

export interface Project {
  id: string;
  name: string;
  isDefault: boolean;
  createdAt: string | null;
}
