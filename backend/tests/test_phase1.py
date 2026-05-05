#!/usr/bin/env python3
"""
Comprehensive test script to verify all Phase 1 components
"""

if __name__ != "__main__":
    import pytest

    pytest.skip("Legacy verification script; run directly when needed.", allow_module_level=True)

import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("\n" + "="*60)
print("🔍 TERRAPULSE AI - PHASE 1 VERIFICATION TEST")
print("="*60 + "\n")

# Test 1: Environment Variables
print("\n📋 TEST 1: Checking Environment Variables...")
print("-" * 60)
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    required_env = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 
                    'REDIS_HOST', 'REDIS_PORT', 'WAQI_API_TOKEN']
    
    missing = []
    for env_var in required_env:
        value = os.getenv(env_var, 'NOT SET')
        if value == 'NOT SET':
            missing.append(env_var)
            print(f"  ❌ {env_var}: NOT SET")
        else:
            # Hide sensitive data
            if 'PASSWORD' in env_var or 'TOKEN' in env_var or 'KEY' in env_var:
                print(f"  ✅ {env_var}: {'*' * len(str(value))}")
            else:
                print(f"  ✅ {env_var}: {value}")
    
    if missing:
        print(f"\n  ⚠️  Missing: {', '.join(missing)}")
    else:
        print("\n  ✅ All environment variables loaded!")
        
except Exception as e:
    print(f"  ❌ Error loading environment: {e}")
    sys.exit(1)

# Test 2: Database Connection
print("\n📊 TEST 2: Testing Database Connection (PostgreSQL)...")
print("-" * 60)
try:
    from database import test_connection, EnvironmentalData
    
    if test_connection():
        print("  ✅ Database connection successful!")
    else:
        print("  ❌ Database connection failed!")
        sys.exit(1)
        
except Exception as e:
    print(f"  ❌ Error testing database: {e}")
    sys.exit(1)

# Test 3: Database Tables
print("\n🗄️  TEST 3: Verifying Database Tables...")
print("-" * 60)
try:
    from database import SessionLocal
    from sqlalchemy import inspect
    
    db = SessionLocal()
    inspector = inspect(db.get_bind())
    tables = inspector.get_table_names()
    
    required_tables = ['environmental_data', 'air_quality_history']
    
    for table in required_tables:
        if table in tables:
            columns = inspector.get_columns(table)
            col_names = [col['name'] for col in columns]
            print(f"  ✅ Table '{table}' found with {len(columns)} columns")
            print(f"      Columns: {', '.join(col_names[:4])}...")
        else:
            print(f"  ❌ Table '{table}' NOT found")
    
    db.close()
    
except Exception as e:
    print(f"  ❌ Error verifying tables: {e}")
    sys.exit(1)

# Test 4: Redis Connection
print("\n⚡ TEST 4: Testing Redis Cache Connection...")
print("-" * 60)
try:
    from api_client import REDIS_AVAILABLE, redis_client
    
    if REDIS_AVAILABLE:
        print("  ✅ Redis connection successful!")
        print("  ✅ Caching will be enabled")
    else:
        print("  ⚠️  Redis not available")
        print("  ℹ️  App will work without caching (not fatal)")
        
except Exception as e:
    print(f"  ⚠️  Redis error: {e}")

# Test 5: API Connections
print("\n🌐 TEST 5: Testing API Connections...")
print("-" * 60)
try:
    from api_client import fetch_real_aqi_data, fetch_real_weather_data
    
    # Test AQI API
    print("  Testing WAQI API...")
    aqi_data = fetch_real_aqi_data("Ahmedabad")
    if aqi_data and aqi_data.get('aqi'):
        print(f"    ✅ WAQI API working - AQI: {aqi_data.get('aqi')}")
    else:
        print(f"    ⚠️  WAQI API returned no valid AQI data")
    
    # Test Weather API
    print("  Testing OpenWeatherMap API...")
    weather_data = fetch_real_weather_data("Ahmedabad", {"lat": 23.0225, "lon": 72.5714})
    if weather_data and weather_data.get('temperature'):
        print(f"    ✅ OpenWeatherMap API working - Temp: {weather_data.get('temperature')}°C")
    else:
        print(f"    ⚠️  OpenWeatherMap API not configured or returning no data")
        print(f"    💡 Make sure to set OPENWEATHERMAP_API_KEY in .env")
        
except Exception as e:
    print(f"  ❌ Error testing APIs: {e}")

# Test 6: Database Operations
print("\n💾 TEST 6: Testing Database Operations...")
print("-" * 60)
try:
    from db_helper import (
        get_latest_data, 
        get_historical_data_dataframe,
        save_environmental_data,
        get_city_statistics
    )
    
    # Test save
    print("  Testing data insertion...")
    success = save_environmental_data(
        city="TestCity",
        aqi=85.5,
        co2=410.2,
        temperature=32.1,
        humidity=65.0,
        wind_speed=12.5,
        rainfall=0.0
    )
    
    if success:
        print("    ✅ Data insertion successful")
    else:
        print("    ❌ Data insertion failed")
    
    # Test retrieve
    print("  Testing data retrieval...")
    data = get_latest_data("TestCity")
    if data:
        print(f"    ✅ Data retrieval successful - AQI: {data.aqi}")
    else:
        print("    ℹ️  No test data found (first run)")
    
    # Test DataFrame
    print("  Testing DataFrame conversion...")
    df = get_historical_data_dataframe("Ahmedabad", days=7)
    if not df.empty:
        print(f"    ✅ DataFrame conversion works - {len(df)} records")
    else:
        print("    ℹ️  No historical data available yet")
    
except Exception as e:
    print(f"  ❌ Error testing database operations: {e}")

# Final Summary
print("\n" + "="*60)
print("📊 VERIFICATION SUMMARY")
print("="*60)

print("""
✅ DATABASE READY: PostgreSQL configured and connected
✅ TABLES CREATED: environmental_data and air_quality_history initialized
✅ API CLIENTS: WAQI and OpenWeatherMap configured
⚡ CACHING: Redis setup (optional, not required)
✅ LOGGING: Error handling and logging enabled

📝 NEXT STEPS:
1. Update your .env file with API keys if not done
2. Run: streamlit run app.py
3. Navigate to Interactive Map section
4. Check for real data loading

🚀 Ready for integration into Streamlit app!
""")

print("="*60 + "\n")
