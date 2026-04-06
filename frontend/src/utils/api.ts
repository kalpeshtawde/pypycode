const BASE = import.meta.env.VITE_API_URL ?? "/api";

async function req<T>(
  path: string,
  options: RequestInit = {},
  token?: string | null
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error ?? "Request failed");
  }
  return res.json();
}

export const api = {
  get: <T>(path: string, token?: string | null) => req<T>(path, { method: "GET" }, token),
  post: <T>(path: string, body: unknown, token?: string | null) =>
    req<T>(path, { method: "POST", body: JSON.stringify(body) }, token),
  delete: <T>(path: string, token?: string | null) => req<T>(path, { method: "DELETE" }, token),
};
