import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";
import type { Problem, Project, BillingAccessStatus } from "../types";

const QUICK_FILTERS = ["all", "easy", "medium", "hard", "solved", "favorite"] as const;

function ProblemCell({
  problem,
  solvedProblems,
  selectedProjectId,
  isLoggedIn,
  canOpenProblem,
  onMissingProject,
  hasBillingAccess,
  billingEnabled,
}: {
  problem: Problem;
  solvedProblems: number[];
  selectedProjectId: string;
  isLoggedIn: boolean;
  canOpenProblem: boolean;
  onMissingProject: () => void;
  hasBillingAccess?: boolean;
  billingEnabled?: boolean;
}) {
  const isSolved = solvedProblems.includes(problem.id);

  const difficultyColors = {
    easy: '#10B981',
    medium: '#F59E0B',
    hard: '#EF4444'
  };

  const cellColor = difficultyColors[problem.difficulty];
  const textColor = isSolved ? 'white' : 'white';
  const opacity = isSolved ? 1 : 0.3;
  const targetPath = selectedProjectId
    ? `/problems/${problem.slug}?projectId=${encodeURIComponent(selectedProjectId)}`
    : `/problems/${problem.slug}`;
  const pricingRedirectPath = `/pricing?required=1&redirect=${encodeURIComponent(targetPath)}`;
  const authRedirectPath = `/auth?redirect=${encodeURIComponent(pricingRedirectPath)}`;

  // If billing is disabled, skip pricing redirect
  const shouldCheckBilling = billingEnabled ?? false;
  const problemLink = !isLoggedIn
    ? authRedirectPath
    : shouldCheckBilling && !hasBillingAccess
    ? pricingRedirectPath
    : targetPath;

  return (
    <Link
      to={problemLink}
      title={`${problem.title} (${problem.difficulty})`}
      style={{
        width: '24px',
        height: '24px',
        borderRadius: '4px',
        background: cellColor,
        border: '1px solid #D1D5DB',
        cursor: 'pointer',
        transition: 'all 150ms ease',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        fontSize: '12px',
        fontWeight: 700,
        color: textColor,
        opacity: opacity
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'scale(1.15)';
        e.currentTarget.style.boxShadow = '0 4px 12px rgba(15,23,42,0.2)';
        if (!isSolved) {
          e.currentTarget.style.opacity = '0.6';
        }
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'scale(1)';
        e.currentTarget.style.boxShadow = 'none';
        e.currentTarget.style.opacity = opacity.toString();
      }}
      onClick={(e) => {
        if (isLoggedIn && !canOpenProblem) {
          e.preventDefault();
          onMissingProject();
        }
      }}
    >
      {isSolved && '✓'}
    </Link>
  );
}

