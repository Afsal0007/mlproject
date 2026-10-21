"""Supabase client factories for user-scoped and trusted admin operations."""
from __future__ import annotations

from flask import current_app
from supabase import Client, create_client


def get_user_client(token: str) -> Client:
    """Create an anon-key client scoped to the caller's JWT (RLS applies)."""
    url = current_app.config.get("SUPABASE_URL")
    anon_key = current_app.config.get("SUPABASE_ANON_KEY")
    if not url or not anon_key:
        raise RuntimeError("Supabase user client is not configured")
    client = create_client(url, anon_key)
    client.postgrest.auth(token)
    return client


def get_service_client() -> Client:
    """Create a service-role client; use only for trusted admin operations."""
    url = current_app.config.get("SUPABASE_URL")
    service_key = current_app.config.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not service_key:
        raise RuntimeError("Supabase service client is not configured")
    return create_client(url, service_key)