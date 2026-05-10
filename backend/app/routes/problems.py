import hmac
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from app.models import Problem, ProblemProjectStat, Submission, TestCase
from app import db
from collections import defaultdict


problems_bp = Blueprint("problems", __name__)


def _derive_arg_types(tags: list, input_str: str) -> list | None:
    """Return arg_types list based on problem tags, or None for plain problems."""
    import ast as _ast, json as _json
    lower_tags = [t.lower() for t in (tags or [])]
    if any(t in {"tree", "binary-tree"} for t in lower_tags):
        first = "tree"
    elif "linked-list" in lower_tags:
        first = "linked_list"
    else:
        return None
    # Count args to build the full list
    n = 1
    if input_str:
        try:
            n = len(_json.loads("[" + input_str + "]"))
        except Exception:
            try:
                n = len(_ast.literal_eval("[" + input_str + "]"))
            except Exception:
                pass
    return [first] + [None] * max(0, n - 1)

# Structural/data-shape tags. These describe the input/output container of a
# problem and are not algorithmic techniques. They are excluded from scoring,
# ranking and quota enforcement so high-frequency tags like "array" cannot
# dominate selection. They are still preserved on the problem and reported in
# logging/metadata.
STRUCTURAL_TAGS = frozenset({
    "array",
    "string",
    "matrix",
    "stack",
    "list",
})

# Lightweight problem-pattern catalog used for secondary diversity.
# Each entry maps a normalized keyword that may appear in the slug or title to
# a coarse "pattern" bucket. The first match wins; problems that match nothing
# fall back to PATTERN_DEFAULT. The catalog is intentionally small and
# heuristic — it only needs to separate common templates so we can cap
# repeats per (algorithmic tag, pattern) pair during selection.
PATTERN_DEFAULT = "misc"

# Tag-combination rules. Each entry is (required_tags, pattern); the first rule
# whose `required_tags` is a subset of the problem's full tag set (algorithmic
# + structural) wins. More specific rules (more required tags) are listed
# first so they win over more general ones. These run BEFORE slug-keyword
# matching so explicit tag combinations dominate naming.
TAG_PATTERN_RULES = (
    # multi-tag (specific) rules first
    (frozenset({"matrix", "dfs"}), "grid"),
    (frozenset({"matrix", "bfs"}), "grid"),
    (frozenset({"matrix", "backtracking"}), "grid"),
    (frozenset({"graph", "eulerian-path"}), "eulerian"),
    (frozenset({"graph", "topological-sort"}), "topological"),
    (frozenset({"graph", "union-find"}), "union-find"),
    (frozenset({"graph", "dijkstra"}), "shortest-path"),
    (frozenset({"graph", "bellman-ford"}), "shortest-path"),
    (frozenset({"graph", "floyd-warshall"}), "shortest-path"),
    (frozenset({"graph", "dfs"}), "graph-traversal"),
    (frozenset({"graph", "bfs"}), "graph-traversal"),
    (frozenset({"trie", "dfs"}), "trie"),
    (frozenset({"greedy", "interval"}), "interval"),
    (frozenset({"dp", "knapsack"}), "knapsack"),
    (frozenset({"dynamic-programming", "knapsack"}), "knapsack"),
    (frozenset({"heap", "kth-element"}), "kth-element"),
    (frozenset({"priority-queue", "kth-element"}), "kth-element"),
    # single-tag (general) rules — last-resort algorithmic mapping
    (frozenset({"sliding-window"}), "sliding-window"),
    (frozenset({"two-pointers"}), "two-pointers"),
    (frozenset({"monotonic-stack"}), "monotonic-stack"),
    (frozenset({"binary-search"}), "binary-search"),
    (frozenset({"trie"}), "trie"),
    (frozenset({"union-find"}), "union-find"),
    (frozenset({"heap"}), "heap"),
    (frozenset({"priority-queue"}), "heap"),
    (frozenset({"bit-manipulation"}), "bit-manipulation"),
)

