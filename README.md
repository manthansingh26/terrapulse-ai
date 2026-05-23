# TerraPulse AI

Real-time environmental intelligence dashboard monitoring live Air Quality Index (AQI) across 20 Indian cities with ML-powered 24-hour forecasts.

**Live:** [terrapulse-ai.vercel.app](https://terrapulse-ai.vercel.app)

---

## Architecture

```
┌──────────────────┐       HTTPS        ┌──────────────────────┐
│   React + TS     │ ◄───────────────── │    Vercel (Edge)      │
│   Vite Frontend  │                    └──────────────────────┘
└────────┬─────────┘
         │ API calls
         ▼
┌──────────────────┐       SQL          ┌──────────────────────┐
│   FastAPI         │ ◄────────────────►│  Neon PostgreSQL      │
│   Python Backend  │                   └──────────────────────┘
└────────┬─────────┘
         │ Scheduled (30 min)
         ▼
┌──────────────────┐
│   WAQI API        │  Live AQI telemetry
│   (aqicn.org)     │  20 cities
└──────────────────┘
```

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18, TypeScript, Vite 5, Tailwind CSS |
| **Charts** | Recharts |
| **Maps** | Leaflet + React-Leaflet |
| **State** | Zustand |
| **Backend** | FastAPI, Uvicorn, Pydantic v2 |
| **Database** | PostgreSQL (Neon), SQLAlchemy 2.0, Alembic |
| **ML** | scikit-learn (RandomForest, GradientBoosting, Linear — auto-selected) |
| **Scheduling** | APScheduler (30-min background AQI sync) |
| **Auth** | JWT (python-jose), bcrypt |
| **CI** | GitHub Actions (lint + test + build) |
| **Deployment** | Vercel (frontend), Render (backend) |
| **External API** | WAQI (World Air Quality Index) |

## Features

- **Live AQI Dashboard** — Real-time air quality for 20 cities via WAQI API
- **Interactive Map** — Leaflet GIS with color-coded AQI markers and risk filters
- **ML Forecasting** — 24-hour AQI predictions with model explainability
- **Model Comparison** — Automated RF vs GradientBoosting vs Linear selection with cross-validation
- **Analytics** — Historical trends, AQI distribution, city comparisons
- **Authentication** — JWT-based user registration and login

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or use SQLite for local dev)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Configure environment
cp .env.example .env         # Edit DATABASE_URL, SECRET_KEY, WAQI_API_TOKEN

# Run
uvicorn app.main:app --reload --port 8000
```

API docs available at `http://localhost:8000/api/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:5173`

### Running Tests

```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm test
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/cities/all` | All city AQI data |
| `GET` | `/api/cities/{city}` | Single city data |
| `POST` | `/api/auth/register` | Register user |
| `POST` | `/api/auth/login` | Login |
| `POST` | `/api/ml/train` | Train ML model |
| `GET` | `/api/ml/metrics` | Model metrics |
| `GET` | `/api/ml/model-comparison` | RF vs GBR vs Linear comparison |
| `GET` | `/api/ml/forecast/all` | 24h forecast for all cities |
| `GET` | `/api/ml/forecast/{city}` | 24h forecast for one city |
| `GET` | `/api/ml/explain/{city}` | Explainability for forecast |

## Project Structure

```
terrapulse-ai/
├── frontend/                # React + TypeScript + Vite
│   ├── src/
│   │   ├── pages/           # Dashboard, Map, Analytics, ModelLab
│   │   ├── components/      # Shared UI components
│   │   ├── services/        # API client (Axios)
│   │   └── hooks/           # WebSocket, custom hooks
│   └── package.json
├── backend/                 # FastAPI + Python
│   ├── app/
│   │   ├── api/endpoints/   # REST routes
│   │   ├── core/            # Config, security
│   │   ├── db/              # SQLAlchemy setup
│   │   ├── ml/              # Model training, prediction, comparison
│   │   ├── models/          # ORM models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # WAQI fetcher, scheduler
│   ├── tests/               # pytest test suite
│   └── requirements.txt
├── .github/workflows/ci.yml # GitHub Actions CI
├── docker-compose.yml       # Docker local dev
└── README.md
```

## License

MIT
