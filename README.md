# TerraPulse AI

Full-stack environmental intelligence dashboard for AQI monitoring, forecasting, alerts, and machine learning operations.

## Current Status

TerraPulse AI is complete as a local full-stack portfolio/demo project:

- React + TypeScript frontend
- FastAPI backend
- PostgreSQL-compatible data layer
- JWT authentication
- Dashboard, map, analytics, profile, and Model Lab pages
- AQI forecasting model with saved artifacts
- Time-based ML validation
- Model run history
- Data quality endpoint
- Prediction explanations
- Opening animation and ML-focused Model Lab animations

It is not yet a fully hosted production SaaS product. See [PROJECT_STATUS.md](./PROJECT_STATUS.md) for the exact completion status and remaining production work.

## Live Demo

- Frontend: https://terrapulse-ai.vercel.app
- Backend API: https://terrapulse-ai.onrender.com
- API Docs: https://terrapulse-ai.onrender.com/api/docs

Demo login:

- Username: `demo`
- Password: `demo123`

## Data Source Notice

The deployed demo currently uses seeded sample AQI/weather records and saved ML artifacts.
AQI values shown in the dashboard, map, analytics, and Model Lab are not official real-time
city readings. Real scheduled ingestion from verified providers such as WAQI, CPCB, or
OpenWeather is listed as production work.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, Recharts, Leaflet |
| Backend | FastAPI, SQLAlchemy, Pydantic, JWT auth |
| ML | scikit-learn RandomForestRegressor, joblib artifacts |
| Data | PostgreSQL-compatible SQLAlchemy models, local SQLite-compatible development |
| DevOps | Docker Compose, Makefile, GitHub Actions structure |

## Main Features

- User registration and login
- Protected dashboard routes
- Demo AQI and environmental analytics
- Interactive city map
- Demo city data with WebSocket support
- Email and ML forecast alert support
- Model Lab for ML operations
- AQI 24-hour forecasting
- Model metrics: MAE, RMSE, R2
- Feature importance
- Versioned training run history
- Data quality and freshness panel
- Per-city prediction explanations

## How To Run Locally

### Backend

```powershell
cd backend
venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

If dependencies are not installed:

```powershell
cd backend
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Frontend

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

Open http://127.0.0.1:3000/ and login with `demo` / `demo123`.

## How To Use The Website

1. Open the frontend URL.
2. Login with the demo account.
3. Use `Dashboard` for overall AQI and ML risk summaries.
4. Use `Map` to inspect city-level AQI locations.
5. Use `Analytics` for trend and comparison charts.
6. Use `Model Lab` for ML metrics, model runs, data quality, retraining, forecasts, and explanations.
7. Use `Profile` for account information.

## Machine Learning APIs

```text
POST /api/ml/train
GET  /api/ml/metrics
GET  /api/ml/runs
GET  /api/ml/runs/{run_id}
GET  /api/ml/data-quality
GET  /api/ml/feature-importance
GET  /api/ml/evaluation-samples
GET  /api/ml/forecast/all
GET  /api/ml/forecast/{city}
GET  /api/ml/explain/top
GET  /api/ml/explain/{city}
```

ML documentation:

- [ML Overview](./docs/ml/README.md)
- [Model Card](./docs/ml/MODEL_CARD.md)
- [Dataset Card](./docs/ml/DATASET_CARD.md)
- [Pipeline](./docs/ml/PIPELINE.md)

## Verification

Run these before presenting or deploying:

```powershell
backend\venv\Scripts\python.exe -m pytest backend/tests -v
cd frontend
npm run lint
npm run type-check
npm run build
```

Current known non-blocking warnings:

- Vite reports a large JavaScript bundle. This is expected until route-level code splitting is added.
- Pytest may warn about cache writes in restricted sandbox environments.
- Pydantic and SQLAlchemy deprecation warnings remain for a future cleanup pass.

## Project Structure

```text
terrapulse-ai/
  backend/
    app/
      api/endpoints/
      core/
      db/
      ml/
      models/
      schemas/
    tests/
  frontend/
    src/
      components/
      context/
      hooks/
      pages/
      services/
      styles/
  docs/
    ml/
    guides/
    api/
  archive/
```

## Production Readiness

The app is demo-complete. For production deployment, finish:

- Hosted domain and HTTPS
- Production secrets management
- Real scheduled AQI/weather ingestion
- Database migrations
- Observability and monitoring
- CI/CD deployment pipeline
- Broader frontend and API test coverage
- Model drift monitoring and scheduled retraining

See [PROJECT_STATUS.md](./PROJECT_STATUS.md).
