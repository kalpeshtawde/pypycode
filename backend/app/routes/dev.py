import os
from flask import Blueprint, jsonify
from app.models import Problem, ProblemSolution

dev_bp = Blueprint("dev", __name__)


def _dev_enabled() -> bool:
    return os.environ.get("DEV_ENDPOINTS_ENABLED", "false").lower() == "true"


@dev_bp.get("/problem-solutions")
def problem_solutions():
    """Return all active problem solutions. Local dev only (DEV_ENDPOINTS_ENABLED=true)."""
    if not _dev_enabled():
        return jsonify(error="Not found"), 404

    rows = (
        Problem.query
        .join(ProblemSolution, ProblemSolution.problem_id == Problem.id)
        .filter(ProblemSolution.is_active.is_(True))
        .with_entities(
            Problem.slug,
            Problem.title,
            Problem.difficulty,
            ProblemSolution.code,
        )
        .all()
    )

    return jsonify([
        {
            "slug": slug,
            "title": title,
            "difficulty": difficulty,
            "solutionCode": code,
        }
        for slug, title, difficulty, code in rows
    ])
