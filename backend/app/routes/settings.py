"""Application settings endpoints with key-specific validation."""
from __future__ import annotations

import math
from typing import Any

from flask import Blueprint, current_app, g, jsonify, request
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from ..auth.decorators import require_auth, require_role
from ..services.audit import log

settings_bp = Blueprint("settings", __name__, url_prefix="/api/settings")


class SettingsUpdate(BaseModel):
    """Allowed setting values and their database-aligned ranges."""
    model_config = ConfigDict(extra="forbid")

    tier1_min_cgpa: float | None = Field(default=None, ge=0, le=10)
    technical_threshold: float | None = Field(default=None, ge=0, le=100)
    aptitude_threshold: float | None = Field(default=None, ge=0, le=100)
    at_risk_probability: float | None = Field(default=None, ge=0, le=1)
    skill_target: float | None = Field(default=None, ge=0, le=100)
    placement_target_rate: float | None = Field(default=None, ge=0, le=1)

    @field_validator("*", mode="before")
    @classmethod
    def require_finite_number(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, bool):
            raise ValueError("must be numeric")
        try:
            if not math.isfinite(float(value)):
                raise ValueError("must be finite")
        except (TypeError, ValueError) as exc:
            if isinstance(exc, ValueError) and str(exc) == "must be finite":
                raise
            raise ValueError("must be numeric") from exc
        return value


@settings_bp.get("")
@require_auth
def get_settings():
    """Return current settings as a key-to-value JSON object."""
    response = g.db.table("app_settings").select("key, value, updated_by, updated_at").execute()
    return jsonify({row["key"]: row["value"] for row in (response.data or [])})


@settings_bp.put("")
@require_role("super_admin")
def update_settings():
    """Validate and persist one or more settings; only super admins may write."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": {"code": "validation_error", "message": "JSON object required", "details": None}}), 400
    try:
        validated = SettingsUpdate.model_validate(payload)
    except ValidationError as exc:
        return jsonify(
            {
                "error": {
                    "code": "validation_error",
                    "message": "Request validation failed",
                    "details": exc.errors(),
                }
            }
        ), 400

    changes = validated.model_dump(exclude_unset=True)
    if not changes or any(value is None for value in changes.values()):
        return jsonify({"error": {"code": "validation_error", "message": "Provide at least one non-null setting", "details": None}}), 400

    saved: dict[str, Any] = {}
    for key, value in changes.items():
        response = g.db.table("app_settings").upsert(
            {"key": key, "value": value, "updated_by": g.user["user_id"]},
            on_conflict="key",
        ).execute()
        saved[key] = value
    log("update", "app_settings", None, {"keys": sorted(changes)})
    current_app.logger.info("Updated application settings: %s", sorted(changes))
    return jsonify(saved)
