from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from google.auth.transport import requests
from google.oauth2 import id_token
from app import db
from app.models import User
import os

auth_bp = Blueprint("auth", __name__)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


@auth_bp.post("/google")
def google_auth():
    """Authenticate user with Google ID token"""
    data = request.get_json()
    token = data.get("token")
    
    if not token:
        return jsonify(error="Missing token"), 400
    
    try:
        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        
        google_id = idinfo.get("sub")
        email = idinfo.get("email")
        name = idinfo.get("name", "").split()[0] if idinfo.get("name") else "User"
        
        # Check if user exists by google_id
        user = User.query.filter_by(google_id=google_id).first()
        
        if user:
            # User exists, just log them in
            token = create_access_token(identity=str(user.id))
            return jsonify(token=token, username=user.username, is_new=False), 200
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # Link Google account to existing user
            existing_user.google_id = google_id
            db.session.commit()
            token = create_access_token(identity=str(existing_user.id))
            return jsonify(token=token, username=existing_user.username, is_new=False), 200
        
        # Create new user
        username = email.split("@")[0]
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{email.split('@')[0]}{counter}"
            counter += 1
        
        new_user = User(username=username, email=email, google_id=google_id)
        db.session.add(new_user)
        db.session.commit()
        
        token = create_access_token(identity=str(new_user.id))
        return jsonify(token=token, username=new_user.username, is_new=True), 201
        
    except ValueError as e:
        return jsonify(error="Invalid token"), 401
    except Exception as e:
        return jsonify(error=str(e)), 500


@auth_bp.get("/me")
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify(error="Not found"), 404
    return jsonify(id=user.id, username=user.username, email=user.email)
