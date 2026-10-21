# PlacementAI: Antigravity Implementation Guide

A phased prompt playbook for building the **Student Placement Prediction System** in Google Antigravity, using your Stitch export (`stitch_student_placement_prediction_system`) as the UI source of truth.

**Stack:** React 18 + Vite + Tailwind CSS 3 · Flask 3 REST API · Supabase Postgres + Supabase Auth · scikit-learn · Pandas · Plotly (react-plotly.js)

---

## 0. Before you start

### 0.1 What's in your Stitch export (and how to use it)

| Stitch folder | Becomes React page | Route |
|---|---|---|
| `login_authentication/` | `LoginPage` | `/login` |
| `placement_dashboard/` | `DashboardPage` | `/` |
| `student_management/` | `StudentsPage` | `/students` |
| `placement_prediction/` | `PredictionPage` | `/prediction` |
| `analytics_reports/` | `AnalyticsPage` | `/analytics` |
| `skill_gap_analysis/` | `SkillGapPage` | `/skill-gap` |
| `admin_settings/` | `AdminPage` | `/admin` |
| `placement_analytics_system/DESIGN.md` | Design rules (colors, type, spacing, components) | n/a |

Each screen folder has a `code.html` (Tailwind CDN markup) and a `screen.png` (reference screenshot). Every `code.html` carries the **same inline `tailwind.config`** with custom tokens (`primary-container`, `surface-container-low`, `font-headline-xl`, `space-lg`, etc.). Copy that object into `tailwind.config.js` and the Stitch classes work as-is.

**Things to know about the export (tell the agent, it matters):**

1. **Use Tailwind v3, not v4.** The Stitch config is a v3 `theme.extend` object. Pin `tailwindcss@3` so it can be reused verbatim.
2. **Icons are Material Symbols Outlined**, not Lucide (DESIGN.md says Lucide, but the code uses `<span class="material-symbols-outlined">`). Keep Material Symbols for fidelity.
3. **The border-radius values in `code.html` don't match DESIGN.md** (`lg` is 0.25rem in code, 0.5rem in DESIGN.md). Treat `code.html` as the source of truth so the build matches the screenshots.
4. **All the numbers in the mockups are fake** (480 students, 93.4% accuracy, ₹42 LPA, "Dr. Sarah Jenkins"). Every number has to come from the API.
5. **Strip claims the system won't actually back up:** "ISO 27001", "AICTE Approved", "SSL 256-Bit", "AES-256 Storage", "2FA Required", "NASSCOM-Proctor", "Bind session to campus subnet", and the one-click "Evaluation Presets" login buttons (they're demo logins, a security hole). Replace them with real status (API health, model version, real metrics) or remove them.
6. The `onclick="triggerToast(...)"` / `runMlInference()` handlers are mock JS. Replace them with real React handlers.

### 0.2 Repository layout to set up first

```
placement-ai/
├── AGENTS.md                      ← Prompt 0 (project rules), read by the agent every phase
├── ANTIGRAVITY_IMPLEMENTATION_GUIDE.md   ← this file
├── design/
│   └── stitch/                    ← unzip your Stitch export here (read-only reference)
├── frontend/
├── backend/
│   └── ml/
├── database/
│   └── schema.sql
├── data/
├── .env.example
└── README.md
```

Unzip the Stitch export into `design/stitch/` **before** Phase 1 so the agent can open each `code.html` and `screen.png`.

### 0.3 How to run each phase in Antigravity

- **One phase = one agent conversation.** Start a new conversation per phase so context stays clean. Each prompt tells the agent to read `AGENTS.md` first.
- Use **Planning mode** for phases 2–3, 5, 8 and 11 (schema, ML, CRUD, prediction, skill gap). Review the implementation plan artifact before approving it.
- **Don't move on until the phase's "Verify" checklist passes.** Paste any failing output back into the same conversation.
- **Commit after every phase that passes** (`git commit -m "phase N: ..."`). That gives you a clean rollback point if a later phase breaks something.
- Keep secrets in `.env` files only. Never paste real keys into prompts.

### 0.4 Supabase setup (manual, ~10 minutes)

1. Create a Supabase project. Note the **Project URL**, the **publishable/anon key** and the **secret/service_role key** (Settings → API).
2. Auth → Providers → Email: enabled. Auth → **disable public sign-ups** (admins are created by other admins, never self-registered).
3. Auth → Users → **Add user** → create your first admin (email + password). Copy the user's UUID; Phase 2 seeds them as `super_admin`.

### 0.5 Dataset (manual)

Recommended: the Kaggle **"Placement Prediction Dataset"** (`placementdata.csv`, about 10,000 rows) with columns `CGPA, Internships, Projects, Workshops/Certifications, AptitudeTestScore, SoftSkillsRating, ExtracurricularActivities, PlacementTraining, SSC_Marks, HSC_Marks, PlacementStatus`. Download it and put it at `data/raw/placementdata.csv`.

If you can't download it, Phase 3 includes a seeded synthetic generator so everything still runs. Predictions from synthetic data are illustrative only, and the UI should say so.

---

## Prompt 0: Project rules (save as `AGENTS.md`)

Save this as `AGENTS.md` in the repo root. If your Antigravity version supports workspace rules, paste it there as well.

```markdown
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
```

---

