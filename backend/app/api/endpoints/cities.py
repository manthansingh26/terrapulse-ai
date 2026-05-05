from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import CityDataResponse
from app.core.config import get_settings

router = APIRouter(prefix="/cities", tags=["Cities"])

settings = get_settings()

# City coordinates for 20 Indian cities
CITY_COORDINATES = {
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Delhi": {"lat": 28.7041, "lon": 77.1025},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Pune": {"lat": 18.5204, "lon": 73.8567},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462},
    "Surat": {"lat": 21.1700, "lon": 72.8311},
    "Indore": {"lat": 22.7196, "lon": 75.8577},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882},
    "Bhopal": {"lat": 23.1815, "lon": 75.7873},
    "Vadodara": {"lat": 22.3072, "lon": 73.1812},
    "Ghaziabad": {"lat": 28.6692, "lon": 77.4538},
    "Ludhiana": {"lat": 30.9010, "lon": 75.8573},
    "Kanpur": {"lat": 26.4499, "lon": 80.3319},
    "Visakhapatnam": {"lat": 17.6869, "lon": 83.2185},
    "Pimpri-Chinchwad": {"lat": 18.6370, "lon": 73.7997}
}


def get_aqi_status_and_color(aqi: int = None):
    """Get AQI status and color"""
    if aqi is None:
        return "Unknown", "#808080"

    if aqi <= 50:
        return "Good", "#00E400"
    elif aqi <= 100:
        return "Satisfactory", "#FFFF00"
    elif aqi <= 200:
        return "Moderately Polluted", "#FF7E00"
    elif aqi <= 300:
        return "Poor", "#FF0000"
    elif aqi <= 400:
        return "Very Poor", "#8F3F97"
    else:
        return "Severe", "#7E0023"


@router.get("/all", response_model=list[CityDataResponse])
async def get_all_cities(db: Session = Depends(get_db)):
    """Get data for all 20 cities"""

    from app.models.models import EnvironmentalData
    from sqlalchemy import func, and_, select
    import logging

    logger = logging.getLogger(__name__)
    cities_data = []

    try:
        for city, coords in CITY_COORDINATES.items():
            try:
                # Get latest data for this city
                latest = db.query(EnvironmentalData).filter(
                    EnvironmentalData.city == city
                ).order_by(EnvironmentalData.timestamp.desc()).first()

                if latest:
                    status, color = get_aqi_status_and_color(latest.aqi)
                    
                    # Build city data with proper type conversion
                    city_response = {
                        "city": str(city),
                        "latitude": float(coords["lat"]),
                        "longitude": float(coords["lon"]),
                        "current_aqi": int(latest.aqi) if latest.aqi else None,
                        "current_temperature": round(float(latest.temperature), 2) if latest.temperature else None,
                        "current_humidity": round(float(latest.humidity), 2) if latest.humidity else None,
                        "aqi_status": str(status),
                        "aqi_color": str(color),
                        "last_updated": latest.timestamp if latest.timestamp else None
                    }
                    
                    # Validate with schema
                    cities_data.append(CityDataResponse(**city_response))
                else:
                    # Return city without current data
                    city_response = {
                        "city": str(city),
                        "latitude": float(coords["lat"]),
                        "longitude": float(coords["lon"]),
                        "current_aqi": None,
                        "current_temperature": None,
                        "current_humidity": None,
                        "aqi_status": "No Data",
                        "aqi_color": "#808080",
                        "last_updated": None
                    }
                    cities_data.append(CityDataResponse(**city_response))
                    
            except Exception as e:
                logger.error(f"Error processing city {city}: {str(e)}", exc_info=True)
                # Still include city with minimal data
                cities_data.append(CityDataResponse(
                    city=city,
                    latitude=coords["lat"],
                    longitude=coords["lon"],
                    current_aqi=None,
                    current_temperature=None,
                    current_humidity=None,
                    aqi_status="Error",
                    aqi_color="#808080",
                    last_updated=None
                ))

        return cities_data
        
    except Exception as e:
        logger.error(f"Critical error in get_all_cities: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving city data: {str(e)}"
        )


@router.get("/{city}", response_model=CityDataResponse)
async def get_city_data(
    city: str,
    db: Session = Depends(get_db)
):
    """Get data for a specific city"""

    from app.models.models import EnvironmentalData

    # Validate city
    if city not in CITY_COORDINATES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City '{city}' not found in monitoring list"
        )

    coords = CITY_COORDINATES[city]

    # Get latest data
    latest = db.query(EnvironmentalData).filter(
        EnvironmentalData.city == city
    ).order_by(EnvironmentalData.timestamp.desc()).first()

    if latest:
        status, color = get_aqi_status_and_color(latest.aqi)
        return CityDataResponse(
            city=city,
            latitude=coords["lat"],
            longitude=coords["lon"],
            current_aqi=int(latest.aqi) if latest.aqi else None,
            current_temperature=round(latest.temperature, 2) if latest.temperature else None,
            current_humidity=round(latest.humidity, 2) if latest.humidity else None,
            aqi_status=status,
            aqi_color=color,
            last_updated=latest.timestamp
        )
    else:
        return CityDataResponse(
            city=city,
            latitude=coords["lat"],
            longitude=coords["lon"],
            current_aqi=None,
            current_temperature=None,
            current_humidity=None,
            aqi_status="No Data",
            aqi_color="#808080",
            last_updated=None
        )


@router.get("/coordinates/all")
async def get_all_coordinates():
    """Get coordinates for all cities"""
    return CITY_COORDINATES
