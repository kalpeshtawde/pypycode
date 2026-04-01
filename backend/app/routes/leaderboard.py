from flask import Blueprint, jsonify
from sqlalchemy import func
from app import db
from app.models import Submission, User

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.get("/")
def leaderboard():
    rows = (
        db.session.query(
            User.username,
            func.count(Submission.id.distinct()).label("solved"),
        )
        .join(Submission, Submission.user_id == User.id)
        .filter(Submission.status == "accepted")
        .group_by(User.username)
        .order_by(func.count(Submission.id.distinct()).desc())
        .limit(50)
        .all()
    )
    return jsonify([
        {"rank": i + 1, "username": r.username, "solved": r.solved}
        for i, r in enumerate(rows)
    ])
