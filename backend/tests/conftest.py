"""
tests/conftest.py — pytest fixtures for the PlacementAI backend.

Creates an isolated test app instance using TestingConfig
so tests never touch the real database or model artifacts.
"""
import pytest
from app import create_app
from app.config import TestingConfig


@pytest.fixture()
def app():
    """Create a test Flask application."""
    _app = create_app(config_object=TestingConfig)
    yield _app


@pytest.fixture()
def client(app):
    """Flask test client."""
    return app.test_client()
