from datetime import datetime, timedelta, timezone
import math
import os
from typing import Optional
from urllib.parse import quote

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import stripe

from app import db
from app.models import StripeWebhookEvent, Subscription, User
import logging

logger = logging.getLogger(__name__)


billing_bp = Blueprint("billing", __name__)


STRIPE_PRODUCT_ID = os.getenv("STRIPE_PRODUCT_ID") or "prod_UIjX4gboLVPWDq"
STRIPE_PRICE_CENTS = int(os.getenv("STRIPE_ANNUAL_PRICE_CENTS") or "3000")
STRIPE_CURRENCY = os.getenv("STRIPE_CURRENCY") or "usd"
STRIPE_INTERVAL = "year"
TRIAL_DAYS = 15
ACTIVE_SUBSCRIPTION_STATUSES = {"active", "trialing", "past_due", "unpaid"}


def _stripe_secret_key() -> Optional[str]:
    return os.getenv("STRIPE_SECRET_KEY")


def _stripe_webhook_secret() -> Optional[str]:
    return os.getenv("STRIPE_WEBHOOK_SECRET")


def _frontend_url() -> str:
    url = os.getenv("FRONTEND_URL")
    if not url:
        url = "http://localhost:5173"
    return url.rstrip("/")


def _safe_redirect_path(path: Optional[str]) -> str:
    if not path:
        return "/problems"
    if not path.startswith("/") or path.startswith("//"):
        return "/problems"
    return path


def _stripe_to_dict(value):
    if hasattr(value, "to_dict_recursive"):
        return value.to_dict_recursive()
    return value


def _to_datetime(unix_ts):
    if not unix_ts:
        return None
    # Return UTC naive datetime for database compatibility
    return datetime.fromtimestamp(unix_ts, tz=timezone.utc).replace(tzinfo=None)


def _as_utc_naive(value: Optional[datetime]):
    if not value:
        return None
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _sync_subscription(stripe_subscription, fallback_user_id=None, checkout_session_id=None):
    stripe_subscription = _stripe_to_dict(stripe_subscription)
    stripe_subscription_id = stripe_subscription.get("id")
    stripe_customer_id = stripe_subscription.get("customer")
    metadata = stripe_subscription.get("metadata") or {}
    user_id = metadata.get("user_id") or fallback_user_id

    local_subscription = None
    if stripe_subscription_id:
        local_subscription = Subscription.query.filter_by(stripe_subscription_id=stripe_subscription_id).first()
    if local_subscription is None and checkout_session_id:
        local_subscription = Subscription.query.filter_by(stripe_checkout_session_id=checkout_session_id).first()
        # If found by checkout session but has different stripe_subscription_id, skip updating checkout_session_id later
        if local_subscription and stripe_subscription_id and local_subscription.stripe_subscription_id != stripe_subscription_id:
            checkout_session_id = None  # Don't try to re-assign, it belongs to another subscription

    if local_subscription is None:
        if not user_id:
            raise ValueError("Cannot associate Stripe subscription with a user")
        local_subscription = Subscription(
            user_id=user_id,
            stripe_product_id=STRIPE_PRODUCT_ID,
            amount_cents=STRIPE_PRICE_CENTS,
            currency=STRIPE_CURRENCY,
            interval=STRIPE_INTERVAL,
        )
        db.session.add(local_subscription)

    items = (stripe_subscription.get("items") or {}).get("data") or []
    first_item = items[0] if items else {}
    price = first_item.get("price") or {}
    recurring = price.get("recurring") or {}

    local_subscription.stripe_customer_id = stripe_customer_id
    local_subscription.stripe_subscription_id = stripe_subscription_id
    if checkout_session_id:
        local_subscription.stripe_checkout_session_id = checkout_session_id
    stripe_status = stripe_subscription.get("status")
    local_subscription.status = stripe_status or local_subscription.status
    logger.info(f"Subscription sync: stripe_status={stripe_status}, local_status={local_subscription.status}")
    local_subscription.stripe_price_id = price.get("id")
    local_subscription.stripe_product_id = price.get("product") or local_subscription.stripe_product_id
    local_subscription.amount_cents = price.get("unit_amount") or local_subscription.amount_cents
    local_subscription.currency = price.get("currency") or local_subscription.currency
    local_subscription.interval = recurring.get("interval") or local_subscription.interval
    local_subscription.current_period_start = _to_datetime(stripe_subscription.get("current_period_start"))
    local_subscription.current_period_end = _to_datetime(stripe_subscription.get("current_period_end"))
    local_subscription.cancel_at_period_end = bool(stripe_subscription.get("cancel_at_period_end"))
    local_subscription.canceled_at = _to_datetime(stripe_subscription.get("canceled_at"))
    local_subscription.raw_payload = _stripe_to_dict(stripe_subscription)

    user = User.query.get(local_subscription.user_id) if local_subscription.user_id else None
    if user:
        user.subscription_status = local_subscription.status or user.subscription_status

    return local_subscription