## Phase 1: Scaffold, environment and health check

**Prompt:**

```
Read AGENTS.md first. Phase 1: scaffold the monorepo. No features yet.

1. frontend/: Vite + React 18 (JS). Install the frontend deps listed in AGENTS.md.
   Configure Tailwind v3.4 with PostCSS. Copy the tailwind.config object from
   design/stitch/placement_dashboard/code.html into tailwind.config.js unchanged
   (content: ./index.html, ./src/**/*.{js,jsx}). In index.html add the Google Fonts links
   for Hanken Grotesk, JetBrains Mono and Material Symbols Outlined exactly as in the Stitch head.
   Port the Stitch <style> base layer (scrollbar, overscroll) into src/index.css.
   Folders: src/{pages,components,layouts,routes,services,hooks,context,lib,utils}.
   Add vite proxy: /api -> http://127.0.0.1:5000.
2. backend/: app factory pattern (backend/app/__init__.py create_app()), config.py reading .env,
   blueprints folder app/routes/, app/services/, app/schemas/, app/auth/, app/utils/.
   requirements.txt with the pinned deps from AGENTS.md. run.py entry point.
   GET /api/health returns {"status":"ok","version":"1.0.0","model_loaded":false,"db":"unknown"}.
   CORS: allow only the origins in CORS_ORIGINS.
   pytest set up with a test for /api/health.
3. backend/ml/ folder with empty train.py, preprocess.py, evaluate.py, predict.py, artifacts/.gitkeep.
4. database/schema.sql (empty placeholder with a header comment), data/README.md placeholder.
5. .env.example at root documenting:
   Frontend: VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY, VITE_API_BASE_URL
   Backend: FLASK_ENV, SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY,
   SUPABASE_JWT_SECRET (optional, legacy HS256), CORS_ORIGINS, MODEL_DIR
6. .gitignore (node_modules, .venv, .env*, !.env.example, __pycache__, dist, artifacts/*.joblib).
7. README.md skeleton with section headings only.
8. A temporary frontend page that calls /api/health and shows the JSON.

Run both servers and the backend tests, then show me the output.
```

**Verify:**
- [ ] `cd backend && python -m venv .venv && pip install -r requirements.txt && pytest` passes
- [ ] `flask --app run run` (or `python run.py`) serves `GET /api/health`
- [ ] `cd frontend && npm i && npm run dev` shows the health JSON through the proxy
- [ ] A test div using `bg-primary-container text-on-primary font-headline-xl` renders in navy with Hanken Grotesk

---

## Phase 2: Database schema, RLS and seed

Use **Planning mode**.

**Prompt:**

```
Read AGENTS.md. Phase 2: write database/schema.sql for Supabase Postgres. It must be
idempotent (safe to re-run: IF NOT EXISTS / CREATE OR REPLACE / DROP POLICY IF EXISTS).

Types:
- placement_status enum: placed, in_process, not_placed, opted_out
- admin_role enum: super_admin, placement_officer, faculty_mentor, auditor

Tables (uuid PKs default gen_random_uuid(), created_at/updated_at timestamptz default now()):
1. admin_profiles: user_id uuid PK references auth.users(id) on delete cascade,
   full_name, email, role admin_role not null default 'placement_officer', department, is_active bool.
2. students: id, usn text unique not null, full_name, email, department text check in
   ('CSE','IT','AIDS','ECE'), batch_year int, tenth_pct, twelfth_pct numeric(5,2) check 0–100,
   cgpa numeric(4,2) check 0–10, aptitude_score, technical_score, communication_score int check 0–100,
   internships, projects, certifications, backlogs int check >= 0, extracurricular bool,
   placement_training bool, placement_status default 'in_process', company text, package_lpa numeric(6,2),
   created_by uuid references auth.users.
3. skill_assessments: id, student_id FK students on delete cascade, dsa, system_design, core_cs,
   aptitude, communication int check 0–100, assessed_at timestamptz, source text.
4. predictions: id, student_id FK nullable (manual what-if runs), features jsonb, probability numeric(5,4),
   predicted_label text, model_version text, contributions jsonb, created_by uuid.
5. ml_models: id, version text unique, algorithm text, metrics jsonb, feature_list jsonb,
   trained_at, is_active bool. Partial unique index so only one row is active.
6. app_settings: key text PK, value jsonb, updated_by, updated_at.
   Seed: tier1_min_cgpa 8.5, technical_threshold 60, aptitude_threshold 65,
   at_risk_probability 0.5, skill_target 75 (per axis), placement_target_rate 0.85.
7. audit_log: id bigserial, actor uuid, action text, entity text, entity_id text, meta jsonb, created_at.
8. report_exports: id, title, type ('csv'|'xlsx'|'pdf'), scope jsonb, row_count, created_by, created_at.

Indexes: students(department, batch_year), students(placement_status), students(cgpa),
predictions(student_id, created_at desc), audit_log(created_at desc), trigram or lower() index for name/usn search.

Trigger: set updated_at on update for students and admin_profiles.

Helper functions (SECURITY DEFINER, search_path = public):
- is_admin() → true if auth.uid() has an active admin_profiles row
- has_role(variadic roles admin_role[]) → bool

RLS: enable on ALL tables. Policies:
- students, skill_assessments: SELECT for is_admin(); INSERT/UPDATE for
  has_role('super_admin','placement_officer','faculty_mentor'); DELETE for has_role('super_admin','placement_officer').
- predictions: SELECT is_admin(); INSERT is_admin() with created_by = auth.uid().
- ml_models, app_settings: SELECT is_admin(); write super_admin only.
- admin_profiles: SELECT is_admin(); write super_admin only.
- audit_log: INSERT is_admin(); SELECT has_role('super_admin','auditor'); no UPDATE/DELETE policies (append-only).
- report_exports: SELECT/INSERT is_admin().
No anon access to anything.

Also create:
- database/seed.sql: a commented template that inserts the first super_admin into admin_profiles
  (I'll paste my auth user UUID), plus 40 realistic demo students across 4 departments with
  matching skill_assessments. Varied, plausible values; Indian names; USNs like 1XX21CS001.
- database/README.md: how to run schema.sql then seed.sql in the Supabase SQL editor, and how to
  verify RLS (query as anon returns 0 rows).

Show me the plan first.
```

