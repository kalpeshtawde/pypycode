import os
import sys
from pathlib import Path
from datetime import datetime, timezone

import pytest
from flask_jwt_extended import create_access_token
from sqlalchemy import JSON

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("CELERY_BROKER_URL", "memory://")
os.environ.setdefault("CELERY_RESULT_BACKEND", "cache+memory://")
os.environ.setdefault("PROBLEM_INGEST_KEY", "ingest-test-key")
os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test_123")
os.environ.setdefault("STRIPE_WEBHOOK_SECRET", "whsec_test_123")

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app import create_app, db
from app.models import Problem, Project, User


Problem.__table__.columns["tags"].type = JSON()


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
        JWT_SECRET_KEY="test-secret",
        PROBLEM_INGEST_KEY="ingest-test-key",
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


def _create_user(email="user@example.com", username="user", screen_name="@user"):
    user = User(
        username=username,
        email=email,
        first_name="Test",
        last_name="User",
        screen_name=screen_name,
        subscription_status="none",
    )
    user.set_password("secret123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def user(app_ctx):
    return _create_user()


@pytest.fixture
def second_user(app_ctx):
    return _create_user(email="other@example.com", username="other", screen_name="@other")


@pytest.fixture
def auth_headers(app, user):
    with app.app_context():
        token = create_access_token(identity=user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def problem(app_ctx):
    item = Problem(
        slug="two-sum",
        title="Two Sum",
        difficulty="easy",
        description="Find indices",
        starter_code="def solution(nums, target):\n    pass",
        test_cases=[{"function": "solution", "input": "[2,7,11,15], 9", "expected": "[0,1]"}],
        examples=[{"input": "nums=[2,7,11,15], target=9", "output": "[0,1]"}],
        tags=["array"],
    )
    db.session.add(item)
    db.session.commit()
    return item


@pytest.fixture
def project(app_ctx, user):
    item = Project(user_id=user.id, name="Default", is_default=True)
    db.session.add(item)
    db.session.commit()
    return item


@pytest.fixture
def utc_now_naive():
    return datetime.now(timezone.utc).replace(tzinfo=None)
