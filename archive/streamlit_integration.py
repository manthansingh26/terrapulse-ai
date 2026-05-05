#!/usr/bin/env python3
"""
Streamlit Integration Module
Connects Streamlit app to real database and APIs
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from api_client import get_combined_data, fetch_real_aqi_data
from db_helper import (
    save_environmental_data, 
    get_latest_data, 
    get_historical_data_dataframe,
    get_city_statistics,
    get_all_latest_cities
)

logger = logging.getLogger(__name__)

# City coordinates
CITY_COORDINATES = {
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Surat": {"lat": 21.1702, "lon": 72.8311},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Delhi": {"lat": 28.7041, "lon": 77.1025},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Pune": {"lat": 18.5204, "lon": 73.8567},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462},
    "Kanpur": {"lat": 26.4499, "lon": 80.3319},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882},
    "Indore": {"lat": 22.7196, "lon": 75.8577},
    "Thane": {"lat": 19.2183, "lon": 72.9781},
    "Bhopal": {"lat": 23.1815, "lon": 77.4104},
    "Visakhapatnam": {"lat": 17.6869, "lon": 83.2185},
    "Patna": {"lat": 25.5941, "lon": 85.1376},
    "Vadodara": {"lat": 22.3072, "lon": 73.1812},
    "Ghaziabad": {"lat": 28.6692, "lon": 77.4538}
}

def get_city_data(city, use_real_api=False):
    """
    Get city data from database or mock data
    
    Args:
        city: City name
        use_real_api: If True, try to fetch from API first
    
    Returns:
        dict with city data
    """
    try:
        # Try to get latest from database first
        db_data = get_latest_data(city)
        
        if db_data and db_data.aqi:
            return {
                'city': city,
                'aqi': db_data.aqi,
                'co2': db_data.co2,
                'temperature': db_data.temperature,
                'humidity': db_data.humidity,
                'wind_speed': db_data.wind_speed,
                'rainfall': db_data.rainfall,
                'source': 'Database (Latest)',
                'timestamp': db_data.timestamp
            }
    except Exception as e:
        logger.warning(f"Could not get database data for {city}: {e}")
    
    # Try real API if requested
    if use_real_api:
        try:
            city_coords = CITY_COORDINATES.get(city)
            if city_coords:
                api_data = get_combined_data(city, city_coords)
                if api_data:
                    # Save to database
                    save_environmental_data(
                        city=city,
                        aqi=api_data.get('aqi', 0),
                        co2=api_data.get('co2', 0),
                        temperature=api_data.get('temperature', 0),
                        humidity=api_data.get('humidity', 0),
                        wind_speed=api_data.get('wind_speed', 0),
                        rainfall=0
                    )
                    
                    return {
                        'city': city,
                        'aqi': api_data.get('aqi'),
                        'temperature': api_data.get('temperature'),
                        'humidity': api_data.get('humidity'),
                        'wind_speed': api_data.get('wind_speed'),
                        'co2': api_data.get('co2', 0),
                        'rainfall': 0,
                        'source': 'Real API',
                        'timestamp': datetime.utcnow()
                    }
        except Exception as e:
            logger.warning(f"Could not fetch API data for {city}: {e}")
    
    # Fallback to mock data
    return generate_mock_data(city)

def generate_mock_data(city, base_aqi=None):
    """Generate mock data for a city (fallback)"""
    if base_aqi is None:
        base_aqi = np.random.uniform(50, 150)
    
    return {
        'city': city,
        'aqi': base_aqi + np.random.uniform(-10, 10),
        'co2': np.random.uniform(380, 450),
        'temperature': np.random.uniform(20, 38),
        'humidity': np.random.uniform(40, 85),
        'wind_speed': np.random.uniform(5, 20),
        'rainfall': np.random.uniform(0, 2),
        'source': 'Mock Data (Demo)',
        'timestamp': datetime.utcnow()
    }

def get_historical_data_with_fallback(city, days=7):
    """Get historical data from database or generate mock"""
    try:
        df = get_historical_data_dataframe(city, days)
        if not df.empty:
            return df, 'Database'
    except Exception as e:
        logger.warning(f"Could not get historical data from DB: {e}")
    
    # Generate mock historical data
    dates = [datetime.utcnow() - timedelta(days=i) for i in range(days, 0, -1)]
    base_aqi = np.random.uniform(60, 140)
    
    mock_df = pd.DataFrame({
        'timestamp': dates,
        'aqi': np.random.normal(base_aqi, 15, days).clip(10, 300),
        'co2': np.random.normal(410, 20, days).clip(350, 500),
        'temperature': np.random.normal(30, 5, days).clip(15, 45),
        'humidity': np.random.normal(65, 15, days).clip(20, 95),
        'wind_speed': np.random.normal(12, 4, days).clip(2, 30),
        'rainfall': np.random.uniform(0, 3, days)
    })
    
    return mock_df, 'Mock (Demo)'

def get_all_cities_data(use_real_api=False):
    """Get data for all cities"""
    all_data = {}
    
    for city in CITY_COORDINATES.keys():
        try:
            all_data[city] = get_city_data(city, use_real_api)
        except Exception as e:
            logger.warning(f"Error getting data for {city}: {e}")
            all_data[city] = generate_mock_data(city)
    
    return all_data

def get_city_statistics_with_fallback(city, days=7):
    """Get statistics for a city or return mock"""
    try:
        stats = get_city_statistics(city, days)
        if stats:
            return stats, 'Calculated from Database'
    except Exception as e:
        logger.warning(f"Could not calculate statistics: {e}")
    
    # Generate mock statistics
    return {
        'city': city,
        'avg_aqi': np.random.uniform(70, 120),
        'max_aqi': np.random.uniform(100, 200),
        'min_aqi': np.random.uniform(40, 80),
        'avg_temperature': np.random.uniform(25, 35),
        'avg_humidity': np.random.uniform(55, 75),
        'avg_wind_speed': np.random.uniform(8, 18),
        'total_rainfall': np.random.uniform(0, 20),
        'record_count': days,
        'date_range': f"Last {days} days"
    }, 'Mock (Demo)'

@st.cache_data(ttl=3600)
def load_city_coordinates():
    """Load city coordinates (cached)"""
    return CITY_COORDINATES

def display_data_source_badge(source):
    """Display badge showing data source"""
    if 'Real API' in source:
        st.badge("🌐 Real API Data")
    elif 'Database' in source:
        st.badge("💾 Database Historical")
    else:
        st.warning("📊 Demo/Mock Data")

if __name__ == "__main__":
    # Test the module
    test_city = "Ahmedabad"
    print(f"\nTesting data retrieval for {test_city}...")
    
    data = get_city_data(test_city)
    print(f"✅ Got city data: {data}")
    
    hist, source = get_historical_data_with_fallback(test_city)
    print(f"✅ Got historical data ({source}): {len(hist)} records")
    
    stats, source = get_city_statistics_with_fallback(test_city)
    print(f"✅ Got statistics ({source}): Avg AQI {stats.get('avg_aqi', 'N/A')}")
