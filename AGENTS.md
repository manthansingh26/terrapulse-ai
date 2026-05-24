# TerraPulse AI — Agent Instructions

Real-time environmental intelligence dashboard (React + FastAPI) monitoring AQI across 20 Indian cities with ML-powered 24-hour forecasts. Deployed: frontend on Vercel, backend on Render.

## Key Commands

**Development**
- `make dev-local` — Start backend (FastAPI) + frontend (React) locally in parallel
- `make dev` — Start all services in Docker (frontend, backend, postgres, pgadmin)
- `make test` — Run all tests (backend + frontend)
- `make type-check` — Type checks (backend: mypy, frontend: tsc)
- `make lint` — Lint backend (flake8) and frontend (eslint)
- `make format` — Format backend (black) and frontend (prettier)

**Single-service dev**
- Backend: `cd backend && python -m uvicorn app.main:app --reload --port 8000`
- Frontend: `cd frontend && npm run dev` (dev server, auto-open at localhost:5173)

**Testing**
- Backend single test: `cd backend && pytest tests/test_api_health.py -v`
- Frontend single test: `cd frontend && npm test -- --testNamePattern="..." --watch=false`
- Backend uses in-memory SQLite (conftest.py), no PostgreSQL needed for tests

**Production**
- `make prod` — Compose up with docker-compose.prod.yml
- Frontend builds via Vercel CI/CD; backend via Render

## Architecture & Boundaries

**Monorepo structure:**
- `backend/` — FastAPI + SQLAlchemy, Python 3.11
- `frontend/` — React 18 + TypeScript + Vite 5
- `docker-compose.yml` — postgres:15, redis, backend, frontend, pgadmin (dev)
- `docker-compose.prod.yml` — production variant (no pgadmin, optimized)

**Backend entry point:** `backend/app/main.py` → FastAPI app with CORS, rate limiting, database init
**Frontend entry point:** `frontend/src/main.tsx` → React, then `App.tsx`

**API routes** (all prefixed `/api`)
- `/health` — health check
- `/cities/all` → all city AQI data
- `/auth/register`, `/auth/login` → JWT auth
- `/ml/train`, `/ml/forecast/{city}`, `/ml/explain/{city}` → ML endpoints
- `/alerts/*` → email alert endpoints
- WebSocket at `/ws` for live updates

**ML pipeline:** `backend/app/ml/aqi_model.py`
- Auto-selects best model (RandomForest, GradientBoosting, or Linear) via cross-validation
- Trained on historical AQI data, exports metrics + feature importance
- 24-hour forecasts per city; artifacts stored in `backend/app/ml/artifacts/`

**Database:** PostgreSQL (Neon in prod, local docker in dev). Migrations via Alembic (if present).
**Background jobs:** APScheduler syncs WAQI API every 30 min (configured in main.py seed_local_data)
**External API:** WAQI (aqicn.org) — requires `WAQI_API_TOKEN` env var

## Environment & Config

**.env loading:** Uses python-dotenv; all vars in `.env.example`. Key secrets:
- `DATABASE_URL` — PostgreSQL or SQLite (tests use in-memory)
- `SECRET_KEY` / `JWT_SECRET_KEY` — must be ≥32 chars
- `WAQI_API_TOKEN` — required for live AQI data
- `CORS_ORIGINS` — comma-sep list or JSON array; default allows localhost:3000, :5173, :3000 (127.0.0.1)

**CI/CD:** GitHub Actions in `.github/workflows/ci.yml`
- Backend: Python 3.11, postgres:15 service, flake8 lint (E9, F63, F7, F82 only), pytest
- Frontend: Node 18, no tests in CI, tsc --noEmit + npm run build
- Both run on push to main and PRs

**Linting/type quirks:**
- Backend flake8 is *strict* on syntax/undefined names but skips style; use `black` for formatting
- Frontend eslint + prettier; CI runs tsc with --noEmit only (no test suite in CI)
- Run `make type-check` locally before pushing — catches runtime errors

## Testing

**Backend tests** live in `backend/tests/`. Use conftest.py fixtures:
- `db_session` — transactional SQLite, auto-rollback per test
- `client` — TestClient with overridden get_db, no real DB calls
- Example: `backend/tests/test_api_health.py` (simple), `test_api_auth.py` (fixtures)

**Frontend tests** — none in CI, but framework ready (Jest-like via Vite defaults). Structure TBD.

**Running subset:** 
- `pytest tests/test_ml_model.py::test_train -v` (specific test)
- `npm test -- --testNamePattern="Login" --watch=false` (frontend, if present)

## Common Mistakes & Gotchas

1. **Environment variables:** Must run backend from `backend/` dir or with `backend/.env` in path. Frontend uses `VITE_*` prefix for build-time vars.
2. **Database:** Local dev defaults to SQLite (`terrapulse.db`). Override `DATABASE_URL` to use postgres. Tests always use in-memory SQLite.
3. **Frontend dev server:** Runs on :5173 by default, not :3000. CORS is already set to allow both.
4. **ML model artifacts:** Stored as pickled .joblib files in `backend/app/ml/artifacts/`. Not git-tracked; trained on first `/ml/train` call.
5. **Port conflicts:** Backend :8000, frontend :5173 (or :3000 in prod), postgres :5432, redis :6379, pgadmin :5050
6. **Rate limiting:** Enabled by default (100 req/min per IP). Configured via SlowAPI + env vars.
7. **Seeding:** `main.py` auto-seeds demo user + sample data on startup if DB empty. Stale data (>12h) triggers re-seed.

## Workflow Notes

- **Type safety is critical.** Run `make type-check` before committing. Backend uses Pydantic v2; frontend is strict TS.
- **Test order matters for CI:** Lint → Type-check → Test. Run locally first (`make test`) to catch issues.
- **Email alerts** (optional feature): Requires Gmail SMTP config (`SMTP_EMAIL`, `SMTP_PASSWORD`). Can be disabled via `SEND_ALERTS=False`.
- **WebSocket:** Available at `/ws` for live updates. Heartbeat every 30s (configurable).
- **Debugging:** Backend logs go to `backend/logs/app.log` (if enabled). Frontend uses browser console.

## References

- **Tech stack details:** See README.md § Tech Stack
- **API docs:** Swagger UI at `http://localhost:8000/api/docs` when backend is running
- **Database schema:** `backend/app/models/models.py` — ORM definitions for User, EnvironmentalData, etc.
- **Frontend architecture:** `frontend/src/` — pages, components, hooks, services (Axios client in services/)
