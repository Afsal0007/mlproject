# Placement AI 🎓

> An intelligent campus placement prediction and recommendation platform powered by machine learning.

---

## What It Does

| Feature | Description |
|---------|-------------|
| **Placement Prediction** | ML model estimates a student's probability of being placed |
| **Salary Estimation** | Predicts expected CTC based on profile |
| **Skill Gap Analysis** | Compares student skills vs. job requirements |
| **Smart Recommendations** | Suggests skills and roles to improve placement chances |
| **Recruiter Dashboard** | Companies can post jobs and shortlist candidates |

---

## Tech Stack

- **Frontend**: React 18 + Vite + Zustand
- **Backend**: Python 3.11 + FastAPI + SQLAlchemy
- **ML**: scikit-learn + XGBoost + pandas
- **Database**: PostgreSQL 15 (SQLite for local dev)
- **Auth**: JWT
- **Infra**: Docker + docker-compose

---

## Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15 (or use SQLite for dev)

### 1. Clone & configure
```bash
git clone <repo-url>
cd placement-ai
cp .env.example .env
# Edit .env with your local values
```

### 2. Backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

App available at: [http://localhost:5173](http://localhost:5173)

### 4. ML Training (optional)
```bash
cd backend
python ml/train.py --data ../data/raw/placement_dataset.csv --output ml/models/
```

---

## Project Structure

```
placement-ai/
├── AGENTS.md                          ← AI agent project rules
├── ANTIGRAVITY_IMPLEMENTATION_GUIDE.md ← Phase-by-phase build guide
├── design/stitch/                     ← UI design reference (read-only)
├── frontend/                          ← React SPA
├── backend/
│   ├── app/                           ← FastAPI application
│   └── ml/                            ← ML pipeline & models
├── database/schema.sql                ← Database DDL
├── data/
│   ├── raw/                           ← Original datasets (immutable)
│   └── processed/                     ← Cleaned/transformed data
├── .env.example                       ← Environment variable template
└── README.md
```

---

## Development Phases

| Phase | Title | Status |
|-------|-------|--------|
| 0 | Repository Setup | ✅ Complete |
| 1 | Database Schema & Migrations | ⏳ Pending |
| 2 | Backend API (FastAPI) | ⏳ Pending |
| 3 | ML Pipeline & Model Training | ⏳ Pending |
| 4 | ML Inference API Integration | ⏳ Pending |
| 5 | Frontend SPA (React + Vite) | ⏳ Pending |
| 6 | Auth, Roles & Security | ⏳ Pending |
| 7 | Docker, CI/CD & Deployment | ⏳ Pending |

---

## Contributing

1. Create a branch: `git checkout -b feature/<your-feature>`
2. Commit using conventional commits: `feat:`, `fix:`, `chore:`
3. Push and open a Pull Request

---

## License

MIT © Placement AI Team
