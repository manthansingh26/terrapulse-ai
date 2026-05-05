"""Train the TerraPulse AQI forecasting model."""

from app.db.database import SessionLocal
from app.ml.aqi_model import train_model


def main():
    db = SessionLocal()
    try:
        metrics = train_model(db)
        print("AQI model trained successfully")
        for key, value in metrics.items():
            print(f"{key}: {value}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
