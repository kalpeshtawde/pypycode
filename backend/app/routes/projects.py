import asyncio
import logging
import os

import requests

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
)

from app import db
from app.models import Project, Submission, Problem, ProblemProjectStat
from app.services.runner import run_submission


projects_bp = Blueprint("projects", __name__)
logger = logging.getLogger(__name__)
MAX_PROJECT_NAME_LENGTH = 80
MAX_GOAL_LENGTH = 500
MAX_STRATEGY_LENGTH = 32
MAX_LEVEL_LENGTH = 16
MAX_PROMPT_LENGTH = 500
DEFAULT_AI_PROJECT_TOTAL = 20
MAX_AI_PROJECT_TOTAL = 50
MIN_AI_PROJECT_TOTAL = 5


def _ensure_problem_project_stat(user_id: str, problem_id: str, project_id: str):
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
        )
        db.session.add(stat)
    return stat


def _upsert_problem_project_stat(user_id: str, problem_id: str, project_id: str):
    stat = _ensure_problem_project_stat(user_id, problem_id, project_id)
    if not stat.attempted:
        stat.attempted = True
    if not stat.submitted:
        stat.submitted = True


def _normalize_problem_ids(value):
    if value is None:
        return None
    if not isinstance(value, list):
        return []
    normalized = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            return []
        normalized.append(item.strip())
    return normalized


def project_to_dict(project: Project):
    return {
        "id": project.id,
        "name": project.name,
        "isDefault": project.is_default,
        "createdAt": project.created_at.isoformat() if project.created_at else None,
        "goal": project.goal,
        "strategy": project.strategy,
        "level": project.level,
        "explanation": project.explanation,
        "aiMetadata": project.ai_metadata,
    }


@projects_bp.get("/")
@jwt_required()
def list_projects():
    user_id = get_jwt_identity()
    projects = (
        Project.query.filter_by(user_id=user_id)
        .order_by(Project.is_default.desc(), Project.created_at.asc())
        .all()
    )
    return jsonify([project_to_dict(project) for project in projects])


@projects_bp.post("/")
@jwt_required()
def create_project():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    provided_problem_ids = _normalize_problem_ids(data.get("problemIds"))

    # Optional AI-authored metadata (set by the Vega agent).
    goal = (data.get("goal") or "").strip() or None
    strategy = (data.get("strategy") or "").strip() or None
    level = (data.get("level") or "").strip() or None
    explanation = (data.get("explanation") or "").strip() or None
    ai_metadata = data.get("aiMetadata")
    if ai_metadata is not None and not isinstance(ai_metadata, dict):
        return jsonify(error="aiMetadata must be an object"), 400

    if not name:
        return jsonify(error="Project name is required"), 400
    if len(name) > MAX_PROJECT_NAME_LENGTH:
        return jsonify(error=f"Project name must be at most {MAX_PROJECT_NAME_LENGTH} characters"), 400
    if goal and len(goal) > MAX_GOAL_LENGTH:
        return jsonify(error=f"goal must be at most {MAX_GOAL_LENGTH} characters"), 400
    if strategy and len(strategy) > MAX_STRATEGY_LENGTH:
        return jsonify(error=f"strategy must be at most {MAX_STRATEGY_LENGTH} characters"), 400
    if level and len(level) > MAX_LEVEL_LENGTH:
        return jsonify(error=f"level must be at most {MAX_LEVEL_LENGTH} characters"), 400
    if data.get("problemIds") is not None and provided_problem_ids == []:
        return jsonify(error="problemIds must be an array of non-empty strings"), 400

    existing = Project.query.filter_by(user_id=user_id, name=name).first()
    if existing:
        return jsonify(error="Project name already exists"), 409

    if provided_problem_ids is None:
        selected_problems = Problem.query.order_by(Problem.created_at.desc(), Problem.id.asc()).all()
    else:
        deduped_problem_ids = list(dict.fromkeys(provided_problem_ids))
        selected_problems = Problem.query.filter(Problem.id.in_(deduped_problem_ids)).all()
        found_problem_ids = {problem.id for problem in selected_problems}
        missing_problem_ids = [problem_id for problem_id in deduped_problem_ids if problem_id not in found_problem_ids]
        if missing_problem_ids:
            return jsonify(error="Some problemIds were not found", missingProblemIds=missing_problem_ids), 400

    has_projects = Project.query.filter_by(user_id=user_id).first() is not None
    project = Project(
        user_id=user_id,
        name=name,
        is_default=not has_projects,
        goal=goal,
        strategy=strategy,
        level=level,
        explanation=explanation,
        ai_metadata=ai_metadata,
    )
    db.session.add(project)
    db.session.flush()

    for problem in selected_problems:
        _ensure_problem_project_stat(user_id, problem.id, project.id)

    db.session.commit()

    return jsonify(project_to_dict(project)), 201