**Verify:**
- [ ] `schema.sql` runs twice in the Supabase SQL editor without errors
- [ ] `seed.sql` (with your UUID) inserts 40 students
- [ ] Table Editor shows RLS **enabled** on every table
- [ ] A REST call with only the anon key returns `[]` for `students`

---

## Phase 3: ML pipeline (preprocess → train → evaluate → save)

Use **Planning mode**.

**Prompt:**

```
Read AGENTS.md. Phase 3: build the ML pipeline in backend/ml/. It runs from the CLI,
not inside Flask.

1. data/README.md: document the dataset source (Kaggle "Placement Prediction Dataset",
   placementdata.csv), where to place it (data/raw/placementdata.csv), license note, the
   column dictionary, and how each raw column maps to our shared field names.
2. backend/ml/generate_synthetic.py: seeded (random_state=42) generator producing 5,000 rows in
   our field names, with a realistic logistic relationship (cgpa, technical_score, aptitude,
   internships, projects raise probability; backlogs lower it). Used ONLY if the raw file is missing.
   Print a clear warning when it's used.
3. backend/ml/preprocess.py:
   - load_raw(): read data/raw/placementdata.csv if present, else synthetic. Inspect the actual
     columns, rename to our field names, map SoftSkillsRating (0–5) → communication_score (0–100),
     Yes/No → bool, PlacementStatus → target (1 placed / 0 not).
   - FEATURES list = only the columns that actually exist in the training data. Fields shown in
     the UI but missing from training data (e.g. technical_score, backlogs if absent) must be
     listed in UNUSED_BY_MODEL and surfaced by the API so the UI can label them "not used by model".
   - Drop leakage columns (status, company, package). Dedupe, clip ranges, impute (median/most_frequent).
   - Build a sklearn ColumnTransformer + Pipeline (StandardScaler for numeric, passthrough for bools).
4. backend/ml/train.py:
   - Stratified 80/20 split. Candidates: LogisticRegression, RandomForestClassifier,
     GradientBoostingClassifier. 5-fold stratified CV, light GridSearchCV per model.
   - Select the best by CV ROC-AUC. Refit on train, evaluate on the held-out test set.
   - Save artifacts/model.joblib (full pipeline), artifacts/metadata.json with: version
     (e.g. "rf-2026.10.21-1"), algorithm, features, unused_by_model, metrics (accuracy, precision,
     recall, f1, roc_auc, cv_mean, cv_std, test_size), confusion_matrix, calibration curve points,
     global feature importances (permutation importance on the test set), trained_at,
     dataset_source ("kaggle"|"synthetic"), training_rows.
   - Optional --register flag: upsert into Supabase ml_models (service key from .env) and mark active.
5. backend/ml/evaluate.py: prints a readable report from metadata.json.
6. backend/ml/predict.py: PlacementModel class
   - load(dir), predict_one(dict) → {probability, label ('placed' if p >= threshold),
     contributions: list of {feature, value, impact}}, predict_batch(DataFrame).
   - Per-prediction contributions: if LogisticRegression, coef × scaled value; if a tree model,
     use shap.TreeExplainer if `shap` is installed, else a fast perturbation method
     (replace each feature with its training median, measure the probability delta).
     Ask me before adding shap to requirements.
   - Validate inputs against expected ranges; raise ValueError with field names.
7. backend/tests/test_ml.py: pipeline trains on synthetic data in <30s, roc_auc > 0.7,
   predict_one returns a probability in [0,1], higher cgpa → higher probability (monotonic sanity
   check), leakage columns absent from features.

Run training and show me the evaluate.py output and test results. Do NOT invent metrics:
whatever the run produces is what the UI will show.
```

**Verify:**
- [ ] `python -m ml.train` (from `backend/`) produces `model.joblib` + `metadata.json`
- [ ] `python -m ml.evaluate` prints real metrics and names the dataset source
- [ ] `pytest tests/test_ml.py` passes
- [ ] `metadata.json` lists `features` and `unused_by_model`, and `placement_status` is absent from features

---

## Phase 4: Flask core, auth middleware and settings

**Prompt:**

