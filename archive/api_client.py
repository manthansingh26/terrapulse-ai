import os
import requests
import logging
from dotenv import load_dotenv
from datetime import datetime
import redis
import json
from functools import wraps
import time

load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Redis connection
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=int(os.getenv('REDIS_DB', 0)),
        decode_responses=True
    )
    # Test connection
    redis_client.ping()
    logger.info("✅ Redis connection established")
    REDIS_AVAILABLE = True
except Exception as e:
    logger.warning(f"⚠️ Redis not available: {e}. Running without caching.")
    REDIS_AVAILABLE = False
    redis_client = None

def cache_result(ttl=3600):
    """Decorator to cache API results in Redis"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not REDIS_AVAILABLE:
                # If Redis not available, just call function
                return func(*args, **kwargs)
            
            # Create cache key
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            try:
                # Try to get from cache
                cached = redis_client.get(cache_key)
                if cached:
                    logger.info(f"🔵 Cache HIT for {func.__name__} with {args}")
                    return json.loads(cached)
            except Exception as e:
                logger.warning(f"Cache retrieval failed: {e}")
            
            # If not in cache, call function
            try:
                result = func(*args, **kwargs)
                if result:
                    # Store in cache
                    redis_client.setex(cache_key, ttl, json.dumps(result, default=str))
                    logger.info(f"🟢 Cache SET for {func.__name__}")
                return result
            except Exception as e:
                logger.error(f"Function {func.__name__} failed: {e}")
                raise
        
        return wrapper
    return decorator

@cache_result(ttl=3600)
def fetch_real_aqi_data(city):
    """Fetch real AQI data from WAQI API"""
    try:
        token = os.getenv('WAQI_API_TOKEN', 'demo')
        url = f"https://api.waqi.info/feed/{city}/?token={token}"
        
        logger.info(f"Fetching AQI data from WAQI for {city}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == 'ok':
            aqi_data = data.get('data', {})
            logger.info(f"✅ Successfully fetched AQI data for {city}")
            
            return {
                'city': city,
                'aqi': aqi_data.get('aqi', None),
                'pm25': aqi_data.get('iaqi', {}).get('pm25', {}).get('v'),
                'pm10': aqi_data.get('iaqi', {}).get('pm10', {}).get('v'),
                'o3': aqi_data.get('iaqi', {}).get('o3', {}).get('v'),
                'no2': aqi_data.get('iaqi', {}).get('no2', {}).get('v'),
                'so2': aqi_data.get('iaqi', {}).get('so2', {}).get('v'),
                'timestamp': datetime.utcnow().isoformat()
            }
        else:
            logger.warning(f"⚠️ WAQI returned status: {data.get('status')}")
            return None
            
    except requests.exceptions.Timeout:
        logger.error(f"❌ AQI API request TIMEOUT for {city}")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"❌ Cannot connect to WAQI API")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ API request failed for {city}: {e}")
        return None

@cache_result(ttl=1800)
def fetch_real_weather_data(city_name, city_coords):
    """Fetch real weather data from OpenWeatherMap"""
    try:
        api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        
        if api_key == 'your_openweathermap_api_key_here':
            logger.warning(f"⚠️ OpenWeatherMap API key not set. Using mock data.")
            return None
        
        url = f"https://api.openweathermap.org/data/2.5/weather"
        
        params = {
            'lat': city_coords['lat'],
            'lon': city_coords['lon'],
            'appid': api_key,
            'units': 'metric'
        }
        
        logger.info(f"Fetching weather data from OpenWeatherMap for {city_name}...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"✅ Successfully fetched weather data for {city_name}")
        
        return {
            'city': city_name,
            'temperature': data['main'].get('temp'),
            'humidity': data['main'].get('humidity'),
            'wind_speed': data['wind'].get('speed'),
            'pressure': data['main'].get('pressure'),
            'clouds': data['clouds'].get('all'),
            'visibility': data.get('visibility'),
            'description': data['weather'][0].get('description'),
            'timestamp': datetime.utcnow().isoformat()
        }
        
    except requests.exceptions.Timeout:
        logger.error(f"❌ Weather API request TIMEOUT for {city_name}")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"❌ Cannot connect to OpenWeatherMap API")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Weather API request failed for {city_name}: {e}")
        return None

def get_combined_data(city_name, city_coords):
    """Combine AQI and weather data"""
    try:
        aqi_data = fetch_real_aqi_data(city_name)
        weather_data = fetch_real_weather_data(city_name, city_coords)
        
        combined = {
            'city': city_name,
            'aqi': aqi_data.get('aqi') if aqi_data else None,
            'pm25': aqi_data.get('pm25') if aqi_data else None,
            'temperature': weather_data.get('temperature') if weather_data else None,
            'humidity': weather_data.get('humidity') if weather_data else None,
            'wind_speed': weather_data.get('wind_speed') if weather_data else None,
            'description': weather_data.get('description') if weather_data else None,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"✅ Combined data fetched for {city_name}")
        return combined
        
    except Exception as e:
        logger.error(f"❌ Error getting combined data for {city_name}: {e}")
        return None

def clear_cache():
    """Clear all Redis cache"""
    if not REDIS_AVAILABLE:
        logger.warning("⚠️ Redis not available, cannot clear cache")
        return False
    
    try:
        redis_client.flushdb()
        logger.info("✅ Cache cleared successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to clear cache: {e}")
        return False

def test_apis():
    """Test API connections"""
    logger.info("\n=== Testing API Connections ===\n")
    
    # Test WAQI
    logger.info("Testing WAQI API...")
    aqi_result = fetch_real_aqi_data("Ahmedabad")
    if aqi_result:
        logger.info(f"✅ WAQI API working - AQI: {aqi_result.get('aqi')}")
    else:
        logger.warning("⚠️ WAQI API returned no data")
    
    # Test OpenWeatherMap
    logger.info("Testing OpenWeatherMap API...")
    weather_result = fetch_real_weather_data("Ahmedabad", {"lat": 23.0225, "lon": 72.5714})
    if weather_result:
        logger.info(f"✅ OpenWeatherMap API working - Temp: {weather_result.get('temperature')}°C")
    else:
        logger.warning("⚠️ OpenWeatherMap API not configured or returning no data")
    
    logger.info("\n=== API Test Complete ===\n")

if __name__ == "__main__":
    test_apis()
