"""
Placement AI — FastAPI Application Entry Point
Phase 0 stub: wired up in Phase 2.
"""
from fastapi import FastAPI

app = FastAPI(
    title="Placement AI API",
    description="Campus Placement Prediction & Recommendation Platform",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "placement-ai-backend"}
