# TerraPulse AI ML Documentation

This folder documents the machine learning layer behind TerraPulse AI.

## Current Model

- Task: 24-hour AQI forecasting for monitored Indian cities
- Model: `RandomForestRegressor`
- Training source: demo `environmental_data` records in PostgreSQL
- Current artifact path: `backend/app/ml/artifacts/`
- Inference API: `/api/ml/forecast/{city}` and `/api/ml/forecast/all`
- Operations UI: frontend `Model Lab`

## Documents

- [Model Card](./MODEL_CARD.md)
- [Dataset Card](./DATASET_CARD.md)
- [Pipeline](./PIPELINE.md)

## Current Status

The project has a working ML demo pipeline with saved artifacts, feature importance,
evaluation samples, backend endpoints, and a frontend model operations page.

The AQI and weather records in the deployed demo are seeded sample values, not official
real-time city readings. The next upgrades are production-oriented: verified real data
ingestion, source metadata, versioned training runs, time-based validation, drift
monitoring, and scheduled retraining.
