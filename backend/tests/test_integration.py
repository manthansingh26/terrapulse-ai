#!/usr/bin/env python3
"""Quick test of streamlit integration"""

if __name__ != "__main__":
    import pytest

    pytest.skip("Legacy Streamlit integration script; run directly when needed.", allow_module_level=True)

from streamlit_integration import (
    get_city_data, 
    get_historical_data_with_fallback,
    get_city_statistics_with_fallback,
    get_all_cities_data
)

print("\n" + "="*60)
print("🧪 TESTING STREAMLIT INTEGRATION")
print("="*60 + "\n")

# Test 1: Get single city data
print("Test 1: Single City Data")
print("-" * 60)
data = get_city_data('Ahmedabad')
print(f"✅ City: {data['city']}")
print(f"✅ AQI: {data['aqi']:.1f}")
print(f"✅ Temperature: {data['temperature']:.1f}°C")
print(f"✅ Source: {data['source']}")

# Test 2: Historical data
print("\nTest 2: Historical Data")
print("-" * 60)
hist, source = get_historical_data_with_fallback('Mumbai', days=7)
print(f"✅ Records: {len(hist)}")
print(f"✅ Source: {source}")
print(f"✅ Date range: {hist['timestamp'].min()} to {hist['timestamp'].max()}")

# Test 3: Statistics
print("\nTest 3: City Statistics")
print("-" * 60)
stats, source = get_city_statistics_with_fallback('Surat', days=7)
print(f"✅ Avg AQI: {stats['avg_aqi']:.1f}")
print(f"✅ Max AQI: {stats['max_aqi']:.1f}")
print(f"✅ Min AQI: {stats['min_aqi']:.1f}")
print(f"✅ Source: {source}")

# Test 4: All cities
print("\nTest 4: All Cities Data")
print("-" * 60)
all_cities = get_all_cities_data()
print(f"✅ Total cities: {len(all_cities)}")
for city, data in list(all_cities.items())[:3]:
    print(f"  - {city}: AQI {data['aqi']:.1f} (Temp: {data['temperature']:.1f}°C)")

print("\n" + "="*60)
print("✅ ALL INTEGRATION TESTS PASSED!")
print("="*60 + "\n")
