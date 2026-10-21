# AGENTS.md — Placement AI Project Rules

> **Read this file at the start of every phase before writing any code.**

---

## 1. Project Overview

**Placement AI** is a full-stack intelligent placement prediction and recommendation platform. It uses machine learning to help students understand their campus placement chances, get personalized skill-gap recommendations, and assist recruiters in shortlisting candidates.

---

## 2. Repository Layout

```
placement-ai/
├── AGENTS.md                          ← This file (read every phase)
├── ANTIGRAVITY_IMPLEMENTATION_GUIDE.md
├── design/
│   └── stitch/                        ← UI design exports (read-only)
├── frontend/                          ← React + Vite SPA
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/        ← API clients
│   │   └── store/           ← Zustand state
│   ├── index.html
│   └── package.json
├── backend/
│   ├── app/                 ← FastAPI application
│   │   ├── api/             ← Route handlers
│   │   ├── core/            ← Config, security, deps
│   │   ├── models/          ← SQLAlchemy ORM models
│   │   ├── schemas/         ← Pydantic schemas
│   │   └── services/        ← Business logic
│   ├── ml/
│   │   ├── models/          ← Trained model artifacts (.pkl / .joblib)
│   │   ├── notebooks/       ← EDA & training notebooks
│   │   ├── pipeline.py      ← Feature engineering pipeline
│   │   ├── train.py         ← Training script
│   │   └── predict.py       ← Inference helper
│   ├── main.py
│   └── requirements.txt
├── database/
│   └── schema.sql
├── data/
│   ├── raw/                 ← Never modify raw data
│   └── processed/
├── .env.example
└── README.md
```

---

## 3. Tech Stack

| Layer       | Technology                                  |
|-------------|---------------------------------------------|
| Frontend    | React 18, Vite, Zustand, React Query, Axios |
| Backend     | Python 3.11, FastAPI, SQLAlchemy 2.x        |
| ML          | scikit-learn, XGBoost, pandas, numpy        |
| Database    | PostgreSQL 15 (prod), SQLite (dev/test)     |
| Auth        | JWT (python-jose), bcrypt                   |
| Deployment  | Docker + docker-compose                     |

---

## 4. Coding Standards

### General
- **No magic numbers** — define constants in `core/config.py` or equivalent.
- **Type annotations everywhere** — Python: full type hints; TypeScript: strict mode.
- **Never commit secrets** — use `.env` files (never `.env.example` with real values).
- **Comments**: explain *why*, not *what*.

### Python / Backend
- Follow **PEP 8**; use `black` for formatting, `isort` for imports.
- All API endpoints must have **Pydantic schemas** for request/response.
- All DB queries via **SQLAlchemy ORM** — no raw SQL in app code.
- Use **dependency injection** for DB sessions and auth.

### JavaScript / Frontend
- Use **functional components** and React hooks exclusively.
- All API calls through the `services/` layer — never `fetch`/`axios` directly in components.
- State: **Zustand** for global, `useState`/`useReducer` for local.
- File naming: `PascalCase` for components, `camelCase` for hooks/services.

### ML
- Keep raw data immutable in `data/raw/`.
- Reproducibility: set and log **random seeds**.
- Save models with metadata (version, date, metrics) alongside the artifact.
- Feature engineering must live in `pipeline.py` — shared between training and inference.

---

## 5. Phase Checklist

Before marking any phase complete, verify:

- [ ] All new files have appropriate docstrings / JSDoc comments.
- [ ] `.env.example` is updated with any new environment variables (no real values).
- [ ] `README.md` reflects any new setup steps.
- [ ] No `console.log` / `print` debug statements left in production code.
- [ ] Linting passes (`black`, `isort`, `eslint`).
- [ ] All new API endpoints are tested (at minimum, manual via `/docs`).

---

## 6. Environment Variables Discipline

- **Backend** reads from `.env` via `pydantic-settings`.
- **Frontend** uses `VITE_` prefixed variables.
- Never hard-code URLs, ports, or credentials.

---

## 7. Git Workflow

- Branch naming: `feature/<slug>`, `fix/<slug>`, `chore/<slug>`
- Commit messages: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:` prefixes.
- Every PR must touch the relevant phase checklist above.

---

*Last updated: Phase 0 — Repository Setup*
