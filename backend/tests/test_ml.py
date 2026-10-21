"""End-to-end checks for the CLI training and inference pipeline."""
from __future__ import annotations

import time

import pytest

from ml.generate_synthetic import generate_synthetic
from ml.predict import PlacementModel
from ml.preprocess import preprocess
from ml.train import train_model


@pytest.fixture(scope="module")
def trained_model(tmp_path_factory):
    output_dir = tmp_path_factory.mktemp("placement-model")
    started = time.perf_counter()
    metadata = train_model(
        generate_synthetic(n_rows=5_000, random_state=42),
        dataset_source="synthetic",
        output_dir=output_dir,
        seed=42,
    )
    elapsed = time.perf_counter() - started
    return PlacementModel.load(output_dir), metadata, elapsed


def test_synthetic_training_is_fast_and_predictive(trained_model):
    _, metadata, elapsed = trained_model
    assert elapsed < 30
    assert metadata["metrics"]["roc_auc"] > 0.7
    assert metadata["dataset_source"] == "synthetic"
    assert metadata["training_rows"] == 5_000


def test_predict_one_probability_and_local_contributions(trained_model):
    model, _, _ = trained_model
    result = model.predict_one(
        {
            "cgpa": 8.4,
            "aptitude_score": 80,
            "technical_score": 82,
            "communication_score": 75,
            "internships": 1,
            "projects": 3,
            "certifications": 2,
            "backlogs": 0,
            "extracurricular": True,
            "placement_training": True,
        }
    )
    assert 0 <= result["probability"] <= 1
    assert result["label"] in {"placed", "not_placed"}
    assert result["contributions"]


def test_higher_cgpa_has_higher_probability(trained_model):
    model, _, _ = trained_model
    common = {
        "aptitude_score": 82,
        "technical_score": 80,
        "communication_score": 75,
        "internships": 1,
        "projects": 3,
        "certifications": 2,
        "backlogs": 0,
        "extracurricular": True,
        "placement_training": True,
    }
    low = model.predict_one({**common, "cgpa": 5.5})["probability"]
    high = model.predict_one({**common, "cgpa": 9.5})["probability"]
    assert high > low


def test_outcome_and_employer_fields_never_become_features():
    cleaned = preprocess(generate_synthetic(n_rows=250))
    assert not {"placement_status", "company", "package_lpa"}.intersection(cleaned.columns)
    from ml import preprocess as preprocessing_module

    assert not {"placement_status", "company", "package_lpa", "target"}.intersection(
        preprocessing_module.FEATURES
    )
    assert "technical_score" not in preprocessing_module.UNUSED_BY_MODEL
    assert "backlogs" not in preprocessing_module.UNUSED_BY_MODEL


def test_kaggle_columns_map_and_unavailable_fields_are_reported():
    import pandas as pd

    raw = pd.DataFrame(
        {
            "StudentID": [1, 2, 3, 4],
            "CGPA": [7.0, 8.0, 6.0, 9.0],
            "SoftSkillsRating": [3.0, 4.0, 2.5, 5.0],
            "ExtracurricularActivities": ["Yes", "No", "Yes", "No"],
            "PlacementTraining": ["No", "Yes", "No", "Yes"],
            "PlacementStatus": ["Not Placed", "Placed", "Not Placed", "Placed"],
        }
    )
    cleaned = preprocess(raw)
    from ml import preprocess as preprocessing_module

    assert cleaned["communication_score"].tolist() == [60.0, 80.0, 50.0, 100.0]
    assert cleaned["target"].tolist() == [0, 1, 0, 1]
    assert cleaned["extracurricular"].tolist() == [True, False, True, False]
    assert "technical_score" in preprocessing_module.UNUSED_BY_MODEL
    assert "backlogs" in preprocessing_module.UNUSED_BY_MODEL
