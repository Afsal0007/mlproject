"""
PlacementAI Backend — Application Factory.

Usage:
    from app import create_app
    app = create_app()

The factory pattern lets us create isolated app instances for testing
without touching module-level globals.
"""
import os
from pathlib import Path

from flask import Flask
from flask_cors import CORS

from .config import Config
from .routes.auth import auth_bp
from .routes.health import health_bp
from .routes.settings import settings_bp
from .routes.students import students_bp
from .utils.errors import register_error_handlers


def create_app(config_object: type = Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    if app.config.get("DEV_BYPASS_AUTH"):
        app.logger.warning("=" * 60)
        app.logger.warning("!!! AUTH BYPASS ENABLED — LOCAL DEVELOPMENT ONLY !!!")
        app.logger.warning("Authentication and RLS are bypassed; service-role access is active.")
        app.logger.warning("=" * 60)

    # Load the trained pipeline once per application process. A missing
    # artifact is a valid startup state during initial setup.
    model = None
    model_dir = app.config.get("MODEL_DIR", "ml/artifacts")
    if not os.path.isabs(model_dir):
        model_dir = str(Path(__file__).resolve().parents[1] / model_dir)
    try:
        from ml.predict import PlacementModel

        model_path = Path(model_dir)
        if (model_path / "model.joblib").is_file() and (model_path / "metadata.json").is_file():
            model = PlacementModel.load(model_path)
    except Exception:
        app.logger.exception("Could not load configured placement model")
    app.extensions["model"] = model

    # ── CORS ────────────────────────────────────────────────────────────
    # Only allow origins listed in CORS_ORIGINS to prevent credential leakage.
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    # ── Blueprints ──────────────────────────────────────────────────────
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(students_bp)
    register_error_handlers(app)

    return app
