import { FormEvent, useMemo, useState } from "react";
import { api } from "../utils/api";

const SAMPLE_EXAMPLES = `[
  {
    "input": "nums = [2,7,11,15], target = 9",
    "output": "[0,1]",
    "explanation": "nums[0] + nums[1] = 9"
  }
]`;

const SAMPLE_TEST_CASES = `[
  {
    "function": "twoSum",
    "input": "[2, 7, 11, 15], 9",
    "expectedOutput": "[0, 1]"
  },
  {
    "function": "twoSum",
    "input": "[3, 2, 4], 6",
    "expectedOutput": "[1, 2]"
  }
]`;

const SAMPLE_TAGS = `[
  "array",
  "hash-table"
]`;

type IngestResponse = {
  id: string;
  slug: string;
  title: string;
  createdAt: string;
};

export default function ProblemIngestPage() {
  const [ingestKey, setIngestKey] = useState("");
  const [slug, setSlug] = useState("");
  const [title, setTitle] = useState("");
  const [difficulty, setDifficulty] = useState<"easy" | "medium" | "hard">("easy");
  const [description, setDescription] = useState("");
  const [starterCode, setStarterCode] = useState("def solution():\n    pass");
  const [examplesText, setExamplesText] = useState(SAMPLE_EXAMPLES);
  const [testCasesText, setTestCasesText] = useState(SAMPLE_TEST_CASES);
  const [tagsText, setTagsText] = useState(SAMPLE_TAGS);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<IngestResponse | null>(null);

  const prettyPayloadPreview = useMemo(() => {
    return {
      slug,
      title,
      difficulty,
      description,
      starterCode,
      examples: examplesText,
      testCases: testCasesText,
      tags: tagsText,
    };
  }, [slug, title, difficulty, description, starterCode, examplesText, testCasesText, tagsText]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    let examples: unknown;
    let testCases: unknown;
    let tags: unknown;

    try {
      examples = JSON.parse(examplesText);
      testCases = JSON.parse(testCasesText);
      tags = JSON.parse(tagsText);
    } catch {
      setError("Examples, test cases, and tags must be valid JSON.");
      return;
    }

    setLoading(true);
    try {
      const res = await api.post<IngestResponse>("/problems/public-ingest", {
        ingestKey,
        slug,
        title,
        difficulty,
        description,
        starterCode,
        examples,
        testCases,
        tags,
      });
      setSuccess(res);
      setSlug("");
      setTitle("");
      setDescription("");
      setStarterCode("def solution():\n    pass");
      setExamplesText(SAMPLE_EXAMPLES);
      setTestCasesText(SAMPLE_TEST_CASES);
      setTagsText(SAMPLE_TAGS);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Problem ingest failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] bg-gradient-to-b from-slate-50 via-white to-slate-50 px-4 py-10 sm:px-6">
      <div className="mx-auto max-w-5xl">
        <div className="mb-8 rounded-2xl border border-slate-200 bg-white/80 p-6 shadow-sm backdrop-blur">
          <h1 className="font-display text-3xl font-semibold text-slate-900">Problem Ingest Portal</h1>
          <p className="mt-2 text-sm text-slate-600">
            Public URL, no login required. Submission is accepted only when `ingestKey` matches
            `PROBLEM_INGEST_KEY` on the server.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="grid gap-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
          style={{ colorScheme: "light" }}
        >
          <label className="grid gap-2">
            <span className="text-sm font-medium text-slate-700">Ingest key</span>
            <input
              type="password"
              value={ingestKey}
              onChange={(e) => setIngestKey(e.target.value)}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 font-mono text-sm text-slate-800 outline-none ring-emerald-500/30 focus:ring"
              required
            />
          </label>

          <div className="grid gap-4 sm:grid-cols-3">
            <label className="grid gap-2 sm:col-span-1">
              <span className="text-sm font-medium text-slate-700">Slug</span>
              <input
                value={slug}
                onChange={(e) => setSlug(e.target.value)}
                placeholder="two-sum"
                className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 outline-none ring-emerald-500/30 focus:ring"
                required
              />
            </label>

            <label className="grid gap-2 sm:col-span-1">
              <span className="text-sm font-medium text-slate-700">Difficulty</span>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value as "easy" | "medium" | "hard")}
                className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 outline-none ring-emerald-500/30 focus:ring"
              >
                <option value="easy">easy</option>
                <option value="medium">medium</option>
                <option value="hard">hard</option>
              </select>
            </label>

            <label className="grid gap-2 sm:col-span-1">
              <span className="text-sm font-medium text-slate-700">Title</span>
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Two Sum"
                className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 outline-none ring-emerald-500/30 focus:ring"
                required
              />
            </label>
          </div>

          <label className="grid gap-2">
            <span className="text-sm font-medium text-slate-700">Description (Markdown)</span>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={8}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 font-mono text-sm text-slate-800 outline-none ring-emerald-500/30 focus:ring"
              required
            />
          </label>

          <label className="grid gap-2">
            <span className="text-sm font-medium text-slate-700">Starter code</span>
            <textarea
              value={starterCode}
              onChange={(e) => setStarterCode(e.target.value)}
              rows={6}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 font-mono text-sm text-slate-800 outline-none ring-emerald-500/30 focus:ring"
              required
            />
          </label>

          <label className="grid gap-2">
            <span className="text-sm font-medium text-slate-700">Examples JSON</span>
            <textarea
              value={examplesText}
              onChange={(e) => setExamplesText(e.target.value)}
              rows={8}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 font-mono text-xs text-slate-800 outline-none ring-emerald-500/30 focus:ring"
              required
            />
          </label>

          <label className="grid gap-2">
            <span className="text-sm font-medium text-slate-700">Test cases JSON</span>
            <textarea
              value={testCasesText}
              onChange={(e) => setTestCasesText(e.target.value)}
              rows={10}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 font-mono text-xs text-slate-800 outline-none ring-emerald-500/30 focus:ring"
              required
            />
          </label>

          <label className="grid gap-2">
            <span className="text-sm font-medium text-slate-700">Tags JSON (array of strings)</span>
            <textarea
              value={tagsText}
              onChange={(e) => setTagsText(e.target.value)}
              rows={4}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 font-mono text-xs text-slate-800 outline-none ring-emerald-500/30 focus:ring"
              required
            />
          </label>

          {error && (
            <div className="rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</div>
          )}

          {success && (
            <div className="rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-sm text-emerald-700">
              Created problem `{success.title}` (`{success.slug}`).
            </div>
          )}

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={loading}
              className={`btn-primary px-6 py-2 text-sm ${loading ? "cursor-not-allowed opacity-60" : ""}`}
            >
              {loading ? "Submitting..." : "Create Problem"}
            </button>
            <span className="text-xs text-slate-500">Endpoint: `POST /problems/public-ingest`</span>
          </div>
        </form>

        <pre className="mt-6 overflow-auto rounded-xl border border-slate-200 bg-slate-900 p-4 text-xs text-slate-100">
{JSON.stringify(prettyPayloadPreview, null, 2)}
        </pre>
      </div>
    </div>
  );
}
