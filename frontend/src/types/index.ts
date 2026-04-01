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
  id: number;
  username: string;
  email: string;
}
