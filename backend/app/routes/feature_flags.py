from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import FeatureFlag, User
from app import db

feature_flags_bp = Blueprint("feature_flags", __name__)


def _is_admin(user_id: str) -> bool:
    user = User.query.get(user_id)
    return user is not None and user.is_admin


@feature_flags_bp.get("/")
@jwt_required()
def list_feature_flags():
    """List all feature flags (admin only)"""
    user_id = get_jwt_identity()
    if not _is_admin(user_id):
        return jsonify(error="Admin access required"), 403

    flags = FeatureFlag.query.order_by(FeatureFlag.name).all()
    return jsonify({
        "featureFlags": [
            {
                "id": flag.id,
                "name": flag.name,
                "enabled": flag.enabled,
                "createdAt": flag.created_at.isoformat() if flag.created_at else None,
                "updatedAt": flag.updated_at.isoformat() if flag.updated_at else None,
            }
            for flag in flags
        ]
    })


@feature_flags_bp.post("/")
@jwt_required()
def create_feature_flag():
    """Create a new feature flag (admin only)"""
    user_id = get_jwt_identity()
    if not _is_admin(user_id):
        return jsonify(error="Admin access required"), 403

    data = request.get_json() or {}
    name = data.get("name", "").strip()
    enabled = data.get("enabled", False)

    if not name:
        return jsonify(error="Flag name is required"), 400

    existing = FeatureFlag.query.filter_by(name=name).first()
    if existing:
        return jsonify(error="Feature flag with this name already exists"), 409

    flag = FeatureFlag(name=name, enabled=enabled)
    db.session.add(flag)
    db.session.commit()

    return jsonify({
        "id": flag.id,
        "name": flag.name,
        "enabled": flag.enabled,
        "createdAt": flag.created_at.isoformat() if flag.created_at else None,
        "updatedAt": flag.updated_at.isoformat() if flag.updated_at else None,
    }), 201


@feature_flags_bp.put("/<flag_id>")
@jwt_required()
def update_feature_flag(flag_id: str):
    """Update a feature flag (admin only)"""
    user_id = get_jwt_identity()
    if not _is_admin(user_id):
        return jsonify(error="Admin access required"), 403

    flag = FeatureFlag.query.get(flag_id)
    if not flag:
        return jsonify(error="Feature flag not found"), 404

    data = request.get_json() or {}
    enabled = data.get("enabled")

    if enabled is not None:
        flag.enabled = enabled

    db.session.commit()

    return jsonify({
        "id": flag.id,
        "name": flag.name,
        "enabled": flag.enabled,
        "createdAt": flag.created_at.isoformat() if flag.created_at else None,
        "updatedAt": flag.updated_at.isoformat() if flag.updated_at else None,
    })


@feature_flags_bp.delete("/<flag_id>")
@jwt_required()
def delete_feature_flag(flag_id: str):
    """Delete a feature flag (admin only)"""
    user_id = get_jwt_identity()
    if not _is_admin(user_id):
        return jsonify(error="Admin access required"), 403

    flag = FeatureFlag.query.get(flag_id)
    if not flag:
        return jsonify(error="Feature flag not found"), 404

    db.session.delete(flag)
    db.session.commit()

    return jsonify({"message": "Feature flag deleted"}), 200
