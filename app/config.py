from pathlib import Path
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

_BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(_BACKEND_DIR / ".env")

# Direct connection URL (standard for cloud providers like Render, Railway)
DATABASE_URL = os.getenv("DATABASE_URL")

# Component-based connection parameters (default for local development)
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "expense_tracker")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Allowed CORS origins (comma-separated in environment variable)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "")


def get_database_url() -> str:
    """Return database URL.

    If DATABASE_URL is set, normalizes driver prefix for psycopg2 and returns it.
    Otherwise falls back to component-based connection parameters from .env.
    """
    if DATABASE_URL and DATABASE_URL.strip():
        url = DATABASE_URL.strip()
        # Normalize postgres:// to postgresql+psycopg2:// for SQLAlchemy compatibility
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url

    if not POSTGRES_PASSWORD:
        raise RuntimeError(
            "POSTGRES_PASSWORD is not set. Add it to the backend .env file or set DATABASE_URL."
        )
    password = quote_plus(POSTGRES_PASSWORD)
    return (
        f"postgresql+psycopg2://{POSTGRES_USER}:{password}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


def get_jwt_secret() -> str:
    if not JWT_SECRET:
        raise RuntimeError(
            "JWT_SECRET is not set. Add it to the backend .env file."
        )
    return JWT_SECRET


def get_allowed_origins() -> list[str]:
    """Return allowed CORS origins for development and production."""
    default_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    if ALLOWED_ORIGINS and ALLOWED_ORIGINS.strip():
        extra = [
            origin.strip()
            for origin in ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]
        for origin in extra:
            if origin not in default_origins:
                default_origins.append(origin)
    return default_origins