```
Read AGENTS.md. Phase 4: backend foundations.

1. app/auth/verify.py: verify_supabase_jwt(token)
   - Primary: PyJWT + PyJWKClient against {SUPABASE_URL}/auth/v1/.well-known/jwks.json
     (asymmetric signing keys), audience "authenticated", cache the JWKS client.
   - Fallback: if SUPABASE_JWT_SECRET is set, HS256 verification.
   - Last resort: supabase.auth.get_user(token).
   Returns {user_id, email}. Raise 401 on any failure; never leak why.
2. app/auth/decorators.py:
   - @require_auth: reads the Bearer token, verifies it, loads admin_profiles via a user-scoped
     client, sets g.user, g.role, g.db (supabase client with postgrest.auth(token)). 401 if
     no token, 403 if no active admin profile.
   - @require_role(*roles): 403 otherwise.
3. app/services/db.py: get_user_client(token), get_service_client() (admin ops only).
4. app/services/audit.py: log(action, entity, entity_id, meta).
5. app/utils/errors.py: consistent JSON error handlers (400 validation via pydantic, 401, 403, 404,
   409 duplicate USN, 422, 500 without stack traces in production).
6. Routes:
   - GET /api/health → also reports model_loaded, model_version and db reachability.
   - GET /api/auth/me → {user_id, email, full_name, role, department}.
   - GET /api/settings, PUT /api/settings (super_admin) with pydantic validation of each key's range.
7. Load PlacementModel once in create_app() and attach it to app.extensions["model"].
8. Tests with a mocked verifier: no token → 401, non-admin → 403, admin → 200 on /api/auth/me,
   faculty_mentor PUT /api/settings → 403.

Run the tests and show the output.
```

**Verify:**
- [ ] `pytest` all green
- [ ] Sign in via the Supabase dashboard or curl to get a JWT, then `curl -H "Authorization: Bearer $JWT" localhost:5000/api/auth/me` returns your profile
- [ ] Without a token: `401`

---

## Phase 5: Students API (CRUD, search, CSV import/export)

Use **Planning mode**.

**Prompt:**

```
Read AGENTS.md. Phase 5: Student Management API (blueprint app/routes/students.py).

Pydantic schemas: StudentCreate, StudentUpdate (all optional), StudentOut, SkillAssessmentIn.
USN uppercase-normalized; email validated; ranges enforced to match the DB checks.

Endpoints (all @require_auth; writes need the roles from the RLS policies):
- GET    /api/students?search=&department=&batch_year=&status=&cgpa_min=&cgpa_max=&sort=cgpa&order=desc&page=1&per_page=10
         → {items, total, page, per_page, summary: {total, placed, in_process, not_placed, requires_support}}
         requires_support = cgpa < 7.0 OR any skill score below the technical/aptitude thresholds from app_settings.
- GET    /api/students/<id>   → student + latest skill_assessment + latest prediction
- POST   /api/students        → 201; 409 on duplicate USN
- PUT    /api/students/<id>
- DELETE /api/students/<id>   → 204
- POST   /api/students/<id>/skills → add a skill assessment
- GET    /api/students/template.csv → header row + one example row
- POST   /api/students/import (multipart file, ?mode=upsert|insert_only&dry_run=true|false)
         Pandas: validate every row against the schema, collect row-level errors
         [{row, field, message}], max 5 MB / 5,000 rows, strip BOM, trim whitespace.
         dry_run returns {valid_count, error_count, errors, preview: first 10 rows} without writing.
         Real run upserts on usn in batches of 500 and returns {inserted, updated, failed, errors}.
- GET    /api/students/export.csv?<same filters> → streamed CSV with a Content-Disposition filename
         including the date. Guard against CSV injection (prefix cells starting with = + - @ with ').

Audit-log every write and every import/export.
Tests: CRUD happy path, duplicate USN 409, validation 400, import dry-run reporting a bad row,
export containing the header and the escaped formula cell.

Run the tests and show the output.
```

**Verify:**
- [ ] `pytest` green
- [ ] Download the template, add 3 rows (1 deliberately invalid), dry-run shows exactly 1 error, real import inserts 2
- [ ] Exported CSV opens cleanly in Excel

---

## Phase 6: Frontend foundation (layout, components, auth, routing)

**Prompt:**

