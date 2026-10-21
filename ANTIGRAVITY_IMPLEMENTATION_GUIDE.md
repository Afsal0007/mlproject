# Antigravity Implementation Guide — Placement AI

> This guide is the single source of truth for how Antigravity (the AI coding agent) should build the **Placement AI** project phase by phase.

---

## Overview

The project is built in **7 phases**. Each phase is self-contained and produces a working, testable increment of the system. Do not skip phases or merge them unless explicitly instructed.

---

## Phase Roadmap

```
Phase 0 → Repository Setup            ✅ (current)
Phase 1 → Database Schema & Migrations
Phase 2 → Backend API (FastAPI)
Phase 3 → ML Pipeline & Model Training
Phase 4 → ML Inference API Integration
Phase 5 → Frontend SPA (React + Vite)
Phase 6 → Auth, Roles & Security
Phase 7 → Docker, CI/CD & Deployment
```

---

## Phase 0 — Repository Setup

**Goal**: Scaffold the repository so every subsequent phase has a stable home.

### Deliverables
- [x] `AGENTS.md` — project rules
- [x] `ANTIGRAVITY_IMPLEMENTATION_GUIDE.md` — this file
- [x] `design/stitch/` — placeholder (drop Stitch export here)
- [x] `frontend/` — empty scaffold
- [x] `backend/` + `backend/ml/` — empty scaffolds
- [x] `database/schema.sql` — initial schema stub
- [x] `data/raw/` + `data/processed/` — data directories
- [x] `.env.example` — documented env vars
- [x] `README.md` — project overview + quickstart

---

## Phase 1 — Database Schema & Migrations

**Goal**: Define all tables; set up Alembic migrations.

### Tables to create
| Table            | Purpose                                    |
|------------------|--------------------------------------------|
| `users`          | Students & recruiters                      |
| `student_profiles` | Academic & skill data for ML input       |
| `companies`      | Recruiting companies                       |
| `job_postings`   | Roles with required skills                 |
| `applications`   | Many-to-many: student ↔ posting            |
| `predictions`    | ML output stored per student               |
| `skill_gaps`     | Recommended skills per student             |

### Deliverables
- `database/schema.sql` — complete DDL
- `backend/alembic/` — migration directory
- `backend/app/models/` — SQLAlchemy ORM models

---

## Phase 2 — Backend API (FastAPI)

**Goal**: REST API with full CRUD for all entities.

### Key Endpoints
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
GET    /api/v1/students/{id}
PUT    /api/v1/students/{id}
GET    /api/v1/companies/
POST   /api/v1/companies/
GET    /api/v1/jobs/
POST   /api/v1/jobs/
POST   /api/v1/applications/
GET    /api/v1/predictions/{student_id}
```

### Deliverables
- `backend/main.py`
- `backend/app/api/` routers
- `backend/app/schemas/` Pydantic models
- `backend/app/services/` business logic
- `backend/requirements.txt`

---

## Phase 3 — ML Pipeline & Model Training

**Goal**: Train a placement prediction model; build reusable feature pipeline.

### Model Targets
1. **Placement Probability** — binary classification (placed / not placed)
2. **Predicted CTC** — regression (if placed)
3. **Skill Gap Score** — derived feature per job posting

### Deliverables
- `data/raw/placement_dataset.csv` — training data
- `backend/ml/pipeline.py` — `FeaturePipeline` class
- `backend/ml/train.py` — training script with CLI args
- `backend/ml/models/` — serialized model artifacts
- `backend/ml/notebooks/01_eda.ipynb`
- `backend/ml/notebooks/02_model_selection.ipynb`

---

## Phase 4 — ML Inference API Integration

**Goal**: Expose ML predictions via the FastAPI backend.

### New Endpoints
```
POST  /api/v1/predict/placement
POST  /api/v1/predict/skill-gap
GET   /api/v1/predict/history/{student_id}
```

### Deliverables
- `backend/ml/predict.py` — `PlacementPredictor` class
- `backend/app/api/predict.py` — FastAPI router
- Background task to store prediction results to DB

---

## Phase 5 — Frontend SPA (React + Vite)

**Goal**: Beautiful, responsive web application.

### Pages
| Route               | Description                           |
|---------------------|---------------------------------------|
| `/`                 | Landing page                          |
| `/auth/login`       | Login                                 |
| `/auth/register`    | Registration                          |
| `/dashboard`        | Student dashboard + prediction widget |
| `/profile`          | Edit academic & skill profile         |
| `/jobs`             | Browse job postings                   |
| `/companies`        | Browse companies                      |
| `/admin`            | Recruiter/admin view                  |

### Deliverables
- `frontend/src/` — all React source
- `frontend/package.json`
- `frontend/vite.config.js`
- Responsive design, dark mode, animations

---

## Phase 6 — Auth, Roles & Security

**Goal**: Secure the entire stack with JWT auth and role-based access.

### Roles
- `student` — view/edit own profile, submit applications, view own predictions
- `recruiter` — view student list, manage job postings
- `admin` — full access

### Deliverables
- `backend/app/core/security.py`
- `backend/app/core/deps.py` — auth dependencies
- Protected route guards in frontend
- Rate limiting middleware

---

## Phase 7 — Docker, CI/CD & Deployment

**Goal**: Containerize and automate.

### Deliverables
- `Dockerfile.backend`
- `Dockerfile.frontend`
- `docker-compose.yml`
- `.github/workflows/ci.yml` — lint + test on PR
- `.github/workflows/deploy.yml` — deploy on main merge

---

## Agent Instructions Per Phase

At the start of **each phase**, the agent must:
1. Re-read `AGENTS.md`.
2. Read the relevant phase section above.
3. Implement all deliverables.
4. Run the phase checklist from `AGENTS.md`.
5. Commit with message: `feat: Phase <N> — <Title>`.

---

*Placement AI · Antigravity Implementation Guide · Phase 0*
