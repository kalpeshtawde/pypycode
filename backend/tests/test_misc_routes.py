from app import db
from app.models import Contact, Problem, Submission


def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_contact_create_success(client):
    res = client.post(
        "/contact/",
        json={
            "name": "Jane",
            "email": "jane@example.com",
            "subject": "Question",
            "message": "Need help",
        },
    )
    assert res.status_code == 201
    assert res.get_json()["contact"]["status"] == "pending"


def test_contact_create_validation_error(client):
    res = client.post(
        "/contact/",
        json={"name": "", "email": "bad", "subject": "", "message": ""},
    )
    assert res.status_code == 400


def test_get_contacts_returns_list(client, app_ctx):
    c = Contact(name="A", email="a@a.com", subject="s", message="m")
    db.session.add(c)
    db.session.commit()

    res = client.get("/contact/")
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_update_contact_status_success(client, app_ctx):
    c = Contact(name="A", email="a@a.com", subject="s", message="m")
    db.session.add(c)
    db.session.commit()

    res = client.put(f"/contact/{c.id}", json={"status": "read"})
    assert res.status_code == 200
    assert res.get_json()["contact"]["status"] == "read"


def test_leaderboard_returns_ranked_users(client, app_ctx, user):
    p = Problem(
        slug="leader-problem",
        title="Leader",
        difficulty="easy",
        description="d",
        starter_code="def solution(): pass",
        test_cases=[{"input": "", "expected": "1"}],
        examples=[{"input": "", "output": "1"}],
        tags=["x"],
    )
    db.session.add(p)
    db.session.commit()

    sub = Submission(user_id=user.id, project_id=user.id, problem_id=p.id, code="x", status="accepted")
    db.session.add(sub)
    db.session.commit()

    res = client.get("/leaderboard/")
    assert res.status_code == 200
    body = res.get_json()
    assert len(body) == 1
    assert body[0]["rank"] == 1
    assert body[0]["solved"] == 1