```
Read AGENTS.md. Phase 6: convert the shared Stitch shell into React and wire up auth.
Open design/stitch/placement_dashboard/code.html and screen.png, and
design/stitch/login_authentication/code.html and screen.png.

1. src/lib/supabase.js (createClient with VITE_ vars). src/context/AuthContext.jsx: session state,
   onAuthStateChange, signIn(email, password), signOut(), and `profile` loaded from GET /api/auth/me.
   If the user is authenticated but /me returns 403, sign out and show "This account is not an
   authorized administrator."
2. src/services/api.js: axios instance (baseURL VITE_API_BASE_URL or /api) with an interceptor that
   attaches the current access token. On 401, refresh the session once, else redirect to /login.
   Normalize errors to {code, message, details}.
   Per-module service files: studentsService, predictionService, analyticsService, skillsService, adminService.
3. src/routes/ProtectedRoute.jsx (+ optional allowedRoles). Router: /login public; everything else
   inside AppLayout behind ProtectedRoute; /admin restricted to super_admin; 404 page.
4. src/layouts/AppLayout.jsx: convert the Stitch <aside> sidebar and <header> topbar 1:1
   (same classes and icons). Active nav state comes from the router. Sidebar footer "Flask REST API"
   chip polls /api/health every 60s and shows Connected / Offline + the real model version.
   Topbar shows the real profile name and role, a dropdown with Sign out, and the global search
   (navigates to /students?search=). Below 1024px: hamburger, sidebar as an off-canvas drawer with overlay.
   Remove the hardcoded avatar photo (use initials).
5. Reusable components extracted from the Stitch markup (src/components/ui/):
   Button (primary/secondary/destructive/accent, loading state), Card, MetricCard (label, value,
   unit, trend badge, icon), StatusChip (placed/in_process/not_placed/opted_out per DESIGN.md colors),
   DataTable (sortable headers, Stitch header styling, banded rows, horizontal scroll inside card),
   Pagination, Select, Input, FilterChip, ProgressBar (6px, gradient #4338CA→#38BDF8), Modal,
   ConfirmDialog, Skeleton, EmptyState, ErrorState, PageHeader (eyebrow + title + subtitle + actions),
   Icon (Material Symbols wrapper).
   Also src/components/charts/PlotlyChart.jsx using react-plotly.js/factory + plotly.js-dist-min,
   with a shared layout theme (Hanken Grotesk, transparent bg, token colors, responsive, displaylogo false).
6. LoginPage: convert login_authentication 1:1, but:
   - Left panel live stats from /api/health only (no fake cohort numbers). Remove the "Autonomous ·
     AICTE", ISO, SSL, 2FA and subnet items, and the Evaluation Presets block.
   - Keep the role tabs as purely visual context or remove them (the role comes from admin_profiles).
   - Real email/password sign-in with inline errors, a show/hide password toggle, a loading button,
     and "Forgot password" → supabase resetPasswordForEmail.
7. Placeholder pages for each route that render PageHeader only.

Run the dev server and test: login works, a wrong password shows an error, a refresh keeps the
session, sign-out returns to /login, and the mobile drawer works at 375px.
```

**Verify:**
- [ ] Login → dashboard shell, reload keeps the session, sign out works
- [ ] Shell matches `screen.png` side by side at 1440px
- [ ] At 375px: drawer menu works, no horizontal page scroll
- [ ] Stopping Flask flips the sidebar chip to "Offline"

---

## Phase 7: Student Management page

**Prompt:**

```
Read AGENTS.md. Phase 7: build StudentsPage from design/stitch/student_management (code.html + screen.png).

- PageHeader + action buttons: Import CSV, Export CSV, Add Student.
- 4 MetricCards from the `summary` returned by GET /api/students (respecting current filters).
- "Bulk Student Ingestion" banner: Download .CSV Template (GET template.csv) and Batch Upload
  → ImportModal: file drop zone → dry-run preview table + row errors → Confirm import → result toast,
  then refresh the list.
- Filter bar: debounced (300ms) search, department, status, CGPA tier; active-constraint chips with
  remove ×; Reset. Sync filters to the URL query string (so the topbar search works).
- DataTable exactly like Stitch: initials avatar, name + USN + email, department chip, CGPA pill
  (red if < 7.0), aptitude/technical/comm (technical red if < threshold), StatusChip (with company).
  Sortable columns, per-page select (10/25/50), server-side pagination.
- Row actions menu: View (drawer with full profile, latest skills, latest prediction, link to
  "Run prediction" and "Skill gap"), Edit, Delete (ConfirmDialog).
- StudentFormModal (create/edit) with client validation mirroring the pydantic rules; field-level
  server errors mapped back onto inputs; 409 → "USN already exists".
- Export CSV uses the current filters.
- Loading skeleton rows, empty state ("No students match these filters"), error state with retry.

Test full CRUD plus import/export in the browser and report what you checked.
```

**Verify:**
- [ ] Add → appears; Edit → updates; Delete → gone, and each write shows up in `audit_log`
- [ ] Filters + pagination + sort agree with SQL counts
- [ ] Import the 40-row CSV with 2 bad rows: errors shown, good rows imported
- [ ] Table scrolls inside its card on mobile

---

## Phase 8: Placement Prediction (API + page)

Use **Planning mode**.

**Prompt:**