export default function ProblemsPage() {
  const { token } = useAuthStore();
  const isLoggedIn = Boolean(token);
  const [accessStatus, setAccessStatus] = useState<BillingAccessStatus | null>(null);
  const hasBillingAccess = accessStatus?.accessStatus === "subscribed" || accessStatus?.accessStatus === "trialing";
  const [billingEnabled, setBillingEnabled] = useState(false);
  const [problems, setProblems] = useState<Problem[]>([]);
  const [allProblemsForStats, setAllProblemsForStats] = useState<Problem[]>([]);
  const [solvedProblems, setSolvedProblems] = useState<number[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<string>(
    () => localStorage.getItem("selectedProjectId") ?? ""
  );
  const [problemSequence, setProblemSequence] = useState<Map<number, number>>(new Map());
  const [filter, setFilter] = useState<typeof QUICK_FILTERS[number]>("all");
  const [sortBy, setSortBy] = useState<"id" | "title" | "difficulty" | "created_at">("id");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");
  const [currentPage, setCurrentPage] = useState(1);
  const [pagination, setPagination] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [switchingDefault, setSwitchingDefault] = useState(false);
  const [chatMode, setChatMode] = useState<'create' | 'update' | null>(null);
  const [chatMessages, setChatMessages] = useState<Array<{ role: 'vega' | 'user'; content: string }>>([]);
  const [chatStep, setChatStep] = useState<'intent' | 'prompt' | 'total' | 'submitting' | 'error'>('intent');
  const [chatInput, setChatInput] = useState('');
  const [chatPrompt, setChatPrompt] = useState('');
  const [chatBusy, setChatBusy] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const chatInputRef = useRef<HTMLTextAreaElement>(null);
  const [dismissedExplanationProjectId, setDismissedExplanationProjectId] = useState<string | null>(null);
  const [showDeleteProjectDialog, setShowDeleteProjectDialog] = useState(false);
  const [deletingProject, setDeletingProject] = useState(false);
  const [deleteProjectError, setDeleteProjectError] = useState<string | null>(null);
  const [favoriteProblemIds, setFavoriteProblemIds] = useState<Set<number>>(new Set());
  const [searchQuery, setSearchQuery] = useState("");
  const fetchRequestIdRef = useRef(0);

  const sortProjects = (items: Project[]) => {
    return [...items].sort((a, b) => {
      if (a.isDefault === b.isDefault) {
        return a.name.localeCompare(b.name);
      }
      return a.isDefault ? -1 : 1;
    });
  };

  const fetchProblems = (page: number = 1, sort: string = sortBy, order: string = sortOrder, difficulty: string = filter) => {
    const requestId = ++fetchRequestIdRef.current;
    const isLatestRequest = () => requestId === fetchRequestIdRef.current;
    setLoading(true);
    const trimmedSearch = searchQuery.trim();

    if (difficulty === "solved") {
      if (!token) {
        setProblems([]);
        setPagination({
          page: 1,
          pages: 1,
          total: 0,
          per_page: 15,
          has_prev: false,
          has_next: false,
          prev_num: null,
          next_num: null,
        });
        setLoading(false);
        return;
      }

      const perPageApi = 50;
      const fetchAllProblems = async () => {
        const collected: Problem[] = [];
        let nextPage = 1;
        let pages = 1;

        while (nextPage <= pages) {
          const params = new URLSearchParams({
            page: String(nextPage),
            per_page: String(perPageApi),
            sort,
            order,
          });
          if (selectedProjectId) {
            params.set("projectId", selectedProjectId);
          }
          if (trimmedSearch) {
            params.set("search", trimmedSearch);
          }

          const data = await api.get<{ problems: Problem[]; pagination: any }>(`/problems/?${params}`, token);
          collected.push(...data.problems);
          pages = data.pagination?.pages || 1;
          nextPage += 1;
        }

        return collected;
      };

      fetchAllProblems()
        .then((allProblems) => {
          if (!isLatestRequest()) return;
          const uniqueProblems = Array.from(new Map(allProblems.map((p) => [p.id, p])).values());
          const solvedSet = new Set(solvedProblems);
          const solvedOnly = uniqueProblems.filter((p) => solvedSet.has(p.id));

          const perPage = 15;
          const total = solvedOnly.length;
          const pages = Math.max(1, Math.ceil(total / perPage));
          const safePage = Math.min(Math.max(page, 1), pages);
          const start = (safePage - 1) * perPage;
          const pageItems = solvedOnly.slice(start, start + perPage);

          setProblems(pageItems);
          setPagination({
            page: safePage,
            pages,
            total,
            per_page: perPage,
            has_prev: safePage > 1,
            has_next: safePage < pages,
            prev_num: safePage > 1 ? safePage - 1 : null,
            next_num: safePage < pages ? safePage + 1 : null,
          });

          const sequence = new Map<number, number>();
          pageItems.forEach((problem, index) => {
            sequence.set(problem.id, (safePage - 1) * perPage + index + 1);
          });
          setProblemSequence(sequence);
        })
        .catch(() => {
          if (!isLatestRequest()) return;
          setProblems([]);
          setPagination({
            page: 1,
            pages: 1,
            total: 0,
            per_page: 15,
            has_prev: false,
            has_next: false,
            prev_num: null,
            next_num: null,
          });
        })
        .finally(() => {
          if (isLatestRequest()) {
            setLoading(false);
          }
        });
      return;
    }

    if (difficulty === "favorite" && !token) {
      setProblems([]);
      setPagination({
        page: 1,
        pages: 1,
        total: 0,
        per_page: 15,
        has_prev: false,
        has_next: false,
        prev_num: null,
        next_num: null,
      });
      setLoading(false);
      return;
    }

    if (difficulty === "favorite" && token) {
      api.get<{ favorites: Array<{ createdAt: string; problem: Problem }> }>("/favorites/", token)
        .then((res) => {
          if (!isLatestRequest()) return;
          const enriched = res.favorites
            .map((f) => ({
              problem: {
                ...f.problem,
                id: Number(f.problem.id),
              },
              favoriteCreatedAt: f.createdAt,
            }))
            .filter(({ problem }) => {
              if (!trimmedSearch) return true;
              const query = trimmedSearch.toLowerCase();
              return (
                problem.title.toLowerCase().includes(query) ||
                problem.slug.toLowerCase().includes(query) ||
                problem.tags.some((t) => t.toLowerCase().includes(query))
              );
            });

          const dedupedEnriched = Array.from(
            new Map(enriched.map((item) => [item.problem.id, item])).values()
          );

          const difficultyRank = (value: string) => {
            if (value === "easy") return 1;
            if (value === "medium") return 2;
            if (value === "hard") return 3;
            return 4;
          };

          dedupedEnriched.sort((a, b) => {
            if (sort === "title") {
              const delta = a.problem.title.localeCompare(b.problem.title);
              return order === "desc" ? -delta : delta;
            }

            if (sort === "difficulty") {
              const delta = difficultyRank(a.problem.difficulty) - difficultyRank(b.problem.difficulty);
              return order === "desc" ? -delta : delta;
            }

            if (sort === "created_at") {
              const aTime = new Date(a.favoriteCreatedAt).getTime();
              const bTime = new Date(b.favoriteCreatedAt).getTime();
              return order === "desc" ? bTime - aTime : aTime - bTime;
            }

            const delta = a.problem.id - b.problem.id;
            return order === "desc" ? -delta : delta;
          });

          const perPage = 15;
          const total = dedupedEnriched.length;
          const pages = Math.max(1, Math.ceil(total / perPage));
          const safePage = Math.min(Math.max(page, 1), pages);
          const start = (safePage - 1) * perPage;
          const pageItems = dedupedEnriched.slice(start, start + perPage).map((item) => item.problem);

          setProblems(pageItems);
          setFavoriteProblemIds(new Set(dedupedEnriched.map((item) => item.problem.id)));
          setPagination({
            page: safePage,
            pages,
            total,
            per_page: perPage,
            has_prev: safePage > 1,
            has_next: safePage < pages,
            prev_num: safePage > 1 ? safePage - 1 : null,
            next_num: safePage < pages ? safePage + 1 : null,
          });

          const sequence = new Map<number, number>();
          pageItems.forEach((problem, index) => {
            sequence.set(problem.id, (safePage - 1) * perPage + index + 1);
          });
          setProblemSequence(sequence);
        })
        .catch(() => {
          if (!isLatestRequest()) return;
          setProblems([]);
          setPagination({
            page: 1,
            pages: 1,
            total: 0,
            per_page: 15,
            has_prev: false,
            has_next: false,
            prev_num: null,
            next_num: null,
          });
        })
        .finally(() => {
          if (isLatestRequest()) {
            setLoading(false);
          }
        });
      return;
    }

    const difficultyParam = ["easy", "medium", "hard"].includes(difficulty) ? difficulty : "";
    const params = new URLSearchParams({
      page: page.toString(),
      per_page: "15",
      sort: sort,
      order: order,
    });
    if (selectedProjectId) {
      params.set("projectId", selectedProjectId);
    }
    if (difficultyParam) {
      params.set("difficulty", difficultyParam);
    }
    if (trimmedSearch) {
      params.set("search", trimmedSearch);
    }
    
    api.get<{ problems: Problem[]; pagination: any }>(`/problems/?${params}`, token)
      .then((data) => {
        if (!isLatestRequest()) return;
        setProblems(data.problems);
        setPagination(data.pagination);
        
        // Generate sequence numbers based on current page
        const sequence = new Map<number, number>();
        data.problems.forEach((problem, index) => {
          sequence.set(problem.id, (page - 1) * 15 + index + 1);
        });
        setProblemSequence(sequence);
      })
      .catch(() => {
        if (!isLatestRequest()) return;
        setProblems([]);
        setPagination(null);
      })
      .finally(() => {
        if (isLatestRequest()) {
          setLoading(false);
        }
      });
  };

  useEffect(() => {
    fetchProblems(1, sortBy, sortOrder, filter);
  }, []);

  useEffect(() => {
    const fetchAllProblemsForStats = async () => {
      const collected: Problem[] = [];
      let page = 1;
      let pages = 1;

      while (page <= pages) {
        const params = new URLSearchParams({
          page: String(page),
          per_page: "50",
          sort: "id",
          order: "asc",
        });
        if (selectedProjectId) {
          params.set("projectId", selectedProjectId);
        }

        const data = await api.get<{ problems: Problem[]; pagination: any }>(`/problems/?${params}`, token);
        collected.push(...data.problems);
        pages = data.pagination?.pages || 1;
        page += 1;
      }

      setAllProblemsForStats(collected);
    };

    fetchAllProblemsForStats().catch(() => {
      setAllProblemsForStats([]);
    });
  }, [selectedProjectId]);

  useEffect(() => {
    setCurrentPage(1);
    fetchProblems(1, sortBy, sortOrder, filter);
  }, [sortBy, sortOrder, filter, searchQuery, selectedProjectId]);

  useEffect(() => {
    if (!token) {
      setProjects([]);
      setSelectedProjectId("");
      return;
    }

    api.get<Project[]>("/projects/", token)
      .then((data) => {
        setProjects(sortProjects(data));
        const defaultProject = data.find((project) => project.isDefault) ?? data[0];
        setSelectedProjectId((current) => {
          if (current && data.some((project) => project.id === current)) {
            return current;
          }
          return defaultProject?.id ?? "";
        });
      })
      .catch(() => {
        setProjects([]);
      });
  }, [token]);

  useEffect(() => {
    if (selectedProjectId) {
      localStorage.setItem("selectedProjectId", selectedProjectId);
      return;
    }
    localStorage.removeItem("selectedProjectId");
  }, [selectedProjectId]);

  useEffect(() => {
    if (!token) return;
    const params = new URLSearchParams();
    if (selectedProjectId) {
      params.set("projectId", selectedProjectId);
    }
    const suffix = params.toString() ? `?${params.toString()}` : "";
    // Fetch all submissions to get latest status for each problem
    api.get<Array<{ id: number; problemId: number; status: string; createdAt: string }>>(`/submissions/all${suffix}`, token)
      .then((data) => {
        // Get the latest submission for each problem
        const latestSubmissions = new Map<number, { status: string; createdAt: string }>();
        data.forEach(sub => {
          const existing = latestSubmissions.get(sub.problemId);
          if (!existing || new Date(sub.createdAt) > new Date(existing.createdAt)) {
            latestSubmissions.set(sub.problemId, { status: sub.status, createdAt: sub.createdAt });
          }
        });
        
        // Only mark as solved if latest status is accepted
        const acceptedProblemIds = Array.from(latestSubmissions.entries())
          .filter(([_, sub]) => sub.status === "accepted")
          .map(([problemId, _]) => problemId);
        
        setSolvedProblems(acceptedProblemIds);
      })
      .catch(() => {
        setSolvedProblems([]);
      });
  }, [token, selectedProjectId]);

  // Fetch billing access status for gating
  useEffect(() => {
    if (!token) {
      setAccessStatus(null);
      return;
    }
    api
      .get<BillingAccessStatus>("/billing/access-status", token)
      .then((res) => setAccessStatus(res))
      .catch(() => setAccessStatus(null));
  }, [token]);

  useEffect(() => {
    api
      .get<{ enabled: boolean }>("/feature-flags/check/Billing")
      .then((res) => setBillingEnabled(res.enabled))
      .catch(() => setBillingEnabled(false));
  }, []);

  // Fetch user's favorite problem IDs
  useEffect(() => {
    if (!token) {
      setFavoriteProblemIds(new Set());
      return;
    }
    api
      .get<{ favorites: Array<{ problem: { id: string | number } }> }>("/favorites/", token)
      .then((res) => {
        const ids = new Set(res.favorites.map((f) => Number(f.problem.id)));
        setFavoriteProblemIds(ids);
      })
      .catch(() => setFavoriteProblemIds(new Set()));
  }, [token]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages, chatBusy]);

  useEffect(() => {
    if (chatMessages.length > 0) {
      setTimeout(() => chatInputRef.current?.focus(), 50);
    }
  }, [chatMessages.length, chatStep]);

  const openChat = (mode?: 'create' | 'update') => {
    if (mode) {
      const greeting = mode === 'create'
        ? "Hi! I'm Vega. Tell me what you want to practice and I'll build a personalised problem set for you."
        : `Hi! I'll help you add more problems to "${selectedProject?.name}". What would you like to work on?`;
      setChatMode(mode);
      setChatMessages([{ role: 'vega', content: greeting }]);
      setChatStep('prompt');
    } else {
      const greeting = selectedProjectId
        ? `Hi! I'm Vega. What would you like to do — create a new project, or add problems to "${selectedProject?.name}"?`
        : "Hi! I'm Vega. Tell me what you'd like to practice and I'll build a personalised project for you.";
      setChatMode(null);
      setChatMessages([{ role: 'vega', content: greeting }]);
      setChatStep('intent');
    }
    setChatInput('');
    setChatPrompt('');
    setChatBusy(false);
  };

  const closeChat = () => {
    if (chatBusy) return;
    setChatMode(null);
    setChatMessages([]);
    setChatInput('');
    setChatPrompt('');
    setChatBusy(false);
  };

  const handleChatSend = async () => {
    const input = chatInput.trim();
    if (!input || chatBusy || !token) return;
    setChatInput('');

    if (chatStep === 'intent') {
      if (input.length > 500) {
        setChatMessages(prev => [...prev,
          { role: 'user', content: input },
          { role: 'vega', content: "That's a bit long — please keep your message under 500 characters." },
        ]);
        return;
      }
      setChatMessages(prev => [...prev, { role: 'user', content: input }]);
      setChatBusy(true);

      try {
        const { intent, total: extracted } = await api.post<{ intent: string; total: number | null }>(
          '/projects/parse-message',
          { prompt: input, has_existing_project: Boolean(selectedProjectId), project_name: selectedProject?.name ?? '' },
          token
        );

        if (intent === 'unclear') {
          setChatMessages(prev => [...prev, {
            role: 'vega',
            content: "I wasn't sure what you'd like to do. Could you clarify — would you like to create a new project from scratch, or add problems to your existing one?",
          }]);
          setChatBusy(false);
          return;
        }

        const resolvedMode = intent as 'create' | 'update';
        setChatMode(resolvedMode);
        setChatPrompt(input);

        if (extracted !== null && extracted >= 5 && extracted <= 50) {
          const confirmMsg = resolvedMode === 'create'
            ? `Perfect! Building a new project with ${extracted} problems now…`
            : `Perfect! Adding ${extracted} new problems to your project now…`;
          setChatMessages(prev => [...prev, { role: 'vega', content: confirmMsg }]);
          setChatStep('submitting');
          try {
            if (resolvedMode === 'create') {
              const project = await api.post<Project>('/projects/from-prompt', { prompt: input, total: extracted }, token);
              setProjects((prev) => sortProjects([...prev, project]));
              setSelectedProjectId(project.id);
            } else {
              await api.post<Project>(`/projects/${selectedProjectId}/update-from-prompt`, { prompt: input, total: extracted }, token);
            }
            closeChat();
          } catch (e: unknown) {
            const msg = e instanceof Error ? e.message : 'Something went wrong.';
            setChatMessages(prev => [...prev, { role: 'vega', content: `Sorry — ${msg} Would you like to try a different number?` }]);
            setChatStep('error');
            setChatBusy(false);
          }
        } else {
          const askMsg = resolvedMode === 'create'
            ? "How many problems would you like in your new project? (5–50)"
            : "How many problems would you like to add? (5–50)";
          setChatMessages(prev => [...prev, { role: 'vega', content: askMsg }]);
          setChatStep('total');
          setChatBusy(false);
        }
      } catch {
        setChatMessages(prev => [...prev, {
          role: 'vega',
          content: "I wasn't sure what you'd like to do. Would you like to create a new project, or add problems to your existing one?",
        }]);
        setChatBusy(false);
      }

    } else if (chatStep === 'prompt') {
      if (input.length > 500) {
        setChatMessages(prev => [...prev,
          { role: 'user', content: input },
          { role: 'vega', content: "That's a bit long — please keep your message under 500 characters." },
        ]);
        return;
      }
      setChatPrompt(input);
      setChatMessages(prev => [...prev, { role: 'user', content: input }]);
      setChatBusy(true);

      try {
        const { total: extracted } = await api.post<{ total: number | null }>(
          '/projects/extract-intent',
          { prompt: input },
          token
        );

        if (extracted !== null && extracted >= 5 && extracted <= 50) {
          const confirmMsg = chatMode === 'create'
            ? `Got it! Building your project with ${extracted} problems now…`
            : `Got it! Adding ${extracted} new problems to your project now…`;
          setChatMessages(prev => [...prev, { role: 'vega', content: confirmMsg }]);
          setChatStep('submitting');

          try {
            if (chatMode === 'create') {
              const project = await api.post<Project>('/projects/from-prompt', { prompt: input, total: extracted }, token);
              setProjects((prev) => sortProjects([...prev, project]));
              setSelectedProjectId(project.id);
            } else {
              await api.post<Project>(`/projects/${selectedProjectId}/update-from-prompt`, { prompt: input, total: extracted }, token);
            }
            closeChat();
          } catch (e: unknown) {
            const msg = e instanceof Error ? e.message : 'Something went wrong. Please try again.';
            setChatMessages(prev => [...prev, { role: 'vega', content: `Sorry — ${msg} Would you like to try a different number?` }]);
            setChatStep('error');
            setChatBusy(false);
          }
        } else {
          setChatMessages(prev => [...prev,
            { role: 'vega', content: "Got it! How many problems would you like? (enter a number between 5 and 50)" },
          ]);
          setChatStep('total');
          setChatBusy(false);
        }
      } catch {
        setChatMessages(prev => [...prev,
          { role: 'vega', content: "Got it! How many problems would you like? (enter a number between 5 and 50)" },
        ]);
        setChatStep('total');
        setChatBusy(false);
      }

    } else if (chatStep === 'total' || chatStep === 'error') {
      setChatMessages(prev => [...prev, { role: 'user', content: input }]);

      const numMatch = input.match(/\b(\d+)\b/);
      const num = numMatch ? parseInt(numMatch[1], 10) : NaN;

      if (isNaN(num)) {
        setChatMessages(prev => [...prev,
          { role: 'vega', content: "I didn't catch a number — how many problems would you like? (5–50)" },
        ]);
        setChatStep('total');
        return;
      }
      if (num < 5 || num > 50) {
        setChatMessages(prev => [...prev,
          { role: 'vega', content: `${num} is outside the range — please pick a number between 5 and 50.` },
        ]);
        setChatStep('total');
        return;
      }

      const confirmMsg = chatMode === 'create'
        ? `Perfect! Building your project with ${num} problems now…`
        : `Perfect! Adding ${num} new problems to your project now…`;
      setChatMessages(prev => [...prev, { role: 'vega', content: confirmMsg }]);
      setChatStep('submitting');
      setChatBusy(true);

      try {
        if (chatMode === 'create') {
          const project = await api.post<Project>('/projects/from-prompt', { prompt: chatPrompt, total: num }, token);
          setProjects((prev) => sortProjects([...prev, project]));
          setSelectedProjectId(project.id);
        } else {
          await api.post<Project>(`/projects/${selectedProjectId}/update-from-prompt`, { prompt: chatPrompt, total: num }, token);
        }
        closeChat();
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Something went wrong. Please try again.';
        setChatMessages(prev => [...prev, { role: 'vega', content: `Sorry — ${msg} Would you like to try a different number?` }]);
        setChatStep('error');
        setChatBusy(false);
      }
    }
  };

  const handleProjectSelection = async (projectId: string) => {
    setSelectedProjectId(projectId);
    if (!token || !projectId || switchingDefault) return;

    setSwitchingDefault(true);
    try {
      const updated = await api.post<Project>(`/projects/${projectId}/set-default`, {}, token);
      setProjects((prev) => sortProjects(
        prev.map((project) => ({
          ...project,
          isDefault: project.id === updated.id,
        }))
      ));
    } catch (e: unknown) {
      alert(e instanceof Error ? e.message : "Failed to set default project");
    } finally {
      setSwitchingDefault(false);
    }
  };

  const handleDeleteProject = async () => {
    if (!token || !selectedProjectId || deletingProject) return;

    setDeletingProject(true);
    setDeleteProjectError(null);
    try {
      await api.delete<{ deletedProjectId: string; deletedSubmissions: number }>(
        `/projects/${selectedProjectId}`,
        token
      );
      const refreshed = await api.get<Project[]>("/projects/", token);
      const sorted = sortProjects(refreshed);
      setProjects(sorted);
      const defaultProject = sorted.find((project) => project.isDefault) ?? sorted[0];
      setSelectedProjectId(defaultProject?.id ?? "");
      setShowDeleteProjectDialog(false);
    } catch (e: unknown) {
      setDeleteProjectError(e instanceof Error ? e.message : "Failed to delete project");
    } finally {
      setDeletingProject(false);
    }
  };

  const solvedSet = new Set(solvedProblems);
  const totalProblemCount = allProblemsForStats.length;
  const solvedCount = allProblemsForStats.filter((p) => solvedSet.has(p.id)).length;
  const easyTotal = allProblemsForStats.filter((p) => p.difficulty === "easy").length;
  const mediumTotal = allProblemsForStats.filter((p) => p.difficulty === "medium").length;
  const hardTotal = allProblemsForStats.filter((p) => p.difficulty === "hard").length;
  const easySolved = allProblemsForStats.filter((p) => p.difficulty === "easy" && solvedSet.has(p.id)).length;
  const mediumSolved = allProblemsForStats.filter((p) => p.difficulty === "medium" && solvedSet.has(p.id)).length;
  const hardSolved = allProblemsForStats.filter((p) => p.difficulty === "hard" && solvedSet.has(p.id)).length;
  const selectedProject = projects.find((project) => project.id === selectedProjectId) ?? null;
  const hasActiveProject = Boolean(selectedProjectId);

  const promptCreateProject = () => {
    if (!token) return;
    openChat('create');
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      {/* GitHub-Style Stats Dashboard */}
      <div style={{
        maxWidth: '1000px',
        margin: '0 auto',
        padding: '0 0 32px 0'
      }}>
        <style>{`
          @keyframes cellEnter {
            from {
              transform: scale(0);
              opacity: 0;
            }
            to {
              transform: scale(1);
              opacity: 1;
            }
          }
          @keyframes statCardEnter {
            from {
              transform: translateY(16px);
              opacity: 0;
            }
            to {
              transform: translateY(0);
              opacity: 1;
            }
          }
          .problem-cell {
            animation: cellEnter 300ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
          }
          .stat-card {
            animation: statCardEnter 400ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
          }
        `}</style>

        {isLoggedIn && (
          <>
            {/* Project Controls */}
            <div style={{ marginBottom: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {/* Active Project Banner */}
              <div style={{
                background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
                border: '1px solid #bbf7d0',
                borderRadius: '14px',
                padding: '14px 24px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '8px',
                boxShadow: '0 2px 8px rgba(16,185,129,0.08)'
              }}>
                <div style={{ fontSize: '10px', fontWeight: 700, color: '#059669', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                  Active Project
                </div>
                {/* Select wrapper with chevron */}
                <div style={{ position: 'relative', width: '100%', maxWidth: '520px' }}>
                  <select
                    value={selectedProjectId}
                    onChange={(e) => handleProjectSelection(e.target.value)}
                    disabled={!token || projects.length === 0 || switchingDefault}
                    style={{
                      width: '100%',
                      fontSize: '15px',
                      fontWeight: 700,
                      color: '#0F172A',
                      background: 'white',
                      border: '1px solid #bbf7d0',
                      borderRadius: '10px',
                      padding: '9px 40px 9px 16px',
                      appearance: 'none',
                      cursor: 'pointer',
                      boxShadow: '0 1px 4px rgba(16,185,129,0.1)',
                      outline: 'none',
                      textOverflow: 'ellipsis',
                    }}
                  >
                    {projects.length === 0 && <option value="">No projects yet</option>}
                    {projects.map((project) => (
                      <option key={project.id} value={project.id}>
                        {project.name}
                      </option>
                    ))}
                  </select>
                  {/* Chevron overlay */}
                  <div style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none', color: '#059669' }}>
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                {switchingDefault && (
                  <div style={{ fontSize: '11px', color: '#6EE7B7' }}>Switching…</div>
                )}
              </div>
              {/* Action buttons (top right) */}
              <div className="flex items-center gap-2 justify-end">
                <button
                  onClick={() => openChat('create')}
                  disabled={!token || chatBusy || deletingProject}
                  className="px-4 py-2 text-sm font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-colors disabled:bg-emerald-300"
                >
                  New Project
                </button>
                <button
                  onClick={() => openChat('update')}
                  disabled={!token || !selectedProjectId || chatBusy || deletingProject}
                  className="px-4 py-2 text-sm font-semibold rounded-lg border border-blue-300 text-blue-600 bg-transparent hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Update Project
                </button>
                <button
                  onClick={() => {
                    setShowDeleteProjectDialog(true);
                    setDeleteProjectError(null);
                  }}
                  disabled={!token || !selectedProjectId || deletingProject || chatBusy}
                  className="px-4 py-2 text-sm font-medium rounded-lg text-slate-400 bg-transparent hover:text-red-500 hover:bg-red-50 focus:outline-none transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Delete Project
                </button>
              </div>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '16px',
              marginBottom: '24px'
            }}>
              {/* Total Solved Card */}
              <div
                className="stat-card"
                style={{
                  background: 'white',
                  borderRadius: '12px',
                  border: '1px solid #E2E8F0',
                  padding: '20px',
                  boxShadow: '0 2px 8px rgba(15,23,42,0.05)',
                  animationDelay: '100ms'
                }}
              >
                <div style={{ fontSize: '12px', fontWeight: 600, color: '#94A3B8', marginBottom: '8px' }}>
                  TOTAL SOLVED
                </div>
                <div style={{ fontSize: '32px', fontWeight: 800, color: '#10B981' }}>
                  {solvedCount}
                </div>
                <div style={{ fontSize: '12px', color: '#CBD5E1', marginTop: '4px' }}>
                  of {totalProblemCount} problems
                </div>
              </div>

              {/* Easy Solved Card */}
              <div
                className="stat-card"
                style={{
                  background: 'white',
                  borderRadius: '12px',
                  border: '1px solid #E2E8F0',
                  padding: '20px',
                  boxShadow: '0 2px 8px rgba(15,23,42,0.05)',
                  animationDelay: '150ms'
                }}
              >
                <div style={{ fontSize: '12px', fontWeight: 600, color: '#94A3B8', marginBottom: '8px' }}>
                  EASY
                </div>
                <div style={{ fontSize: '32px', fontWeight: 800, color: '#10B981' }}>
                  {easySolved}
                </div>
                <div style={{ fontSize: '12px', color: '#CBD5E1', marginTop: '4px' }}>
                  of {easyTotal}
                </div>
              </div>

              {/* Medium Solved Card */}
              <div
                className="stat-card"
                style={{
                  background: 'white',
                  borderRadius: '12px',
                  border: '1px solid #E2E8F0',
                  padding: '20px',
                  boxShadow: '0 2px 8px rgba(15,23,42,0.05)',
                  animationDelay: '200ms'
                }}
              >
                <div style={{ fontSize: '12px', fontWeight: 600, color: '#94A3B8', marginBottom: '8px' }}>
                  MEDIUM
                </div>
                <div style={{ fontSize: '32px', fontWeight: 800, color: '#F59E0B' }}>
                  {mediumSolved}
                </div>
                <div style={{ fontSize: '12px', color: '#CBD5E1', marginTop: '4px' }}>
                  of {mediumTotal}
                </div>
              </div>

              {/* Hard Solved Card */}
              <div
                className="stat-card"
                style={{
                  background: 'white',
                  borderRadius: '12px',
                  border: '1px solid #E2E8F0',
                  padding: '20px',
                  boxShadow: '0 2px 8px rgba(15,23,42,0.05)',
                  animationDelay: '250ms'
                }}
              >
                <div style={{ fontSize: '12px', fontWeight: 600, color: '#94A3B8', marginBottom: '8px' }}>
                  HARD
                </div>
                <div style={{ fontSize: '32px', fontWeight: 800, color: '#EF4444' }}>
                  {hardSolved}
                </div>
                <div style={{ fontSize: '12px', color: '#CBD5E1', marginTop: '4px' }}>
                  of {hardTotal}
                </div>
              </div>
            </div>


            {/* Contribution Grid */}
            <div style={{
              background: 'white',
              borderRadius: '12px',
              border: '1px solid #E2E8F0',
              padding: '24px',
              boxShadow: '0 2px 8px rgba(15,23,42,0.05)',
              marginBottom: '24px'
            }}>
              <h3 style={{
                fontSize: '16px',
                fontWeight: 700,
                color: '#0F172A',
                margin: '0 0 20px 0'
              }}>
                Problem Completion
              </h3>

              <div style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '6px',
                alignItems: 'flex-start'
              }}>
                {problems.map((p, idx) => (
                  <div
                    key={p.id}
                    className="problem-cell"
                    style={{
                      animationDelay: `${100 + (idx * 30)}ms`
                    }}
                  >
                    <ProblemCell
                      problem={p}
                      solvedProblems={solvedProblems}
                      selectedProjectId={selectedProjectId}
                      isLoggedIn={isLoggedIn}
                      canOpenProblem={hasActiveProject}
                      onMissingProject={promptCreateProject}
                      hasBillingAccess={hasBillingAccess}
                      billingEnabled={billingEnabled}
                    />
                  </div>
                ))}
              </div>

              {/* Legend */}
              <div style={{
                marginTop: '24px',
                paddingTop: '20px',
                borderTop: '1px solid #F1F5F9',
                display: 'flex',
                gap: '20px',
                alignItems: 'center',
                fontSize: '13px',
                color: '#64748B'
              }}>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <div style={{
                    width: '24px',
                    height: '24px',
                    borderRadius: '4px',
                    background: '#10B981',
                    border: '1px solid #D1D5DB',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '12px',
                    fontWeight: 700
                  }}>
                    ✓
                  </div>
                  <span style={{ fontWeight: 500 }}>Solved</span>
                </div>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <div style={{
                    width: '24px',
                    height: '24px',
                    borderRadius: '4px',
                    background: '#10B981',
                    border: '1px solid #D1D5DB'
                  }} />
                  <span style={{ fontWeight: 500 }}>Easy</span>
                </div>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <div style={{
                    width: '24px',
                    height: '24px',
                    borderRadius: '4px',
                    background: '#F59E0B',
                    border: '1px solid #D1D5DB'
                  }} />
                  <span style={{ fontWeight: 500 }}>Medium</span>
                </div>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <div style={{
                    width: '24px',
                    height: '24px',
                    borderRadius: '4px',
                    background: '#EF4444',
                    border: '1px solid #D1D5DB'
                  }} />
                  <span style={{ fontWeight: 500 }}>Hard</span>
                </div>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <div style={{
                    width: '24px',
                    height: '24px',
                    borderRadius: '4px',
                    background: '#E5E7EB',
                    border: '1px solid #D1D5DB'
                  }} />
                  <span style={{ fontWeight: 500 }}>Unsolved</span>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Vega explanation banner — shown for AI-generated projects */}
        {selectedProject?.explanation &&
          dismissedExplanationProjectId !== selectedProject.id && (
            <div className="mt-6 rounded-xl border border-indigo-100 bg-gradient-to-r from-indigo-50 to-purple-50 px-5 py-4 shadow-sm">
              <div className="flex items-start gap-4">
                {/* Icon */}
                <div className="flex-shrink-0 mt-0.5 h-9 w-9 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 text-white flex items-center justify-center shadow-md">
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" />
                  </svg>
                </div>
                {/* Left: heading + explanation text (~65%) */}
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-bold text-indigo-900 mb-1.5 flex items-center gap-2">
                    <span>Why this set</span>
                    <span className="text-xs font-normal text-indigo-600 bg-indigo-100 px-2 py-0.5 rounded-full">
                      AI-generated
                    </span>
                  </div>
                  <p className="text-sm text-slate-700 leading-relaxed">
                    {selectedProject.explanation}
                  </p>
                </div>
                {/* Right: meta badges + dismiss (~35%) */}
                <div className="flex-shrink-0 flex flex-col items-end gap-2 ml-4">
                  {selectedProject.level && (
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/80 border border-indigo-200 text-indigo-700 text-xs font-medium shadow-sm whitespace-nowrap">
                      <svg className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                      </svg>
                      Level: {selectedProject.level}
                    </span>
                  )}
                  {selectedProject.strategy && (
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/80 border border-indigo-200 text-indigo-700 text-xs font-medium shadow-sm whitespace-nowrap">
                      <svg className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                      </svg>
                      {selectedProject.strategy.replace(/_/g, " ")}
                    </span>
                  )}
                  <button
                    onClick={() => setDismissedExplanationProjectId(selectedProject.id)}
                    className="mt-1 text-slate-400 hover:text-slate-600 hover:bg-white/50 rounded-lg p-1 transition-colors"
                    aria-label="Dismiss"
                  >
                    <svg className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          )}

        {/* Filter + Search bar — unified row */}
        <div className="flex items-center justify-between gap-4 mb-4 mt-6">
          {/* Left: filter pills */}
          <div className="inline-flex items-center gap-1 p-1 rounded-2xl border border-slate-200 bg-white shadow-sm flex-shrink-0">
          {QUICK_FILTERS.map((d) => {
            const isActive = filter === d;
            const label =
              d === "favorite"
                ? "Favourite"
                : d === "solved"
                  ? "Solved"
                  : d.charAt(0).toUpperCase() + d.slice(1);
            const activeTone =
              d === "easy"
                ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                : d === "medium"
                  ? "bg-amber-50 text-amber-700 border-amber-200"
                  : d === "hard"
                    ? "bg-red-50 text-red-700 border-red-200"
                    : d === "solved"
                      ? "bg-teal-50 text-teal-700 border-teal-200"
                    : d === "favorite"
                      ? "bg-yellow-50 text-yellow-700 border-yellow-200"
                      : "bg-slate-100 text-slate-700 border-slate-200";

            return (
            <button
              key={d}
              onClick={() => setFilter(d)}
              className={`px-3 py-1.5 rounded-xl text-sm font-semibold border transition-all ${
                isActive
                  ? activeTone
                  : "border-transparent text-slate-500 hover:text-slate-700 hover:bg-slate-50"
              }`}
            >
              {label}
            </button>
            );
          })}
          </div>
          {/* Right: search */}
          <div className="flex items-center gap-2 max-w-xs w-full">
            <svg className="w-4 h-4 text-slate-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by title or tags..."
              className="w-full px-3 py-1.5 text-sm border border-slate-200 rounded-lg bg-white text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="text-slate-400 hover:text-slate-600 p-1 flex-shrink-0"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        </div>

        {/* Problems List */}
        <div style={{ marginTop: '0' }}>
          <div style={{
            background: 'white',
            borderRadius: '12px',
            border: '1px solid #E2E8F0',
            boxShadow: '0 2px 8px rgba(15,23,42,0.05)',
            overflow: 'hidden'
          }}>
            {/* Table Header */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '30px 40px 60px 1fr 150px 120px',
              gap: '16px',
              padding: '16px 24px',
              background: '#F8FAFC',
              borderBottom: '1px solid #E2E8F0',
              fontSize: '12px',
              fontWeight: 600,
              color: '#94A3B8',
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              <div style={{ textAlign: 'center' }}>★</div>
              <div></div>
              <div 
                style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}
                onClick={() => {
                  if (sortBy === 'id') {
                    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
                  } else {
                    setSortBy('id');
                    setSortOrder('asc');
                  }
                }}
              >
                # {sortBy === 'id' && (sortOrder === 'asc' ? '↑' : '↓')}
              </div>
              <div 
                style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}
                onClick={() => {
                  if (sortBy === 'title') {
                    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
                  } else {
                    setSortBy('title');
                    setSortOrder('asc');
                  }
                }}
              >
                Title {sortBy === 'title' && (sortOrder === 'asc' ? '↑' : '↓')}
              </div>
              <div>Tags</div>
              <div 
                style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '4px' }}
                onClick={() => {
                  if (sortBy === 'difficulty') {
                    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
                  } else {
                    setSortBy('difficulty');
                    setSortOrder('asc');
                  }
                }}
              >
                Difficulty {sortBy === 'difficulty' && (sortOrder === 'asc' ? '↑' : '↓')}
              </div>
            </div>

            {/* Table Rows */}
            {(() => {
              const visibleProblems = filter === "favorite"
                ? problems.filter((problem) => favoriteProblemIds.has(problem.id))
                : problems;

              return visibleProblems.map((p) => {
                const isSolved = solvedProblems.includes(p.id);
                const targetPath = selectedProjectId
                  ? `/problems/${p.slug}?projectId=${encodeURIComponent(selectedProjectId)}`
                  : `/problems/${p.slug}`;
                const pricingRedirectPath = `/pricing?required=1&redirect=${encodeURIComponent(targetPath)}`;
                const authRedirectPath = `/auth?redirect=${encodeURIComponent(pricingRedirectPath)}`;

                // If billing is disabled, skip pricing redirect
                const shouldCheckBilling = billingEnabled ?? false;
                const problemLink = !isLoggedIn
                  ? authRedirectPath
                  : shouldCheckBilling && !hasBillingAccess
                  ? pricingRedirectPath
                  : targetPath;

                const isFavorite = favoriteProblemIds.has(p.id);

                return (
                  <Link
                    key={p.id}
                    to={problemLink}
                    style={{
                      display: 'grid',
                      gridTemplateColumns: '30px 40px 60px 1fr 150px 120px',
                      gap: '16px',
                      padding: '16px 24px',
                      borderBottom: '1px solid #F1F5F9',
                      alignItems: 'center',
                      cursor: 'pointer',
                      transition: 'all 150ms ease',
                      background: isSolved ? 'linear-gradient(90deg, #F0FDF4 0%, #FFFFFF 100%)' : 'white',
                      textDecoration: 'none',
                      color: 'inherit'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = isSolved
                        ? 'linear-gradient(90deg, #DCFCE7 0%, #F8FAFC 100%)'
                        : '#F8FAFC';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = isSolved
                        ? 'linear-gradient(90deg, #F0FDF4 0%, #FFFFFF 100%)'
                        : 'white';
                    }}
                    onClick={(e) => {
                      if (isLoggedIn && !hasActiveProject) {
                        e.preventDefault();
                        promptCreateProject();
                      }
                    }}
                  >
                    {/* Favorite Star */}
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      {isFavorite && (
                        <svg
                          className="w-5 h-5"
                          style={{
                            width: '20px',
                            height: '20px',
                            fill: '#FBBF24',
                            filter: 'drop-shadow(0 1px 2px rgba(251, 191, 36, 0.3))'
                          }}
                          viewBox="0 0 24 24"
                        >
                          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                        </svg>
                      )}
                    </div>

                    {/* Solved Checkmark */}
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                    {isSolved && (
                      <div
                        style={{
                          width: '24px',
                          height: '24px',
                          borderRadius: '50%',
                          background: '#10B981',
                          border: '2px solid white',
                          boxShadow: '0 2px 8px rgba(16,185,129,0.3)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                          fontSize: '14px',
                          fontWeight: 800
                        }}
                      >
                        ✓
                      </div>
                    )}
                    </div>

                    {/* Problem Number */}
                    <div style={{
                      fontSize: '14px',
                      fontWeight: 600,
                      color: isSolved ? '#10B981' : '#CBD5E1'
                    }}>
                    {String(problemSequence.get(p.id) || 0).padStart(2, '0')}
                    </div>

                    {/* Title */}
                    <div style={{
                      fontSize: '15px',
                      fontWeight: 600,
                      color: isSolved ? '#10B981' : '#0F172A'
                    }}>
                      {p.title}
                    </div>

                  {/* Tags */}
                  <div style={{
                    display: 'flex',
                    gap: '6px',
                    flexWrap: 'wrap'
                  }}>
                    {(p.tags || []).slice(0, 2).map((tag) => (
                      <span
                        key={tag}
                        style={{
                          background: '#EEF3FF',
                          color: '#1A6BFF',
                          fontSize: '11px',
                          fontWeight: 600,
                          padding: '2px 8px',
                          borderRadius: '999px',
                          border: '1px solid rgba(26,107,255,0.15)'
                        }}
                      >
                        {tag}
                      </span>
                    ))}
                    </div>

                    {/* Difficulty Badge */}
                    <div style={{ textAlign: 'right' }}>
                      <div
                        style={{
                          display: 'inline-block',
                          fontSize: '12px',
                          fontWeight: 700,
                          padding: '4px 12px',
                          borderRadius: '999px',
                          textTransform: 'capitalize',
                          background: p.difficulty === 'easy'
                            ? '#ECFDF5'
                            : p.difficulty === 'medium'
                            ? '#FFFBEB'
                            : '#FEF2F2',
                          color: p.difficulty === 'easy'
                            ? '#10B981'
                            : p.difficulty === 'medium'
                            ? '#F59E0B'
                            : '#EF4444',
                          border: p.difficulty === 'easy'
                            ? '1px solid rgba(16,185,129,0.2)'
                            : p.difficulty === 'medium'
                            ? '1px solid rgba(245,158,11,0.2)'
                            : '1px solid rgba(239,68,68,0.2)'
                        }}
                      >
                        {p.difficulty}
                    </div>
                  </div>
                </Link>
              );
            });
          })()}
          </div>
        </div>
      </div>

      {/* Vega Floating Action Button */}
      {isLoggedIn && chatMessages.length === 0 && (
        <button
          onClick={() => openChat()}
          className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 shadow-xl flex items-center justify-center hover:scale-105 active:scale-95 transition-transform border border-slate-700"
          title="Chat with Vega"
        >
          <div className="relative">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-emerald-400 to-blue-500 flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 border-2 border-slate-900 rounded-full" />
          </div>
        </button>
      )}

      {/* Vega Chat Widget — bottom-right */}
      {isLoggedIn && chatMessages.length > 0 && (
        <div
          className="fixed bottom-6 right-6 z-50 flex flex-col rounded-2xl overflow-hidden shadow-2xl border border-slate-200 bg-white"
          style={{ width: '460px', minHeight: '480px', maxHeight: '840px' }}
        >
          {/* Header */}
          <div className="px-4 py-3 bg-gradient-to-r from-slate-900 to-slate-800 flex items-center gap-2.5 flex-shrink-0">
            <div className="relative flex-shrink-0">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-400 to-blue-500 flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 border-2 border-slate-900 rounded-full" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-white font-semibold text-sm leading-tight">Vega</div>
              <div className="text-slate-400 text-xs truncate leading-tight">
                {chatMode === 'create' ? 'New project' : `Updating "${selectedProject?.name}"`}
              </div>
            </div>
            <button
              onClick={closeChat}
              disabled={chatBusy}
              className="w-7 h-7 flex items-center justify-center rounded-lg text-slate-400 hover:text-white hover:bg-slate-700 transition-colors disabled:opacity-30 flex-shrink-0"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-3 py-3 space-y-2.5 bg-slate-50">
            {chatMessages.map((msg, i) => (
              <div key={i} className={`flex items-end gap-1.5 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {msg.role === 'vega' && (
                  <div className="w-6 h-6 rounded-md bg-gradient-to-br from-emerald-500 to-blue-600 flex items-center justify-center flex-shrink-0 mb-0.5">
                    <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                )}
                <div className={`max-w-[240px] px-3 py-2 text-sm leading-relaxed rounded-2xl ${
                  msg.role === 'vega'
                    ? 'bg-white border border-slate-200 text-slate-800 rounded-tl-sm shadow-sm'
                    : chatMode === 'create'
                      ? 'bg-emerald-600 text-white rounded-tr-sm'
                      : 'bg-blue-600 text-white rounded-tr-sm'
                }`}>
                  {msg.content}
                </div>
              </div>
            ))}

            {/* Typing indicator */}
            {chatBusy && (
              <div className="flex items-end gap-1.5 justify-start">
                <div className="w-6 h-6 rounded-md bg-gradient-to-br from-emerald-500 to-blue-600 flex items-center justify-center flex-shrink-0 mb-0.5">
                  <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div className="bg-white border border-slate-200 px-3 py-2.5 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-1">
                  <span className="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Input */}
          <div className="px-3 py-2.5 border-t border-slate-100 bg-white flex items-end gap-2 flex-shrink-0">
            <textarea
              ref={chatInputRef}
              rows={1}
              value={chatInput}
              disabled={chatBusy || chatStep === 'submitting'}
              onChange={(e) => {
                setChatInput(e.target.value);
                e.currentTarget.style.height = 'auto';
                e.currentTarget.style.height = Math.min(e.currentTarget.scrollHeight, 100) + 'px';
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleChatSend();
                }
              }}
              placeholder={
                chatStep === 'intent'
                  ? 'Tell Vega what you’d like to do…'
                  : chatStep === 'prompt'
                  ? (chatMode === 'create' ? 'What do you want to practice?' : 'What problems do you want to add?')
                  : chatStep === 'total' || chatStep === 'error'
                  ? 'How many problems? (5–50)'
                  : ''
              }
              className="flex-1 resize-none overflow-hidden text-sm px-3 py-2 border border-slate-200 rounded-xl bg-slate-50 text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-transparent disabled:opacity-40"
              style={{ minHeight: '36px', maxHeight: '100px' }}
            />
            <button
              onClick={handleChatSend}
              disabled={chatBusy || chatStep === 'submitting' || !chatInput.trim()}
              className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center transition-all disabled:opacity-40 disabled:cursor-not-allowed ${
                chatMode === 'update'
                  ? 'bg-blue-600 hover:bg-blue-700 text-white'
                  : 'bg-emerald-600 hover:bg-emerald-700 text-white'
              }`}
            >
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {isLoggedIn && showDeleteProjectDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/45 px-4">
          <div className="w-full max-w-md rounded-2xl bg-white shadow-2xl border border-slate-200">
            <div className="px-6 py-5 border-b border-slate-100">
              <h3 className="text-lg font-bold text-slate-900">Delete Project</h3>
              <p className="text-sm text-slate-500 mt-1">This action cannot be undone.</p>
            </div>
            <div className="px-6 py-5">
              {selectedProject?.isDefault ? (
                <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-700">
                  The default project <span className="font-semibold">{selectedProject?.name || "this project"}</span> cannot be deleted.
                </div>
              ) : (
                <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                  Deleting <span className="font-semibold">{selectedProject?.name || "this project"}</span> will remove all progress and submissions under this project.
                </div>
              )}
              {deleteProjectError && (
                <div className="mt-3 text-sm text-red-600">{deleteProjectError}</div>
              )}
            </div>
            <div className="px-6 py-4 border-t border-slate-100 flex items-center justify-end gap-2">
              <button
                onClick={() => {
                  if (deletingProject) return;
                  setShowDeleteProjectDialog(false);
                  setDeleteProjectError(null);
                }}
                className="px-4 py-2 text-sm rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteProject}
                disabled={deletingProject || selectedProject?.isDefault}
                className="px-4 py-2 text-sm font-semibold rounded-lg bg-red-600 text-white hover:bg-red-700 disabled:bg-red-300 disabled:cursor-not-allowed"
              >
                {deletingProject ? "Deleting..." : "Delete Project"}
              </button>
            </div>
          </div>
        </div>
      )}

      {pagination && pagination.pages > 1 && (
        <div className="flex justify-center items-center gap-2 mt-8">
          <button
            onClick={() => {
              setCurrentPage(pagination.prev_num);
              fetchProblems(pagination.prev_num, sortBy, sortOrder, filter);
            }}
            disabled={!pagination.has_prev}
            className={`px-3 py-2 text-sm font-mono rounded-lg border transition-colors ${
              pagination.has_prev
                ? "border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
                : "border-slate-100 bg-slate-50 text-slate-400 cursor-not-allowed"
            }`}
          >
            ←
          </button>

          {/* Page numbers */}
          <div className="flex items-center gap-1">
            {Array.from({ length: Math.min(5, pagination.pages) }, (_, i) => {
              let pageNum;
              if (pagination.pages <= 5) {
                pageNum = i + 1;
              } else if (currentPage <= 3) {
                pageNum = i + 1;
              } else if (currentPage >= pagination.pages - 2) {
                pageNum = pagination.pages - 4 + i;
              } else {
                pageNum = currentPage - 2 + i;
              }

              return (
                <button
                  key={pageNum}
                  onClick={() => {
                    setCurrentPage(pageNum);
                    fetchProblems(pageNum, sortBy, sortOrder, filter);
                  }}
                  className={`px-3 py-2 text-sm font-mono rounded-lg border transition-colors ${
                    pageNum === currentPage
                      ? "border-emerald-500 bg-emerald-50 text-emerald-700"
                      : "border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
                  }`}
                >
                  {pageNum}
                </button>
              );
            })}
          </div>

          <button
            onClick={() => {
              setCurrentPage(pagination.next_num);
              fetchProblems(pagination.next_num, sortBy, sortOrder, filter);
            }}
            disabled={!pagination.has_next}
            className={`px-3 py-2 text-sm font-mono rounded-lg border transition-colors ${
              pagination.has_next
                ? "border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
                : "border-slate-100 bg-slate-50 text-slate-400 cursor-not-allowed"
            }`}
          >
            →
          </button>
        </div>
      )}

      {/* Loading indicator */}
      {loading && (
        <div className="flex justify-center items-center gap-2 mt-8">
          <div className="w-4 h-4 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-sm font-mono text-slate-600">Loading...</span>
        </div>
      )}
    </div>
  );
}
