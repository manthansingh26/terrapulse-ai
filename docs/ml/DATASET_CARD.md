# Dataset Card: Environmental AQI Records

## Source Table

Primary training data comes from the PostgreSQL `environmental_data` table.

Columns used by the current model:

- `city`
- `aqi`
- `co2`
- `temperature`
- `humidity`
- `wind_speed`
- `rainfall`
- `timestamp`

## Target Construction

For each city, records are sorted by timestamp. A training example uses the current
record as features and the AQI from 24 records later as the target.

This assumes approximately hourly records. If ingestion frequency changes, target
construction must be updated to select by timestamp delta instead of row offset.

## Data Quality Rules

Current behavior:

- Records without AQI are skipped.
- Missing numeric inputs fall back to defaults during feature generation.
- Synthetic hourly history can be inserted if the database is too small to train.

Needed production behavior:

- Track whether each row is real, synthetic, or imputed.
- Validate expected timestamp frequency per city.
- Store source API, station ID, and ingestion time.
- Reject or flag impossible values before training.

## Current Limitations

- The real-vs-synthetic split is not visible in the database schema.
- External API provenance is not stored per observation.
- No formal missingness report is generated before training.
- No drift report compares the training distribution with recent inference data.

## Recommended Dataset Upgrades

- Add `source`, `station_id`, `is_synthetic`, and `quality_flags` fields.
- Add daily ingestion jobs for AQI and weather.
- Add a pre-training data validation report.
- Add a dataset snapshot identifier to every model run.

