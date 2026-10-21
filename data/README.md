# data/ — Dataset Directory

## Structure

| Directory | Purpose |
|-----------|---------|
| `raw/` | **Read-only.** Original source datasets. Never modify these files. |
| `processed/` | Cleaned / feature-engineered data produced by `backend/ml/preprocess.py`. |

## Files

| File | Description |
|------|-------------|
| `raw/placements.csv` | 10,000-row placement dataset (StudentID, CGPA, Internships, …, PlacementStatus) |

## Rules (from AGENTS.md)

- Raw data is **immutable** — never edit `raw/` files.
- All transformations must go through `backend/ml/preprocess.py`.
- Reproducibility: document any manual data-cleaning steps here.
