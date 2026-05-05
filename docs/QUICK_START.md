# TerraPulse AI Quick Start

## URLs

When running locally:

| Service | URL |
| --- | --- |
| Frontend | http://127.0.0.1:3000/ |
| Backend API | http://127.0.0.1:8000/ |
| Swagger API Docs | http://127.0.0.1:8000/api/docs |
| ML Data Quality | http://127.0.0.1:8000/api/ml/data-quality |
| ML Runs | http://127.0.0.1:8000/api/ml/runs |

Demo login:

| Username | Password |
| --- | --- |
| `demo` | `demo123` |

## Start Locally On Windows

Backend:

```powershell
cd backend
venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd frontend
npm run dev -- --host 127.0.0.1
```

## Verify Project

Backend tests:

```powershell
backend\venv\Scripts\python.exe -m pytest backend/tests -v
```

Frontend checks:

```powershell
cd frontend
npm run lint
npm run type-check
npm run build
```

## Use The Website

1. Open http://127.0.0.1:3000/
2. Login with `demo` / `demo123`.
3. Go to `Dashboard` for AQI and ML risk summaries.
4. Go to `Map` for city-level AQI markers.
5. Go to `Analytics` for charts and trends.
6. Go to `Model Lab` for:
   - model metrics
   - training runs
   - data quality
   - feature importance
   - prediction explanations
   - retraining
   - ML alert checks

## Key ML Endpoints

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

## Important Files

| File | Purpose |
| --- | --- |
| `README.md` | Main project overview |
| `PROJECT_STATUS.md` | Completion and production-readiness status |
| `docs/ml/MODEL_CARD.md` | ML model card |
| `docs/ml/DATASET_CARD.md` | Dataset notes and limitations |
| `docs/ml/PIPELINE.md` | Training and artifact pipeline |
| `frontend/src/pages/ModelLab.tsx` | ML operations UI |
| `backend/app/ml/aqi_model.py` | Training, inference, and explanations |
| `backend/app/api/endpoints/ml.py` | ML API endpoints |

