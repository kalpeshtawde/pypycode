from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify(error="Missing fields"), 400
    if User.query.filter(
        (User.email == data["email"]) | (User.username == data["username"])
    ).first():
        return jsonify(error="User already exists"), 409
    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=str(user.id))
    return jsonify(token=token, username=user.username), 201


@auth_bp.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password", "")):
        return jsonify(error="Invalid credentials"), 401
    token = create_access_token(identity=str(user.id))
    return jsonify(token=token, username=user.username)


@auth_bp.get("/me")
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify(error="Not found"), 404
    return jsonify(id=user.id, username=user.username, email=user.email)