```
Read AGENTS.md. Phase 8: real ML predictions.

Backend (app/routes/predict.py):
- GET  /api/model → active model metadata (version, algorithm, metrics, features, unused_by_model,
       trained_at, dataset_source, training_rows, threshold).
- POST /api/predict  body: {student_id?} OR {features:{...}}; optional save=true.
       Uses app.extensions["model"]. Threshold = app_settings.at_risk_probability.
       Returns {probability, label, confidence ('high' if |p-0.5| > 0.3, 'medium' if > 0.15, else 'low'),
       contributions (sorted by |impact|), percentile (vs latest predictions for the same batch, if any),
       advisory (rule-based text: top 2 positive and top 2 negative drivers, phrased as guidance,
       not a guarantee), model_version}.
       If save=true, insert into predictions + audit log.
- POST /api/predict/batch  body: {department?, batch_year?, only_unpredicted?: bool}
       → predicts with Pandas in one pass, bulk inserts, returns {count, placed_pred, at_risk}.
- GET  /api/predictions?student_id=&page=&search= → audit log of inference runs with a feature snapshot.
- GET  /api/predictions/export.csv
Tests: manual features predict, student_id predict, invalid feature 400, batch run count.

Frontend PredictionPage from design/stitch/placement_prediction:
- Model banner: real architecture/version, CV accuracy ± std, test set size, trained date,
  ROC-AUC, "Leakage guard: placement outcome fields excluded" (true by construction).
- Left "Inference Feature Pipeline": tabs Select Existing Student (searchable async select that
  autofills from the registry) | Manual Assessment. Stage 1 and Stage 2 inputs as in Stitch.
  Inputs listed in unused_by_model get a small "not used by model" tag. Reset Defaults; Run prediction.
  Remove the hardcoded preset student chips (or replace them with the 3 most recent real students).
- Right result card: PREDICTED: PLACED/NOT PLACED, probability bar with threshold marker,
  confidence chip, contributions list (bars, + green / - rose), advisory panel, cohort percentile,
  "Commit to Profile" (save=true). Disclaimer line: "Statistical estimate from historical data, not
  a guarantee of placement."
- "Run Batch Inference" button → modal (department/batch) → progress → result toast.
- "Inspect Weights" → drawer with global feature importances as a Plotly horizontal bar.
- Saved Inference Audit Log table with paging, filter, CSV export, view-details drawer.

Test a high-CGPA and a low-CGPA student and confirm the probabilities differ sensibly.
```

**Verify:**
- [ ] Probability changes when you edit inputs (e.g. CGPA 6.5 vs 9.2)
- [ ] Banner metrics equal `metadata.json`, not the Stitch numbers
- [ ] Commit to Profile → row in `predictions`, visible in the audit log table
- [ ] Batch inference on 40 students completes and the counts match the DB

---

## Phase 9: Dashboard

**Prompt:**

```
Read AGENTS.md. Phase 9: DashboardPage from design/stitch/placement_dashboard.

Backend GET /api/dashboard?department=&batch_year=&status= (Pandas aggregation over students +
latest predictions) returns:
- kpis: total_eligible (excluding opted_out), opted_out, placed, placement_rate, target_rate
  (app_settings), students_to_target, avg_placed_cgpa, min/max placed cgpa, yoy deltas when the
  previous batch exists (null otherwise; hide the badge when null).
- outcome_distribution: counts by status.
- department_performance: [{department, placed, eligible, rate}].
- cgpa_tiers: tiers >9, 8–8.9, 7–7.9, <7 with candidates, placed, rate (actual) and avg predicted
  probability (model).
- top_recruiters: group by company → hires, max/avg package_lpa (top 5).
- recent_activity: last 10 audit_log rows joined to student names.
- at_risk_count: latest prediction probability < threshold.

Frontend:
- Header actions: Import CSV (reuse ImportModal), Export Summary (CSV of KPIs + departments),
  Run ML Prediction (batch modal from Phase 8), Add Student (StudentFormModal).
- Filter strip (department, batch, status pills) re-queries; model chip shows the real algorithm,
  accuracy and "updated X ago".
- 4 MetricCards; donut (Plotly pie with hole=0.7, center annotation = total) for outcomes;
  department bars (Percentage/Counts toggle); CGPA tier cards; top recruiters list;
  "AI Recommendation" strip generated from at_risk_count and the lowest tier
  (link → /skill-gap?tier=4); activity feed with relative times and a Refresh button.
- Charts: Plotly with the shared theme, hover tooltips, and click on a department bar → /students?department=X.

Verify the numbers against SQL counts and report.
```

**Verify:**
- [ ] KPI totals match `select placement_status, count(*) from students group by 1`
- [ ] Changing filters updates every widget
- [ ] Clicking a chart bar navigates to the filtered student list

---

## Phase 10: Analytics & Reports

**Prompt:**

```
Read AGENTS.md. Phase 10: AnalyticsPage from design/stitch/analytics_reports.

Backend (app/routes/analytics.py, Pandas):
- GET /api/analytics/overview?filters → conversion rate vs target, median and mean package, max
  package + company, inter-branch parity (min dept rate / max dept rate), tier-1 conversion share.
- GET /api/analytics/departments → enrolled, eligible (opted-in), placed, avg/top package,
  dream offers (> configurable LPA) per dept.
- GET /api/analytics/cgpa-correlation → per CGPA tier: students, placed, rate, avg package;
  Pearson r between cgpa and placed (point-biserial) computed for real.
- GET /api/analytics/packages → histogram bins + tier buckets (Super Dream / Dream / High Potential /
  Core & IT, cutoffs from app_settings).
- GET /api/analytics/skills → average of each skill axis by department.
- Report exports (record each in report_exports + audit_log):
  GET /api/reports/department-ledger.csv, GET /api/reports/company-audit.xlsx (pandas + openpyxl,
  one sheet per company; ask before adding openpyxl), GET /api/reports/summary.pdf (optional:
  only if I approve adding a PDF lib; otherwise hide this card).
- GET /api/reports/history → recent report_exports rows.

Frontend:
- Cohort slicing filter panel with Apply/Reset and active chips.
- 4 KPI cards; department benchmark cards; grouped bar chart (Enrolled / Eligible / Placed) with a
  Graphical | Tabular toggle (the table view uses DataTable).
- CGPA vs Placement tier list + a Plotly scatter (cgpa vs latest probability, colored by status).
- Package spread: stacked ratio bar + tier cards + Plotly histogram.
- Skills by department: Plotly heatmap.
- Export Center: preset cards → download; history table with type chips and download actions.
- Every chart: hover, zoom/reset, download PNG via the modebar, resizes on window change.

Test that each export downloads and opens.
```

