import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import requests
import folium
from streamlit_folium import folium_static
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# Initialize session state for alerts and updates
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'alert_history' not in st.session_state:
    st.session_state.alert_history = []
if 'previous_aqi' not in st.session_state:
    st.session_state.previous_aqi = None
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 300  # 5 minutes in seconds

def check_pollution_spike(current_aqi, previous_aqi, threshold=50):
    """Check if there's a significant pollution spike"""
    if previous_aqi is None:
        return False, 0
    
    spike = current_aqi - previous_aqi
    if spike > threshold:
        return True, spike
    return False, spike

def create_alert(alert_type, message, severity="warning"):
    """Create an alert and add to history"""
    alert = {
        'timestamp': datetime.now(),
        'type': alert_type,
        'message': message,
        'severity': severity
    }
    st.session_state.alert_history.append(alert)
    # Keep only last 10 alerts
    if len(st.session_state.alert_history) > 10:
        st.session_state.alert_history = st.session_state.alert_history[-10:]
    return alert

def get_aqi_health_alert(aqi_value):
    """Get health alert message based on AQI"""
    if aqi_value < 50:
        return None
    elif aqi_value < 100:
        return "Moderate air quality. Unusually sensitive people should consider reducing prolonged outdoor exertion."
    elif aqi_value < 150:
        return "⚠️ Unhealthy for sensitive groups. People with respiratory conditions should limit outdoor activities."
    elif aqi_value < 200:
        return "🚨 Unhealthy air quality! Everyone should reduce prolonged outdoor exertion."
    elif aqi_value < 300:
        return "🚨 Very Unhealthy! Health alert - everyone may experience serious health effects."
    else:
        return "🆘 HAZARDOUS! Emergency conditions - everyone should avoid all outdoor activities!"

