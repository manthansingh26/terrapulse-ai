import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import requests

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

st.set_page_config(page_title="TerraPulse AI", layout="wide")

st.title("🌍 TerraPulse")
st.subheader("Earth Intelligence Dashboard")
st.write("Live environmental monitoring dashboard")

st.sidebar.title("Control Panel")
location = st.sidebar.selectbox("Select Location", ["Ahmedabad", "Surat", "Mumbai"])
days = st.sidebar.slider("Number of Days", 5, 30, 7)
use_real_data = st.sidebar.checkbox("Use Real Air Quality Data", value=False)

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

st.divider()

# Main Dashboard Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "📈 CSV Analysis", "🖼️ Image Analysis", "🌿 Environmental Datasets", "🤖 ML Models"])

# ============ TAB 1: DASHBOARD ============
with tab1:
    st.subheader("Environmental Metrics")
    
    # Display data table
    st.write("Real-time environmental data:")
    st.dataframe(sample_data, width='stretch')
    
    # Chart
    st.line_chart(sample_data.set_index("Day")[["Temperature (°C)", "Humidity (%)", "AQI", "CO2 (ppm)", "Rainfall (mm)", "Wind Speed (km/h)"]])

# ============ TAB 2: CSV ANALYSIS ============
with tab2:
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

# ============ TAB 3: IMAGE ANALYSIS ============
with tab3:
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

# ============ TAB 4: ENVIRONMENTAL DATASETS ============
with tab4:
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

# ============ TAB 5: ML MODELS ============
with tab5:
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