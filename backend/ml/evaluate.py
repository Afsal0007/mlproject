"""Print the saved model evaluation report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def evaluate(model: Any, X_test: Any, y_test: Any) -> dict[str, float]:
    """Return common holdout metrics for a fitted binary classifier."""
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

    probability = model.predict_proba(X_test)[:, 1]
    predicted = (probability >= 0.5).astype(int)
    return {
        "accuracy": float(accuracy_score(y_test, predicted)),
        "precision": float(precision_score(y_test, predicted, zero_division=0)),
        "recall": float(recall_score(y_test, predicted, zero_division=0)),
        "f1": float(f1_score(y_test, predicted, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probability)),
    }


def format_report(metadata: dict[str, Any]) -> str:
    metrics = metadata["metrics"]
    lines = [
        f"PlacementAI model evaluation — {metadata['version']}",
        "=" * 64,
        f"Algorithm:       {metadata['algorithm']}",
        f"Dataset:         {metadata['dataset_source']} ({metadata['training_rows']:,} rows)",
        f"Trained at:      {metadata['trained_at']}",
        f"Features:        {', '.join(metadata['features'])}",
        f"Not used:        {', '.join(metadata['unused_by_model']) or 'None'}",
        "",
        "Held-out test metrics:",
        f"  Accuracy:      {metrics['accuracy']:.4f}",
        f"  Precision:     {metrics['precision']:.4f}",
        f"  Recall:        {metrics['recall']:.4f}",
        f"  F1:            {metrics['f1']:.4f}",
        f"  ROC-AUC:       {metrics['roc_auc']:.4f}",
        f"  CV ROC-AUC:    {metrics['cv_mean']:.4f} ± {metrics['cv_std']:.4f}",
        f"  Test rows:     {metrics['test_size']:,}",
        "",
        "Confusion matrix (actual rows [not placed, placed]; predicted columns [not placed, placed]):",
        f"  {metadata['confusion_matrix'][0]}",
        f"  {metadata['confusion_matrix'][1]}",
        "",
        "Calibration points (mean predicted probability → observed positive fraction):",
    ]
    calibration = metadata["calibration_curve"]
    lines.extend(
        f"  {predicted:.3f} → {observed:.3f}"
        for predicted, observed in zip(
            calibration["mean_predicted_probability"], calibration["fraction_positive"]
        )
    )
    lines.extend(["", "Permutation feature importance (test ROC-AUC decrease):"])
    lines.extend(
        f"  {item['feature']:<24} {item['importance']:+.5f}"
        for item in metadata["feature_importances"]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print saved PlacementAI evaluation metadata")
    parser.add_argument(
        "--metadata",
        type=Path,
        default=Path(__file__).resolve().parent / "artifacts" / "metadata.json",
        help="Path to metadata.json",
    )
    args = parser.parse_args()
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    print(format_report(metadata))


if __name__ == "__main__":
    main()
