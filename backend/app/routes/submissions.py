from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from celery.exceptions import TimeoutError as CeleryTimeoutError, NotRegistered
from app import db
from app.models import Submission, Problem, Project, ProblemProjectStat, User
from app.services.runner import run_submission, run_code_for_problem

submissions_bp = Blueprint("submissions", __name__)


def _resolve_user_project(user_id: str, project_id=None):
    if project_id:
        return Project.query.filter_by(id=project_id, user_id=user_id).first()
    return (
        Project.query.filter_by(user_id=user_id, is_default=True)
        .order_by(Project.created_at.asc())
        .first()
    )


def _upsert_problem_project_stat(user_id: str, problem_id: str, project_id: str, *, attempted=False, submitted=False):
    stat = ProblemProjectStat.query.filter_by(
        user_id=user_id,
        problem_id=problem_id,
        project_id=project_id,
    ).first()
    if not stat:
        stat = ProblemProjectStat(
            user_id=user_id,
            problem_id=problem_id,
            project_id=project_id,
            attempted=attempted,
            submitted=submitted,
        )
        db.session.add(stat)
        return

    if attempted and not stat.attempted:
        stat.attempted = True
    if submitted and not stat.submitted:
        stat.submitted = True


@submissions_bp.post("/run")
@jwt_required()
def run_code():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    problem = Problem.query.filter_by(slug=data.get("problemSlug")).first_or_404()

    project = _resolve_user_project(user_id, data.get("projectId"))
    if not project:
        return jsonify(error="Project not found"), 404

    code = data.get("code")
    if not isinstance(code, str) or not code.strip():
        return jsonify(error="Code is required"), 400

    _upsert_problem_project_stat(
        user_id=user_id,
        problem_id=problem.id,
        project_id=project.id,
        attempted=True,
    )
    db.session.commit()

    task = run_code_for_problem.delay(problem.id, code)
    try:
        result = task.get(timeout=15)
    except NotRegistered:
        return jsonify(error="Run worker task is not registered. Restart celery worker."), 503
    except CeleryTimeoutError:
        return jsonify(
            status="time_limit",
            passedTests=0,
            totalTests=len(problem.test_cases),
            runtimeMs=None,
            memoryKb=None,
            errorOutput=None,
        )

    return jsonify(
        status=result["status"],
        passedTests=result["passed_tests"],
        totalTests=result["total_tests"],
        runtimeMs=result["runtime_ms"],
        memoryKb=result["memory_kb"],
        errorOutput=result["error_output"],
    )


@submissions_bp.post("/")
@jwt_required()
def submit():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    problem = Problem.query.filter_by(slug=data.get("problemSlug")).first_or_404()
    project_id = data.get("projectId")
    if not project_id:
        return jsonify(error="Project is required"), 400

    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify(error="Project not found"), 404

    code = data.get("code")
    if not isinstance(code, str) or not code.strip():
        return jsonify(error="Code is required"), 400

    sub = Submission(
        user_id=user_id,
        project_id=project.id,
        problem_id=problem.id,
        code=code,
        total_tests=len(problem.test_cases),
    )
    db.session.add(sub)
    _upsert_problem_project_stat(
        user_id=user_id,
        problem_id=problem.id,
        project_id=project.id,
        attempted=True,
        submitted=True,
    )
    db.session.commit()
    print(f"Queuing submission {sub.id} with task")
    task = run_submission.delay(sub.id)
    print(f"Task queued: {task.id}")
    sub.task_id = task.id
    db.session.commit()
    return jsonify(id=sub.id, taskId=task.id, status="pending"), 202


