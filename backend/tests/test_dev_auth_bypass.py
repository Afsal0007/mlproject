"""Tests for the explicit local-development authentication bypass."""
from __future__ import annotations

from flask import g, jsonify

from app.auth import decorators
from app.auth.decorators import require_auth, require_role
from app import create_app
from app.config import TestingConfig


class FakeServiceClient:
    pass


def test_require_auth_bypass_skips_token_and_profile_lookup(app, monkeypatch):
    app.config["DEV_BYPASS_AUTH"] = True
    service_client = FakeServiceClient()
    monkeypatch.setattr(decorators, "get_service_client", lambda: service_client)
    monkeypatch.setattr(
        decorators,
        "verify_supabase_jwt",
        lambda _token: (_ for _ in ()).throw(AssertionError("verifier must be skipped")),
    )
    monkeypatch.setattr(
        decorators,
        "get_user_client",
        lambda _token: (_ for _ in ()).throw(AssertionError("profile client must be skipped")),
    )

    @require_auth
    def endpoint():
        return jsonify({
            "user": g.user,
            "role": g.role,
            "db_is_service": g.db is service_client,
            "access_token": g.access_token,
        })

    with app.test_request_context("/private"):
        response = endpoint()
        assert response.get_json() == {
            "user": {
                "user_id": "dev-bypass",
                "email": "dev@local",
                "full_name": "Dev Bypass",
                "role": "super_admin",
                "department": None,
            },
            "role": "super_admin",
            "db_is_service": True,
            "access_token": None,
        }


def test_require_role_bypass_allows_any_role(app, monkeypatch):
    app.config["DEV_BYPASS_AUTH"] = True
    monkeypatch.setattr(decorators, "get_service_client", FakeServiceClient)

    @require_role("auditor")
    def endpoint():
        return jsonify({"role": g.role})

    with app.test_request_context("/private"):
        assert endpoint().get_json() == {"role": "super_admin"}


def test_app_startup_logs_loud_warning_when_bypass_enabled(caplog):
    class DevBypassTestingConfig(TestingConfig):
        DEV_BYPASS_AUTH = True

    with caplog.at_level("WARNING", logger="app"):
        create_app(DevBypassTestingConfig)

    assert "AUTH BYPASS ENABLED" in caplog.text