from celery.exceptions import NotRegistered

from app import db
from app.models import Problem, Project, Submission, TestCase


class DummyRunTask:
    def __init__(self, value=None, raises=None):
        self.value = value
        self.raises = raises
        self.id = "task-xyz"

    def get(self, timeout=15):
        if self.raises:
            raise self.raises
        return self.value


class DummyQueueTask:
    def __init__(self, task_id="task-submit"):
        self.id = task_id


def test_run_code_success(client, auth_headers, app_ctx, user, problem, project, mocker):
    mock_task = DummyRunTask(
        value={
            "status": "accepted",
            "passed_tests": 1,
            "total_tests": 1,
            "runtime_ms": 7,
            "memory_kb": 123,
            "error_output": None,
        }
    )
    mocker.patch("app.routes.submissions.run_code_for_problem.delay", return_value=mock_task)

    res = client.post(
        "/submissions/run",
        headers=auth_headers,
        json={"problemSlug": problem.slug, "projectId": project.id, "code": "def solution(): return 1"},
    )
    assert res.status_code == 200
    assert res.get_json()["status"] == "accepted"


def test_run_code_handles_not_registered(client, auth_headers, problem, mocker):
    mocker.patch("app.routes.submissions.run_code_for_problem.delay", return_value=DummyRunTask(raises=NotRegistered("x")))
    res = client.post(
        "/submissions/run",
        headers=auth_headers,
        json={"problemSlug": problem.slug, "code": "def solution(): return 1"},
    )
    assert res.status_code == 503


def test_submit_creates_submission(client, auth_headers, problem, project, mocker):
    mocker.patch("app.routes.submissions.run_submission.delay", return_value=DummyQueueTask("task-999"))

    res = client.post(
        "/submissions/",
        headers=auth_headers,
        json={"problemSlug": problem.slug, "projectId": project.id, "code": "def solution(): return 1"},
    )
    assert res.status_code == 202
    assert res.get_json()["taskId"] == "task-999"


def test_submit_requires_project(client, auth_headers, problem):
    res = client.post(
        "/submissions/",
        headers=auth_headers,
        json={"problemSlug": problem.slug, "code": "def solution(): return 1"},
    )
    assert res.status_code == 400


def test_get_submission_forbidden(client, auth_headers, app_ctx, user, second_user):
    problem = Problem(
        slug="forbidden-problem",
        title="Forbidden",
        difficulty="easy",
        description="d",
        starter_code="def solution(): pass",
        examples=[{"input": "", "output": "1"}],
        tags=["x"],
    )
    db.session.add(problem)
    db.session.flush()
    
    # Create test case separately
    tc = TestCase(problem_id=problem.id, serial_number=0, function="solution", input="", expected_output="1")
    db.session.add(tc)
    
    project = Project(user_id=second_user.id, name="Other", is_default=True)
    db.session.add(project)
    db.session.commit()

    sub = Submission(user_id=second_user.id, project_id=project.id, problem_id=problem.id, code="x")
    db.session.add(sub)
    db.session.commit()

    res = client.get(f"/submissions/{sub.id}", headers=auth_headers)
    assert res.status_code == 403


def test_get_all_and_accepted_submissions(client, auth_headers, app_ctx, user, problem):
    project = Project(user_id=user.id, name="P", is_default=True)
    db.session.add(project)
    db.session.commit()

    db.session.add_all(
        [
            Submission(user_id=user.id, project_id=project.id, problem_id=problem.id, code="x", status="accepted"),
            Submission(user_id=user.id, project_id=project.id, problem_id=problem.id, code="x", status="wrong_answer"),
        ]
    )
    db.session.commit()

    all_res = client.get("/submissions/all", headers=auth_headers)
    accepted_res = client.get("/submissions/accepted", headers=auth_headers)

    assert all_res.status_code == 200
    assert len(all_res.get_json()) == 2
    assert accepted_res.status_code == 200
    assert len(accepted_res.get_json()) == 1


def test_submissions_for_problem(client, auth_headers, app_ctx, user, problem):
    project = Project(user_id=user.id, name="ProblemScope", is_default=True)
    db.session.add(project)
    db.session.commit()

    db.session.add(
        Submission(
            user_id=user.id,
            project_id=project.id,
            problem_id=problem.id,
            code="def solution(): return 1",
            status="accepted",
            passed_tests=1,
            total_tests=1,
            runtime_ms=10,
        )
    )
    db.session.commit()

    res = client.get(f"/submissions/problem/{problem.slug}", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.get_json()) == 1