@submissions_bp.get("/difficulty-stats")
@jwt_required()
def difficulty_stats():
    requested_user_id = request.args.get("userId") or get_jwt_identity()
    user = User.query.filter_by(id=requested_user_id).first()
    if not user:
        return jsonify(error="User not found"), 404

    rows = (
        db.session.query(
            Problem.difficulty.label("difficulty"),
            db.func.max(db.case((ProblemProjectStat.attempted.is_(True), 1), else_=0)).label("attempted_flag"),
            db.func.max(db.case((ProblemProjectStat.submitted.is_(True), 1), else_=0)).label("submitted_flag"),
        )
        .join(Problem, Problem.id == ProblemProjectStat.problem_id)
        .filter(ProblemProjectStat.user_id == requested_user_id)
        .group_by(ProblemProjectStat.problem_id, Problem.difficulty)
        .all()
    )

    stats = {
        "easy": {"attempted": 0, "submitted": 0, "score": 0.0},
        "medium": {"attempted": 0, "submitted": 0, "score": 0.0},
        "hard": {"attempted": 0, "submitted": 0, "score": 0.0},
    }

    for row in rows:
        level = (row.difficulty or "").lower()
        if level not in stats:
            continue
        stats[level]["attempted"] += int(row.attempted_flag or 0)
        stats[level]["submitted"] += int(row.submitted_flag or 0)

    for level in stats:
        attempted = stats[level]["attempted"]
        submitted = stats[level]["submitted"]
        stats[level]["score"] = round((submitted / attempted), 4) if attempted > 0 else 0.0

    last_attempt_at = (
        db.session.query(db.func.max(ProblemProjectStat.updated_at))
        .filter(
            ProblemProjectStat.user_id == requested_user_id,
            ProblemProjectStat.attempted.is_(True),
        )
        .scalar()
    )

    return jsonify(
        lastAttemptAt=last_attempt_at.isoformat() if last_attempt_at else None,
        **stats,
    )


@submissions_bp.get("/<sub_id>")
@jwt_required()
def get_submission(sub_id):
    user_id = get_jwt_identity()
    sub = Submission.query.get_or_404(sub_id)
    if sub.user_id != user_id:
        return jsonify(error="Forbidden"), 403
    return jsonify(
        id=sub.id,
        projectId=sub.project_id,
        status=sub.status,
        passedTests=sub.passed_tests,
        totalTests=sub.total_tests,
        runtimeMs=sub.runtime_ms,
        memoryKb=sub.memory_kb,
        errorOutput=sub.error_output,
        createdAt=sub.created_at.isoformat(),
    )


@submissions_bp.get("/all")
@jwt_required()
def get_all_submissions():
    user_id = get_jwt_identity()
    project_id = request.args.get("projectId")
    query = Submission.query.filter_by(user_id=user_id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    subs = query.order_by(Submission.created_at.desc()).all()
    return jsonify([
        {
            "id": s.id,
            "projectId": s.project_id,
            "problemId": s.problem_id,
            "status": s.status,
            "createdAt": s.created_at.isoformat(),
        }
        for s in subs
    ])


@submissions_bp.get("/accepted")
@jwt_required()
def get_accepted_submissions():
    user_id = get_jwt_identity()
    subs = (
        Submission.query.filter_by(user_id=user_id, status="accepted")
        .all()
    )
    return jsonify([
        {
            "id": s.id,
            "projectId": s.project_id,
            "problemId": s.problem_id,
            "status": s.status,
            "createdAt": s.created_at.isoformat(),
        }
        for s in subs
    ])


@submissions_bp.get("/problem/<slug>")
@jwt_required()
def submissions_for_problem(slug):
    user_id = get_jwt_identity()
    problem = Problem.query.filter_by(slug=slug).first_or_404()
    project_id = request.args.get("projectId")
    query = Submission.query.filter_by(user_id=user_id, problem_id=problem.id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    subs = query.order_by(Submission.created_at.desc()).limit(20).all()
    return jsonify([
        {
            "id": s.id,
            "projectId": s.project_id,
            "status": s.status,
            "passedTests": s.passed_tests,
            "totalTests": s.total_tests,
            "runtimeMs": s.runtime_ms,
            "code": s.code,
            "createdAt": s.created_at.isoformat(),
        }
        for s in subs
    ])
