"""
PlacementAI Backend — Entry Point.

Run with:
    python run.py

Or in production:
    gunicorn "run:app"
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Debug mode is controlled via FLASK_ENV in .env.
    # Never set debug=True hardcoded in production.
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
