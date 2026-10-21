"""
Health blueprint — GET /api/health

This endpoint is intentionally unauthenticated so load-balancers and
monitoring tools can probe the backend without a JWT.
"""
from flask import Blueprint, current_app, jsonify

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.get("/health")
def health():
    """Return service liveness status."""
    model = current_app.extensions.get("model")
    db_status = "unknown"
    if current_app.config.get("SUPABASE_URL") and current_app.config.get("SUPABASE_ANON_KEY"):
        try:
            from supabase import create_client

            client = create_client(
                current_app.config["SUPABASE_URL"],
                current_app.config["SUPABASE_ANON_KEY"],
            )
            client.table("app_settings").select("key").limit(1).execute()
            db_status = "ok"
        except Exception:
            db_status = "unavailable"
    return jsonify(
        {
            "status": "ok",
            "version": "1.0.0",
            "model_loaded": model is not None,
            "model_version": model.metadata.get("version") if model else None,
            "db": db_status,
        }
    ), 200
