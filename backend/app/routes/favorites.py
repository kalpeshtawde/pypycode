from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Favorite, Problem, User
from app import db

favorites_bp = Blueprint("favorites", __name__)


def _problem_to_dict(problem: Problem):
    return {
        "id": problem.id,
        "slug": problem.slug,
        "title": problem.title,
        "difficulty": problem.difficulty,
        "tags": problem.tags or [],
    }


@favorites_bp.get("/")
@jwt_required()
def list_favorites():
    """List all favorite problems for the current user"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(error="User not found"), 404

    favorites = Favorite.query.filter_by(user_id=user_id).join(Problem).all()

    return jsonify({
        "favorites": [
            {
                "id": fav.id,
                "createdAt": fav.created_at.isoformat(),
                "problem": _problem_to_dict(fav.problem),
            }
            for fav in favorites
        ]
    })


@favorites_bp.post("/")
@jwt_required()
def add_favorite():
    """Add a problem to user's favorites"""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    problem_id = data.get("problemId")

    if not problem_id:
        return jsonify(error="problemId is required"), 400

    problem = Problem.query.get(problem_id)
    if not problem:
        return jsonify(error="Problem not found"), 404

    existing = Favorite.query.filter_by(user_id=user_id, problem_id=problem_id).first()
    if existing:
        return jsonify(error="Problem is already in favorites"), 409

    favorite = Favorite(user_id=user_id, problem_id=problem_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "id": favorite.id,
        "createdAt": favorite.created_at.isoformat(),
        "problem": _problem_to_dict(favorite.problem),
    }), 201


@favorites_bp.delete("/<problem_id>")
@jwt_required()
def remove_favorite(problem_id: str):
    """Remove a problem from user's favorites"""
    user_id = get_jwt_identity()

    favorite = Favorite.query.filter_by(user_id=user_id, problem_id=problem_id).first()
    if not favorite:
        return jsonify(error="Favorite not found"), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed"}), 200


@favorites_bp.get("/check/<problem_id>")
@jwt_required()
def check_favorite(problem_id: str):
    """Check if a problem is in user's favorites"""
    user_id = get_jwt_identity()

    favorite = Favorite.query.filter_by(user_id=user_id, problem_id=problem_id).first()

    return jsonify({"isFavorite": favorite is not None})