**Verify:**
- [ ] Each Plotly chart is interactive and correct on mobile
- [ ] Correlation coefficient matches a quick Pandas check
- [ ] Exports download and appear in history

---

## Phase 11: Skill Gap Analysis

Use **Planning mode**.

**Prompt:**

```
Read AGENTS.md. Phase 11: SkillGapPage from design/stitch/skill_gap_analysis.

Backend app/services/skill_rules.py: a deterministic, transparent rule engine.
- Inputs: the student's latest skill_assessment (dsa, system_design, core_cs, aptitude, communication),
  cgpa, and app_settings (skill_target per axis, technical/aptitude thresholds, tier-1 CGPA).
- Output: overall_competency (mean), per-axis {score, target, gap, severity:
  'critical' (gap >= 20) | 'needs_refinement' (0 < gap < 20) | 'meets' | 'surplus'},
  critical_domain (largest gap), strongest_domain, eligible_tier ('tier1' if cgpa >= tier1_min_cgpa
  and no critical gaps, etc.), and a prioritized roadmap: for each gap axis a remediation item from a
  static catalog in skill_catalog.py (title, code like REM-DSA-01, focus modules, deliverables,
  priority 1–3 by severity). Communication/other surpluses produce a "strength reinforcement" item.
  Every item includes a human-readable "diagnostic trigger" explaining exactly which rule fired.
- GET /api/skills/gap/<student_id>
- GET /api/skills/cohort?department=&batch_year=&severity=&search=&page= → table rows with the
  primary deficit flag and remediation status.
- PATCH /api/skills/remediation/<student_id> {status: 'enrolled'|'action_required'|'awaiting_retest'|'benchmark_met'}
  (add a remediation_status column on students or a small table via a migration file
  database/migrations/002_remediation.sql; keep schema.sql updated too).
- GET /api/skills/cohort/export.csv
Unit tests for the rule engine: boundary values at exactly the threshold, missing assessment → 404
with a helpful message, ordering of priorities.

Frontend:
- Target-student async selector (URL param ?student=), gap and tier badges.
- 4 summary cards. 5-axis Plotly radar (scatterpolar): student (filled) vs target threshold (dashed),
  plus a 5-cell score strip with deficits/surpluses.
- Sub-topic performance bars per axis with severity chips.
- Right column: "Rule engine" explainer card (accurate wording: deterministic thresholds
  configured in Admin) and roadmap cards styled by priority. Buttons update remediation status.
- Cohort deficit table with filters, pagination, status change and CSV export.
- "Trigger Batch Assessment Sync": recompute flags for the filtered cohort (no fake sync source).
- "Export Diagnostic Report": CSV for the selected student.
```

**Verify:**
- [ ] Student with DSA 52 and target 75 → critical DSA gap, priority-1 roadmap item
- [ ] Changing `skill_target` in settings changes the result
- [ ] `pytest tests/test_skill_rules.py` green

---

## Phase 12: Admin & Settings

**Prompt:**

```
Read AGENTS.md. Phase 12: AdminPage from design/stitch/admin_settings (super_admin only; auditor
gets read-only access to the audit trail).

Backend app/routes/admin.py:
- GET /api/admin/users; POST /api/admin/users {email, full_name, role, department} → create the
  auth user with the service client (auth.admin.create_user, email_confirm true, temporary password
  OR auth.admin.invite_user_by_email) and insert admin_profiles; PATCH role/is_active; prevent removing
  or demoting the last super_admin; prevent self-deactivation.
- GET /api/admin/audit?action=&actor=&from=&to=&page= ; GET /api/admin/audit/export.csv
- GET /api/admin/model → active model metadata + list of ml_models versions.
- POST /api/admin/model/retrain → background thread (or subprocess) running ml.train --register;
  returns a job id; GET /api/admin/model/jobs/<id> for status. On success, hot-reload the model in
  app.extensions. Only one job at a time (409 otherwise).
- POST /api/admin/model/activate/<version> → switch the active model (artifacts are versioned in
  artifacts/<version>/).
- Settings use the Phase 4 endpoints.

Frontend:
- Current session identity card (real user, role, last sign-in from the Supabase session).
- Production ML telemetry card (real metrics); "Run diagnostic" = /api/health + a sample prediction latency.
- RBAC table: search, role filter, add-admin modal, role change, activate/deactivate with confirm.
  Drop the fake 2FA / session columns, or show only what Supabase actually provides (last_sign_in_at).
- Model governance: metric tiles, the feature-vector list (used vs unused), a calibration curve
  (Plotly line from metadata), a feature importance bar, Retrain with job progress, version list
  with Activate.
- Thresholds & cutoffs: sliders bound to app_settings with min/max/defaults, Save with confirm,
  "last saved by/at".
- System preferences: API base URL display (read-only), default page size (saved per user in
  localStorage with try/catch), allowed CORS origins (read-only display).
- Security audit trail: filterable list + CSV export.

Test: create a placement_officer, sign in as them in a private window, confirm /admin is blocked
and student delete works but settings save is forbidden.
```

