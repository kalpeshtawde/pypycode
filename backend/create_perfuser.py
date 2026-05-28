#!/usr/bin/env python3
"""
One-time script to create the perfuser for local performance testing.

Usage:
    cd backend
    PERF_USER_EMAIL=perfuser@local.test PERF_USER_PASSWORD=changeme python create_perfuser.py

Or put credentials in backend/.env and run:
    python create_perfuser.py
"""
import os
import sys
from datetime import datetime, timezone, timedelta

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass  # Running inside Docker — env vars already injected by the container

TRIAL_YEARS = 100  # effectively permanent

PERF_EMAIL = os.environ.get("PERF_USER_EMAIL", "perfuser@local.test")
PERF_PASSWORD = os.environ.get("PERF_USER_PASSWORD", "")
PERF_SCREEN_NAME = "@perfuser"
PERF_PROJECT_NAME = "Perf Default"


def main():
    if not PERF_PASSWORD:
        print("Error: PERF_USER_PASSWORD env var is required")
        sys.exit(1)

    from app import create_app, db
    from app.models import User, Project

    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=PERF_EMAIL).first()

        now = datetime.now(timezone.utc)
        trial_end = now + timedelta(days=365 * TRIAL_YEARS)

        if user:
            print(f"User {PERF_EMAIL} already exists (id={user.id}), updating password + trial...")
            user.set_password(PERF_PASSWORD)
            user.trial_started_at = now
            user.trial_ends_at = trial_end
            user.trial_used = True
            db.session.commit()
        else:
            handle = "perfuser"
            username = handle
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{handle}{counter}"
                counter += 1

            screen_name = PERF_SCREEN_NAME
            if User.query.filter_by(screen_name=screen_name).first():
                screen_name = f"@perfuser_{counter}"

            user = User(
                username=username,
                email=PERF_EMAIL,
                first_name="Perf",
                last_name="User",
                screen_name=screen_name,
                trial_started_at=now,
                trial_ends_at=trial_end,
                trial_used=True,
            )
            user.set_password(PERF_PASSWORD)
            db.session.add(user)
            db.session.flush()
            print(f"Created perfuser: {PERF_EMAIL} (id={user.id})")

        default_project = Project.query.filter_by(user_id=user.id, is_default=True).first()
        if not default_project:
            default_project = Project(
                user_id=user.id,
                name=PERF_PROJECT_NAME,
                is_default=True,
            )
            db.session.add(default_project)
            print(f"Created default project: {PERF_PROJECT_NAME}")
        else:
            print(f"Default project already exists: {default_project.name} (id={default_project.id})")

        db.session.commit()
        print("Done.")
        print(f"  email   : {PERF_EMAIL}")
        print(f"  username: {user.username}")
        print(f"  project : {default_project.name} (id={default_project.id})")


if __name__ == "__main__":
    main()
