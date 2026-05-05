import logging
from database import SessionLocal, EnvironmentalData, AirQualityHistory
from datetime import datetime, timedelta
from sqlalchemy import desc
import pandas as pd

logger = logging.getLogger(__name__)

def save_environmental_data(city, aqi, co2, temperature, humidity, wind_speed, rainfall):
    """Save data to database"""
    try:
        db = SessionLocal()
        data = EnvironmentalData(
            city=city,
            aqi=aqi,
            co2=co2,
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            rainfall=rainfall,
            timestamp=datetime.utcnow()
        )
        db.add(data)
        db.commit()
        logger.info(f"✅ Saved environmental data for {city}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to save data: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def save_air_quality_data(city, aqi, co2, pm25=None, pm10=None):
    """Save air quality data to history"""
    try:
        db = SessionLocal()
        data = AirQualityHistory(
            city=city,
            aqi=aqi,
            co2=co2,
            pm25=pm25,
            pm10=pm10,
            timestamp=datetime.utcnow()
        )
        db.add(data)
        db.commit()
        logger.info(f"✅ Saved air quality history for {city}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to save air quality data: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def get_historical_data(city, days=7):
    """Retrieve historical data for a city"""
    try:
        db = SessionLocal()
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        data = db.query(EnvironmentalData).filter(
            EnvironmentalData.city == city,
            EnvironmentalData.timestamp >= cutoff_date
        ).order_by(desc(EnvironmentalData.timestamp)).all()
        
        logger.info(f"✅ Retrieved {len(data)} records for {city}")
        return data
    except Exception as e:
        logger.error(f"❌ Failed to retrieve historical data: {e}")
        return []
    finally:
        db.close()

def get_historical_data_dataframe(city, days=7):
    """Retrieve historical data as pandas DataFrame"""
    try:
        db = SessionLocal()
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        data = db.query(EnvironmentalData).filter(
            EnvironmentalData.city == city,
            EnvironmentalData.timestamp >= cutoff_date
        ).order_by(EnvironmentalData.timestamp).all()
        
        # Convert to DataFrame
        if data:
            df = pd.DataFrame([{
                'timestamp': d.timestamp,
                'aqi': d.aqi,
                'co2': d.co2,
                'temperature': d.temperature,
                'humidity': d.humidity,
                'wind_speed': d.wind_speed,
                'rainfall': d.rainfall
            } for d in data])
            logger.info(f"✅ Retrieved {len(df)} records for {city} as DataFrame")
            return df
        else:
            logger.warning(f"⚠️ No data found for {city}")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"❌ Failed to retrieve historical data: {e}")
        return pd.DataFrame()
    finally:
        db.close()

def get_latest_data(city):
    """Get most recent data for a city"""
    try:
        db = SessionLocal()
        data = db.query(EnvironmentalData).filter(
            EnvironmentalData.city == city
        ).order_by(desc(EnvironmentalData.timestamp)).first()
        
        if data:
            logger.info(f"✅ Retrieved latest data for {city}")
        else:
            logger.warning(f"⚠️ No data found for {city}")
        return data
    except Exception as e:
        logger.error(f"❌ Failed to retrieve latest data: {e}")
        return None
    finally:
        db.close()

def get_all_latest_cities():
    """Get latest data for all cities"""
    try:
        db = SessionLocal()
        
        # Get latest record for each city
        subquery = db.query(
            EnvironmentalData.city,
            desc(EnvironmentalData.timestamp)
        ).distinct(EnvironmentalData.city).subquery()
        
        data = db.query(EnvironmentalData).from_statement(
            db.query(EnvironmentalData).filter(
                EnvironmentalData.id.in_(
                    db.query(EnvironmentalData.id)
                    .filter(EnvironmentalData.city == subquery.c.city)
                    .order_by(desc(EnvironmentalData.timestamp))
                    .limit(1)
                    .correlate(None)
                    .subquery()
                )
            ).statement
        ).order_by(desc(EnvironmentalData.aqi)).all()
        
        logger.info(f"✅ Retrieved latest data for {len(data)} cities")
        return data
    except Exception as e:
        logger.error(f"❌ Failed to retrieve all latest data: {e}")
        # Fallback: just get all latest without grouping
        try:
            db = SessionLocal()
            data = db.query(EnvironmentalData).order_by(
                EnvironmentalData.city,
                desc(EnvironmentalData.timestamp)
            ).all()
            return data
        except:
            return []
    finally:
        db.close()

def get_city_statistics(city, days=7):
    """Get statistics for a city"""
    try:
        df = get_historical_data_dataframe(city, days)
        
        if df.empty:
            return None
        
        stats = {
            'city': city,
            'avg_aqi': df['aqi'].mean(),
            'max_aqi': df['aqi'].max(),
            'min_aqi': df['aqi'].min(),
            'avg_temperature': df['temperature'].mean(),
            'avg_humidity': df['humidity'].mean(),
            'avg_wind_speed': df['wind_speed'].mean(),
            'total_rainfall': df['rainfall'].sum(),
            'record_count': len(df),
            'date_range': f"{df['timestamp'].min()} to {df['timestamp'].max()}"
        }
        
        logger.info(f"✅ Calculated statistics for {city}")
        return stats
    except Exception as e:
        logger.error(f"❌ Failed to calculate statistics: {e}")
        return None

def delete_old_data(days=30):
    """Delete data older than specified days"""
    try:
        db = SessionLocal()
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        deleted = db.query(EnvironmentalData).filter(
            EnvironmentalData.timestamp < cutoff_date
        ).delete()
        
        db.commit()
        logger.info(f"✅ Deleted {deleted} old records from database")
        return deleted
    except Exception as e:
        logger.error(f"❌ Failed to delete old data: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

def test_database():
    """Test database connection and operations"""
    logger.info("\n=== Testing Database Connection ===\n")
    
    try:
        # Test 1: Connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        logger.info("✅ Database connection successful")
        
        # Test 2: Query
        latest = get_latest_data("Ahmedabad")
        if latest:
            logger.info(f"✅ Database query successful - Found {latest.city} data")
        else:
            logger.info("ℹ️ No data in database yet (this is OK for first run)")
        
        # Test 3: Statistics
        stats = get_city_statistics("Ahmedabad")
        if stats:
            logger.info(f"✅ Statistics working - Avg AQI: {stats['avg_aqi']:.1f}")
        else:
            logger.info("ℹ️ No historical data yet for statistics")
        
        logger.info("\n=== Database Tests Complete ===\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    test_database()
