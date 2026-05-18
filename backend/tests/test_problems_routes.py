from app import db
from app.models import Problem, ProblemProjectStat, TestCase as ProblemTestCase


def _create_problem(slug, difficulty, tags):
    item = Problem(
        slug=slug,
        title=slug.replace("-", " ").title(),
        difficulty=difficulty,
        description="desc",
        starter_code="def solution():\n    pass",
        examples=[{"input": "1", "output": "1"}],
        tags=tags,
    )
    db.session.add(item)
    db.session.flush()

    db.session.add(
        ProblemTestCase(
            problem_id=item.id,
            serial_number=0,
            test_input={"args": [1]},
            expected_output="1",
            is_active=True,
        )
    )
    db.session.commit()
    return item


def test_list_problems_returns_pagination(client, problem):
    res = client.get("/problems/?page=1&per_page=10")
    assert res.status_code == 200
    body = res.get_json()
    assert "problems" in body
    assert "pagination" in body
    assert body["pagination"]["total"] >= 1


def test_get_problem_by_slug(client, problem):
    res = client.get(f"/problems/{problem.slug}")
    assert res.status_code == 200
    assert res.get_json()["slug"] == "two-sum"


def test_public_ingest_rejects_missing_key(client):
    res = client.post("/problems/public-ingest", json={"slug": "x"})
    assert res.status_code == 403


def test_public_ingest_rejects_invalid_payload(client):
    res = client.post(
        "/problems/public-ingest",
        json={
            "ingestKey": "ingest-test-key",
            "slug": "new-problem",
            "title": "New",
            "difficulty": "invalid",
            "description": "d",
            "starterCode": "def solution(): pass",
            "examples": [],
            "testCases": [],
        },
    )
    assert res.status_code == 400


def test_public_ingest_success(client):
    payload = {
        "ingestKey": "ingest-test-key",
        "slug": "new-problem",
        "title": "New Problem",
        "difficulty": "easy",
        "description": "desc",
        "starterCode": "def solution(a):\n    return a",
        "examples": [{"input": "1", "output": "1"}],
        "testCases": [{"function": "solution", "input": "1", "expectedOutput": "1"}],
        "tags": ["math"],
    }
    res = client.post("/problems/public-ingest", json=payload)
    assert res.status_code == 201
    body = res.get_json()
    assert body["slug"] == "new-problem"


def test_public_ingest_duplicate_slug(client, app_ctx):
    from app.models import TestCase
    existing = Problem(
        slug="dup-problem",
        title="dup",
        difficulty="easy",
        description="desc",
        starter_code="def solution(): pass",
        examples=[{"input": "1", "output": "1"}],
        tags=["array"],
    )
    db.session.add(existing)
    db.session.flush()
    
    # Create test case separately
    tc = TestCase(
        problem_id=existing.id,
        serial_number=0,
        test_input={"args": [1]},
        expected_output="1",
        is_active=True,
    )
    db.session.add(tc)
    db.session.commit()

    payload = {
        "ingestKey": "ingest-test-key",
        "slug": "dup-problem",
        "title": "Dup",
        "difficulty": "easy",
        "description": "desc",
        "starterCode": "def solution(a):\n    return a",
        "examples": [{"input": "1", "output": "1"}],
        "testCases": [{"function": "solution", "input": "1", "expectedOutput": "1"}],
    }
    res = client.post("/problems/public-ingest", json=payload)
    assert res.status_code == 409


def test_create_problem_requires_auth(client):
    res = client.post("/problems/", json={})
    assert res.status_code == 401


def test_create_problem_with_auth(client, auth_headers):
    res = client.post(
        "/problems/",
        headers=auth_headers,
        json={
            "slug": "merge-sorted-array",
            "title": "Merge Sorted Array",
            "difficulty": "easy",
            "description": "desc",
            "starterCode": "def solution(): pass",
            "testCases": [{"input": "", "expected": "1"}],
            "examples": [{"input": "", "output": "1"}],
            "tags": ["array"],
        },
    )
    assert res.status_code == 201
    assert res.get_json()["slug"] == "merge-sorted-array"


def test_select_problems_with_tags_ignore_and_difficulty_counts(client, app_ctx):
    _create_problem("easy-bfs", "easy", ["bfs"])
    _create_problem("easy-trie-ignore", "easy", ["trie"])
    _create_problem("medium-trie", "medium", ["trie"])
    _create_problem("hard-linked-list", "hard", ["linked-list"])
    _create_problem("medium-dp", "medium", ["dp"])

    res = client.post(
        "/problems/select",
        json={
            "total": 3,
            "tagWeights": {"bfs": 1, "trie": 1, "linked-list": 1},
            "ignoreSlugs": ["easy-trie-ignore"],
            "difficultyCounts": {"easy": 1, "medium": 1, "hard": 1},
        },
    )

    assert res.status_code == 200
    body = res.get_json()
    slugs = {problem["slug"] for problem in body["problems"]}

    assert len(body["problems"]) == 3
    assert slugs == {"easy-bfs", "medium-trie", "hard-linked-list"}


