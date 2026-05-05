#!/usr/bin/env python
"""Add sample environmental data to database"""

from app.db.database import SessionLocal
from app.models.models import EnvironmentalData
from datetime import datetime
from sqlalchemy import text

db = SessionLocal()

try:
    # Check if data exists
    result = db.execute(text("SELECT COUNT(*) FROM environmental_data")).scalar()
    print(f"Current records: {result}")
    
    # Add sample data for multiple cities
    cities_data = [
        {"city": "Ahmedabad", "aqi": 85, "temperature": 32.5, "humidity": 45},
        {"city": "Mumbai", "aqi": 120, "temperature": 28.3, "humidity": 72},
        {"city": "Bangalore", "aqi": 65, "temperature": 24.2, "humidity": 68},
        {"city": "Delhi", "aqi": 150, "temperature": 29.1, "humidity": 52},
        {"city": "Hyderabad", "aqi": 78, "temperature": 31.4, "humidity": 55},
        {"city": "Chennai", "aqi": 95, "temperature": 30.2, "humidity": 80},
        {"city": "Pune", "aqi": 72, "temperature": 26.8, "humidity": 60},
        {"city": "Kolkata", "aqi": 135, "temperature": 27.5, "humidity": 75},
        {"city": "Jaipur", "aqi": 110, "temperature": 33.2, "humidity": 48},
        {"city": "Lucknow", "aqi": 125, "temperature": 30.1, "humidity": 58},
    ]
    
    print(f"\nAdding {len(cities_data)} cities...")
    
    for city_info in cities_data:
        data = EnvironmentalData(
            city=city_info["city"],
            aqi=city_info["aqi"],
            temperature=city_info["temperature"],
            humidity=city_info["humidity"],
            wind_speed=5.2,
            co2=425.3,
            rainfall=0,
            timestamp=datetime.now()
        )
        db.add(data)
        print(f"  ✅ Added {city_info['city']} (AQI: {city_info['aqi']})")
    
    db.commit()
    print("\n✅ Sample data added successfully!")
    
    # Verify
    final_count = db.execute(text("SELECT COUNT(*) FROM environmental_data")).scalar()
    print(f"Total records now: {final_count}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
