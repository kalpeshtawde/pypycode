from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Submission, Problem
from app.services.runner import run_submission

submissions_bp = Blueprint("submissions", __name__)


@submissions_bp.post("/")
@jwt_required()
def submit():
    user_id = get_jwt_identity()
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
    print(f"Queuing submission {sub.id} with task")
    task = run_submission.delay(sub.id)
    print(f"Task queued: {task.id}")
    sub.task_id = task.id
    db.session.commit()
    return jsonify(id=sub.id, taskId=task.id, status="pending"), 202


@submissions_bp.get("/<sub_id>")
@jwt_required()
def get_submission(sub_id):
    user_id = get_jwt_identity()
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


@submissions_bp.get("/all")
@jwt_required()
def get_all_submissions():
    user_id = get_jwt_identity()
    subs = (
        Submission.query.filter_by(user_id=user_id)
        .order_by(Submission.created_at.desc())
        .all()
    )
    return jsonify([
        {
            "id": s.id,
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
            "code": s.code,
            "createdAt": s.created_at.isoformat(),
        }
        for s in subs
    ])
