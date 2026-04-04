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
    sort_by = request.args.get("sort", "id")  # id, difficulty, created_at
    order = request.args.get("order", "asc")  # asc, desc
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 15, type=int), 50)  # max 50 per page
    
    q = Problem.query
    
    # Apply filters
    if difficulty:
        q = q.filter_by(difficulty=difficulty)
    if tag:
        q = q.filter(Problem.tags.contains([tag]))
    
    # Apply sorting
    if sort_by == "difficulty":
        if order == "desc":
            q = q.order_by(db.case(
                (Problem.difficulty == "hard", 3),
                (Problem.difficulty == "medium", 2),
                (Problem.difficulty == "easy", 1),
                else_=0
            ).desc())
        else:
            q = q.order_by(db.case(
                (Problem.difficulty == "easy", 1),
                (Problem.difficulty == "medium", 2),
                (Problem.difficulty == "hard", 3),
                else_=4
            ).asc())
    elif sort_by == "created_at":
        if order == "desc":
            q = q.order_by(Problem.created_at.desc())
        else:
            q = q.order_by(Problem.created_at.asc())
    else:  # default sort by id
        if order == "desc":
            q = q.order_by(Problem.id.desc())
        else:
            q = q.order_by(Problem.id.asc())
    
    # Apply pagination
    pagination = q.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        "problems": [problem_to_dict(p) for p in pagination.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_prev": pagination.has_prev,
            "has_next": pagination.has_next,
            "prev_num": pagination.prev_num,
            "next_num": pagination.next_num
        }
    })


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
