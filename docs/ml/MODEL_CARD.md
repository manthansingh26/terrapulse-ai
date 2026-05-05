# Model Card: AQI 24-Hour Forecaster

## Summary

TerraPulse AI uses a supervised regression model to predict AQI 24 hours ahead for
each monitored city. The model consumes latest environmental readings and time/city
features, then returns a predicted AQI, expected change, risk level, and confidence
score.

## Intended Use

- Rank cities by forecasted AQI risk.
- Support early warning alerts when predicted AQI crosses a threshold.
- Provide a portfolio-grade machine learning demonstration for environmental data.

## Not Intended For

- Public health decisions without validation against certified monitoring stations.
- Regulatory compliance reporting.
- High-stakes automated alerting without human review and monitored model quality.

## Model Details

- Algorithm: Random Forest Regressor
- Library: scikit-learn
- Target: AQI value 24 hours after the source record
- Features:
  - current AQI
  - CO2
  - temperature
  - humidity
  - wind speed
  - rainfall
  - hour
  - day of week
  - month
  - city code

## Evaluation

The current project stores these metrics in `backend/app/ml/artifacts/metrics.json`:

- MAE: mean absolute error in AQI points
- RMSE: root mean squared error in AQI points
- R2: explained variance
- training rows
- test rows
- synthetic rows inserted during training

Forecasting validation should use a time-based holdout so later timestamps are used
for evaluation. Random train/test splits can overstate performance for time series
forecasting.

## Known Limitations

- Some historical records may be synthetic fallback data when real ingestion is not
  available.
- City identity is currently encoded as an integer code, not learned from spatial
  coordinates or richer station metadata.
- Confidence is heuristic and should not be interpreted as calibrated probability.
- Feature importance is global; it does not explain a single city prediction.
- No drift monitoring is currently enforced before inference.

## Recommended Upgrades

- Add a versioned model registry or local run history.
- Store train/test time windows with each run.
- Add SHAP or another local explanation method.
- Add scheduled retraining and freshness checks.
- Track prediction error after actual future AQI arrives.

