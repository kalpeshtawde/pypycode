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
    first_name = data.get("firstName", "").strip()
    last_name = data.get("lastName", "").strip()
    screen_name = data.get("screenName", "").strip()
    
    if not token:
        return jsonify(error="Missing token"), 400
    
    try:
        def is_profile_complete(u: User) -> bool:
            return bool(u.first_name and u.last_name and u.screen_name)

        def normalize_and_validate_screen_name(raw_screen_name: str):
            handle = raw_screen_name.lstrip("@").strip()
            normalized = f"@{handle}" if handle else ""
            if not handle.replace("_", "").isalnum():
                return None, None
            return handle, normalized

        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        
        google_id = idinfo.get("sub")
        email = idinfo.get("email")
        
        # Check if user exists by google_id
        user = User.query.filter_by(google_id=google_id).first()
        
        if user:
            if not is_profile_complete(user):
                if not first_name or not last_name or not screen_name:
                    return jsonify(
                        requiresProfileSetup=True,
                        is_new=False,
                        firstName=user.first_name,
                        lastName=user.last_name,
                        screenName=user.screen_name,
                    ), 200

                handle, normalized_screen_name = normalize_and_validate_screen_name(screen_name)
                if not normalized_screen_name:
                    return jsonify(error="Screen name can only contain letters, numbers, and underscores"), 400

                taken = User.query.filter(
                    User.screen_name == normalized_screen_name,
                    User.id != user.id,
                ).first()
                if taken:
                    return jsonify(error="Screen name already taken"), 409

                user.first_name = first_name
                user.last_name = last_name
                user.screen_name = normalized_screen_name
                db.session.commit()

            # User exists, log them in
            token = create_access_token(identity=str(user.id))
            return jsonify(
                token=token,
                username=user.username,
                screenName=user.screen_name,
                firstName=user.first_name,
                lastName=user.last_name,
                is_new=False
            ), 200
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # Link Google account to existing user
            existing_user.google_id = google_id
            if not is_profile_complete(existing_user):
                if not first_name or not last_name or not screen_name:
                    db.session.commit()
                    return jsonify(
                        requiresProfileSetup=True,
                        is_new=False,
                        firstName=existing_user.first_name,
                        lastName=existing_user.last_name,
                        screenName=existing_user.screen_name,
                    ), 200

                handle, normalized_screen_name = normalize_and_validate_screen_name(screen_name)
                if not normalized_screen_name:
                    return jsonify(error="Screen name can only contain letters, numbers, and underscores"), 400

                taken = User.query.filter(
                    User.screen_name == normalized_screen_name,
                    User.id != existing_user.id,
                ).first()
                if taken:
                    return jsonify(error="Screen name already taken"), 409

                existing_user.first_name = first_name
                existing_user.last_name = last_name
                existing_user.screen_name = normalized_screen_name

            db.session.commit()
            token = create_access_token(identity=str(existing_user.id))
            return jsonify(
                token=token,
                username=existing_user.username,
                screenName=existing_user.screen_name,
                firstName=existing_user.first_name,
                lastName=existing_user.last_name,
                is_new=False
            ), 200
        
        # New user - require first name, last name, and screen name
        if not first_name or not last_name or not screen_name:
            return jsonify(requiresProfileSetup=True, is_new=True), 200

        handle, normalized_screen_name = normalize_and_validate_screen_name(screen_name)
        
        # Check if screen name handle is valid (alphanumeric and underscores only)
        if not normalized_screen_name:
            return jsonify(error="Screen name can only contain letters, numbers, and underscores"), 400
        
        # Check if screen name already exists
        if User.query.filter_by(screen_name=normalized_screen_name).first():
            return jsonify(error="Screen name already taken"), 409
        
        # Generate username from screen name handle
        username = handle
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{handle}{counter}"
            counter += 1
        
        new_user = User(
            username=username,
            email=email,
            google_id=google_id,
            first_name=first_name,
            last_name=last_name,
            screen_name=normalized_screen_name
        )
        db.session.add(new_user)
        db.session.commit()
        
        token = create_access_token(identity=str(new_user.id))
        return jsonify(
            token=token,
            username=new_user.username,
            screenName=new_user.screen_name,
            firstName=new_user.first_name,
            lastName=new_user.last_name,
            is_new=True
        ), 201
        
    except ValueError as e:
        return jsonify(error="Invalid token"), 401
    except Exception as e:
        return jsonify(error=str(e)), 500


@auth_bp.post("/signup")
def signup():
    """Create a new user account with email and password"""
    data = request.get_json()
    
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    first_name = data.get("firstName", "").strip()
    last_name = data.get("lastName", "").strip()
    screen_name = data.get("screenName", "").strip()
    
    # Validation
    if not email or not password or not screen_name:
        return jsonify(error="Email, password, and screen name are required"), 400
    
    if len(password) < 6:
        return jsonify(error="Password must be at least 6 characters"), 400
    
    handle = screen_name.lstrip("@").strip()
    normalized_screen_name = f"@{handle}" if handle else ""

    # Check if screen name handle is valid (alphanumeric and underscores only)
    if not handle.replace("_", "").isalnum():
        return jsonify(error="Screen name can only contain letters, numbers, and underscores"), 400
    
    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify(error="Email already registered"), 409
    
    # Check if screen name already exists
    if User.query.filter_by(screen_name=normalized_screen_name).first():
        return jsonify(error="Screen name already taken"), 409

    # Generate username from screen name handle
    username = handle
    counter = 1
    while User.query.filter_by(username=username).first():
        username = f"{handle}{counter}"
        counter += 1
    
    # Create new user
    new_user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        screen_name=normalized_screen_name
    )
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    token = create_access_token(identity=str(new_user.id))
    return jsonify(
        token=token,
        username=new_user.username,
        screenName=new_user.screen_name,
        firstName=new_user.first_name,
        lastName=new_user.last_name,
        is_new=True
    ), 201


@auth_bp.post("/login")
def login():
    """Login with email and password"""
    data = request.get_json()
    
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    
    if not email or not password:
        return jsonify(error="Email and password are required"), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify(error="Invalid email or password"), 401
    
    token = create_access_token(identity=str(user.id))
    return jsonify(
        token=token,
        username=user.username,
        screenName=user.screen_name,
        firstName=user.first_name,
        lastName=user.last_name
    ), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(error="Not found"), 404
    return jsonify(
        id=user.id,
        username=user.username,
        email=user.email,
        firstName=user.first_name,
        lastName=user.last_name,
        screenName=user.screen_name
    )
