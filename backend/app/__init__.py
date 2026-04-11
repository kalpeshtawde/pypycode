import os
import json
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery
from app.config import CONFIGS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
celery_app = Celery(include=["app.services.runner"])


def create_app():
    app = Flask(__name__)

    config_name = os.environ.get("APP_CONFIG", "default")
    config_cls = CONFIGS.get(config_name, CONFIGS["default"])
    app.config.from_object(config_cls)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE_URL (or PERF_DATABASE_URL for APP_CONFIG=perf) is required")

    CORS(app, origins=app.config.get("ALLOWED_ORIGINS", "*").split(","))

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Configure Celery
    celery_app.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask

    from app.routes.auth import auth_bp
    from app.routes.problems import problems_bp
    from app.routes.projects import projects_bp
    from app.routes.submissions import submissions_bp
    from app.routes.leaderboard import leaderboard_bp
    from app.routes.billing import billing_bp
    from app.routes.favorites import favorites_bp
    from app.routes import auth, problems, projects, submissions, leaderboard, contact, billing, favorites
    from app.routes.contact import contact_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(problems_bp, url_prefix="/problems")
    app.register_blueprint(projects_bp, url_prefix="/projects")
    app.register_blueprint(submissions_bp, url_prefix="/submissions")
    app.register_blueprint(leaderboard_bp, url_prefix="/leaderboard")
    app.register_blueprint(contact_bp, url_prefix="/contact")
    app.register_blueprint(billing_bp, url_prefix="/billing")
    app.register_blueprint(favorites_bp, url_prefix="/favorites")

    from app.admin import init_admin
    init_admin(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    # CLI command to validate all problems
    @app.cli.command("validate-problems")
    def validate_problems():
        """Validate all problems have valid test cases."""
        from app.models import Problem

        print("=" * 70)
        print("PROBLEM VALIDATION REPORT")
        print("=" * 70)
        print()

        problems = Problem.query.all()
        total = len(problems)
        passed = 0
        failed = 0
        failed_slugs = []

        print(f"Found {total} problems to validate...")
        print()

        for idx, problem in enumerate(problems, 1):
            errors = []

            # Check basic fields
            if not problem.slug:
                errors.append("Missing slug")
            if not problem.title:
                errors.append("Missing title")
            if not problem.difficulty:
                errors.append("Missing difficulty")

            # Validate test cases
            test_cases = problem.test_cases or []
            if not test_cases:
                errors.append("No test cases")
            else:
                for i, tc in enumerate(test_cases):
                    # Check required fields
                    if "expected" not in tc:
                        errors.append(f"Test case {i+1}: missing 'expected'")
                        continue

                    expected = tc.get("expected")

                    # Try to parse string expected values as JSON
                    if isinstance(expected, str):
                        try:
                            json.loads(expected)
                        except json.JSONDecodeError:
                            # Non-JSON strings are OK (like "multiple found")
                            pass

                    # Check function name
                    if not tc.get("function"):
                        errors.append(f"Test case {i+1}: missing 'function'")

                    # Check input or args
                    if "input" not in tc and "args" not in tc:
                        errors.append(f"Test case {i+1}: missing 'input' or 'args'")

            # Validate examples
            examples = problem.examples or []
            if not examples:
                errors.append("No examples")

            # Report result
            if errors:
                failed += 1
                failed_slugs.append(problem.slug)
                print(f"[{idx:4d}/{total:4d}] ❌ {problem.slug}")
                for err in errors:
                    print(f"         → {err}")
                print()
            else:
                passed += 1
                print(f"[{idx:4d}/{total:4d}] ✅ {problem.slug}")

        print()
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Total:    {total}")
        print(f"Passed:   {passed} ✅")
        print(f"Failed:   {failed} ❌")
        print()

        if failed_slugs:
            print("Failed problems:")
            for slug in failed_slugs:
                print(f"  - {slug}")
            print()

        if failed > 0:
            print("Exiting with error code 1")
            sys.exit(1)
        else:
            print("All problems validated successfully!")
            sys.exit(0)

    return app


app = create_app()
