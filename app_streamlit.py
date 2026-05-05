#!/usr/bin/env python3
"""
TerraPulse AI - Streamlit Frontend
Streamlit-based dashboard for environmental monitoring and air quality tracking
Connects to FastAPI backend at http://localhost:8000/api
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import logging
from typing import Dict, List, Optional
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="TerraPulse AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# STYLING & THEMING
# ============================================================================

st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    .main-header {
        text-align: center;
        color: #1e3a8a;
        margin-bottom: 2rem;
    }
    .city-card {
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f9fafb;
    }
    .aqi-good { color: #10b981; }
    .aqi-moderate { color: #f59e0b; }
    .aqi-unhealthy { color: #ef4444; }
    .aqi-hazardous { color: #7c3aed; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# API CONFIGURATION
# ============================================================================

API_BASE_URL = "http://localhost:8000/api"
SESSION_TIMEOUT = 3600  # 1 hour

# City data with coordinates
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

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0

initialize_session_state()

# ============================================================================
# API FUNCTIONS
# ============================================================================

def register_user(username: str, email: str, full_name: str, password: str) -> tuple:
    """Register a new user"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={
                "username": username,
                "email": email,
                "full_name": full_name,
                "password": password
            },
            timeout=10
        )
        
        if response.status_code == 201:
            return True, response.json().get("message", "Registration successful")
        else:
            error_msg = response.json().get("detail", "Registration failed")
            return False, error_msg
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return False, f"Connection error: {str(e)}"

def login_user(username: str, password: str) -> tuple:
    """Login user and get JWT token"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return True, data.get("access_token"), data.get("user", {})
        else:
            error_msg = response.json().get("detail", "Login failed")
            return False, None, error_msg
    except Exception as e:
        logger.error(f"Login error: {e}")
        return False, None, f"Connection error: {str(e)}"

def get_all_cities_latest(token: str) -> Optional[List[Dict]]:
    """Get latest data for all cities"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE_URL}/data/all/latest",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Error fetching cities data: {e}")
        return None

def get_city_latest(city: str, token: str) -> Optional[Dict]:
    """Get latest data for a specific city"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE_URL}/data/latest/{city}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Error fetching city data: {e}")
        return None

def get_city_history(city: str, token: str, days: int = 7) -> Optional[pd.DataFrame]:
    """Get historical data for a city"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE_URL}/data/history/{city}?days={days}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return pd.DataFrame(data)
        return None
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return None

def get_city_statistics(city: str, token: str, days: int = 7) -> Optional[Dict]:
    """Get statistics for a city"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE_URL}/data/statistics/{city}?days={days}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        return None

def get_current_user(token: str) -> Optional[Dict]:
    """Get current user info"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE_URL}/auth/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        return None

# ============================================================================
# PAGE: LOGIN & REGISTRATION
# ============================================================================

