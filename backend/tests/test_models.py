from datetime import datetime, timedelta

from app import db
from app.models import (
    Contact,
    Favorite,
    PerfTestConfig,
    Problem,
    Project,
    StripeWebhookEvent,
    Submission,
    Subscription,
    User,
)


def test_user_password_hash_and_check(app_ctx):
    user = User(username="alice", email="alice@example.com")
    user.set_password("abc12345")
    assert user.password_hash is not None
    assert user.check_password("abc12345") is True
    assert user.check_password("wrong") is False


def test_user_check_password_without_hash(app_ctx):
    user = User(username="bob", email="bob@example.com")
    assert user.check_password("any") is False


def test_problem_model_persists_fields(app_ctx):
    problem = Problem(
        slug="valid-parentheses",
        title="Valid Parentheses",
        difficulty="easy",
        description="desc",
        starter_code="def solution(s):\n    pass",
        test_cases=[{"input": '"()"', "expected": "True"}],
        examples=[{"input": 's="()"', "output": "True"}],
        tags=["stack", "string"],
    )
    db.session.add(problem)
    db.session.commit()

    saved = Problem.query.filter_by(slug="valid-parentheses").first()
    assert saved is not None
    assert saved.tags == ["stack", "string"]


def test_project_submission_relationships(app_ctx, user):
    problem = Problem(
        slug="contains-duplicate",
        title="Contains Duplicate",
        difficulty="easy",
        description="desc",
        starter_code="def solution(nums):\n    pass",
        test_cases=[{"input": "[1,2,3]", "expected": "False"}],
        examples=[{"input": "[1,2,3]", "output": "False"}],
        tags=["array"],
    )
    project = Project(user_id=user.id, name="Arrays", is_default=True)
    db.session.add_all([problem, project])
    db.session.commit()

    sub = Submission(
        user_id=user.id,
        project_id=project.id,
        problem_id=problem.id,
        code="def solution(nums): return False",
        status="accepted",
        passed_tests=1,
        total_tests=1,
    )
    db.session.add(sub)
    db.session.commit()

    fetched = Submission.query.get(sub.id)
    assert fetched.user.id == user.id
    assert fetched.project.id == project.id
    assert fetched.problem.slug == "contains-duplicate"


def test_contact_defaults(app_ctx):
    contact = Contact(name="A", email="a@b.com", subject="Help", message="Hello")
    db.session.add(contact)
    db.session.commit()

    saved = Contact.query.get(contact.id)
    assert saved.status == "pending"
    assert saved.created_at is not None
    assert saved.updated_at is not None


def test_perf_test_config_defaults(app_ctx):
    cfg = PerfTestConfig(name="load-test")
    db.session.add(cfg)
    db.session.commit()

    saved = PerfTestConfig.query.filter_by(name="load-test").first()
    assert saved.enabled is True
    assert saved.login_path == "/auth/login"
    assert saved.submit_path == "/submissions/"


def test_subscription_and_webhook_event_persist(app_ctx, user):
    sub = Subscription(
        user_id=user.id,
        stripe_product_id="prod_test",
        status="active",
        amount_cents=3000,
        currency="usd",
        interval="year",
        current_period_start=datetime.utcnow(),
        current_period_end=datetime.utcnow() + timedelta(days=365),
    )
    event = StripeWebhookEvent(
        id="evt_123",
        event_type="customer.subscription.created",
        payload={"id": "evt_123"},
        processed=False,
    )
    db.session.add_all([sub, event])
    db.session.commit()

    saved_sub = Subscription.query.get(sub.id)
    saved_event = StripeWebhookEvent.query.get("evt_123")
    assert saved_sub.user_id == user.id
    assert saved_sub.status == "active"
    assert saved_event.event_type == "customer.subscription.created"
