import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";
import type { Problem } from "../types";

const DIFFS = ["all", "easy", "medium", "hard"] as const;

function ProblemCell({ problem, solvedProblems }: { problem: Problem; solvedProblems: number[] }) {
  const isSolved = solvedProblems.includes(problem.id);
  
  const difficultyColors = {
    easy: '#10B981',
    medium: '#F59E0B',
    hard: '#EF4444'
  };

  const cellColor = difficultyColors[problem.difficulty];
  const textColor = isSolved ? 'white' : 'white';
  const opacity = isSolved ? 1 : 0.3;

  return (
    <Link
      to={`/problems/${problem.slug}`}
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
    >
      {isSolved && '✓'}
    </Link>
  );
}

export default function ProblemsPage() {
  const { token } = useAuthStore();
  const [problems, setProblems] = useState<Problem[]>([]);
  const [solvedProblems, setSolvedProblems] = useState<number[]>([]);
  const [problemSequence, setProblemSequence] = useState<Map<number, number>>(new Map());
  const [filter, setFilter] = useState<typeof DIFFS[number]>("all");
  const [sortBy, setSortBy] = useState<"id" | "difficulty" | "created_at">("id");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");
  const [currentPage, setCurrentPage] = useState(1);
  const [pagination, setPagination] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchProblems = (page: number = 1, sort: string = sortBy, order: string = sortOrder, difficulty: string = filter) => {
    setLoading(true);
    const params = new URLSearchParams({
      page: page.toString(),
      per_page: "15",
      sort: sort,
      order: order,
      ...(difficulty !== "all" && { difficulty })
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
    setCurrentPage(1);
    fetchProblems(1, sortBy, sortOrder, filter);
  }, [sortBy, sortOrder, filter]);

  useEffect(() => {
    if (!token) return;
    // Fetch all submissions to get latest status for each problem
    api.get<Array<{ id: number; problemId: number; status: string; createdAt: string }>>(`/submissions/all`, token)
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
  }, [token]);

  const solvedCount = problems.filter((p) => solvedProblems.includes(p.id)).length;

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      {/* Filter tabs */}
      <div className="flex items-center gap-2 mb-6">
        {DIFFS.map((d) => (
          <button
            key={d}
            onClick={() => setFilter(d)}
            className={`px-4 py-1.5 rounded-lg text-sm font-mono capitalize transition-all ${
              filter === d
                ? "bg-surface border border-accent/30 text-accent"
                : "text-slate-500 hover:text-slate-300"
            }`}
          >
            {d}
          </button>
        ))}
      </div>

      {/* Solved counter */}
      <div className="flex justify-center mb-6">
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            background: 'white',
            border: '1px solid #E2E8F0',
            borderRadius: '999px',
            padding: '6px 16px',
            fontSize: '13px',
            fontWeight: 600,
            color: '#10B981',
            boxShadow: '0 1px 4px rgba(16, 185, 129, 0.1)'
          }}
        >
          <div
            style={{
              width: '16px',
              height: '16px',
              borderRadius: '50%',
              background: '#10B981',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '14px',
              fontWeight: 800
            }}
          >
            ✓
          </div>
          {solvedCount} solved
        </div>
      </div>

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

        {/* Stats Cards Row */}
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
              of {problems.length} problems
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
              {problems.filter(p => p.difficulty === 'easy' && solvedProblems.includes(p.id)).length}
            </div>
            <div style={{ fontSize: '12px', color: '#CBD5E1', marginTop: '4px' }}>
              of {problems.filter(p => p.difficulty === 'easy').length}
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
              {problems.filter(p => p.difficulty === 'medium' && solvedProblems.includes(p.id)).length}
            </div>
            <div style={{ fontSize: '12px', color: '#CBD5E1', marginTop: '4px' }}>
              of {problems.filter(p => p.difficulty === 'medium').length}
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
              {problems.filter(p => p.difficulty === 'hard' && solvedProblems.includes(p.id)).length}
            </div>
            <div style={{ fontSize: '12px', color: '#CBD5E1', marginTop: '4px' }}>
              of {problems.filter(p => p.difficulty === 'hard').length}
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
                <ProblemCell problem={p} solvedProblems={solvedProblems} />
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

        {/* Problems List */}
        <div style={{ marginTop: '60px' }}>
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
              gridTemplateColumns: '40px 60px 1fr 150px 120px',
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
              <div></div>
              <div>#</div>
              <div>Title</div>
              <div>Tags</div>
              <div style={{ textAlign: 'right' }}>Difficulty</div>
            </div>

            {/* Table Rows */}
            {problems.map((p) => {
              const isHidden = filter !== 'all' && p.difficulty !== filter;
              const isSolved = solvedProblems.includes(p.id);

              if (isHidden) return null;

              return (
                <Link
                  key={p.id}
                  to={`/problems/${p.slug}`}
                  style={{
                    display: 'grid',
                    gridTemplateColumns: '40px 60px 1fr 150px 120px',
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
                >
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
            })}
          </div>
        </div>
      </div>

      {/* Pagination */}
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
