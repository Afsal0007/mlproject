"""Audit-log helper for authenticated write operations."""
from __future__ import annotations

from typing import Any

from flask import g


def log(action: str, entity: str, entity_id: str | None, meta: dict[str, Any] | None = None) -> None:
    """Insert an audit event through the current user's RLS-scoped client."""
    g.db.table("audit_log").insert(
        {
            "actor": g.user["user_id"],
            "action": action,
            "entity": entity,
            "entity_id": str(entity_id) if entity_id is not None else None,
            "meta": meta or {},
        }
    ).execute()