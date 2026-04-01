import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
celery_app = Celery(include=["app.services.runner"])


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")
    app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600 * 24  # 24h

    app.config["CELERY_BROKER_URL"] = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/1")
    app.config["CELERY_RESULT_BACKEND"] = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/2")

    CORS(app, origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","))

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
    from app.routes.submissions import submissions_bp
    from app.routes.leaderboard import leaderboard_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(problems_bp, url_prefix="/problems")
    app.register_blueprint(submissions_bp, url_prefix="/submissions")
    app.register_blueprint(leaderboard_bp, url_prefix="/leaderboard")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