PATTERN_KEYWORDS = (
    ("subset", "subset"),
    ("permutation", "permutation"),
    ("permute", "permutation"),
    ("combination", "combination"),
    ("combinations", "combination"),
    ("partition", "partition"),
    ("palindrom", "palindrome"),
    ("anagram", "anagram"),
    ("parenthes", "parentheses"),
    ("bracket", "parentheses"),
    ("sliding-window", "sliding-window"),
    ("substring", "substring-window"),
    ("subarray", "subarray-window"),
    ("two-sum", "k-sum"),
    ("three-sum", "k-sum"),
    ("k-sum", "k-sum"),
    ("kth", "kth-element"),
    ("merge", "merge"),
    ("interval", "interval"),
    ("schedule", "interval"),
    ("island", "grid"),
    ("grid", "grid"),
    ("rotate", "grid"),
    ("course", "graph"),
    ("clone", "graph"),
    ("topological", "topological"),
    ("traversal", "tree"),
    ("ancestor", "tree"),
    ("linked", "linked-list"),
    ("cycle", "linked-list"),
    ("prefix", "trie"),
    ("dijkstra", "shortest-path"),
    ("shortest", "shortest-path"),
    ("knapsack", "knapsack"),
    ("coin", "knapsack"),
    ("stock", "stock"),
    ("rob", "house-robber"),
    ("longest", "longest-sequence"),
    ("buy-sell", "stock"),
)


def _primary_algo_tag(algo_tags, algo_tag_weights=None):
    """Pick the dominant algorithmic tag for fallback pattern naming.

    If `algo_tag_weights` are provided, prefer the tag with the highest
    weight; ties break alphabetically. Without weights, fall back to the
    alphabetically first tag for determinism.
    """
    if not algo_tags:
        return None
    if algo_tag_weights:
        return min(
            algo_tags,
            key=lambda tag: (-algo_tag_weights.get(tag, 0.0), tag),
        )
    return min(algo_tags)


def _extract_problem_pattern(slug, title=None, tags=None, primary_algo_tag=None):
    """Return a coarse pattern bucket for a problem.

    Priority:
      1. Tag-combination rules (TAG_PATTERN_RULES).
      2. Slug/title keyword match (PATTERN_KEYWORDS).
      3. `<primary_algo_tag>-general` fallback so every problem with an
         algorithmic tag has a meaningful bucket instead of "misc".
      4. PATTERN_DEFAULT only if the problem has no algorithmic tags at
         all and no slug/title keyword match.
    """
    tag_set = frozenset(tags or [])
    if tag_set:
        for required, pattern in TAG_PATTERN_RULES:
            if required <= tag_set:
                return pattern

    haystack_parts = []
    if isinstance(slug, str) and slug.strip():
        haystack_parts.append(slug.strip().lower())
    if isinstance(title, str) and title.strip():
        haystack_parts.append(title.strip().lower())
    haystack = " ".join(haystack_parts)
    if haystack:
        for keyword, pattern in PATTERN_KEYWORDS:
            if keyword in haystack:
                return pattern

    if primary_algo_tag:
        return f"{primary_algo_tag}-general"

    return PATTERN_DEFAULT


def problem_to_dict(p: Problem, hide_tests=True):
    data = {
        "id": p.id,
        "slug": p.slug,
        "title": p.title,
        "difficulty": p.difficulty,
        "description": p.description,
        "starterCode": p.starter_code,
        "examples": p.examples,
        "tags": p.tags or [],
        "comparisonStrategy": p.comparison_strategy,
        "createdAt": p.created_at.isoformat(),
    }
    if not hide_tests and p.test_cases:
        data["testCases"] = [
            {
                "serialNumber": tc.serial_number,
                "function": tc.function,
                "input": tc.input,
                "expectedOutput": tc.expected_output,
            }
            for tc in p.test_cases
            if tc.is_active
        ]
    return data


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


def _normalize_string_list(values):
    if values is None:
        return []
    if not isinstance(values, list):
        return None

    normalized = []
    for item in values:
        if not isinstance(item, str) or not item.strip():
            return None
        normalized.append(item.strip())
    return normalized


def _normalize_tag_weights(values):
    if values is None:
        return {}
    if not isinstance(values, dict):
        return None

    normalized = {}
    for tag, weight in values.items():
        if not isinstance(tag, str) or not tag.strip():
            return None
        if isinstance(weight, bool) or not isinstance(weight, (int, float)) or weight < 0:
            return None

        normalized_tag = tag.strip().lower()
        normalized[normalized_tag] = max(float(weight), normalized.get(normalized_tag, 0.0))

    return normalized


def _parse_non_negative_int(data, key, default=0):
    value = data.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