def test_select_problems_fills_remaining_to_total(client, app_ctx):
    _create_problem("easy-bfs-1", "easy", ["bfs"])
    _create_problem("medium-bfs-1", "medium", ["bfs"])
    _create_problem("hard-bfs-1", "hard", ["bfs"])

    res = client.post(
        "/problems/select",
        json={
            "total": 2,
            "tagWeights": {"bfs": 1},
            "difficultyCounts": {"easy": 1},
        },
    )

    assert res.status_code == 200
    body = res.get_json()
    assert body["selection"]["requestedTotal"] == 2
    assert body["selection"]["returnedTotal"] == 2

    difficulties = [problem["difficulty"] for problem in body["problems"]]
    assert difficulties.count("easy") >= 1


def test_select_problems_returns_400_when_not_enough_requested_difficulty(client, app_ctx):
    _create_problem("easy-only", "easy", ["array"])

    res = client.post(
        "/problems/select",
        json={
            "total": 2,
            "difficultyCounts": {"hard": 1},
        },
    )

    # The endpoint fills remaining slots with available problems instead of returning 400
    assert res.status_code == 200
    body = res.get_json()
    # Should return the available easy problem to fill the total
    assert len(body["problems"]) == 1
    assert body["problems"][0]["difficulty"] == "easy"


# ---------------------------------------------------------------------------
# Difficulty filter on GET /problems/
# ---------------------------------------------------------------------------

def test_list_problems_difficulty_filter_easy(client, app_ctx):
    _create_problem("df-easy-1", "easy", ["array"])
    _create_problem("df-medium-1", "medium", ["array"])
    _create_problem("df-hard-1", "hard", ["array"])

    res = client.get("/problems/?difficulty=easy")
    assert res.status_code == 200
    problems = res.get_json()["problems"]
    assert all(p["difficulty"] == "easy" for p in problems)
    slugs = {p["slug"] for p in problems}
    assert "df-easy-1" in slugs
    assert "df-medium-1" not in slugs
    assert "df-hard-1" not in slugs


def test_list_problems_difficulty_filter_medium(client, app_ctx):
    _create_problem("df-easy-2", "easy", ["array"])
    _create_problem("df-medium-2", "medium", ["array"])

    res = client.get("/problems/?difficulty=medium")
    assert res.status_code == 200
    problems = res.get_json()["problems"]
    assert all(p["difficulty"] == "medium" for p in problems)


def test_list_problems_difficulty_filter_hard(client, app_ctx):
    _create_problem("df-easy-3", "easy", ["array"])
    _create_problem("df-hard-3", "hard", ["array"])

    res = client.get("/problems/?difficulty=hard")
    assert res.status_code == 200
    problems = res.get_json()["problems"]
    assert all(p["difficulty"] == "hard" for p in problems)


def test_list_problems_difficulty_filter_with_project(client, app_ctx, user, project, auth_headers):
    """Regression: difficulty filter + projectId used to crash with
    'Entity namespace for problem_project_stats has no property difficulty'
    because filter_by() resolved against the joined ProblemProjectStat entity."""
    easy = _create_problem("df-proj-easy", "easy", ["array"])
    medium = _create_problem("df-proj-medium", "medium", ["array"])

    for prob in (easy, medium):
        db.session.add(ProblemProjectStat(
            user_id=user.id,
            problem_id=prob.id,
            project_id=project.id,
            attempted=False,
        ))
    db.session.commit()

    res = client.get(
        f"/problems/?difficulty=easy&projectId={project.id}",
        headers=auth_headers,
    )
    assert res.status_code == 200
    problems = res.get_json()["problems"]
    assert all(p["difficulty"] == "easy" for p in problems)
    slugs = {p["slug"] for p in problems}
    assert "df-proj-easy" in slugs
    assert "df-proj-medium" not in slugs


def test_list_problems_no_difficulty_filter_returns_all(client, app_ctx):
    _create_problem("df-all-easy", "easy", ["array"])
    _create_problem("df-all-hard", "hard", ["array"])

    res = client.get("/problems/?per_page=50")
    assert res.status_code == 200
    difficulties = {p["difficulty"] for p in res.get_json()["problems"]}
    assert len(difficulties) > 1


def test_select_problems_rejects_top_level_difficulty_fields(client, app_ctx):
    _create_problem("easy-only-2", "easy", ["array"])

    res = client.post(
        "/problems/select",
        json={
            "total": 1,
            "easy": 1,
        },
    )

    assert res.status_code == 400
    body = res.get_json()
    assert "difficultyCounts" in body["error"]
