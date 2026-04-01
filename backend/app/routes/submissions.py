from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Submission, Problem
from app.services.runner import run_submission

submissions_bp = Blueprint("submissions", __name__)


@submissions_bp.post("/")
@jwt_required()
def submit():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    problem = Problem.query.filter_by(slug=data.get("problemSlug")).first_or_404()
    sub = Submission(
        user_id=user_id,
        problem_id=problem.id,
        code=data["code"],
        total_tests=len(problem.test_cases),
    )
    db.session.add(sub)
    db.session.commit()
    task = run_submission.delay(sub.id)
    sub.task_id = task.id
    db.session.commit()
    return jsonify(id=sub.id, taskId=task.id, status="pending"), 202


@submissions_bp.get("/<int:sub_id>")
@jwt_required()
def get_submission(sub_id):
    user_id = int(get_jwt_identity())
    sub = Submission.query.get_or_404(sub_id)
    if sub.user_id != user_id:
        return jsonify(error="Forbidden"), 403
    return jsonify(
        id=sub.id,
        status=sub.status,
        passedTests=sub.passed_tests,
        totalTests=sub.total_tests,
        runtimeMs=sub.runtime_ms,
        memoryKb=sub.memory_kb,
        errorOutput=sub.error_output,
        createdAt=sub.created_at.isoformat(),
    )


@submissions_bp.get("/problem/<slug>")
@jwt_required()
def submissions_for_problem(slug):
    user_id = int(get_jwt_identity())
    problem = Problem.query.filter_by(slug=slug).first_or_404()
    subs = (
        Submission.query.filter_by(user_id=user_id, problem_id=problem.id)
        .order_by(Submission.created_at.desc())
        .limit(20)
        .all()
    )
    return jsonify([
        {
            "id": s.id,
            "status": s.status,
            "passedTests": s.passed_tests,
            "totalTests": s.total_tests,
            "runtimeMs": s.runtime_ms,
            "createdAt": s.created_at.isoformat(),
        }
        for s in subs
    ])
