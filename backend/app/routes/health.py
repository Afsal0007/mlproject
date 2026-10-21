"""
Health blueprint — GET /api/health

This endpoint is intentionally unauthenticated so load-balancers and
monitoring tools can probe the backend without a JWT.
"""
import os
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.get("/health")
def health():
    """Return service liveness status."""
    # Detect whether a model artifact exists in MODEL_DIR.
    model_dir: str = os.getenv("MODEL_DIR", "ml/artifacts")
    model_loaded: bool = any(
        f.endswith((".pkl", ".joblib"))
        for f in os.listdir(model_dir)
        if os.path.isfile(os.path.join(model_dir, f))
    ) if os.path.isdir(model_dir) else False

    # DB status will be enriched in Phase 2 once Supabase client is wired.
    return jsonify(
        {
            "status": "ok",
            "version": "1.0.0",
            "model_loaded": model_loaded,
            "db": "unknown",
        }
    ), 200
