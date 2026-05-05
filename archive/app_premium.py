#!/usr/bin/env python3
"""
TerraPulse AI - Earth Intelligence Dashboard PREMIUM
Real Database Integration • Real-Time Data • Production Ready
"""

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import folium
from streamlit_folium import folium_static
from datetime import datetime
import logging

# Import integration modules
try:
    from streamlit_integration import (
        get_city_data,
        get_historical_data_with_fallback,
        get_city_statistics_with_fallback,
        get_all_cities_data,
        CITY_COORDINATES
    )
    INTEGRATION_READY = True
except ImportError as e:
    st.error(f"Integration module error: {e}")
    INTEGRATION_READY = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="TerraPulse AI Premium",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS ============
st.markdown("""
    <style>
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(15,118,110,0.1), rgba(6,182,212,0.05));
        border: 1px solid rgba(6,182,212,0.2);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    }
    [data-testid="metric-container"]:hover {
        box-shadow: 0 8px 12px rgba(6,182,212,0.15);
    }
    h1 {
        background: linear-gradient(135deg, #0F766E 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    </style>
""", unsafe_allow_html=True)

# ============ HELPER FUNCTIONS ============

def get_aqi_color(aqi):
    """Return emoji, status, and color based on AQI"""
    if aqi < 50:
        return "🟢", "Good", "#10B981"
    elif aqi < 100:
        return "🟡", "Moderate", "#F59E0B"
    elif aqi < 150:
        return "🟠", "Unhealthy for Sensitive", "#EF6C42"
    elif aqi < 200:
        return "🔴", "Unhealthy", "#EF4444"
    elif aqi < 300:
        return "🟣", "Very Unhealthy", "#8B5CF6"
    else:
        return "🟤", "Hazardous", "#7C2D12"

# ============ MAIN APP ============

st.title("🌍 TerraPulse AI")
st.subheader("Earth Intelligence Dashboard - Premium Edition")
st.write("🔴 Real-time environmental monitoring • 📊 Historical data persistence • 🤖 AI-powered predictions")

if not INTEGRATION_READY:
    st.error("⚠️ Integration module not available. Please check modules.")
    st.stop()

st.divider()

# ============ SIDEBAR ============
st.sidebar.title("📍 Navigation")
selected_section = st.sidebar.radio(
    "Select Section:",
    ["📊 Dashboard", "🗺️ Interactive Map", "📈 Analytics", "📂 CSV Analysis", "🖼️ Image Analysis", "🤖 ML Models"]
)

st.sidebar.divider()
st.sidebar.title("⚙️ Controls")
location = st.sidebar.selectbox("Select Location", list(CITY_COORDINATES.keys()), index=0)
days_range = st.sidebar.slider("Historical Range (days)", 5, 30, 7)
use_real_api = st.sidebar.checkbox("Use Real API (when available)", False)

# ============ DASHBOARD ============
if selected_section == "📊 Dashboard":
    st.header("📊 Environmental Dashboard")
    
    with st.spinner("Loading real-time data..."):
        try:
            city_data = get_city_data(location, use_real_api)
            
            emoji, status, color = get_aqi_color(city_data['aqi'])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📍 Location", location)
            col2.metric(f"{emoji} AQI", f"{city_data['aqi']:.1f}", delta=status)
            col3.metric("🌡 Temperature", f"{city_data['temperature']:.1f}°C")
            col4.metric("💨 Wind Speed", f"{city_data['wind_speed']:.1f} km/h")
            
            st.info(f"📡 Data Source: **{city_data['source']}** | Updated: {city_data['timestamp'].strftime('%H:%M:%S')}")
            
            # Historical data
            st.subheader("📈 Historical Trends")
            hist_data, hist_source = get_historical_data_with_fallback(location, days_range)
            
            if not hist_data.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.line_chart(hist_data[['aqi', 'co2']])
                    st.caption("AQI & CO₂ Levels")
                with col2:
                    st.line_chart(hist_data[['temperature', 'humidity']])
                    st.caption("Temperature & Humidity")
            
            # Statistics
            st.subheader("📊 Statistics")
            stats, stats_source = get_city_statistics_with_fallback(location, days_range)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Avg AQI", f"{stats['avg_aqi']:.1f}")
            col2.metric("Max AQI", f"{stats['max_aqi']:.1f}")
            col3.metric("Min AQI", f"{stats['min_aqi']:.1f}")
            col4.metric("Avg Temp", f"{stats['avg_temperature']:.1f}°C")
            
        except Exception as e:
            st.error(f"Error loading dashboard: {e}")
            logger.error(f "Dashboard error: {e}")