def show_login_page():
    """Display login and registration page"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🔐 Login")
        
        username = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                success, token, user = login_user(username, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.token = token
                    st.session_state.user = user
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error(f"❌ Login failed: {user}")
                    st.session_state.login_attempts += 1
            else:
                st.warning("Please enter username and password")
        
        st.divider()
        st.info("📝 Demo Credentials:\n- Username: `demo`\n- Password: `demo123`")
    
    with col2:
        st.header("📝 Register")
        
        reg_email = st.text_input("Email", key="reg_email")
        reg_username = st.text_input("Username", key="reg_username")
        reg_fullname = st.text_input("Full Name", key="reg_fullname")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register", key="register_btn", use_container_width=True):
            if not all([reg_email, reg_username, reg_fullname, reg_password, reg_password_confirm]):
                st.warning("Please fill all fields")
            elif reg_password != reg_password_confirm:
                st.error("Passwords don't match")
            elif len(reg_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                success, message = register_user(reg_username, reg_email, reg_fullname, reg_password)
                if success:
                    st.success(f"✅ {message}")
                    st.info("Now you can login with your credentials!")
                else:
                    st.error(f"❌ Registration failed: {message}")

# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

def show_dashboard(token: str):
    """Display main dashboard"""
    st.header("🌍 TerraPulse AI - Environmental Monitoring Dashboard")
    
    # Fetch all cities data
    cities_data = get_all_cities_latest(token)
    
    if not cities_data:
        st.error("❌ Unable to fetch data from API. Make sure backend is running!")
        return
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(cities_data)
    
    # ========== TOP METRICS ==========
    st.subheader("📊 Overall Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_aqi = df['aqi'].mean() if 'aqi' in df.columns else 0
        st.metric("Average AQI", f"{avg_aqi:.1f}", 
                  delta=f"Max: {df['aqi'].max():.1f}" if 'aqi' in df.columns else "")
    
    with col2:
        avg_temp = df['temperature'].mean() if 'temperature' in df.columns else 0
        st.metric("Avg Temperature", f"{avg_temp:.1f}°C")
    
    with col3:
        avg_humidity = df['humidity'].mean() if 'humidity' in df.columns else 0
        st.metric("Avg Humidity", f"{avg_humidity:.1f}%")
    
    with col4:
        cities_count = len(df)
        st.metric("Cities Monitored", cities_count)
    
    # ========== CHARTS ==========
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["📈 Top Polluted Cities", "🗺️ AQI Distribution", "📊 Temperature Map"])
    
    with tab1:
        st.subheader("Top 10 Most Polluted Cities")
        
        if 'aqi' in df.columns and 'city' in df.columns:
            top_10 = df.nlargest(10, 'aqi')[['city', 'aqi']].reset_index(drop=True)
            
            fig = px.bar(
                top_10,
                x='aqi',
                y='city',
                orientation='h',
                color='aqi',
                color_continuous_scale='Reds',
                labels={'aqi': 'AQI Level', 'city': 'City'},
                title="Top 10 Most Polluted Cities"
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("AQI Status Distribution")
        
        if 'aqi' in df.columns:
            # Categorize AQI
            aqi_categories = []
            for aqi in df['aqi']:
                if aqi <= 50:
                    aqi_categories.append('Good')
                elif aqi <= 100:
                    aqi_categories.append('Fair')
                elif aqi <= 150:
                    aqi_categories.append('Poor')
                elif aqi <= 200:
                    aqi_categories.append('Very Poor')
                else:
                    aqi_categories.append('Hazardous')
            
            df['aqi_category'] = aqi_categories
            category_counts = df['aqi_category'].value_counts()
            
            colors = {
                'Good': '#10b981',
                'Fair': '#f59e0b',
                'Poor': '#ef4444',
                'Very Poor': '#dc2626',
                'Hazardous': '#7c3aed'
            }
            
            fig = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                color=category_counts.index,
                color_discrete_map=colors,
                title="Air Quality Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Temperature Distribution")
        
        if 'temperature' in df.columns:
            fig = px.histogram(
                df,
                x='temperature',
                nbins=15,
                labels={'temperature': 'Temperature (°C)', 'count': 'Number of Cities'},
                title="Temperature Distribution Across Cities",
                color_discrete_sequence=['#3b82f6']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== CITIES TABLE ==========
    st.divider()
    st.subheader("📋 All Cities Data")
    
    if len(df) > 0:
        # Display data table
        display_df = df[['city', 'aqi', 'temperature', 'humidity', 'wind_speed']].copy()
        display_df = display_df.round(2)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "city": st.column_config.TextColumn("City", width="medium"),
                "aqi": st.column_config.NumberColumn("AQI", format="%.1f"),
                "temperature": st.column_config.NumberColumn("Temp (°C)", format="%.1f"),
                "humidity": st.column_config.NumberColumn("Humidity (%)", format="%.1f"),
                "wind_speed": st.column_config.NumberColumn("Wind Speed (m/s)", format="%.1f"),
            }
        )

# ============================================================================
# PAGE: CITY DETAILS
# ============================================================================

def show_city_details(token: str):
    """Display detailed information for a selected city"""
    st.header("🏙️ City Details & Analytics")
    
    # City selector
    city = st.selectbox("Select a City", list(CITY_COORDINATES.keys()))
    
    # Fetch city data
    city_data = get_city_latest(city, token)
    
    if not city_data:
        st.error(f"❌ Unable to fetch data for {city}")
        return
    
    # Display current readings
    st.subheader(f"📍 Current Readings - {city}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        aqi = city_data.get('aqi', 0)
        st.metric("AQI", f"{aqi:.1f}")
    
    with col2:
        temp = city_data.get('temperature', 0)
        st.metric("Temperature", f"{temp:.1f}°C")
    
    with col3:
        humidity = city_data.get('humidity', 0)
        st.metric("Humidity", f"{humidity:.1f}%")
    
    with col4:
        wind = city_data.get('wind_speed', 0)
        st.metric("Wind Speed", f"{wind:.1f} m/s")
    
    with col5:
        co2 = city_data.get('co2', 0)
        st.metric("CO₂", f"{co2:.1f} ppm")
    
    # Fetch historical data
    st.divider()
    st.subheader("📈 Historical Trends")
    
    days = st.slider("Select number of days", 1, 30, 7)
    
    history_df = get_city_history(city, token, days)
    
    if history_df is not None and len(history_df) > 0:
        # Convert timestamp to datetime if needed
        if 'timestamp' in history_df.columns:
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
            history_df = history_df.sort_values('timestamp')
        
        # Plot AQI trend
        col1, col2 = st.columns(2)
        
        with col1:
            if 'aqi' in history_df.columns and 'timestamp' in history_df.columns:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=history_df['timestamp'],
                    y=history_df['aqi'],
                    mode='lines+markers',
                    name='AQI',
                    line=dict(color='#ef4444', width=2)
                ))
                fig.update_layout(title="AQI Trend", height=400, xaxis_title="Date", yaxis_title="AQI")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'temperature' in history_df.columns and 'timestamp' in history_df.columns:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=history_df['timestamp'],
                    y=history_df['temperature'],
                    mode='lines+markers',
                    name='Temperature',
                    line=dict(color='#f97316', width=2)
                ))
                fig.update_layout(title="Temperature Trend", height=400, xaxis_title="Date", yaxis_title="Temperature (°C)")
                st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    st.divider()
    st.subheader(f"📊 {days}-Day Statistics")
    
    stats = get_city_statistics(city, token, days)
    
    if stats:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Avg AQI", f"{stats.get('avg_aqi', 0):.1f}")
            st.metric("Max AQI", f"{stats.get('max_aqi', 0):.1f}")
            st.metric("Min AQI", f"{stats.get('min_aqi', 0):.1f}")
        
        with col2:
            st.metric("Avg Temperature", f"{stats.get('avg_temperature', 0):.1f}°C")
            st.metric("Avg Humidity", f"{stats.get('avg_humidity', 0):.1f}%")
            st.metric("Avg Wind Speed", f"{stats.get('avg_wind_speed', 0):.1f} m/s")
        
        with col3:
            st.metric("Total Rainfall", f"{stats.get('total_rainfall', 0):.1f} mm")
            st.metric("Records", f"{stats.get('record_count', 0)}")

# ============================================================================
# PAGE: PROFILE
# ============================================================================

def show_profile(token: str):
    """Display user profile"""
    st.header("👤 User Profile")
    
    user = get_current_user(token)
    
    if not user:
        st.error("❌ Unable to fetch user information")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("User Information")
        st.info(f"""
        **Username:** {user.get('username', 'N/A')}
        
        **Email:** {user.get('email', 'N/A')}
        
        **Full Name:** {user.get('full_name', 'N/A')}
        
        **User ID:** {user.get('id', 'N/A')}
        
        **Created At:** {user.get('created_at', 'N/A')}
        """)
    
    with col2:
        st.subheader("Account Status")
        
        is_admin = user.get('is_admin', False)
        
        if is_admin:
            st.success("✅ Administrator Account")
        else:
            st.info("ℹ️ Standard User Account")
        
        st.subheader("Quick Links")
        st.markdown("""
        - 📚 [API Documentation](http://localhost:8000/api/docs)
        - 📖 [Swagger UI](http://localhost:8000/api/docs)
        - 📋 [ReDoc](http://localhost:8000/api/redoc)
        """)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application logic"""
    
    # Header
    st.markdown("<h1 class='main-header'>🌍 TerraPulse AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Real-time Environmental Monitoring & Air Quality Tracking</p>", unsafe_allow_html=True)
    
    # Authentication check
    if not st.session_state.authenticated:
        show_login_page()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.title("🌍 TerraPulse AI")
            st.markdown("---")
            
            # Display logged-in user
            if st.session_state.user:
                st.write(f"**Logged in as:** {st.session_state.user.get('username', 'User')}")
                st.markdown("---")
            
            # Navigation
            page = st.radio(
                "Navigation",
                ["📊 Dashboard", "🏙️ City Details", "👤 Profile"],
                key="nav"
            )
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.token = None
                st.session_state.user = None
                st.rerun()
            
            st.markdown("---")
            
            # Info footer
            st.info("""
            **Backend Status:** Running at http://localhost:8000
            
            **API Docs:** http://localhost:8000/api/docs
            """)
        
        # Page routing
        token = st.session_state.token
        
        if page == "📊 Dashboard":
            show_dashboard(token)
        elif page == "🏙️ City Details":
            show_city_details(token)
        elif page == "👤 Profile":
            show_profile(token)

if __name__ == "__main__":
    main()
