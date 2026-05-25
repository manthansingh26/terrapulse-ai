"""
Live AQI data fetcher using WAQI (World Air Quality Index) API.

Fetches real-time AQI, temperature, humidity, wind speed, and pollutant
data for all 20 monitored Indian cities and stores it in PostgreSQL.
"""

import logging
from datetime import datetime, timezone
from typing import Optional

import httpx

from app.core.config import get_settings
from app.db.database import SessionLocal
from app.models.models import EnvironmentalData

logger = logging.getLogger(__name__)

settings = get_settings()

# Mapping from our city names → WAQI feed identifiers
CITY_WAQI_MAP = {
    "Ahmedabad": "ahmedabad",
    "Mumbai": "mumbai",
    "Delhi": "delhi",
    "Bangalore": "bangalore",
    "Hyderabad": "hyderabad",
    "Chennai": "chennai",
    "Kolkata": "kolkata",
    "Pune": "pune",
    "Jaipur": "jaipur",
    "Lucknow": "lucknow",
    "Surat": "surat",
    "Indore": "indore",
    "Nagpur": "nagpur",
    "Bhopal": "bhopal",
    "Vadodara": "vadodara",
    "Ghaziabad": "ghaziabad",
    "Ludhiana": "ludhiana",
    "Kanpur": "kanpur",
    "Visakhapatnam": "visakhapatnam",
    "Pimpri-Chinchwad": "pune",  # Nearest major station
}


def _extract_iaqi(data: dict, key: str) -> Optional[float]:
    """Safely extract a value from the WAQI iaqi dict."""
    try:
        return float(data.get("iaqi", {}).get(key, {}).get("v"))
    except (TypeError, ValueError):
        return None


def fetch_single_city(city: str, feed_name: str, token: str) -> Optional[dict]:
    """Fetch AQI data for one city from WAQI API."""
    url = f"https://api.waqi.info/feed/{feed_name}/?token={token}"
    try:
        response = httpx.get(url, timeout=15.0)
        payload = response.json()

        if payload.get("status") != "ok":
            logger.warning(f"WAQI returned non-ok for {city}: {payload.get('data')}")
            return None

        data = payload["data"]
        aqi_value = data.get("aqi")

        # Some stations return '-' when data is unavailable
        if aqi_value is None or aqi_value == "-":
            logger.warning(f"No AQI data for {city}")
            return None

        return {
            "city": city,
            "aqi": int(aqi_value),
            "co2": _extract_iaqi(data, "co"),
            "temperature": _extract_iaqi(data, "t"),
            "humidity": _extract_iaqi(data, "h"),
            "wind_speed": _extract_iaqi(data, "w"),
            "rainfall": _extract_iaqi(data, "r") or 0,
            "timestamp": datetime.now(timezone.utc),
        }
    except httpx.TimeoutException:
        logger.warning(f"Timeout fetching AQI for {city}")
        return None
    except Exception as e:
        logger.error(f"Error fetching AQI for {city}: {e}")
        return None


def fetch_all_cities() -> None:
    """Fetch live AQI data for all cities and save to database."""
    token = settings.WAQI_API_TOKEN

    if not token or token == "demo":
        logger.info("⏭️ WAQI token not configured — skipping live AQI fetch")
        return

    logger.info("🌍 Fetching live AQI data for all cities...")

    db = SessionLocal()
    success_count = 0
    error_count = 0

    try:
        for city, feed_name in CITY_WAQI_MAP.items():
            result = fetch_single_city(city, feed_name, token)
            if result:
                db.add(EnvironmentalData(**result))
                success_count += 1
            else:
                error_count += 1

        db.commit()
        logger.info(
            f"✅ Live AQI fetch complete: {success_count} cities updated, "
            f"{error_count} failed"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to save AQI data: {e}")
    finally:
        db.close()
