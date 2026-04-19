import os
import json
import sys
import subprocess
import tempfile
from flask import Flask
import click
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
    from app.api_docs import register_api_docs

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(problems_bp, url_prefix="/problems")
    app.register_blueprint(projects_bp, url_prefix="/projects")
    app.register_blueprint(submissions_bp, url_prefix="/submissions")
    app.register_blueprint(leaderboard_bp, url_prefix="/leaderboard")
    app.register_blueprint(contact_bp, url_prefix="/contact")
    app.register_blueprint(billing_bp, url_prefix="/billing")
    app.register_blueprint(favorites_bp, url_prefix="/favorites")
    register_api_docs(app)

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

    @app.cli.command("sync-remote-db")
    @click.option("--env-file", default=".env.db-sync", show_default=True, help="Path to env file with SSH and DB settings")
    @click.option("--yes", is_flag=True, help="Skip confirmation prompt before local DB overwrite")
    def sync_remote_db(env_file: str, yes: bool):
        """Sync remote Postgres DB to local DB through SSH tunnel."""
        from dotenv import dotenv_values
        from sshtunnel import SSHTunnelForwarder

        cfg = dotenv_values(env_file)
        required = [
            "SSH_HOST",
            "SSH_USER",
            "REMOTE_DB_HOST",
            "REMOTE_DB_PORT",
            "REMOTE_DB_NAME",
            "REMOTE_DB_USER",
            "REMOTE_DB_PASSWORD",
            "LOCAL_DB_HOST",
            "LOCAL_DB_PORT",
            "LOCAL_DB_NAME",
            "LOCAL_DB_USER",
            "LOCAL_DB_PASSWORD",
        ]
        missing = [key for key in required if not cfg.get(key)]
        if missing:
            raise click.ClickException(f"Missing required env vars: {', '.join(missing)}")

        if not yes:
            click.echo(
                f"This will overwrite local DB '{cfg['LOCAL_DB_NAME']}' on {cfg['LOCAL_DB_HOST']}:{cfg['LOCAL_DB_PORT']}."
            )
            if not click.confirm("Continue?"):
                click.echo("Cancelled")
                return

        ssh_kwargs = {"ssh_username": cfg["SSH_USER"]}
        if cfg.get("SSH_PRIVATE_KEY"):
            ssh_kwargs["ssh_pkey"] = cfg["SSH_PRIVATE_KEY"]
            if cfg.get("SSH_PRIVATE_KEY_PASSPHRASE"):
                ssh_kwargs["ssh_private_key_password"] = cfg["SSH_PRIVATE_KEY_PASSPHRASE"]
        elif cfg.get("SSH_PASSWORD"):
            ssh_kwargs["ssh_password"] = cfg["SSH_PASSWORD"]

        def run_or_fail(cmd: list[str], env: dict[str, str], step: str):
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            if result.returncode != 0:
                stderr = (result.stderr or "").strip()
                raise click.ClickException(f"{step} failed: {stderr or 'Unknown error'}")

        dump_path = ""
        with tempfile.NamedTemporaryFile(suffix=".dump", delete=False) as tmp:
            dump_path = tmp.name

        try:
            click.echo("Opening SSH tunnel...")
            with SSHTunnelForwarder(
                (cfg["SSH_HOST"], int(cfg.get("SSH_PORT") or 22)),
                remote_bind_address=(cfg["REMOTE_DB_HOST"], int(cfg["REMOTE_DB_PORT"])),
                local_bind_address=("127.0.0.1", 0),
                **ssh_kwargs,
            ) as tunnel:
                click.echo("Dumping remote database...")
                dump_env = os.environ.copy()
                dump_env["PGPASSWORD"] = cfg["REMOTE_DB_PASSWORD"]
                run_or_fail(
                    [
                        "pg_dump",
                        "-h",
                        "127.0.0.1",
                        "-p",
                        str(tunnel.local_bind_port),
                        "-U",
                        cfg["REMOTE_DB_USER"],
                        "-d",
                        cfg["REMOTE_DB_NAME"],
                        "-F",
                        "c",
                        "--no-owner",
                        "--no-privileges",
                        "-f",
                        dump_path,
                    ],
                    dump_env,
                    "Remote dump",
                )

            click.echo("Resetting local schema...")
            local_env = os.environ.copy()
            local_env["PGPASSWORD"] = cfg["LOCAL_DB_PASSWORD"]
            run_or_fail(
                [
                    "psql",
                    "-h",
                    cfg["LOCAL_DB_HOST"],
                    "-p",
                    str(cfg["LOCAL_DB_PORT"]),
                    "-U",
                    cfg["LOCAL_DB_USER"],
                    "-d",
                    cfg["LOCAL_DB_NAME"],
                    "-v",
                    "ON_ERROR_STOP=1",
                    "-c",
                    "DROP SCHEMA public CASCADE; CREATE SCHEMA public;",
                ],
                local_env,
                "Local schema reset",
            )

            click.echo("Restoring dump to local database...")
            run_or_fail(
                [
                    "pg_restore",
                    "-h",
                    cfg["LOCAL_DB_HOST"],
                    "-p",
                    str(cfg["LOCAL_DB_PORT"]),
                    "-U",
                    cfg["LOCAL_DB_USER"],
                    "-d",
                    cfg["LOCAL_DB_NAME"],
                    "--no-owner",
                    "--no-privileges",
                    dump_path,
                ],
                local_env,
                "Local restore",
            )

            click.echo("Remote DB synced to local DB successfully")
        finally:
            if dump_path and os.path.exists(dump_path):
                os.remove(dump_path)

    return app


app = create_app()
