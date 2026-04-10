import os
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

    return app


app = create_app()