@projects_bp.post("/from-prompt")
@jwt_required()
def create_project_from_prompt():
    """Create a project by invoking the Vega agent with a user-supplied prompt.

    Vega itself talks to this backend over HTTP for stats and persistence
    (loop-back via a freshly minted JWT for the calling user), so this
    handler just orchestrates: validate input → mint token → run graph →
    return the resulting project + agent metadata.
    """
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    prompt = (data.get("prompt") or "").strip()
    requested_total = data.get("total")

    if not prompt:
        return jsonify(error="prompt is required"), 400
    if len(prompt) > MAX_PROMPT_LENGTH:
        return jsonify(error=f"prompt must be at most {MAX_PROMPT_LENGTH} characters"), 400

    total = DEFAULT_AI_PROJECT_TOTAL
    if requested_total is not None:
        if not isinstance(requested_total, int) or isinstance(requested_total, bool):
            return jsonify(error="total must be an integer"), 400
        if requested_total < MIN_AI_PROJECT_TOTAL or requested_total > MAX_AI_PROJECT_TOTAL:
            return jsonify(
                error=f"total must be between {MIN_AI_PROJECT_TOTAL} and {MAX_AI_PROJECT_TOTAL}",
            ), 400
        total = requested_total

    # Mint a short-lived JWT so Vega's BackendClient can call back as this user.
    auth_token = create_access_token(identity=user_id)

    # Call Vega service via HTTP
    vega_service_url = os.environ.get("VEGA_SERVICE_URL", "http://vega:5001")
    
    try:
        response = requests.post(
            f"{vega_service_url}/generate",
            json={
                "prompt": prompt,
                "problem_count": total,
                "auth_token": auth_token,
                "user_id": user_id,
            },
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        logger.exception("Vega service call failed")
        return jsonify(error=f"Project generation failed: {exc}"), 503

    project = result.get("project") or {}
    project_id = result.get("project_id") or project.get("id")

    if not project_id:
        # Persistence failed inside the graph (fail-soft path) — surface to caller.
        return jsonify(
            error=project.get("persistence_error") or "Project was generated but not saved",
            agent=project,
        ), 502

    saved = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not saved:
        return jsonify(error="Project was created but could not be loaded"), 500

    return jsonify(project_to_dict(saved)), 201


@projects_bp.post("/<project_id>/update-from-prompt")
@jwt_required()
def update_project_from_prompt(project_id):
    """Add more problems to an existing project using the Vega agent."""
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify(error="Project not found"), 404

    data = request.get_json() or {}
    prompt = (data.get("prompt") or "").strip()
    requested_total = data.get("total")

    if not prompt:
        return jsonify(error="prompt is required"), 400
    if len(prompt) > MAX_PROMPT_LENGTH:
        return jsonify(error=f"prompt must be at most {MAX_PROMPT_LENGTH} characters"), 400

    total = DEFAULT_AI_PROJECT_TOTAL
    if requested_total is not None:
        if not isinstance(requested_total, int) or isinstance(requested_total, bool):
            return jsonify(error="total must be an integer"), 400
        if requested_total < MIN_AI_PROJECT_TOTAL or requested_total > MAX_AI_PROJECT_TOTAL:
            return jsonify(
                error=f"total must be between {MIN_AI_PROJECT_TOTAL} and {MAX_AI_PROJECT_TOTAL}",
            ), 400
        total = requested_total

    auth_token = create_access_token(identity=user_id)
    vega_service_url = os.environ.get("VEGA_SERVICE_URL", "http://vega:5001")

    try:
        response = requests.post(
            f"{vega_service_url}/generate",
            json={
                "prompt": prompt,
                "problem_count": total,
                "auth_token": auth_token,
                "user_id": user_id,
                "project_id": project_id,
            },
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        logger.exception("Vega service call failed")
        return jsonify(error=f"Project update failed: {exc}"), 503

    project_result = result.get("project") or {}
    if project_result.get("persistence_error"):
        return jsonify(error=project_result["persistence_error"]), 502

    saved = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not saved:
        return jsonify(error="Project could not be loaded after update"), 500

    return jsonify(project_to_dict(saved)), 200


@projects_bp.post("/parse-message")
@jwt_required()
def parse_prompt_message():
    """Proxy to Vega's /parse-message: classifies intent and extracts total in one LLM call."""
    data = request.get_json() or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify(intent="unclear", total=None), 200

    vega_service_url = os.environ.get("VEGA_SERVICE_URL", "http://vega:5001")
    try:
        response = requests.post(
            f"{vega_service_url}/parse-message",
            json={
                "prompt": prompt,
                "has_existing_project": data.get("has_existing_project", False),
                "project_name": data.get("project_name", ""),
            },
            timeout=15,
        )
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.RequestException:
        return jsonify(intent="unclear", total=None), 200


@projects_bp.post("/extract-intent")
@jwt_required()
def extract_prompt_intent():
    """Proxy to Vega's /extract-intent to parse problem count from a user prompt."""
    data = request.get_json() or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify(total=None), 200

    vega_service_url = os.environ.get("VEGA_SERVICE_URL", "http://vega:5001")
    try:
        response = requests.post(
            f"{vega_service_url}/extract-intent",
            json={"prompt": prompt},
            timeout=15,
        )
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.RequestException:
        return jsonify(total=None), 200


@projects_bp.post("/<project_id>/set-default")
@jwt_required()
def set_default_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify(error="Project not found"), 404

    Project.query.filter_by(user_id=user_id).update({"is_default": False})
    project.is_default = True
    db.session.commit()

    return jsonify(project_to_dict(project)), 200
 

@projects_bp.get("/<project_id>/problems")
@jwt_required()
def get_project_problems(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify(error="Project not found"), 404

    problems = (
        db.session.query(Problem)
        .join(ProblemProjectStat, ProblemProjectStat.problem_id == Problem.id)
        .filter(
            ProblemProjectStat.project_id == project_id,
            ProblemProjectStat.user_id == user_id,
        )
        .all()
    )

    return jsonify([
        {"id": p.id, "slug": p.slug, "title": p.title}
        for p in problems
    ])


@projects_bp.put("/<project_id>")
@jwt_required()
def update_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify(error="Project not found"), 404

    data = request.get_json() or {}
    problem_ids = data.get("problemIds", [])

    existing_ids = {
        stat.problem_id
        for stat in ProblemProjectStat.query.filter_by(
            user_id=user_id, project_id=project_id
        ).all()
    }

    for pid in problem_ids:
        if pid not in existing_ids:
            db.session.add(ProblemProjectStat(
                user_id=user_id,
                problem_id=pid,
                project_id=project_id,
            ))

    db.session.commit()

    return jsonify(project_to_dict(project)), 200


@projects_bp.delete("/<project_id>")
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify(error="Project not found"), 404

    was_default = project.is_default
    deleted_submissions = Submission.query.filter_by(
        user_id=user_id,
        project_id=project.id,
    ).delete(synchronize_session=False)
    ProblemProjectStat.query.filter_by(
        user_id=user_id,
        project_id=project.id,
    ).delete(synchronize_session=False)
    db.session.delete(project)
    db.session.flush()

    if was_default:
        next_project = (
            Project.query.filter_by(user_id=user_id)
            .order_by(Project.created_at.asc())
            .first()
        )
        if next_project:
            next_project.is_default = True

    db.session.commit()

    return jsonify(
        deletedProjectId=project_id,
        deletedSubmissions=deleted_submissions,
    ), 200


@projects_bp.post("/<project_id>/submit")
@jwt_required()
def submit_to_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify(error="Project not found"), 404

    data = request.get_json() or {}
    problem_slug = data.get("problemSlug") or data.get("problem_slug")
    problem = Problem.query.filter_by(slug=problem_slug).first_or_404()

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
    _upsert_problem_project_stat(user_id, problem.id, project.id)
    db.session.commit()

    task = run_submission.delay(sub.id)
    sub.task_id = task.id
    db.session.commit()
    return jsonify(id=sub.id, taskId=task.id, status="pending"), 202