def _latest_subscription_for_user(user_id: str):
    return (
        Subscription.query.filter_by(user_id=user_id)
        .order_by(Subscription.updated_at.desc(), Subscription.created_at.desc())
        .first()
    )


def _trial_days_remaining(trial_ends_at):
    trial_ends_at = _as_utc_naive(trial_ends_at)
    if not trial_ends_at:
        return 0
    now = datetime.utcnow()
    if trial_ends_at <= now:
        return 0
    seconds_remaining = (trial_ends_at - now).total_seconds()
    return max(math.ceil(seconds_remaining / 86400), 0)


def _serialize_access_status(user: User, subscription: Optional[Subscription]):
    now = datetime.utcnow()
    subscription_status = (subscription.status if subscription else user.subscription_status) or "none"
    trial_ends_at = _as_utc_naive(user.trial_ends_at)
    trial_started_at = _as_utc_naive(user.trial_started_at)
    trial_active = bool(trial_ends_at and trial_ends_at > now)
    has_active_subscription = bool(subscription and subscription_status in ACTIVE_SUBSCRIPTION_STATUSES)

    if has_active_subscription:
        access_status = "subscribed"
    elif trial_active:
        access_status = "trialing"
    elif user.trial_used:
        access_status = "trial_expired"
    else:
        access_status = "none"

    return {
        "accessStatus": access_status,
        "subscriptionStatus": subscription_status,
        "trial": {
            "isActive": trial_active,
            "used": bool(user.trial_used),
            "daysRemaining": _trial_days_remaining(trial_ends_at),
            "startedAt": trial_started_at.isoformat() if trial_started_at else None,
            "endsAt": trial_ends_at.isoformat() if trial_ends_at else None,
        },
        "subscription": _serialize_subscription(subscription) if subscription else None,
    }


def _serialize_subscription(subscription: Subscription):
    return {
        "id": subscription.id,
        "status": subscription.status,
        "stripeProductId": subscription.stripe_product_id,
        "stripePriceId": subscription.stripe_price_id,
        "stripeCustomerId": subscription.stripe_customer_id,
        "stripeSubscriptionId": subscription.stripe_subscription_id,
        "amountCents": subscription.amount_cents,
        "currency": subscription.currency,
        "interval": subscription.interval,
        "currentPeriodStart": subscription.current_period_start.isoformat() if subscription.current_period_start else None,
        "currentPeriodEnd": subscription.current_period_end.isoformat() if subscription.current_period_end else None,
        "cancelAtPeriodEnd": subscription.cancel_at_period_end,
        "canceledAt": subscription.canceled_at.isoformat() if subscription.canceled_at else None,
        "createdAt": subscription.created_at.isoformat() if subscription.created_at else None,
        "updatedAt": subscription.updated_at.isoformat() if subscription.updated_at else None,
    }


@billing_bp.get("/pricing")
def pricing():
    return jsonify(
        plan="annual_all_access",
        productId=STRIPE_PRODUCT_ID,
        amountCents=STRIPE_PRICE_CENTS,
        amountDisplay="$30",
        currency=STRIPE_CURRENCY,
        interval=STRIPE_INTERVAL,
        trialDays=TRIAL_DAYS,
    )


@billing_bp.get("/subscription")
@jwt_required()
def get_subscription():
    user_id = get_jwt_identity()

    subscription = _latest_subscription_for_user(user_id)

    return jsonify(subscription=_serialize_subscription(subscription) if subscription else None)


@billing_bp.get("/access-status")
@jwt_required()
def get_access_status():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(error="User not found"), 404

    subscription = _latest_subscription_for_user(user_id)
    return jsonify(_serialize_access_status(user, subscription)), 200


@billing_bp.post("/start-trial")
@jwt_required()
def start_trial():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(error="User not found"), 404

    subscription = _latest_subscription_for_user(user_id)
    access_status = _serialize_access_status(user, subscription)
    if access_status["accessStatus"] == "subscribed":
        return jsonify(error="Subscription already active"), 400
    if access_status["accessStatus"] == "trialing":
        return jsonify(access_status), 200
    if user.trial_used:
        return jsonify(error="Trial already used"), 400

    now = datetime.utcnow()
    user.trial_started_at = now
    user.trial_ends_at = now + timedelta(days=TRIAL_DAYS)
    user.trial_used = True
    user.subscription_status = "none"
    db.session.commit()

    refreshed_status = _serialize_access_status(user, _latest_subscription_for_user(user_id))
    return jsonify(refreshed_status), 200


