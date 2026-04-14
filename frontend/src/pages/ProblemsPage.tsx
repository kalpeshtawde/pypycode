import { useEffect, useState } from "react";
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
}: {
  problem: Problem;
  solvedProblems: number[];
  selectedProjectId: string;
  isLoggedIn: boolean;
  canOpenProblem: boolean;
  onMissingProject: () => void;
  hasBillingAccess?: boolean;
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

  // If logged in but no billing access, go to pricing
  const problemLink = !isLoggedIn
    ? authRedirectPath
    : hasBillingAccess
    ? targetPath
    : pricingRedirectPath;

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
  const [problems, setProblems] = useState<Problem[]>([]);
  const [allProblemsForStats, setAllProblemsForStats] = useState<Problem[]>([]);
  const [solvedProblems, setSolvedProblems] = useState<number[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<string>(
    () => localStorage.getItem("selectedProjectId") ?? ""
  );
  const [problemSequence, setProblemSequence] = useState<Map<number, number>>(new Map());
  const [filter, setFilter] = useState<typeof QUICK_FILTERS[number]>("all");
  const [sortBy, setSortBy] = useState<"id" | "difficulty" | "created_at">("id");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");
  const [currentPage, setCurrentPage] = useState(1);
  const [pagination, setPagination] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [creatingProject, setCreatingProject] = useState(false);
  const [switchingDefault, setSwitchingDefault] = useState(false);
  const [showCreateProjectDialog, setShowCreateProjectDialog] = useState(false);
  const [newProjectName, setNewProjectName] = useState("");
  const [createProjectError, setCreateProjectError] = useState<string | null>(null);
  const [showDeleteProjectDialog, setShowDeleteProjectDialog] = useState(false);
  const [deletingProject, setDeletingProject] = useState(false);
  const [deleteProjectError, setDeleteProjectError] = useState<string | null>(null);
  const [favoriteProblemIds, setFavoriteProblemIds] = useState<Set<number>>(new Set());
  const [searchQuery, setSearchQuery] = useState("");

  const sortProjects = (items: Project[]) => {
    return [...items].sort((a, b) => {
      if (a.isDefault === b.isDefault) {
        return a.name.localeCompare(b.name);
      }
      return a.isDefault ? -1 : 1;
    });
  };

  const fetchProblems = (page: number = 1, sort: string = sortBy, order: string = sortOrder, difficulty: string = filter) => {
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
            ...(trimmedSearch && { search: trimmedSearch }),
          });

          const data = await api.get<{ problems: Problem[]; pagination: any }>(`/problems/?${params}`);
          collected.push(...data.problems);
          pages = data.pagination?.pages || 1;
          nextPage += 1;
        }

        return collected;
      };

      fetchAllProblems()
        .then((allProblems) => {
          const solvedSet = new Set(solvedProblems);
          const solvedOnly = allProblems.filter((p) => solvedSet.has(p.id));

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
          setLoading(false);
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

          const difficultyRank = (value: string) => {
            if (value === "easy") return 1;
            if (value === "medium") return 2;
            if (value === "hard") return 3;
            return 4;
          };

          enriched.sort((a, b) => {
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
          const total = enriched.length;
          const pages = Math.max(1, Math.ceil(total / perPage));
          const safePage = Math.min(Math.max(page, 1), pages);
          const start = (safePage - 1) * perPage;
          const pageItems = enriched.slice(start, start + perPage).map((item) => item.problem);

          setProblems(pageItems);
          setFavoriteProblemIds(new Set(enriched.map((item) => item.problem.id)));
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
          setLoading(false);
        });
      return;
    }

    const difficultyParam = ["easy", "medium", "hard"].includes(difficulty) ? difficulty : "";
    const params = new URLSearchParams({
      page: page.toString(),
      per_page: "15",
      sort: sort,
      order: order,
      ...(difficultyParam && { difficulty: difficultyParam }),
      ...(trimmedSearch && { search: trimmedSearch }),
    });
    
    api.get<{ problems: Problem[]; pagination: any }>(`/problems/?${params}`)
      .then((data) => {
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
        setProblems([]);
        setPagination(null);
      })
      .finally(() => {
        setLoading(false);
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

        const data = await api.get<{ problems: Problem[]; pagination: any }>(`/problems/?${params}`);
        collected.push(...data.problems);
        pages = data.pagination?.pages || 1;
        page += 1;
      }

      setAllProblemsForStats(collected);
    };

    fetchAllProblemsForStats().catch(() => {
      setAllProblemsForStats([]);
    });
  }, []);

  useEffect(() => {
    setCurrentPage(1);
    fetchProblems(1, sortBy, sortOrder, filter);
  }, [sortBy, sortOrder, filter, searchQuery]);

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

  const handleCreateProject = async () => {
    if (!token || creatingProject) return;
    const name = newProjectName.trim();

    if (!name) {
      setCreateProjectError("Project name is required");
      return;
    }
    if (name.length > 25) {
      setCreateProjectError("Project name must be at most 25 characters");
      return;
    }

    setCreatingProject(true);
    setCreateProjectError(null);
    try {
      const project = await api.post<Project>("/projects/", { name }, token);
      setProjects((prev) => sortProjects([...prev, project]));
      setSelectedProjectId(project.id);
      setShowCreateProjectDialog(false);
      setNewProjectName("");
    } catch (e: unknown) {
      setCreateProjectError(e instanceof Error ? e.message : "Unable to create project");
    } finally {
      setCreatingProject(false);
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
    setShowCreateProjectDialog(true);
    setCreateProjectError("Please create a project before opening a problem");
    setNewProjectName("");
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      {/* GitHub-Style Stats Dashboard */}
      <div style={{
        maxWidth: '1000px',
        margin: '0 auto',
        padding: '0 24px 80px 24px'
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
            {/* Stats Cards Row */}
            <div style={{
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: '12px',
              flexWrap: 'wrap'
            }}>
              <div className="flex items-center gap-3">
                <div style={{
                  fontSize: '16px',
                  fontWeight: 700,
                  color: '#0F172A',
                  margin: 0
                }}>
                  Active Project
                </div>
                <select
                  value={selectedProjectId}
                  onChange={(e) => handleProjectSelection(e.target.value)}
                  disabled={!token || projects.length === 0 || switchingDefault}
                  className="px-3 py-2 text-sm font-mono border border-emerald-200 rounded-lg bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 disabled:bg-slate-100 disabled:text-slate-400 min-w-[220px]"
                >
                  {projects.length === 0 && <option value="">No projects</option>}
                  {projects.map((project) => (
                    <option key={project.id} value={project.id}>
                      {project.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    setShowCreateProjectDialog(true);
                    setCreateProjectError(null);
                    setNewProjectName("");
                  }}
                  disabled={!token || creatingProject || deletingProject}
                  className="px-4 py-2 text-sm font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-colors disabled:bg-emerald-300"
                >
                  Create New Project
                </button>
                <button
                  onClick={() => {
                    setShowDeleteProjectDialog(true);
                    setDeleteProjectError(null);
                  }}
                  disabled={!token || !selectedProjectId || deletingProject || creatingProject}
                  className="px-4 py-2 text-sm font-semibold rounded-lg bg-red-600 text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors disabled:bg-red-300"
                >
                  Delete Project
                </button>
              </div>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '16px',
              marginBottom: '40px'
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
              boxShadow: '0 2px 8px rgba(15,23,42,0.05)'
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

        {/* Quick filters */}
        <div className="mt-6 mb-6">
          <div className="inline-flex items-center gap-1.5 p-1 rounded-2xl border border-slate-200 bg-white shadow-sm">
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
              className={`px-4 py-2 rounded-xl text-sm font-semibold border transition-all ${
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
        </div>

        {/* Problems List */}
        <div style={{ marginTop: '30px' }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '20px'
          }}>
            <h3 style={{
              fontSize: '18px',
              fontWeight: 700,
              color: '#0F172A',
              margin: '0'
            }}>
              All Problems
            </h3>

            {/* Search input */}
            <div className="flex items-center gap-2 flex-1 max-w-md mx-8">
              <svg className="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
                  className="text-slate-400 hover:text-slate-600 p-1"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>

            {/* Sort controls - same line as heading */}
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono text-slate-600">Sort:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="px-3 py-1.5 text-sm font-mono border border-slate-200 rounded-lg bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="id">Default</option>
                <option value="difficulty">Difficulty</option>
                <option value="created_at">Date Added</option>
              </select>
              <button
                onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
                className="px-3 py-1.5 text-sm font-mono border border-slate-200 rounded-lg bg-white text-slate-700 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-colors"
              >
                {sortOrder === "asc" ? "↑" : "↓"}
              </button>
            </div>
          </div>

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
              <div>#</div>
              <div>Title</div>
              <div>Tags</div>
              <div style={{ textAlign: 'right' }}>Difficulty</div>
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

                // If logged in but no billing access, go to pricing
                const problemLink = !isLoggedIn
                  ? authRedirectPath
                  : hasBillingAccess
                  ? targetPath
                  : pricingRedirectPath;

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

      {/* Pagination */}
      {isLoggedIn && showCreateProjectDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/45 px-4">
          <div className="w-full max-w-md rounded-2xl bg-white shadow-2xl border border-slate-200">
            <div className="px-6 py-5 border-b border-slate-100">
              <h3 className="text-lg font-bold text-slate-900">Create New Project</h3>
              <p className="text-sm text-slate-500 mt-1">Track submissions under a dedicated project.</p>
            </div>
            <div className="px-6 py-5">
              <label className="block text-xs font-semibold text-slate-600 mb-2">Project Name</label>
              <input
                autoFocus
                maxLength={25}
                value={newProjectName}
                onChange={(e) => {
                  setNewProjectName(e.target.value);
                  setCreateProjectError(null);
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    handleCreateProject();
                  }
                }}
                placeholder="e.g. Interview Prep Jan 2026"
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
              <div className="mt-2 text-xs text-slate-500">{newProjectName.trim().length}/25 characters</div>
              {createProjectError && (
                <div className="mt-2 text-sm text-red-600">{createProjectError}</div>
              )}
            </div>
            <div className="px-6 py-4 border-t border-slate-100 flex items-center justify-end gap-2">
              <button
                onClick={() => {
                  if (creatingProject) return;
                  setShowCreateProjectDialog(false);
                  setCreateProjectError(null);
                  setNewProjectName("");
                }}
                className="px-4 py-2 text-sm rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateProject}
                disabled={creatingProject}
                className="px-4 py-2 text-sm font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 disabled:bg-emerald-300"
              >
                {creatingProject ? "Creating..." : "Create"}
              </button>
            </div>
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
              <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                Deleting <span className="font-semibold">{selectedProject?.name || "this project"}</span> will remove all progress and submissions under this project.
              </div>
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
                disabled={deletingProject}
                className="px-4 py-2 text-sm font-semibold rounded-lg bg-red-600 text-white hover:bg-red-700 disabled:bg-red-300"
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
