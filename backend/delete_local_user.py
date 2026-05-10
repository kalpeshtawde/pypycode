#!/usr/bin/env python3
"""Delete a user and all related data from the local DB, respecting FK order.

Usage:
    python delete_local_user.py user@example.com
"""
import sys
from app import create_app, db
from app.models import User


def delete_user(email: str):
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"ERROR: No user found with email '{email}'")
            sys.exit(1)

        uid = user.id
        print(f"Found user: {uid} ({email})")

        # Delete in FK-safe order (children before parent)
        counts = {}
        for table, col in [
            ("favorites",             "user_id"),
            ("subscriptions",         "user_id"),
            ("problem_project_stats", "user_id"),
            ("submissions",           "user_id"),
            ("projects",              "user_id"),
        ]:
            result = db.session.execute(
                db.text(f"DELETE FROM {table} WHERE {col} = :uid"),
                {"uid": uid},
            )
            counts[table] = result.rowcount

        result = db.session.execute(
            db.text("DELETE FROM contacts WHERE email = :email"),
            {"email": email},
        )
        counts["contacts"] = result.rowcount

        db.session.execute(
            db.text("DELETE FROM users WHERE id = :uid"),
            {"uid": uid},
        )
        db.session.commit()

        print("Deleted:")
        for table, n in counts.items():
            if n:
                print(f"  {table}: {n} row(s)")
        print(f"  users: 1 row")
        print("Done.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python delete_local_user.py <email>")
        sys.exit(1)
    delete_user(sys.argv[1])
