# ML Pipeline

## Current Flow

1. Environmental records are stored in PostgreSQL.
2. `train_model` reads all records from `environmental_data`.
3. If there is too little history, deterministic synthetic hourly data is inserted.
4. Features are generated from current AQI, weather, time, and city code.
5. The target is the AQI 24 records ahead for the same city.
6. A Random Forest model is trained and evaluated.
7. Artifacts are saved under `backend/app/ml/artifacts/`.
8. FastAPI serves metrics, feature importance, evaluation samples, and forecasts.
9. The frontend Model Lab displays model operations and predictions.

## Artifact Files

- `aqi_forecaster.joblib`: trained model bundle
- `metrics.json`: training and evaluation metrics
- `feature_importance.json`: global permutation importance
- `evaluation_samples.json`: predicted-vs-actual samples
- `run_history.json`: recent versioned training runs
- `latest_run.json`: pointer to the latest run summary
- `runs/{run_id}/`: per-run metrics, feature importance, and evaluation samples

## Production Gap List

- Move synthetic fallback behind an explicit development flag.
- Extend run versioning to include immutable model binaries, not only metrics and evaluation files.
- Use time-based validation for forecasting.
- Store train/test date windows.
- Add data validation before training.
- Add drift monitoring before inference.
- Add scheduled retraining.
- Add endpoint tests for the ML API.

## Suggested Future Structure

```text
backend/app/ml/
  artifacts.py      # load/save versioned artifacts
  features.py       # feature and target construction
  training.py       # training and evaluation
  inference.py      # prediction and risk scoring
  monitoring.py     # drift and freshness checks
```
