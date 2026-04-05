from flask import Blueprint, jsonify
from sqlalchemy import func
from app import db
from app.models import Submission, User

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.get("/")
def leaderboard():
    rows = (
        db.session.query(
            User.id,
            User.username,
            User.screen_name,
            User.first_name,
            User.last_name,
            func.count(Submission.problem_id.distinct()).label("solved"),
        )
        .join(Submission, Submission.user_id == User.id)
        .filter(Submission.status == "accepted")
        .group_by(User.id, User.username, User.screen_name, User.first_name, User.last_name)
        .order_by(func.count(Submission.problem_id.distinct()).desc())
        .limit(50)
        .all()
    )
    
    result = []
    for i, row in enumerate(rows):
        user_id, username, screen_name, first_name, last_name, solved = row
        
        # Use screen_name if available, otherwise use first_name + last_name, fallback to username
        if screen_name:
            display_name = screen_name
        elif first_name or last_name:
            display_name = f"{first_name or ''} {last_name or ''}".strip()
        else:
            display_name = username
        
        result.append({
            "rank": i + 1,
            "displayName": display_name,
            "username": display_name,
            "solved": solved
        })
    
    return jsonify(result)
