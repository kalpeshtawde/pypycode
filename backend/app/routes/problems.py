import hmac
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Problem, Submission, TestCase
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


def _require_non_empty_string(data: dict, field: str):
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def _validate_examples(examples):
    if not isinstance(examples, list) or not examples:
        return False

    for example in examples:
        if not isinstance(example, dict):
            return False
        if not isinstance(example.get("input"), str) or not isinstance(example.get("output"), str):
            return False
        if "explanation" in example and not isinstance(example.get("explanation"), str):
            return False

    return True


def _validate_test_cases(test_cases):
    if not isinstance(test_cases, list) or not test_cases:
        return False

    for test_case in test_cases:
        if not isinstance(test_case, dict):
            return False
        # New format: function, input, expectedOutput
        if "expectedOutput" not in test_case:
            return False
        if "input" not in test_case:
            return False
        if "function" not in test_case or not isinstance(test_case.get("function"), str):
            return False

    return True


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


@problems_bp.post("/public-ingest")
def public_ingest_problem():
    data = request.get_json() or {}

    expected_key = current_app.config.get("PROBLEM_INGEST_KEY")
    provided_key = data.get("ingestKey")

    if not expected_key:
        return jsonify(error="Problem ingest key is not configured on server"), 503

    if not isinstance(provided_key, str) or not hmac.compare_digest(provided_key, expected_key):
        return jsonify(error="Invalid ingest key"), 403

    slug = _require_non_empty_string(data, "slug")
    title = _require_non_empty_string(data, "title")
    difficulty = _require_non_empty_string(data, "difficulty")
    description = _require_non_empty_string(data, "description")
    starter_code = _require_non_empty_string(data, "starterCode")
    examples = data.get("examples")
    test_cases = data.get("testCases")
    tags = data.get("tags", [])

    if not slug or not title or not difficulty or not description or not starter_code:
        return jsonify(error="slug, title, difficulty, description, and starterCode are required"), 400

    difficulty = difficulty.lower()
    if difficulty not in {"easy", "medium", "hard"}:
        return jsonify(error="difficulty must be one of: easy, medium, hard"), 400

    if not _validate_examples(examples):
        return jsonify(error="examples must be a non-empty array of {input, output, explanation?}"), 400

    if not _validate_test_cases(test_cases):
        return jsonify(error="testCases must be a non-empty array with expected and input or args"), 400

    if tags is None:
        tags = []
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        return jsonify(error="tags must be an array of strings"), 400

    if Problem.query.filter_by(slug=slug).first():
        return jsonify(error="Problem slug already exists"), 409

    problem = Problem(
        slug=slug,
        title=title,
        difficulty=difficulty,
        description=description,
        starter_code=starter_code,
        examples=examples,
        tags=tags,
    )
    db.session.add(problem)
    db.session.flush()  # Get problem.id before committing

    # Create test cases as separate records
    for idx, tc in enumerate(test_cases):
        test_case = TestCase(
            problem_id=problem.id,
            serial_number=idx,
            function=tc.get("function", "solution"),
            input=tc.get("input", ""),
            expected_output=tc.get("expectedOutput", ""),
            is_active=tc.get("isActive", True),
        )
        db.session.add(test_case)

    db.session.commit()

    return jsonify(problem_to_dict(problem)), 201


@problems_bp.get("/<slug>")
def get_problem(slug):
    p = Problem.query.filter_by(slug=slug).first_or_404()
    return jsonify(problem_to_dict(p))


@problems_bp.post("/")
@jwt_required()
def create_problem():
    data = request.get_json()
    test_cases_data = data.get("testCases", [])
    
    p = Problem(
        slug=data["slug"],
        title=data["title"],
        difficulty=data["difficulty"],
        description=data["description"],
        starter_code=data["starterCode"],
        examples=data["examples"],
        tags=data.get("tags", []),
    )
    db.session.add(p)
    db.session.flush()
    
    # Create test cases
    for idx, tc in enumerate(test_cases_data):
        test_case = TestCase(
            problem_id=p.id,
            serial_number=idx,
            function=tc.get("function", "solution"),
            input=tc.get("input", ""),
            expected_output=tc.get("expectedOutput", ""),
            is_active=tc.get("isActive", True),
        )
        db.session.add(test_case)
    
    db.session.commit()
    return jsonify(problem_to_dict(p)), 201