@billing_bp.post("/checkout-session")
@jwt_required()
def create_checkout_session():
    secret_key = _stripe_secret_key()
    if not secret_key:
        return jsonify(error="STRIPE_SECRET_KEY is not configured"), 500

    stripe.api_key = secret_key
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(error="User not found"), 404

    frontend_url = _frontend_url()
    data = request.get_json(silent=True) or {}
    safe_redirect = _safe_redirect_path(data.get("redirect"))
    encoded_redirect = quote(safe_redirect, safe="")

    latest_customer_subscription = (
        Subscription.query.filter_by(user_id=user_id)
        .filter(Subscription.stripe_customer_id.isnot(None))
        .order_by(Subscription.updated_at.desc(), Subscription.created_at.desc())
        .first()
    )
    stripe_customer_id = latest_customer_subscription.stripe_customer_id if latest_customer_subscription else None

    try:
        if not stripe_customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                name=f"{(user.first_name or '').strip()} {(user.last_name or '').strip()}".strip() or user.username,
                metadata={"user_id": user.id},
            )
            stripe_customer_id = customer.id

        session = stripe.checkout.Session.create(
            mode="subscription",
            customer=stripe_customer_id,
            client_reference_id=user.id,
            success_url=f"{frontend_url}/pricing?success=1&redirect={encoded_redirect}",
            cancel_url=f"{frontend_url}/pricing?canceled=1&redirect={encoded_redirect}",
            line_items=[
                {
                    "price_data": {
                        "currency": STRIPE_CURRENCY,
                        "product": STRIPE_PRODUCT_ID,
                        "unit_amount": STRIPE_PRICE_CENTS,
                        "recurring": {"interval": STRIPE_INTERVAL},
                    },
                    "quantity": 1,
                }
            ],
            metadata={"user_id": user.id},
            subscription_data={"metadata": {"user_id": user.id}},
        )

        pending_subscription = Subscription(
            user_id=user.id,
            stripe_customer_id=stripe_customer_id,
            stripe_checkout_session_id=session.id,
            stripe_product_id=STRIPE_PRODUCT_ID,
            status="checkout_created",
            amount_cents=STRIPE_PRICE_CENTS,
            currency=STRIPE_CURRENCY,
            interval=STRIPE_INTERVAL,
            raw_payload={"checkout_session": _stripe_to_dict(session)},
        )
        db.session.add(pending_subscription)
        user.subscription_status = "checkout_created"
        db.session.commit()

        return jsonify(url=session.url, sessionId=session.id), 200
    except stripe.error.StripeError as exc:
        db.session.rollback()
        return jsonify(error=str(exc)), 400


@billing_bp.post("/webhook")
def stripe_webhook():
    secret_key = _stripe_secret_key()
    webhook_secret = _stripe_webhook_secret()
    if not secret_key or not webhook_secret:
        return jsonify(error="Stripe webhook is not configured"), 500

    stripe.api_key = secret_key

    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    if not sig_header:
        return jsonify(error="Missing Stripe-Signature header"), 400

    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=sig_header, secret=webhook_secret)
    except ValueError:
        return jsonify(error="Invalid payload"), 400
    except stripe.error.SignatureVerificationError:
        return jsonify(error="Invalid signature"), 400

    event_payload = _stripe_to_dict(event)

    existing_event = StripeWebhookEvent.query.get(event_payload["id"])
    if existing_event:
        return jsonify(received=True, duplicate=True), 200

    webhook_event = StripeWebhookEvent(
        id=event_payload["id"],
        event_type=event_payload["type"],
        stripe_created_at=_to_datetime(event_payload.get("created")),
        payload=event_payload,
        processed=False,
    )
    db.session.add(webhook_event)

    try:
        event_type = event_payload["type"]
        event_object = event_payload["data"]["object"]

        if event_type == "checkout.session.completed":
            if event_object.get("mode") == "subscription":
                subscription_id = event_object.get("subscription")
                user_id = event_object.get("client_reference_id")
                logger.info(f"Checkout completed: subscription_id={subscription_id}, user_id={user_id}")
                if subscription_id:
                    stripe_subscription = stripe.Subscription.retrieve(subscription_id)
                    logger.info(f"Retrieved Stripe subscription: current_period_end={stripe_subscription.get('current_period_end')}")
                    local_sub = _sync_subscription(
                        stripe_subscription,
                        fallback_user_id=user_id,
                        checkout_session_id=event_object.get("id"),
                    )
                    logger.info(f"Synced subscription: id={local_sub.id}, current_period_end={local_sub.current_period_end}")

        elif event_type in {
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
        }:
            logger.info(f"Subscription event: {event_type}, sub_id={event_object.get('id')}, period_end={event_object.get('current_period_end')}")
            local_sub = _sync_subscription(event_object)
            logger.info(f"Synced from {event_type}: id={local_sub.id}, current_period_end={local_sub.current_period_end}")

        elif event_type in {"invoice.payment_succeeded", "invoice.payment_failed"}:
            subscription_id = event_object.get("subscription")
            if subscription_id:
                stripe_subscription = stripe.Subscription.retrieve(subscription_id)
                _sync_subscription(stripe_subscription)

        webhook_event.processed = True
        db.session.commit()
        return jsonify(received=True), 200
    except Exception as exc:
        webhook_event.processing_error = str(exc)
        db.session.commit()
        return jsonify(error="Webhook processing failed"), 500
