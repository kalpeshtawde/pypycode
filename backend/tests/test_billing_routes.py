from datetime import datetime, timedelta

import stripe

from app import db
from app.models import StripeWebhookEvent, Subscription, User
from app.routes import billing


class DictLike:
    def __init__(self, data):
        self._data = data

    def to_dict_recursive(self):
        return self._data


class CheckoutSessionMock:
    def __init__(self, session_id, url):
        self.id = session_id
        self.url = url

    def to_dict_recursive(self):
        return {"id": self.id, "url": self.url}


def test_pricing_endpoint(client):
    res = client.get("/billing/pricing")
    assert res.status_code == 200
    body = res.get_json()
    assert body["plan"] == "annual_all_access"
    assert body["interval"] == "year"


def test_subscription_endpoint_returns_none(client, auth_headers):
    res = client.get("/billing/subscription", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["subscription"] is None


def test_access_status_user_not_found(client, app, auth_headers, mocker):
    mocker.patch("app.routes.billing.get_jwt_identity", return_value="missing-user")
    res = client.get("/billing/access-status", headers=auth_headers)
    assert res.status_code == 404


def test_start_trial_success(client, auth_headers, user):
    res = client.post("/billing/start-trial", headers=auth_headers)
    assert res.status_code == 200
    body = res.get_json()
    assert body["accessStatus"] == "trialing"
    assert body["trial"]["used"] is True


def test_start_trial_already_used(client, auth_headers, app_ctx, user):
    user.trial_used = True
    db.session.commit()

    res = client.post("/billing/start-trial", headers=auth_headers)
    assert res.status_code == 400


def test_checkout_session_requires_secret_key(client, auth_headers, mocker):
    mocker.patch("app.routes.billing._stripe_secret_key", return_value=None)
    res = client.post("/billing/checkout-session", headers=auth_headers, json={"redirect": "/pricing"})
    assert res.status_code == 500


def test_checkout_session_success_creates_pending_subscription(client, auth_headers, user, mocker):
    mocker.patch("app.routes.billing._stripe_secret_key", return_value="sk_test")
    mocker.patch("app.routes.billing._frontend_url", return_value="http://localhost:5173")

    customer_mock = type("Customer", (), {"id": "cus_123"})
    session_mock = CheckoutSessionMock("cs_123", "https://checkout.stripe.com/s/cs_123")

    mocker.patch("stripe.Customer.create", return_value=customer_mock)
    mocker.patch("stripe.checkout.Session.create", return_value=session_mock)

    res = client.post(
        "/billing/checkout-session",
        headers=auth_headers,
        json={"redirect": "/problems"},
    )

    assert res.status_code == 200
    body = res.get_json()
    assert body["sessionId"] == "cs_123"

    pending = Subscription.query.filter_by(stripe_checkout_session_id="cs_123").first()
    assert pending is not None
    assert pending.status == "checkout_created"


def test_checkout_session_handles_stripe_error(client, auth_headers, mocker):
    mocker.patch("app.routes.billing._stripe_secret_key", return_value="sk_test")
    mocker.patch("stripe.Customer.create", side_effect=stripe.error.StripeError("boom"))

    res = client.post("/billing/checkout-session", headers=auth_headers, json={"redirect": "/problems"})
    assert res.status_code == 400


def test_webhook_requires_signature(client, mocker):
    mocker.patch("app.routes.billing._stripe_secret_key", return_value="sk_test")
    mocker.patch("app.routes.billing._stripe_webhook_secret", return_value="whsec_test")

    res = client.post("/billing/webhook", data=b"{}")
    assert res.status_code == 400


def test_webhook_duplicate_event_returns_duplicate(client, app_ctx, mocker):
    existing = StripeWebhookEvent(id="evt_dup", event_type="invoice.payment_succeeded", payload={"id": "evt_dup"}, processed=True)
    db.session.add(existing)
    db.session.commit()

    event_payload = {
        "id": "evt_dup",
        "type": "invoice.payment_succeeded",
        "created": 1710000000,
        "data": {"object": {"subscription": "sub_1"}},
    }

    mocker.patch("app.routes.billing._stripe_secret_key", return_value="sk_test")
    mocker.patch("app.routes.billing._stripe_webhook_secret", return_value="whsec_test")
    mocker.patch("stripe.Webhook.construct_event", return_value=DictLike(event_payload))

    res = client.post("/billing/webhook", data=b"{}", headers={"Stripe-Signature": "sig"})
    assert res.status_code == 200
    assert res.get_json()["duplicate"] is True


def test_webhook_subscription_updated_path(client, user, mocker):
    event_payload = {
        "id": "evt_new",
        "type": "customer.subscription.updated",
        "created": 1710000000,
        "data": {
            "object": {
                "id": "sub_123",
                "customer": "cus_123",
                "status": "active",
                "metadata": {"user_id": user.id},
                "items": {"data": [{"price": {"id": "price_1", "product": "prod_1", "unit_amount": 3000, "currency": "usd", "recurring": {"interval": "year"}}}]},
                "current_period_start": 1710000000,
                "current_period_end": 1720000000,
                "cancel_at_period_end": False,
                "canceled_at": None,
            }
        },
    }

    mocker.patch("app.routes.billing._stripe_secret_key", return_value="sk_test")
    mocker.patch("app.routes.billing._stripe_webhook_secret", return_value="whsec_test")
    mocker.patch("stripe.Webhook.construct_event", return_value=DictLike(event_payload))

    res = client.post("/billing/webhook", data=b"{}", headers={"Stripe-Signature": "sig"})
    assert res.status_code == 200

    sub = Subscription.query.filter_by(stripe_subscription_id="sub_123").first()
    assert sub is not None
    assert sub.status == "active"


def test_sync_subscription_uses_fallback_user(app_ctx, user):
    stripe_sub = {
        "id": "sub_fallback",
        "customer": "cus_fallback",
        "status": "active",
        "metadata": {},
        "items": {"data": [{"price": {"id": "price_f", "product": "prod_f", "unit_amount": 3000, "currency": "usd", "recurring": {"interval": "year"}}}]},
    }

    local = billing._sync_subscription(stripe_sub, fallback_user_id=user.id)
    db.session.commit()

    assert local.user_id == user.id
    assert local.status == "active"


def test_serialize_access_status_trial_expired(app_ctx, user):
    user.trial_used = True
    user.trial_started_at = datetime.utcnow() - timedelta(days=20)
    user.trial_ends_at = datetime.utcnow() - timedelta(days=5)

    body = billing._serialize_access_status(user, None)
    assert body["accessStatus"] == "trial_expired"
