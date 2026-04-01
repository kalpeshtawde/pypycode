from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Problem, Submission
from app import db

problems_bp = Blueprint("problems", __name__)


def problem_to_dict(p: Problem, hide_tests=True):
    return {
        "id": p.id,
        "slug": p.slug,
        "title": p.title,
        "difficulty": p.difficulty,
        "description": p.description,
        "starterCode": p.starter_code,
        "examples": p.examples,
        "tags": p.tags or [],
        "createdAt": p.created_at.isoformat(),
    }


@problems_bp.get("/")
def list_problems():
    difficulty = request.args.get("difficulty")
    tag = request.args.get("tag")
    q = Problem.query
    if difficulty:
        q = q.filter_by(difficulty=difficulty)
    if tag:
        q = q.filter(Problem.tags.contains([tag]))
    problems = q.order_by(Problem.id).all()
    return jsonify([problem_to_dict(p) for p in problems])


@problems_bp.get("/<slug>")
def get_problem(slug):
    p = Problem.query.filter_by(slug=slug).first_or_404()
    return jsonify(problem_to_dict(p))


@problems_bp.post("/")
@jwt_required()
def create_problem():
    data = request.get_json()
    p = Problem(
        slug=data["slug"],
        title=data["title"],
        difficulty=data["difficulty"],
        description=data["description"],
        starter_code=data["starterCode"],
        test_cases=data["testCases"],
        examples=data["examples"],
        tags=data.get("tags", []),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(problem_to_dict(p)), 201