# ============ INTERACTIVE MAP ============
elif selected_section == "🗺️ Interactive Map":
    st.header("🗺️ Real-Time City Monitoring")
    st.write("20 Indian cities with live environmental data")
    
    try:
        all_cities = get_all_cities_data()
        
        m = folium.Map(
            location=[22.0, 73.0],
            zoom_start=5,
            tiles='CartoDB positron'
        )
        
        for city_name, coords in CITY_COORDINATES.items():
            city_info = all_cities.get(city_name)
            if city_info:
                aqi = city_info['aqi']
                emoji, status, color_hex = get_aqi_color(aqi)
                
                popup_html = f"<b>{city_name}</b><br>AQI: {aqi:.1f}<br>Temp: {city_info['temperature']:.1f}°C"
                
                folium.CircleMarker(
                    location=[coords['lat'], coords['lon']],
                    radius=min(aqi / 30, 25),
                    popup=folium.Popup(popup_html, max_width=300),
                    color=color_hex,
                    fill=True,
                    fillColor=color_hex,
                    fillOpacity=0.7,
                    weight=2
                ).add_to(m)
        
        folium_static(m, width=1400, height=700)
        
        st.divider()
        st.subheader("📋 All Cities - Live Data")
        
        cities_list = []
        for city, data in all_cities.items():
            cities_list.append({
                'City': city,
                'AQI': f"{data['aqi']:.1f}",
                'Status': get_aqi_color(data['aqi'])[1],
                'Temp (°C)': f"{data['temperature']:.1f}",
                'Humidity (%)': f"{data['humidity']:.1f}",
                'Source': data['source']
            })
        
        cities_df = pd.DataFrame(cities_list).sort_values('AQI', ascending=False, key=pd.to_numeric)
        st.dataframe(cities_df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Map error: {e}")
        logger.error(f"Map error: {e}")

# ============ ANALYTICS ============
elif selected_section == "📈 Analytics":
    st.header("📈 Environmental Analytics")
    
    top_cities = st.multiselect(
        "Select cities to compare:",
        list(CITY_COORDINATES.keys()),
        default=["Ahmedabad", "Mumbai", "Surat"]
    )
    
    if top_cities:
        comparison_data = []
        for city in top_cities:
            city_data = get_city_data(city, use_real_api)
            comparison_data.append({
                'City': city,
                'AQI': city_data['aqi'],
                'Temperature': city_data['temperature'],
                'Humidity': city_data['humidity']
            })
        
        comp_df = pd.DataFrame(comparison_data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(comp_df.set_index('City')['AQI'])
            st.caption("AQI Comparison")
        with col2:
            st.bar_chart(comp_df.set_index('City')['Temperature'])
            st.caption("Temperature Comparison")

# ============ CSV ANALYSIS ============
elif selected_section == "📂 CSV Analysis":
    st.header("📂 CSV Data Analysis")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✓ CSV uploaded")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Size", f"{uploaded_file.size / 1024:.1f} KB")
        
        st.dataframe(df.head(10), use_container_width=True)

# ============ IMAGE ANALYSIS ============
elif selected_section == "🖼️ Image Analysis":
    st.header("🖼️ Image Analysis")
    
    uploaded_image = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.success("✓ Image uploaded")
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, use_column_width=True)
        with col2:
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Width", f"{image.size[0]}px")
            col_b.metric("Height", f"{image.size[1]}px")
            col_c.metric("Format", image.format or "Unknown")

# ============ ML MODELS ============
elif selected_section == "🤖 ML Models":
    st.header("🤖 Machine Learning Models")
    
    model_type = st.selectbox(
        "Select Model:",
        ["Temperature Forecasting", "Anomaly Detection", "AQI Classification"]
    )
    
    hist_data, _ = get_historical_data_with_fallback(location, days_range)
    
    if model_type == "Temperature Forecasting" and not hist_data.empty:
        st.subheader("🌡️ Temperature Forecasting (Linear Regression)")
        
        X = np.arange(len(hist_data)).reshape(-1, 1)
        y = hist_data['temperature'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        col1, col2 = st.columns(2)
        with col1:
            st.line_chart(pd.DataFrame({'Temp': y}))
        with col2:
            st.metric("Model R² Score", f"{model.score(X, y):.3f}")

st.divider()
st.markdown("<div style='text-align: center; color: #999; font-size: 11px; padding: 20px;'>TerraPulse AI • Powered by PostgreSQL & Python • Real-time Environmental Intelligence</div>", unsafe_allow_html=True)
