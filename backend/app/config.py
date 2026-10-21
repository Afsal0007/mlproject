"""
PlacementAI Backend — Configuration.

Reads all settings from environment variables via python-dotenv.
Never hardcode URLs, ports, or credentials here.
"""
import os
from dotenv import load_dotenv

# Load .env from the backend directory (or project root if run from there).
load_dotenv()


def _parse_cors_origins(raw: str) -> list[str]:
    """Split a comma-separated CORS_ORIGINS string into a list."""
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


class Config:
    """Base configuration — all settings read from environment."""

    # Flask
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    DEBUG: bool = FLASK_ENV == "development"

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")  # legacy HS256
    DEV_BYPASS_AUTH: bool = os.getenv("DEV_BYPASS_AUTH", "false").strip().lower() == "true"

    # CORS — comma-separated list of allowed origins
    CORS_ORIGINS: list[str] = _parse_cors_origins(
        os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    )

    # ML
    MODEL_DIR: str = os.getenv("MODEL_DIR", "ml/artifacts")


class TestingConfig(Config):
    """Configuration used by pytest."""

    TESTING: bool = True
    DEBUG: bool = True
    # Role and auth tests must exercise the real decorator path by default.
    DEV_BYPASS_AUTH: bool = False
    # Allow any origin during testing so we don't need a real browser.
    CORS_ORIGINS: list[str] = ["*"]
