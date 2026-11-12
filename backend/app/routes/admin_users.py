from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import case, func, or_

from app import db
from app.models import Submission, Subscription, User
from app.routes.billing import ACTIVE_SUBSCRIPTION_STATUSES, _serialize_access_status

admin_users_bp = Blueprint("admin_users", __name__)

SORT_FIELDS = {"created_at", "username", "email", "solved", "submissions", "last_activity"}


def _current_admin() -> User | None:
    user = User.query.get(get_jwt_identity())
    return user if user and user.is_admin else None


@admin_users_bp.get("/users")
@jwt_required()
def list_users():
    """Paginated user directory with usage and subscription detail (admin only)."""
    if not _current_admin():
        return jsonify(error="Admin access required"), 403

    query_text = (request.args.get("q") or "").strip()
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", 25)), 1), 100)
    except ValueError:
        return jsonify(error="Invalid pagination parameters"), 400

    sort = request.args.get("sort", "created_at")
    if sort not in SORT_FIELDS:
        return jsonify(error="Invalid sort field"), 400

    order = (request.args.get("order") or "desc").lower()
    if order not in {"asc", "desc"}:
        return jsonify(error="Invalid sort order"), 400

    solved_expr = func.count(
        func.distinct(case((Submission.status == "accepted", Submission.problem_id), else_=None))
    )
    stats = (
        db.session.query(
            Submission.user_id.label("user_id"),
            func.count(Submission.id).label("submissions"),
            solved_expr.label("solved"),
            func.max(Submission.created_at).label("last_activity"),
        )
        .group_by(Submission.user_id)
        .subquery()
    )

    query = db.session.query(
        User,
        func.coalesce(stats.c.submissions, 0).label("submissions"),
        func.coalesce(stats.c.solved, 0).label("solved"),
        stats.c.last_activity.label("last_activity"),
    ).outerjoin(stats, stats.c.user_id == User.id)

    if query_text:
        like = f"%{query_text}%"
        query = query.filter(
            or_(
                User.username.ilike(like),
                User.email.ilike(like),
                User.first_name.ilike(like),
                User.last_name.ilike(like),
                User.screen_name.ilike(like),
            )
        )

    sort_columns = {
        "created_at": User.created_at,
        "username": func.lower(User.username),
        "email": func.lower(User.email),
        "solved": func.coalesce(stats.c.solved, 0),
        "submissions": func.coalesce(stats.c.submissions, 0),
        "last_activity": stats.c.last_activity,
    }
    sort_column = sort_columns[sort]
    query = query.order_by(
        sort_column.asc() if order == "asc" else sort_column.desc(),
        User.id.asc(),
    )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    rows = pagination.items

    user_ids = [row[0].id for row in rows]
    latest_subscriptions: dict[str, Subscription] = {}
    if user_ids:
        subscriptions = (
            Subscription.query.filter(Subscription.user_id.in_(user_ids))
            .order_by(Subscription.updated_at.desc(), Subscription.created_at.desc())
            .all()
        )
        for subscription in subscriptions:
            latest_subscriptions.setdefault(subscription.user_id, subscription)

    users = []
    for user, submissions, solved, last_activity in rows:
        access = _serialize_access_status(user, latest_subscriptions.get(user.id))
        users.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "screenName": user.screen_name,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "isAdmin": bool(user.is_admin),
                "provider": "google" if user.google_id else "password",
                "createdAt": user.created_at.isoformat() if user.created_at else None,
                "submissions": int(submissions or 0),
                "solved": int(solved or 0),
                "lastActivityAt": last_activity.isoformat() if last_activity else None,
                "accessStatus": access["accessStatus"],
                "subscriptionStatus": access["subscriptionStatus"],
                "trial": access["trial"],
                "subscription": access["subscription"],
            }
        )

    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    summary = {
        "totalUsers": User.query.count(),
        "newThisWeek": User.query.filter(User.created_at >= week_ago).count(),
        "activeTrials": User.query.filter(
            User.trial_ends_at.isnot(None), User.trial_ends_at > now
        ).count(),
        "activeSubscriptions": db.session.query(func.count(func.distinct(Subscription.user_id)))
        .filter(Subscription.status.in_(ACTIVE_SUBSCRIPTION_STATUSES))
        .scalar()
        or 0,
    }

    return jsonify(
        users=users,
        pagination={
            "page": pagination.page,
            "perPage": pagination.per_page,
            "total": pagination.total,
            "totalPages": pagination.pages,
        },
        summary=summary,
    )