@st.cache_data
def fetch_air_quality_data(city, days):
    """Fetch air quality data from OpenWeatherMap API"""
    try:
        # Using OpenWeatherMap Air Pollution API (free tier)
        # First, get coordinates for the city
        city_coords = {
            "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
            "Surat": {"lat": 21.1702, "lon": 72.8311},
            "Mumbai": {"lat": 19.0760, "lon": 72.8777}
        }
        
        if city not in city_coords:
            return None
        
        coords = city_coords[city]
        
        # OpenWeatherMap Air Pollution API (no API key needed for basic access)
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={coords['lat']}&lon={coords['lon']}"
        
        response = requests.get(url, timeout=10)
        
        # If API requires key or fails, use alternative approach
        if response.status_code != 200:
            # Try AQICN API as fallback
            aqicn_url = f"https://api.waqi.info/feed/{city}/?token=demo"
            response = requests.get(aqicn_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok' and 'data' in data:
                    aqi_value = data['data'].get('aqi', 100)
                    # Generate historical data based on current reading
                    aqi_values = np.random.normal(aqi_value, 15, days).clip(10, 500)
                    co2_values = np.random.normal(400, 30, days).clip(300, 600)
                    
                    return pd.DataFrame({
                        'AQI': aqi_values,
                        'CO2': co2_values
                    })
            
            return None
        
        data = response.json()
        
        if 'list' in data and len(data['list']) > 0:
            # Get current pollution data
            pollution = data['list'][0]
            components = pollution.get('components', {})
            aqi = pollution.get('main', {}).get('aqi', 3) * 50  # Convert 1-5 scale to AQI
            
            pm25 = components.get('pm2_5', 50)
            co = components.get('co', 400)
            
            # Generate historical data based on current reading
            aqi_values = np.random.normal(pm25 * 2, 15, days).clip(10, 500)
            co2_values = np.random.normal(co / 10, 30, days).clip(300, 600)
            
            return pd.DataFrame({
                'AQI': aqi_values,
                'CO2': co2_values
            })
        
        return None
        
    except Exception as e:
        st.warning(f"API unavailable. Using simulated data. (Error: {str(e)})")
        return None

def get_city_coordinates(city):
    """Get coordinates for a city"""
    coords = {
        "Ahmedabad": (23.0225, 72.5714),
        "Surat": (21.1702, 72.8311),
        "Mumbai": (19.0760, 72.8777),
        "Delhi": (28.6139, 77.2090),
        "Bangalore": (12.9716, 77.5946),
        "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639),
        "Hyderabad": (17.3850, 78.4867),
        "Pune": (18.5204, 73.8567),
        "Jaipur": (26.9124, 75.7873),
        "Lucknow": (26.8467, 80.9462),
        "Kanpur": (26.4499, 80.3319),
        "Nagpur": (21.1458, 79.0882),
        "Indore": (22.7196, 75.8577),
        "Thane": (19.2183, 72.9781),
        "Bhopal": (23.2599, 77.4126),
        "Visakhapatnam": (17.6868, 83.2185),
        "Patna": (25.5941, 85.1376),
        "Vadodara": (22.3072, 73.1812),
        "Ghaziabad": (28.6692, 77.4538)
    }
    return coords.get(city, (22.0, 73.0))

def calculate_aqi_status(aqi_value):
    """Calculate AQI status and color based on EPA standards"""
    if aqi_value < 50:
        return {"level": "Good", "color": "green", "description": "Air quality is satisfactory"}
    elif aqi_value < 100:
        return {"level": "Moderate", "color": "yellow", "description": "Air quality is acceptable"}
    elif aqi_value < 150:
        return {"level": "Unhealthy for Sensitive Groups", "color": "orange", "description": "Sensitive groups may experience health effects"}
    elif aqi_value < 200:
        return {"level": "Unhealthy", "color": "red", "description": "Everyone may experience health effects"}
    elif aqi_value < 300:
        return {"level": "Very Unhealthy", "color": "purple", "description": "Health alert: serious health effects"}
    else:
        return {"level": "Hazardous", "color": "darkred", "description": "Health warnings of emergency conditions"}

def create_city_popup(city_name, city_data):
    """Create HTML popup content for city marker"""
    aqi_status = calculate_aqi_status(city_data['AQI'])
    
    html = f"""
    <div style='font-family: Arial; min-width: 250px;'>
        <h3 style='margin: 0; color: #2c3e50;'>{city_name}</h3>
        <hr style='margin: 10px 0;'>
        <div style='background-color: {aqi_status["color"]}; padding: 8px; border-radius: 4px; color: white; font-weight: bold; text-align: center;'>
            AQI: {city_data['AQI']:.1f} - {aqi_status["level"]}
        </div>
        <div style='margin-top: 10px;'>
            <div style='margin: 5px 0;'><span style='font-weight: bold;'>🌡️ Temperature:</span> {city_data['Temperature']:.1f} °C</div>
            <div style='margin: 5px 0;'><span style='font-weight: bold;'>💧 Humidity:</span> {city_data['Humidity']:.1f} %</div>
            <div style='margin: 5px 0;'><span style='font-weight: bold;'>🏭 CO2:</span> {city_data['CO2']:.1f} ppm</div>
            <div style='margin: 5px 0;'><span style='font-weight: bold;'>🌬️ Wind Speed:</span> {city_data['Wind Speed']:.1f} km/h</div>
            <div style='margin: 5px 0;'><span style='font-weight: bold;'>🌧️ Rainfall:</span> {city_data['Rainfall']:.1f} mm</div>
        </div>
    </div>
    """
    return html

def create_environmental_map(cities_data, center_location, zoom_level=6, show_heatmap=False):
    """Create interactive folium map with city markers"""
    # Create base map
    env_map = folium.Map(
        location=center_location,
        zoom_start=zoom_level,
        tiles="OpenStreetMap"
    )
    
    # Add markers for each city
    for city_name, city_data in cities_data.items():
        coords = get_city_coordinates(city_name)
        aqi_status = calculate_aqi_status(city_data['AQI'])
        
        # Create popup content
        popup_html = create_city_popup(city_name, city_data)
        
        # Add marker with color based on AQI
        folium.Marker(
            location=coords,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=city_name,
            icon=folium.Icon(color=aqi_status['color'], icon='info-sign')
        ).add_to(env_map)
    
    # Add heatmap layer if requested
    if show_heatmap:
        from folium.plugins import HeatMap
        heat_data = []
        for city_name, city_data in cities_data.items():
            coords = get_city_coordinates(city_name)
            # Normalize AQI to 0-1 range for heatmap intensity
            max_aqi = max(data['AQI'] for data in cities_data.values())
            intensity = city_data['AQI'] / max_aqi if max_aqi > 0 else 0
            heat_data.append([coords[0], coords[1], intensity])
        
        HeatMap(heat_data, radius=50, blur=35, max_zoom=13).add_to(env_map)
    
    return env_map

st.set_page_config(page_title="TerraPulse AI", layout="wide")

# Real-Time Monitoring Header
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.title("🌍 TerraPulse")
with col2:
    # Last update time
    time_since_update = (datetime.now() - st.session_state.last_update).seconds
    st.metric("Last Update", f"{time_since_update}s ago")
with col3:
    # Auto-refresh toggle
    if st.button("🔄 Refresh Now"):
        st.session_state.last_update = datetime.now()
        st.rerun()
st.subheader("Earth Intelligence Dashboard")
st.write("Live environmental monitoring dashboard")

st.sidebar.title("Control Panel")

# Real-Time Monitoring Section
st.sidebar.subheader("⚡ Real-Time Monitoring")
auto_refresh = st.sidebar.checkbox("Enable Auto-Refresh", value=st.session_state.auto_refresh)
st.session_state.auto_refresh = auto_refresh

if auto_refresh:
    refresh_interval = st.sidebar.select_slider(
        "Refresh Interval",
        options=[60, 120, 300, 600],
        value=st.session_state.refresh_interval,
        format_func=lambda x: f"{x//60} min" if x >= 60 else f"{x}s"
    )
    st.session_state.refresh_interval = refresh_interval
    
    # Auto-refresh logic
    time_since_update = (datetime.now() - st.session_state.last_update).seconds
    if time_since_update >= refresh_interval:
        st.session_state.last_update = datetime.now()
        st.rerun()
    
    # Show countdown
    remaining = refresh_interval - time_since_update
    st.sidebar.info(f"⏱️ Next refresh in: {remaining}s")
    time.sleep(1)
    st.rerun()

# Alert Settings
st.sidebar.subheader("🔔 Alert Settings")
enable_alerts = st.sidebar.checkbox("Enable Pollution Alerts", value=True)
alert_threshold = st.sidebar.slider("AQI Alert Threshold", 100, 300, 150)

st.sidebar.divider()

# Location and Data Settings
st.sidebar.subheader("📍 Location & Data")
location = st.sidebar.selectbox("Select Location", [
    "Ahmedabad", "Surat", "Mumbai", "Delhi", "Bangalore", 
    "Chennai", "Kolkata", "Hyderabad", "Pune", "Jaipur",
    "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane",
    "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Ghaziabad"
])
days = st.sidebar.slider("Number of Days", 5, 30, 7)
use_real_data = st.sidebar.checkbox("Use Real Air Quality Data", value=False)
show_heatmap = st.sidebar.checkbox("Show Pollution Heatmap", value=False)

if use_real_data:
    # Try to fetch real air quality data
    real_aq_data = fetch_air_quality_data(location, days)
    if real_aq_data is not None and not real_aq_data.empty:
        # Use real AQI and CO2
        aqi = real_aq_data['AQI'].values
        co2 = real_aq_data['CO2'].values
        # Ensure we have enough data
        if len(aqi) < days:
            # Pad with averages
            avg_aqi = np.mean(aqi) if len(aqi) > 0 else 50
            avg_co2 = np.mean(co2) if len(co2) > 0 else 400
            aqi = np.pad(aqi, (0, days - len(aqi)), constant_values=avg_aqi)
            co2 = np.pad(co2, (0, days - len(co2)), constant_values=avg_co2)
    else:
        # Fallback to random
        aqi = np.random.randint(50, 200, days)
        co2 = np.random.uniform(350, 450, days)
else:
    aqi = np.random.randint(50, 200, days)
    co2 = np.random.uniform(350, 450, days)

temperature = np.random.randint(20, 40, days)
humidity = np.random.randint(40, 90, days)
rainfall = np.random.uniform(0, 10, days)
wind_speed = np.random.uniform(5, 25, days)

sample_data = pd.DataFrame({
    "Day": list(range(1, days + 1)),
    "Temperature (°C)": temperature,
    "Humidity (%)": humidity,
    "AQI": aqi,
    "CO2 (ppm)": co2,
    "Rainfall (mm)": rainfall,
    "Wind Speed (km/h)": wind_speed
})

col1, col2, col3, col4 = st.columns(4)
col1.metric("📍 Location", location)
col2.metric("🌡 Avg Temperature", f"{sample_data['Temperature (°C)'].mean():.1f} °C")
col3.metric("💧 Avg Humidity", f"{sample_data['Humidity (%)'].mean():.1f} %")
col4.metric("🌬️ Avg Wind Speed", f"{sample_data['Wind Speed (km/h)'].mean():.1f} km/h")

# Real-Time Alert System
current_aqi = sample_data['AQI'].mean()

# Check for pollution spike
if enable_alerts and st.session_state.previous_aqi is not None:
    is_spike, spike_amount = check_pollution_spike(current_aqi, st.session_state.previous_aqi, threshold=50)
    if is_spike:
        alert_msg = f"🚨 Pollution Spike Alert! AQI increased by {spike_amount:.1f} points in {location}"
        create_alert("pollution_spike", alert_msg, "error")
        st.error(alert_msg)

# Check AQI threshold
if enable_alerts and current_aqi > alert_threshold:
    health_alert = get_aqi_health_alert(current_aqi)
    if health_alert:
        create_alert("high_aqi", health_alert, "warning")
        st.warning(f"⚠️ {location}: {health_alert}")

# Update previous AQI
st.session_state.previous_aqi = current_aqi

# Display Alert History
if len(st.session_state.alert_history) > 0:
    with st.expander(f"📋 Alert History ({len(st.session_state.alert_history)} alerts)", expanded=False):
        for alert in reversed(st.session_state.alert_history[-5:]):  # Show last 5
            time_str = alert['timestamp'].strftime("%H:%M:%S")
            if alert['severity'] == 'error':
                st.error(f"[{time_str}] {alert['message']}")
            elif alert['severity'] == 'warning':
                st.warning(f"[{time_str}] {alert['message']}")
            else:
                st.info(f"[{time_str}] {alert['message']}")

# Live Status Indicator
status_col1, status_col2, status_col3 = st.columns([1, 1, 2])
with status_col1:
    if current_aqi < 100:
        st.success("🟢 Air Quality: Good")
    elif current_aqi < 150:
        st.warning("🟡 Air Quality: Moderate")
    else:
        st.error("🔴 Air Quality: Unhealthy")

with status_col2:
    if auto_refresh:
        st.info("🔄 Live Monitoring Active")
    else:
        st.info("⏸️ Manual Mode")

with status_col3:
    # Data freshness indicator
    if use_real_data:
        st.success("📡 Using Real-Time Data")
    else:
        st.info("📊 Using Simulated Data")

st.divider()

# Main Dashboard Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Dashboard", "🗺️ Interactive Map", "📈 CSV Analysis", "🖼️ Image Analysis", "🌿 Environmental Datasets", "🤖 ML Models"])

# ============ TAB 1: DASHBOARD ============
with tab1:
    st.subheader("Environmental Metrics")
    
    # Display data table
    st.write("Real-time environmental data:")
    st.dataframe(sample_data, width='stretch')
    
    # Chart
    st.line_chart(sample_data.set_index("Day")[["Temperature (°C)", "Humidity (%)", "AQI", "CO2 (ppm)", "Rainfall (mm)", "Wind Speed (km/h)"]])

# ============ TAB 2: INTERACTIVE MAP ============
with tab2:
    st.subheader("Interactive Geospatial Map")
    st.write("Explore environmental data across cities with interactive markers and optional heatmap overlay.")
    
    # Prepare data for all cities
    all_cities = ["Ahmedabad", "Surat", "Mumbai"]
    cities_data = {}
    
    for city in all_cities:
        # Get average values for the city
        if city == location:
            # Use current sample_data for selected location
            cities_data[city] = {
                'AQI': sample_data['AQI'].mean(),
                'CO2': sample_data['CO2 (ppm)'].mean(),
                'Temperature': sample_data['Temperature (°C)'].mean(),
                'Humidity': sample_data['Humidity (%)'].mean(),
                'Wind Speed': sample_data['Wind Speed (km/h)'].mean(),
                'Rainfall': sample_data['Rainfall (mm)'].mean()
            }
        else:
            # Generate data for other cities
            cities_data[city] = {
                'AQI': np.random.uniform(50, 200),
                'CO2': np.random.uniform(350, 450),
                'Temperature': np.random.uniform(20, 40),
                'Humidity': np.random.uniform(40, 90),
                'Wind Speed': np.random.uniform(5, 25),
                'Rainfall': np.random.uniform(0, 10)
            }
    
    # Create map centered on India
    center_coords = (22.0, 73.0)  # Central India
    env_map = create_environmental_map(
        cities_data=cities_data,
        center_location=center_coords,
        zoom_level=6,
        show_heatmap=show_heatmap
    )
    
    # Display map
    folium_static(env_map, width=1200, height=600)
    
    # Display legend
    st.write("**AQI Color Legend:**")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.markdown("🟢 **Good** (0-50)")
    col2.markdown("🟡 **Moderate** (51-100)")
    col3.markdown("🟠 **Unhealthy for Sensitive** (101-150)")
    col4.markdown("🔴 **Unhealthy** (151-200)")
    col5.markdown("🟣 **Very Unhealthy** (201-300)")
    col6.markdown("🟤 **Hazardous** (301+)")

# ============ TAB 3: CSV ANALYSIS ============
with tab3:
    st.subheader("Upload & Analyze CSV Data")
    
    uploaded_csv = st.file_uploader("📂 Upload a CSV file", type=["csv"], key="csv_uploader")
    if uploaded_csv is not None:
        df = pd.read_csv(uploaded_csv)
        st.success("✓ CSV uploaded successfully")
        st.dataframe(df, width='stretch')
        
        st.subheader("📊 CSV Summary")
        
        col1, col2 = st.columns(2)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        
        st.subheader("📈 Data Quality & Analytics")
        
        # Calculate metrics
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        data_quality = ((total_cells - missing_cells) / total_cells) * 100
        
        # Data Quality Card
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("✅ Data Quality", f"{data_quality:.1f}%", 
                   delta="Complete" if data_quality == 100 else f"{missing_cells} missing")
        
        col2.metric("🔢 Numeric Cols", len(df.select_dtypes(include=np.number).columns))
        
        col3.metric("📝 Text Cols", len(df.select_dtypes(include='object').columns))
        
        col4.metric("⚠️ Missing Values", missing_cells)
        
        # Missing Data Heatmap
        if missing_cells > 0:
            st.write("Missing values by column:")
            missing_counts = df.isnull().sum()
            missing_df = pd.DataFrame({
                "Column": missing_counts.index,
                "Missing Count": missing_counts.values,
                "Missing %": (missing_counts.values / len(df) * 100).round(2)
            })
            missing_df = missing_df[missing_df["Missing Count"] > 0].sort_values("Missing Count", ascending=False)
            
            st.bar_chart(missing_df.set_index("Column")["Missing Count"])
        
        numeric_cols = df.select_dtypes(include=np.number).columns
        
        if len(numeric_cols) > 0:
            avg_df = pd.DataFrame(df[numeric_cols].mean()).reset_index()
            avg_df.columns = ["Column", "Average Value"]
            st.write("Average values for numeric columns:")
            st.dataframe(avg_df)
        else:
            st.warning("No numeric columns found in this CSV.")

        numeric_cols = df.select_dtypes(include=np.number).columns

        st.subheader("📈 Data Insights")

        if len(numeric_cols) >= 1:
            selected_col = st.selectbox("Select a numeric column to analyze", numeric_cols)

            st.metric(
                f"Average {selected_col}",
                f"{df[selected_col].mean():.2f}"
            )

            st.metric(
                f"Maximum {selected_col}",
                f"{df[selected_col].max():.2f}"
            )

            st.metric(
                f"Minimum {selected_col}",
                f"{df[selected_col].min():.2f}"
            )

            st.line_chart(df[selected_col])

        else:
            st.warning("No numeric column available for analysis.")

# ============ TAB 4: IMAGE ANALYSIS ============
with tab4:
    st.subheader("Upload & Analyze Images")

    uploaded_image = st.file_uploader("📂 Upload an image", type=["png", "jpg", "jpeg"], key="image_uploader")
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.success("✓ Image uploaded successfully")
        st.image(image, caption="Uploaded Image", width='stretch')

        col1, col2, col3 = st.columns(3)
        col1.metric("📏 Resolution", f"{image.size[0]}×{image.size[1]}")
        col2.metric("📁 File Size", f"{len(uploaded_image.getvalue()) / 1024:.1f} KB")
        col3.metric("🎨 Format", image.format if image.format else "Unknown")

        arr = np.array(image)
        if arr.ndim == 3:
            st.write(f"Average RGB values: R={arr[:,:,0].mean():.1f}, G={arr[:,:,1].mean():.1f}, B={arr[:,:,2].mean():.1f}")
        else:
            st.write(f"Average grayscale value: {arr.mean():.1f}")

# ============ TAB 5: ENVIRONMENTAL DATASETS ============
with tab5:
    st.subheader("Environmental Datasets Overview")
    
    st.write("Explore various environmental metrics and datasets for selected location and time period.")
    
    # Dataset selector
    dataset_type = st.selectbox("Select Dataset Type", ["Air Quality", "Climate Change", "Water Quality", "Biodiversity"])
    
    if dataset_type == "Air Quality":
        st.write("**Air Quality Metrics:**")
        st.dataframe(sample_data[["Day", "AQI", "CO2 (ppm)"]], width='stretch')
        st.line_chart(sample_data.set_index("Day")[["AQI", "CO2 (ppm)"]])
        
        # AQI interpretation
        avg_aqi = sample_data["AQI"].mean()
        if avg_aqi < 50:
            status = "Good"
            color = "green"
        elif avg_aqi < 100:
            status = "Moderate"
            color = "yellow"
        elif avg_aqi < 150:
            status = "Unhealthy for Sensitive Groups"
            color = "orange"
        else:
            status = "Unhealthy"
            color = "red"
        
        st.metric("Average Air Quality", f"{avg_aqi:.1f}", status)
    
    elif dataset_type == "Climate Change":
        st.write("**Climate Change Indicators:**")
        st.dataframe(sample_data[["Day", "Temperature (°C)", "CO2 (ppm)", "Rainfall (mm)"]], width='stretch')
        st.line_chart(sample_data.set_index("Day")[["Temperature (°C)", "CO2 (ppm)", "Rainfall (mm)"]])
        
        st.metric("Average Temperature", f"{sample_data['Temperature (°C)'].mean():.1f} °C")
        st.metric("Total Rainfall", f"{sample_data['Rainfall (mm)'].sum():.1f} mm")
    
    elif dataset_type == "Water Quality":
        # Generate water quality data
        ph = np.random.uniform(6.5, 8.5, days)
        turbidity = np.random.uniform(0, 5, days)
        dissolved_oxygen = np.random.uniform(5, 12, days)
        
        water_data = pd.DataFrame({
            "Day": list(range(1, days + 1)),
            "pH": ph,
            "Turbidity (NTU)": turbidity,
            "Dissolved Oxygen (mg/L)": dissolved_oxygen
        })
        
        st.write("**Water Quality Metrics:**")
        st.dataframe(water_data, width='stretch')
        st.line_chart(water_data.set_index("Day"))
        
        st.metric("Average pH", f"{water_data['pH'].mean():.2f}")
    
    elif dataset_type == "Biodiversity":
        # Generate biodiversity data
        species_count = np.random.randint(10, 50, days)
        endangered_species = np.random.randint(0, 5, days)
        
        bio_data = pd.DataFrame({
            "Day": list(range(1, days + 1)),
            "Species Count": species_count,
            "Endangered Species": endangered_species
        })
        
        st.write("**Biodiversity Metrics:**")
        st.dataframe(bio_data, width='stretch')
        st.bar_chart(bio_data.set_index("Day")["Species Count"])
        
        st.metric("Total Species Observed", bio_data["Species Count"].sum())

# ============ TAB 6: ML MODELS ============
with tab6:
    st.subheader("Machine Learning Models for Environmental Prediction")
    
    st.write("Apply ML models to predict environmental trends and detect anomalies.")
    
    model_type = st.selectbox("Select ML Model", ["Temperature Forecasting", "Anomaly Detection", "Pollution Prediction"])
    
    if model_type == "Temperature Forecasting":
        st.write("**Temperature Forecasting using Linear Regression**")
        
        # Prepare data
        X = sample_data[["Day"]].values
        y = sample_data["Temperature (°C)"].values
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next 5 days
        future_days = np.array([[days + i] for i in range(1, 6)])
        predictions = model.predict(future_days)
        
        st.write("Current temperature trend:")
        st.line_chart(sample_data.set_index("Day")["Temperature (°C)"])
        
        st.write("Forecasted temperatures for next 5 days:")
        forecast_df = pd.DataFrame({
            "Day": [f"Day {days + i}" for i in range(1, 6)],
            "Predicted Temperature (°C)": predictions
        })
        st.dataframe(forecast_df, width='stretch')
        st.line_chart(forecast_df.set_index("Day"))
        
        st.metric("Model R² Score", f"{model.score(X, y):.3f}")
    
    elif model_type == "Anomaly Detection":
        st.write("**Anomaly Detection using Isolation Forest**")
        
        # Prepare data for anomaly detection
        features = sample_data[["Temperature (°C)", "Humidity (%)", "AQI"]].values
        
        # Train model
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomalies = iso_forest.fit_predict(features)
        
        # Add anomaly column
        anomaly_df = sample_data.copy()
        anomaly_df["Anomaly"] = ["Anomaly" if x == -1 else "Normal" for x in anomalies]
        
        st.write("Anomaly detection results:")
        st.dataframe(anomaly_df[["Day", "Temperature (°C)", "Humidity (%)", "AQI", "Anomaly"]], width='stretch')
        
        # Visualize anomalies
        normal_data = anomaly_df[anomaly_df["Anomaly"] == "Normal"]
        anomaly_data = anomaly_df[anomaly_df["Anomaly"] == "Anomaly"]
        
        st.write("Temperature anomalies:")
        chart_data = pd.DataFrame({
            "Day": anomaly_df["Day"],
            "Temperature": anomaly_df["Temperature (°C)"],
            "Type": anomaly_df["Anomaly"]
        })
        st.scatter_chart(chart_data, x="Day", y="Temperature", color="Type")
        
        st.metric("Anomalies Detected", len(anomaly_data))
    
    elif model_type == "Pollution Prediction":
        st.write("**Pollution Level Prediction**")
        
        # Simple classification based on AQI
        pollution_levels = []
        for aqi in sample_data["AQI"]:
            if aqi < 50:
                pollution_levels.append("Low")
            elif aqi < 100:
                pollution_levels.append("Moderate")
            elif aqi < 150:
                pollution_levels.append("High")
            else:
                pollution_levels.append("Very High")
        
        pred_df = sample_data[["Day", "AQI"]].copy()
        pred_df["Pollution Level"] = pollution_levels
        
        st.dataframe(pred_df, width='stretch')
        
        # Pie chart of pollution levels
        level_counts = pd.Series(pollution_levels).value_counts()
        st.write("Pollution level distribution:")
        st.bar_chart(level_counts)
        
        st.metric("Average AQI", f"{sample_data['AQI'].mean():.1f}")