#!/usr/bin/env python3
"""
Reset and recreate database tables with correct schema
"""

from sqlalchemy import text
from database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SessionLocal()

try:
    # Drop old tables
    print("Dropping old tables...")
    db.execute(text("DROP TABLE IF EXISTS air_quality_history CASCADE;"))
    db.execute(text("DROP TABLE IF EXISTS environmental_data CASCADE;"))
    db.execute(text("DROP INDEX IF EXISTS idx_air_quality_city;"))
    db.execute(text("DROP INDEX IF EXISTS idx_air_quality_timestamp;"))
    db.execute(text("DROP INDEX IF EXISTS idx_environmental_city;"))
    db.execute(text("DROP INDEX IF EXISTS idx_environmental_timestamp;"))
    db.commit()
    print("✅ Old tables dropped")
    
    # Create correct tables
    print("\nCreating new tables with correct schema...")
    
    sql_statements = [
        """CREATE TABLE environmental_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100) NOT NULL,
            aqi DOUBLE PRECISION,
            co2 DOUBLE PRECISION,
            temperature DOUBLE PRECISION,
            humidity DOUBLE PRECISION,
            wind_speed DOUBLE PRECISION,
            rainfall DOUBLE PRECISION,
            timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
        );""",
        
        "CREATE INDEX idx_environmental_city ON environmental_data(city);",
        "CREATE INDEX idx_environmental_timestamp ON environmental_data(timestamp);",
        
        """CREATE TABLE air_quality_history (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100) NOT NULL,
            aqi DOUBLE PRECISION,
            co2 DOUBLE PRECISION,
            pm25 DOUBLE PRECISION,
            pm10 DOUBLE PRECISION,
            timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
        );""",
        
        "CREATE INDEX idx_air_quality_city ON air_quality_history(city);",
        "CREATE INDEX idx_air_quality_timestamp ON air_quality_history(timestamp);"
    ]
    
    for statement in sql_statements:
        db.execute(text(statement))
    
    db.commit()
    print("✅ New tables created with correct schema")
    
    # Insert sample data
    print("\nInserting sample data...")
    db.execute(text("""
        INSERT INTO environmental_data 
        (city, aqi, co2, temperature, humidity, wind_speed, rainfall) 
        VALUES 
        ('Ahmedabad', 85.5, 410.2, 32.1, 65.0, 12.5, 0.0),
        ('Mumbai', 92.3, 415.1, 31.5, 72.0, 14.2, 0.5),
        ('Surat', 78.9, 408.5, 33.2, 58.0, 11.8, 0.0);
    """))
    db.commit()
    print("✅ Sample data inserted (3 records)")
    
    # Verify
    print("\nVerifying data...")
    result = db.execute(text("SELECT COUNT(*) as count FROM environmental_data;"))
    row = result.fetchone()
    print(f"✅ Total records in database: {row[0]}")
    
    print("\n" + "="*60)
    print("✅ DATABASE RESET - READY TO USE")
    print("="*60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
