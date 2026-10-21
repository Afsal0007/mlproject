"""Flask authentication and admin-role decorators."""
from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from flask import current_app, g, jsonify, request

from ..services.db import get_user_client
from .verify import AuthenticationError, verify_supabase_jwt


def _error(status: int, code: str, message: str):
    return jsonify({"error": {"code": code, "message": message, "details": None}}), status


def require_auth(view: Callable[..., Any]) -> Callable[..., Any]:
    """Authenticate the bearer token and require an active admin profile."""
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any):
        header = request.headers.get("Authorization", "")
        scheme, separator, token = header.partition(" ")
        if not separator or scheme.lower() != "bearer" or not token.strip():
            return _error(401, "unauthorized", "Authentication required")
        token = token.strip()
        try:
            identity = verify_supabase_jwt(token)
            client = get_user_client(token)
            result = (
                client.table("admin_profiles")
                .select("user_id, full_name, email, role, department, is_active")
                .eq("user_id", identity["user_id"])
                .eq("is_active", True)
                .limit(1)
                .execute()
            )
            profiles = result.data or []
            if not profiles:
                return _error(403, "forbidden", "An active administrator profile is required")
            profile = profiles[0]
        except AuthenticationError:
            return _error(401, "unauthorized", "Invalid authentication credentials")
        except Exception:
            current_app.logger.warning("Admin profile lookup failed")
            return _error(403, "forbidden", "An active administrator profile is required")

        g.user = {
            "user_id": identity["user_id"],
            "email": identity.get("email") or profile.get("email"),
            "full_name": profile.get("full_name"),
            "role": profile.get("role"),
            "department": profile.get("department"),
        }
        g.role = profile.get("role")
        g.db = client
        g.access_token = token
        return view(*args, **kwargs)

    return wrapped


def require_role(*roles: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Require one of the specified roles after admin authentication."""
    def decorator(view: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(view)
        @require_auth
        def wrapped(*args: Any, **kwargs: Any):
            if g.role not in roles:
                return _error(403, "forbidden", "Insufficient permissions")
            return view(*args, **kwargs)

        return wrapped

    return decorator