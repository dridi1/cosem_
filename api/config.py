import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def is_production_environment():
    return os.getenv("VERCEL_ENV") == "production" or os.getenv("FLASK_ENV") == "production"


def get_secret_key():
    secret_key = os.getenv("SECRET_KEY")
    if secret_key:
        return secret_key
    if is_production_environment():
        raise RuntimeError("SECRET_KEY environment variable is required in production.")
    return "dev-secret-key"


def get_database_uri():
    database_uri = os.getenv("DATABASE_URL")
    if database_uri and database_uri.startswith("postgres://"):
        return database_uri.replace("postgres://", "postgresql://", 1)
    if database_uri:
        return database_uri
    return f"sqlite:///{BASE_DIR / 'cosem.db'}"


class BaseConfig:
    SECRET_KEY = get_secret_key()
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    TESTING = False
    WTF_CSRF_ENABLED = True