**Verify:**
- [ ] New admin can sign in; their role restrictions hold in both UI and API
- [ ] Retrain completes, new version appears, Activate switches predictions
- [ ] Threshold change takes effect in Prediction and Skill Gap

---

## Phase 13: Hardening, responsive QA, tests and README

**Prompt:**

```
Read AGENTS.md. Phase 13: production readiness pass. Don't add features.

1. Security review: every /api route except health has @require_auth; role decorators match the RLS
   policies; no service key in frontend bundles (grep dist/); CORS restricted; request size limits;
   pydantic on all bodies; CSV injection guard on all exports; rate-limit /api/predict and the import
   endpoint (ask before adding flask-limiter); generic 500 messages.
2. RLS test script database/tests/rls_check.sql (or a Python script) proving anon gets nothing and
   faculty_mentor cannot delete.
3. Responsive QA at 375, 768, 1024 and 1440px for all 7 pages; fix overflow, tap targets >= 40px,
   chart resizing, table scrolling. Keyboard focus rings (focus:ring-secondary). aria-labels on
   icon-only buttons.
4. Performance: lazy-load route pages and Plotly; memoize heavy tables; debounce filters.
5. Tests: backend pytest coverage for all blueprints (aim for 80%+ on routes/services). Frontend:
   Vitest + React Testing Library for MetricCard, StatusChip, StudentFormModal validation and
   ProtectedRoute (ask before adding).
6. README.md complete: overview + screenshots, architecture diagram (Mermaid), prerequisites,
   Supabase setup (schema → seed → first admin → disable sign-ups), dataset setup, training the model,
   env vars table, running backend and frontend, running tests, CSV format spec, API endpoint table,
   role/permission matrix, troubleshooting (CORS, JWT/JWKS, RLS 0 rows, model not loaded), and
   deployment notes (Render/Railway for Flask with gunicorn; Vercel/Netlify for the frontend; set
   VITE_API_BASE_URL).
7. Final full-system walkthrough: login → add student → predict → skill gap → analytics → export →
   admin changes threshold → re-predict. Report the results.
```

**Verify:**
- [ ] `npm run build` produces no errors; `grep -r "service_role\|sb_secret" frontend/dist` → nothing
- [ ] Backend and frontend test suites green
- [ ] A fresh clone + README steps works end to end

---

## Appendix A: API endpoint map

| Method | Endpoint | Roles |
|---|---|---|
| GET | `/api/health` | public |
| GET | `/api/auth/me` | any admin |
| GET/PUT | `/api/settings` | read: any · write: super_admin |
| GET/POST | `/api/students` | read: any · write: SA, PO, FM |
| GET/PUT/DELETE | `/api/students/<id>` | delete: SA, PO |
| POST | `/api/students/<id>/skills` | SA, PO, FM |
| GET | `/api/students/template.csv`, `/export.csv` | any |
| POST | `/api/students/import` | SA, PO |
| GET | `/api/model` | any |
| POST | `/api/predict`, `/api/predict/batch` | any / SA, PO |
| GET | `/api/predictions`, `/export.csv` | any |
| GET | `/api/dashboard` | any |
| GET | `/api/analytics/*`, `/api/reports/*` | any |
| GET/PATCH | `/api/skills/*` | read: any · write: SA, PO, FM |
| * | `/api/admin/*` | super_admin (audit: + auditor) |

SA = super_admin · PO = placement_officer · FM = faculty_mentor

## Appendix B: CSV import format

```
usn,full_name,email,department,batch_year,tenth_pct,twelfth_pct,cgpa,aptitude_score,technical_score,communication_score,internships,projects,certifications,backlogs,extracurricular,placement_training,placement_status,company,package_lpa,dsa,system_design,core_cs,aptitude,communication
1RV21CS001,Aditya Rao,aditya.rao@college.edu.in,CSE,2025,89.2,86.5,8.85,86,92,84,1,3,2,0,true,true,placed,TCS,7.0,80,72,78,86,84
```
Skill columns are optional; when present, they create a `skill_assessments` row.

## Appendix C: When things go wrong

| Symptom | Likely cause | Prompt to paste back |
|---|---|---|
| API returns `[]` though data exists | RLS: user not in `admin_profiles`, or the backend is using the anon client without the user JWT | "Lists come back empty for my admin user. Check get_user_client sets postgrest.auth(token) and that is_admin() finds my admin_profiles row." |
| 401 on every call | JWKS/audience mismatch or an expired token | "All /api calls 401. Log (dev only) which verification path fails and fix the JWT verification per Phase 4." |
| Stitch classes don't apply | Tailwind v4 installed or config not copied | "Tailwind tokens like bg-primary-container aren't applied. Confirm tailwind v3.4 and that the Stitch config is in tailwind.config.js." |
| Plotly blank / huge bundle | Wrong import | "Use react-plotly.js/factory with plotly.js-dist-min and lazy-load the chart component." |
| Model not loaded | Artifacts missing | "Health says model_loaded false. Run ml.train and make create_app load from MODEL_DIR with a clear log line." |
| Numbers look like the mockup | Hardcoded HTML left in | "Search the page components for any literal numbers or names copied from Stitch and replace them with API data." |

---

**Order of work:** 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13. Each phase depends on the ones before it, so don't skip ahead.