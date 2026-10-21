"""Generate deterministic, illustrative student placement training data."""
from __future__ import annotations

import numpy as np
import pandas as pd


def generate_synthetic(n_rows: int = 5_000, random_state: int = 42) -> pd.DataFrame:
    """Return synthetic rows in the application's shared field names.

    Placement outcomes follow a logistic relationship with academic and experience
    features. This fallback is for pipeline development only, not real-world claims.
    """
    rng = np.random.default_rng(random_state)
    cgpa = np.clip(rng.normal(7.35, 1.15, n_rows), 4.0, 10.0).round(2)
    aptitude_score = np.clip(rng.normal(66, 16, n_rows), 20, 100).round().astype(int)
    technical_score = np.clip(rng.normal(64, 17, n_rows), 15, 100).round().astype(int)
    communication_score = np.clip(rng.normal(68, 14, n_rows), 20, 100).round().astype(int)
    internships = np.clip(rng.poisson(0.85, n_rows), 0, 4).astype(int)
    projects = np.clip(rng.poisson(2.2, n_rows), 0, 8).astype(int)
    certifications = np.clip(rng.poisson(1.7, n_rows), 0, 8).astype(int)
    backlogs = np.clip(rng.poisson(0.24, n_rows), 0, 4).astype(int)
    extracurricular = rng.random(n_rows) < 0.48
    placement_training = rng.random(n_rows) < 0.68
    tenth_pct = np.clip(rng.normal(78, 10, n_rows), 45, 100).round(2)
    twelfth_pct = np.clip(rng.normal(75, 11, n_rows), 40, 100).round(2)

    linear_score = (
        -5.4
        + 0.58 * (cgpa - 7.0)
        + 0.026 * (technical_score - 60)
        + 0.021 * (aptitude_score - 60)
        + 0.48 * internships
        + 0.16 * projects
        + 0.12 * certifications
        - 0.92 * backlogs
        + 0.42 * placement_training
        + 0.20 * extracurricular
    )
    probability = 1 / (1 + np.exp(-linear_score))
    placed = rng.random(n_rows) < probability

    departments = np.array(["CSE", "IT", "AIDS", "ECE"])
    dept = rng.choice(departments, n_rows)
    prefix = {"CSE": "CS", "IT": "IT", "AIDS": "AD", "ECE": "EC"}
    usn = [f"1XX21{prefix[d]}{i + 1:03d}" for i, d in enumerate(dept)]

    return pd.DataFrame(
        {
            "usn": usn,
            "full_name": [f"Demo Student {i + 1:04d}" for i in range(n_rows)],
            "email": [f"demo{i + 1:04d}@example.edu" for i in range(n_rows)],
            "department": dept,
            "batch_year": np.full(n_rows, 2025, dtype=int),
            "tenth_pct": tenth_pct,
            "twelfth_pct": twelfth_pct,
            "cgpa": cgpa,
            "aptitude_score": aptitude_score,
            "technical_score": technical_score,
            "communication_score": communication_score,
            "internships": internships,
            "projects": projects,
            "certifications": certifications,
            "backlogs": backlogs,
            "extracurricular": extracurricular,
            "placement_training": placement_training,
            "placement_status": np.where(placed, "placed", "not_placed"),
        }
    )
