from app import db
from app.models import Problem, Project, Submission


class DummyTask:
    def __init__(self, task_id="task-1"):
        self.id = task_id


def test_list_projects(client, auth_headers, project):
    res = client.get("/projects/", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_create_project_success(client, auth_headers):
    res = client.post("/projects/", headers=auth_headers, json={"name": "Algorithms"})
    assert res.status_code == 201
    assert res.get_json()["name"] == "Algorithms"


def test_create_project_duplicate_name(client, auth_headers, project):
    res = client.post("/projects/", headers=auth_headers, json={"name": "Default"})
    assert res.status_code == 409


def test_set_default_project(client, auth_headers, app_ctx, user):
    p1 = Project(user_id=user.id, name="P1", is_default=True)
    p2 = Project(user_id=user.id, name="P2", is_default=False)
    db.session.add_all([p1, p2])
    db.session.commit()

    res = client.post(f"/projects/{p2.id}/set-default", headers=auth_headers)
    assert res.status_code == 200

    db.session.refresh(p1)
    db.session.refresh(p2)
    assert p1.is_default is False
    assert p2.is_default is True


def test_delete_project_removes_project_and_submissions(client, auth_headers, app_ctx, user, problem):
    project = Project(user_id=user.id, name="ToDelete", is_default=True)
    db.session.add(project)
    db.session.commit()

    sub = Submission(user_id=user.id, project_id=project.id, problem_id=problem.id, code="x")
    db.session.add(sub)
    db.session.commit()

    res = client.delete(f"/projects/{project.id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["deletedSubmissions"] == 1


def test_submit_to_project_queues_task(client, auth_headers, app_ctx, user, problem, mocker):
    project = Project(user_id=user.id, name="SubmitProject", is_default=True)
    db.session.add(project)
    db.session.commit()

    mocker.patch("app.routes.projects.run_submission.delay", return_value=DummyTask("task-123"))

    res = client.post(
        f"/projects/{project.id}/submit",
        headers=auth_headers,
        json={"problemSlug": problem.slug, "code": "def solution(): return 1"},
    )

    assert res.status_code == 202
    body = res.get_json()
    assert body["taskId"] == "task-123"
