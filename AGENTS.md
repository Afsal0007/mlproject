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
# PlacementAI — Project Rules (read before every task)

## Product
Student Placement Prediction System for a university placement cell. Admin-only web app
(no student logins). Modules: Admin Authentication, Dashboard, Student Management (CRUD +
CSV import/export), Placement Prediction (real scikit-learn model), Analytics & Reports
(interactive Plotly charts + exports), Skill Gap Analysis (rule engine + radar), Admin & Settings.

## Stack (do not substitute)
- frontend/: React 18 + Vite + JavaScript (JSX) + Tailwind CSS v3.4 + React Router v6
  + @supabase/supabase-js v2 + axios + react-plotly.js with plotly.js-dist-min + react-hot-toast
- backend/: Python 3.11, Flask 3, flask-cors, supabase (supabase-py v2), pydantic v2,
  PyJWT[crypto], pandas, scikit-learn, joblib, python-dotenv, pytest
- Database/Auth: Supabase Postgres + Supabase Auth (email/password)

## UI source of truth
- design/stitch/<screen>/code.html and screen.png are the reference designs.
  Reproduce layout, spacing, colors and typography faithfully.
- design/stitch/placement_analytics_system/DESIGN.md defines tokens and component rules.
- Copy the `tailwind.config` object from any Stitch code.html into frontend/tailwind.config.js
  unchanged. Where code.html and DESIGN.md conflict, code.html wins.
- Icons: Material Symbols Outlined (Google Fonts link), same names as in Stitch.
- Fonts: Hanken Grotesk (text) + JetBrains Mono (numbers, IDs, labels). Numeric columns
  use `font-variant-numeric: tabular-nums`.
- NEVER hardcode mock numbers, names or companies from the Stitch HTML. All data comes from the API.
  Show skeleton loaders while loading, empty states when there's no data, and error states on failure.
- Remove unbacked claims from the mockups (ISO 27001, AICTE Approved, SSL/AES badges, 2FA,
  NASSCOM, subnet binding, demo login presets).
- Responsive: sidebar becomes an off-canvas drawer under 1024px; tables scroll horizontally
  inside their card (never the page); grids collapse to 1 column on phones; 16px side gutter.

## Architecture rules
- Frontend talks ONLY to Flask for data (via src/services/api.js). It uses supabase-js ONLY
  for sign-in/sign-out/session. The access token goes in `Authorization: Bearer <jwt>`.
- Flask verifies the Supabase JWT on every /api route except GET /api/health.
- Flask uses a user-scoped Supabase client (the caller's JWT) for data access so RLS applies.
  The secret/service-role key is used ONLY for admin user management and is never sent to the browser.
- Role check: the caller must have a row in public.admin_profiles; role-gated routes use a decorator.
- Validate every request body with pydantic. Return JSON errors: {"error": {"code", "message", "details"}}.
- Every write (create/update/delete/import/predict/settings change) inserts a row in public.audit_log.
- The ML model is loaded once at startup from backend/ml/artifacts/. Never train inside a request
  (retraining runs as a background job).
- Leakage guard: placement_status, company, package_lpa are NEVER model features.

## Shared field names (use exactly these everywhere: DB, API, ML, UI)
usn, full_name, email, department, batch_year, tenth_pct, twelfth_pct, cgpa,
aptitude_score, technical_score, communication_score, internships, projects,
certifications, backlogs, extracurricular, placement_training,
placement_status ('placed'|'in_process'|'not_placed'|'opted_out'), company, package_lpa
Skill scores (0–100): dsa, system_design, core_cs, aptitude, communication
Departments: 'CSE','IT','AIDS','ECE'

## Working style
- Build incrementally. Only touch files for the current phase unless a fix is required elsewhere.
- After each phase: run the app, run the tests, and report what passed or failed with real output.
- Never commit .env files. Keep .env.example updated with every new variable (no real values).
- Ask before adding a dependency that isn't listed above.