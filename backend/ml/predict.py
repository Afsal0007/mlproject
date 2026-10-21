"""
Placement AI — ML Inference Helper (Phase 0 stub)
Full implementation in Phase 4.
"""
from __future__ import annotations


class PlacementPredictor:
    """
    Wraps trained model artifacts and the FeaturePipeline
    to produce placement predictions and skill gap scores.
    """

    def __init__(self, model_dir: str, version: str = "v1") -> None:
        self.model_dir = model_dir
        self.version = version
        # Models loaded in Phase 4

    def predict_placement(self, student_profile: dict) -> dict:
        """
        Returns:
            {
                "placement_probability": float,  # 0–1
                "predicted_ctc_lpa": float | None,
                "model_version": str,
            }
        """
        raise NotImplementedError("Implement in Phase 4")

    def compute_skill_gap(self, student_skills: list[str], required_skills: list[str]) -> dict:
        """
        Returns:
            {
                "missing_skills": list[str],
                "gap_score": float,  # 0 = no gap, 1 = full gap
            }
        """
        raise NotImplementedError("Implement in Phase 4")