@problems_bp.get("/")
def list_problems():
    verify_jwt_in_request(optional=True)
    user_id = get_jwt_identity()
    difficulty = request.args.get("difficulty")
    tag = request.args.get("tag")
    project_id = request.args.get("projectId")
    search = (request.args.get("search") or "").strip()
    sort_by = request.args.get("sort", "id")  # id, difficulty, created_at
    order = request.args.get("order", "asc")  # asc, desc
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 15, type=int), 50)  # max 50 per page
    
    q = Problem.query
    
    if project_id:
        if not user_id:
            return jsonify(error="Authentication required for project filtering"), 401
        q = q.join(
            ProblemProjectStat,
            ProblemProjectStat.problem_id == Problem.id,
        ).filter(
            ProblemProjectStat.user_id == user_id,
            ProblemProjectStat.project_id == project_id,
        )

    # Apply filters
    if difficulty:
        q = q.filter_by(difficulty=difficulty)
    if tag:
        q = q.filter(Problem.tags.contains([tag]))
    if search:
        pattern = f"%{search}%"
        q = q.filter(
            db.or_(
                Problem.title.ilike(pattern),
                Problem.slug.ilike(pattern),
                db.cast(Problem.tags, db.String).ilike(pattern),
            )
        )
    
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


@problems_bp.post("/select")
def select_problems():
    data = request.get_json(silent=True) or {}

    total = _parse_non_negative_int(data, "total", default=None)
    if total is None or total <= 0:
        return jsonify(error="total must be a positive integer"), 400

    if "tags" in data:
        return jsonify(error="Use tagWeights instead of tags"), 400

    if "tagWeights" in data and "tag_weights" in data:
        return jsonify(error="Provide only one of tagWeights or tag_weights"), 400

    raw_tag_weights = data.get("tagWeights") if "tagWeights" in data else data.get("tag_weights")
    tag_weights = _normalize_tag_weights(raw_tag_weights)
    if tag_weights is None:
        return jsonify(error="tagWeights/tag_weights must be an object mapping non-empty tag names to non-negative numbers"), 400

    ignore_slugs = _normalize_string_list(data.get("ignoreSlugs"))
    if ignore_slugs is None:
        return jsonify(error="ignoreSlugs must be an array of non-empty strings"), 400

    for deprecated_key in ("easy", "medium", "hard"):
        if deprecated_key in data:
            return jsonify(error="Use difficultyCounts.{easy|medium|hard} instead of top-level difficulty fields"), 400

    provided_difficulty_counts = data.get("difficultyCounts") or {}
    if not isinstance(provided_difficulty_counts, dict):
        return jsonify(error="difficultyCounts must be an object with easy, medium, and hard"), 400

    difficulty_counts = {"easy": 0, "medium": 0, "hard": 0}
    for level in ("easy", "medium", "hard"):
        if level in provided_difficulty_counts:
            parsed = _parse_non_negative_int(provided_difficulty_counts, level, 0)
            if parsed is None:
                return jsonify(error=f"difficultyCounts.{level} must be a non-negative integer"), 400
            difficulty_counts[level] = parsed

    requested_by_difficulty = sum(difficulty_counts.values())
    if requested_by_difficulty > total:
        return jsonify(error="sum of easy, medium, and hard cannot exceed total"), 400

    normalized_ignore_slugs = {slug.lower() for slug in ignore_slugs}

    candidates = Problem.query.order_by(
        Problem.created_at.desc(),
        Problem.id.asc(),
    ).all()

    def _problem_tags(problem):
        return [
            tag.strip().lower()
            for tag in (problem.tags or [])
            if isinstance(tag, str) and tag.strip()
        ]

    def _algo_tags(tags):
        # Algorithmic tags only — used for scoring and quota enforcement.
        # Structural tags are filtered out so they cannot influence ranking
        # or selection diversity.
        return [tag for tag in tags if tag not in STRUCTURAL_TAGS]

    # Drop structural tags from tag_weights up-front so all downstream
    # scoring and quota derivation is algorithmic-only.
    algo_tag_weights = {
        tag: weight
        for tag, weight in tag_weights.items()
        if tag not in STRUCTURAL_TAGS
    }

    # ---------------------------------------------------------------
    # Stage 1: rank by pure tag-weight relevance over algorithmic tags.
    # Structural tags (array, string, matrix, stack, list) are ignored
    # for scoring. Tag quotas are NOT used here; they only constrain
    # selection in stage 2.
    # Stable tie-break by original DB order (created_at desc, id asc).
    # ---------------------------------------------------------------
    ranked_candidates = []
    for index, problem in enumerate(candidates):
        if problem.slug.lower() in normalized_ignore_slugs:
            continue
        tags = _problem_tags(problem)
        algo_tags = _algo_tags(tags)
        score = sum(algo_tag_weights.get(tag, 0.0) for tag in set(algo_tags))
        primary = _primary_algo_tag(algo_tags, algo_tag_weights)
        pattern = _extract_problem_pattern(
            problem.slug,
            problem.title,
            tags=tags,
            primary_algo_tag=primary,
        )
        ranked_candidates.append((problem, score, index, tags, algo_tags, pattern))

    ranked_candidates.sort(key=lambda item: (-item[1], item[2]))

    # ---------------------------------------------------------------
    # Derive tagQuota (algorithmic tags only):
    #   1) Use explicit tagQuotas from request if provided. Structural
    #      entries are dropped so quotas only apply to algorithmic tags.
    #   2) Otherwise, compute proportional allocation from
    #      algo_tag_weights:
    #         quota[tag] = round(weight[tag] / sum(weights) * total)
    # ---------------------------------------------------------------
    raw_tag_quota = data.get("tagQuotas")
    tag_quota = {}
    if isinstance(raw_tag_quota, dict) and raw_tag_quota:
        for tag, limit in raw_tag_quota.items():
            if (
                isinstance(tag, str)
                and tag.strip()
                and isinstance(limit, int)
                and not isinstance(limit, bool)
                and limit >= 0
            ):
                normalized = tag.strip().lower()
                if normalized in STRUCTURAL_TAGS:
                    continue
                tag_quota[normalized] = limit
    elif algo_tag_weights:
        weight_sum = sum(algo_tag_weights.values())
        if weight_sum > 0:
            for tag, weight in algo_tag_weights.items():
                tag_quota[tag] = max(0, round((weight / weight_sum) * total))

    # ---------------------------------------------------------------
    # Stage 2: greedy selection with HARD per-tag quota enforcement.
    # A candidate is taken only if adding it does not push any of its
    # tags past its tagQuota limit. Tags without a quota are
    # unrestricted. tag_used is incremented only when actually taken.
    # Difficulty buckets are honored first (in ranked order), then a
    # global pass fills the remaining slots up to `total` while still
    # respecting the same hard quota.
    # ---------------------------------------------------------------
    # Optional secondary diversity cap per (algorithmic tag, pattern) pair.
    # `patternCap` in the request controls how many problems sharing the same
    # algo-tag + pattern bucket may be selected. Default is 2; pass 0 to
    # disable the secondary cap entirely.
    raw_pattern_cap = data.get("patternCap", 2)
    if (
        isinstance(raw_pattern_cap, bool)
        or not isinstance(raw_pattern_cap, int)
        or raw_pattern_cap < 0
    ):
        return jsonify(error="patternCap must be a non-negative integer"), 400
    pattern_cap = raw_pattern_cap

    selected = []
    selected_ids = set()
    tag_used = defaultdict(int)
    pattern_used = defaultdict(int)  # keyed by (algo_tag, pattern)

    def _fits_quota(algo_tags, pattern):
        # Tag quota: only algorithmic tags participate.
        if tag_quota:
            for tag in algo_tags:
                if tag in tag_quota and tag_used[tag] + 1 > tag_quota[tag]:
                    return False
        # Pattern diversity cap: a candidate cannot push any of its
        # (algo_tag, pattern) pairs over pattern_cap.
        if pattern_cap and algo_tags:
            for tag in algo_tags:
                if pattern_used[(tag, pattern)] + 1 > pattern_cap:
                    return False
        return True

    def _take(problem, algo_tags, pattern):
        selected.append(problem)
        selected_ids.add(problem.id)
        # Only algorithmic tags increment the global usage counter so
        # structural tags can never trip the quota check.
        for tag in algo_tags:
            tag_used[tag] += 1
            pattern_used[(tag, pattern)] += 1

    by_difficulty = {"easy": [], "medium": [], "hard": []}
    for entry in ranked_candidates:
        level = (entry[0].difficulty or "").lower()
        if level in by_difficulty:
            by_difficulty[level].append(entry)

    for level in ("easy", "medium", "hard"):
        needed = difficulty_counts[level]
        if needed <= 0:
            continue
        for problem, _, _, _, algo_tags, pattern in by_difficulty[level]:
            if needed <= 0:
                break
            if problem.id in selected_ids:
                continue
            if not _fits_quota(algo_tags, pattern):
                continue
            _take(problem, algo_tags, pattern)
            needed -= 1

    # Global fill: top up to `total` from the ranked list,
    # still enforcing tag quotas and the pattern diversity cap.
    for problem, _, _, _, algo_tags, pattern in ranked_candidates:
        if len(selected) >= total:
            break
        if problem.id in selected_ids:
            continue
        if not _fits_quota(algo_tags, pattern):
            continue
        _take(problem, algo_tags, pattern)

    # ---------------------------------------------------------------
    # Logging: how many of the selected problems carry each tag.
    # ---------------------------------------------------------------
    algo_counts = {}
    structural_counts = {}
    pattern_counts = {}
    selected_id_set = {p.id for p in selected}
    for problem, _, _, _, algo_tags, pattern in ranked_candidates:
        if problem.id not in selected_id_set:
            continue
        for tag in _problem_tags(problem):
            bucket = structural_counts if tag in STRUCTURAL_TAGS else algo_counts
            bucket[tag] = bucket.get(tag, 0) + 1
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

    def _sorted_counts(counts):
        return dict(sorted(counts.items(), key=lambda x: (-x[1], x[0])))

    current_app.logger.info(
        "Problem selection: selected=%s algorithmic=%s structural=%s patterns=%s quotas=%s patternCap=%s",
        len(selected),
        _sorted_counts(algo_counts),
        _sorted_counts(structural_counts),
        _sorted_counts(pattern_counts),
        dict(sorted(tag_quota.items())),
        pattern_cap,
    )

    return jsonify(
        problems=[problem_to_dict(p) for p in selected],
        selection={
            "requestedTotal": total,
            "returnedTotal": len(selected),
            "requestedDifficulty": difficulty_counts,
            "usedTagWeights": tag_weights,
            "usedTagQuotas": tag_quota,
            "patternCap": pattern_cap,
            "ignoredSlugs": ignore_slugs,
        },
    )


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
    comparison_strategy = _require_non_empty_string(data, "comparisonStrategy") or "exact"
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

    if comparison_strategy not in {"exact", "unordered", "unordered_nested", "float", "set"}:
        return jsonify(error="comparisonStrategy must be one of: exact, unordered, unordered_nested, float, set"), 400

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
        comparison_strategy=comparison_strategy,
        examples=examples,
        tags=tags,
    )
    db.session.add(problem)
    db.session.flush()  # Get problem.id before committing

    # Create test cases as separate records
    for idx, tc in enumerate(test_cases):
        input_str = tc.get("input", "")
        test_case = TestCase(
            problem_id=problem.id,
            serial_number=idx,
            function=tc.get("function", "solution"),
            input=input_str,
            expected_output=tc.get("expectedOutput", ""),
            arg_types=tc.get("argTypes") or _derive_arg_types(tags, input_str),
            is_active=tc.get("isActive", True),
        )
        db.session.add(test_case)

    db.session.commit()

    return jsonify(problem_to_dict(problem)), 201


@problems_bp.get("/<slug>")
def get_problem(slug):
    p = Problem.query.filter_by(slug=slug).first_or_404()
    return jsonify(problem_to_dict(p, hide_tests=False))


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
        comparison_strategy=data.get("comparisonStrategy", "exact"),
        examples=data["examples"],
        tags=data.get("tags", []),
    )
    db.session.add(p)
    db.session.flush()
    
    # Create test cases
    for idx, tc in enumerate(test_cases_data):
        input_str = tc.get("input", "")
        test_case = TestCase(
            problem_id=p.id,
            serial_number=idx,
            function=tc.get("function", "solution"),
            input=input_str,
            expected_output=tc.get("expectedOutput", ""),
            arg_types=tc.get("argTypes") or _derive_arg_types(data.get("tags", []), input_str),
            is_active=tc.get("isActive", True),
        )
        db.session.add(test_case)
    
    db.session.commit()
    return jsonify(problem_to_dict(p)), 201
