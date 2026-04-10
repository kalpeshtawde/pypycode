from app import db
from app.models import Problem, Submission, User


def test_signup_success(client):
    res = client.post(
        "/auth/signup",
        json={
            "email": "new@example.com",
            "password": "secret123",
            "firstName": "New",
            "lastName": "User",
            "screenName": "@new_user",
        },
    )
    assert res.status_code == 201
    body = res.get_json()
    assert body["screenName"] == "@new_user"
    assert body["is_new"] is True


def test_signup_rejects_duplicate_email(client, app_ctx):
    user = User(username="u1", email="dup@example.com", screen_name="@dup")
    user.set_password("secret123")
    db.session.add(user)
    db.session.commit()

    res = client.post(
        "/auth/signup",
        json={
            "email": "dup@example.com",
            "password": "secret123",
            "screenName": "@another",
        },
    )
    assert res.status_code == 409


def test_login_success(client, app_ctx):
    user = User(username="loginuser", email="login@example.com", screen_name="@login")
    user.set_password("secret123")
    db.session.add(user)
    db.session.commit()

    res = client.post("/auth/login", json={"email": "login@example.com", "password": "secret123"})
    assert res.status_code == 200
    assert "token" in res.get_json()


def test_login_invalid_credentials(client, app_ctx):
    user = User(username="loginuser2", email="bad@example.com", screen_name="@bad")
    user.set_password("secret123")
    db.session.add(user)
    db.session.commit()

    res = client.post("/auth/login", json={"email": "bad@example.com", "password": "wrong"})
    assert res.status_code == 401


def test_me_returns_authenticated_user(client, auth_headers, user):
    res = client.get("/auth/me", headers=auth_headers)
    assert res.status_code == 200
    body = res.get_json()
    assert body["id"] == user.id
    assert body["email"] == user.email


def test_screen_name_availability_reports_taken(client, app_ctx):
    existing = User(username="taken", email="taken@example.com", screen_name="@taken")
    existing.set_password("secret123")
    db.session.add(existing)
    db.session.commit()

    res = client.get("/auth/screen-name-availability?screenName=@taken")
    assert res.status_code == 200
    assert res.get_json()["available"] is False


def test_update_profile_success(client, auth_headers):
    res = client.post(
        "/auth/profile",
        headers=auth_headers,
        json={"firstName": "Updated", "lastName": "Name", "screenName": "@updated_name"},
    )
    assert res.status_code == 200
    assert res.get_json()["screenName"] == "@updated_name"


def test_profile_includes_stats_and_activity(client, auth_headers, app_ctx, user):
    p1 = Problem(
        slug="p1",
        title="P1",
        difficulty="easy",
        description="d",
        starter_code="def solution(): pass",
        test_cases=[{"input": "", "expected": "1"}],
        examples=[{"input": "", "output": "1"}],
        tags=["x"],
    )
    p2 = Problem(
        slug="p2",
        title="P2",
        difficulty="easy",
        description="d",
        starter_code="def solution(): pass",
        test_cases=[{"input": "", "expected": "1"}],
        examples=[{"input": "", "output": "1"}],
        tags=["y"],
    )
    db.session.add_all([p1, p2])
    db.session.commit()

    db.session.add_all(
        [
            Submission(user_id=user.id, project_id=user.id, problem_id=p1.id, code="x", status="accepted", passed_tests=1, total_tests=1),
            Submission(user_id=user.id, project_id=user.id, problem_id=p2.id, code="x", status="wrong_answer", passed_tests=0, total_tests=1),
        ]
    )
    db.session.commit()

    res = client.get("/auth/profile", headers=auth_headers)
    assert res.status_code == 200
    body = res.get_json()
    assert body["stats"]["totalSubmissions"] == 2
    assert body["stats"]["acceptedSubmissions"] == 1
    assert body["stats"]["solvedProblems"] == 1
