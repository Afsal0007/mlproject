"""
PlacementAI Backend — Application Factory.

Usage:
    from app import create_app
    app = create_app()

The factory pattern lets us create isolated app instances for testing
without touching module-level globals.
"""
from flask import Flask
from flask_cors import CORS

from .config import Config
from .routes.health import health_bp


def create_app(config_object: type = Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # ── CORS ────────────────────────────────────────────────────────────
    # Only allow origins listed in CORS_ORIGINS to prevent credential leakage.
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    # ── Blueprints ──────────────────────────────────────────────────────
    app.register_blueprint(health_bp)

    return app
