import os
from sqlalchemy.pool import NullPool


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    db_url = os.environ.get("DATABASE_URL", "")
    if os.environ.get("CELERY_WORKER") == "1":
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "poolclass": NullPool,
        }
    elif db_url.startswith("sqlite") or not db_url:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_size": 3,
            "max_overflow": 2,
        }

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    JWT_ACCESS_TOKEN_EXPIRES = 3600 * 24  # 24h

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/1")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/2")

    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*")
    PROBLEM_INGEST_KEY = os.environ.get("PROBLEM_INGEST_KEY")

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.zoho.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@pypycode.com")
    MAIL_ADMIN_EMAIL = os.environ.get("MAIL_ADMIN_EMAIL")


class PerfConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "PERF_DATABASE_URL",
        os.environ.get("DATABASE_URL", "postgresql://localhost/pypycode_perf"),
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_size": int(os.environ.get("PERF_SQLALCHEMY_POOL_SIZE", "20")),
        "max_overflow": int(os.environ.get("PERF_SQLALCHEMY_MAX_OVERFLOW", "40")),
    }


CONFIGS = {
    "default": Config,
    "perf": PerfConfig,
}
