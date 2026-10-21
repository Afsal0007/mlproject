"""Authentication and current-admin profile endpoints."""
from flask import Blueprint, g, jsonify

from ..auth.decorators import require_auth

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.get("/me")
@require_auth
def me():
    """Return the authenticated administrator's public profile."""
    return jsonify(
        {
            "user_id": g.user["user_id"],
            "email": g.user["email"],
            "full_name": g.user["full_name"],
            "role": g.user["role"],
            "department": g.user["department"],
        }
    )
