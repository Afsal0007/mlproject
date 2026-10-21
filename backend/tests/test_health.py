"""
tests/test_health.py — Tests for GET /api/health.

Verifies the exact shape of the response documented in the Phase 1 spec.
"""
import json


def test_health_returns_200(client):
    """Health endpoint must always return HTTP 200."""
    response = client.get("/api/health")
    assert response.status_code == 200


def test_health_json_shape(client):
    """Response must contain all required fields with correct types."""
    response = client.get("/api/health")
    data = json.loads(response.data)

    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
    assert isinstance(data["model_loaded"], bool)
    assert "db" in data


def test_health_content_type(client):
    """Response must be JSON."""
    response = client.get("/api/health")
    assert response.content_type == "application/json"


def test_health_model_not_loaded_when_artifact_is_missing(client, app):
    """Health reports no model when the app has no loaded artifact."""
    app.extensions["model"] = None
    response = client.get("/api/health")
    data = json.loads(response.data)
    assert data["model_loaded"] is False


def test_health_model_loaded_when_artifact_exists(client, app):
    """Health reports the model instance loaded during application startup."""
    app.extensions["model"] = type("FakeModel", (), {"metadata": {"version": "test-v1"}})()
    response = client.get("/api/health")
    data = json.loads(response.data)
    assert data["model_loaded"] is True
    assert data["model_version"] == "test-v1"
