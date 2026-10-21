"""
ml/predict.py — Inference helper loaded at Flask startup (Phase 4 implementation).

LEAKAGE GUARD: placement_status, company, package_lpa are NEVER model features.
The model is loaded ONCE at startup from ml/artifacts/ and reused for every request.
"""


class PlacementPredictor:
    """Wraps the trained model artifact for inference."""

    def __init__(self, model_dir: str) -> None:
        self.model_dir = model_dir
        # Model loaded in Phase 4
        self._model = None

    def predict(self, student_profile: dict) -> dict:
        """Return placement probability for a single student profile."""
        raise NotImplementedError("Implement in Phase 4")
