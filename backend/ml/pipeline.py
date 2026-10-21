"""
Placement AI — ML Pipeline (Phase 0 stub)
Full implementation in Phase 3.
"""
from __future__ import annotations


class FeaturePipeline:
    """
    Shared feature engineering pipeline used by both
    training (train.py) and inference (predict.py).

    Ensures training-serving skew is impossible.
    """

    def fit(self, X, y=None):
        """Fit the pipeline on training data."""
        raise NotImplementedError("Implement in Phase 3")

    def transform(self, X):
        """Transform raw input into model-ready features."""
        raise NotImplementedError("Implement in Phase 3")

    def fit_transform(self, X, y=None):
        """Fit and transform in one step."""
        return self.fit(X, y).transform(X)
