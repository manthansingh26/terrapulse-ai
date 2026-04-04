# 📖 TerraPulse AI - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Real-Time Monitoring](#real-time-monitoring)
4. [Interactive Map](#interactive-map)
5. [Machine Learning Models](#machine-learning-models)
6. [Data Analysis](#data-analysis)
7. [Alerts & Notifications](#alerts--notifications)
8. [Tips & Best Practices](#tips--best-practices)

---

## Getting Started

### First Launch
1. Start the application: `streamlit run app.py`
2. Open browser to `http://localhost:8501`
3. You'll see the main dashboard with environmental metrics

### Interface Overview
- **Top Bar**: Title, last update time, and refresh button
- **Sidebar**: Control panel with all settings
- **Main Area**: Tabbed interface with different features
- **Status Bar**: Real-time indicators for air quality and monitoring status

---

## Dashboard Overview

### Main Tabs

#### 📊 Dashboard
- View real-time environmental metrics
- See trend charts for all parameters
- Monitor temperature, humidity, AQI, CO2, rainfall, wind speed

#### 🗺️ Interactive Map
- Explore 20 Indian cities on an interactive map
- Click markers for detailed city information
- Toggle pollution heatmap overlay
- Zoom and pan to explore regions

#### 📈 CSV Analysis
- Upload custom environmental datasets
- Analyze data quality and completeness
- View summary statistics
- Detect missing values

#### 🖼️ Image Analysis
- Upload environmental images
- View image metadata (resolution, format, size)
- Analyze RGB/grayscale values

#### 🌿 Environmental Datasets
- Explore different dataset types
- Air Quality, Climate Change, Water Quality, Biodiversity
- View specialized metrics for each category

#### 🤖 ML Models
- Run advanced machine learning models
- Prophet forecasting, LSTM prediction, K-Means clustering
- Anomaly detection and multi-variable prediction

---

## Real-Time Monitoring

### Enabling Auto-Refresh

1. **Open Sidebar** → "⚡ Real-Time Monitoring"
2. **Check** "Enable Auto-Refresh"
3. **Select Interval**: Choose from 1, 2, 5, or 10 minutes
4. **Monitor Countdown**: See time until next refresh in sidebar

### How It Works
- Data automatically refreshes at selected interval
- Page updates without manual interaction
- Countdown timer shows time remaining
- Click "🔄 Refresh Now" for immediate update

### Best Practices
- Use 5-minute intervals for general monitoring
- Use 1-minute intervals for critical situations
- Disable auto-refresh when analyzing historical data
- Enable alerts for automatic notifications

---

## Interactive Map

### Basic Navigation

#### Viewing Cities
- Map displays all 20 cities with color-coded markers
- **Green**: Good air quality (AQI 0-50)
- **Yellow**: Moderate (AQI 51-100)
- **Orange**: Unhealthy for sensitive groups (AQI 101-150)
- **Red**: Unhealthy (AQI 151-200)
- **Purple**: Very unhealthy (AQI 201-300)
- **Maroon**: Hazardous (AQI 301+)

#### Interacting with Markers
1. **Click** any city marker
2. **Popup appears** with detailed metrics:
   - City name
   - AQI value and status
   - Temperature
   - Humidity
   - CO2 levels
   - Wind speed
   - Rainfall

#### Using the Heatmap
1. **Enable** "Show Pollution Heatmap" in sidebar
2. **View** pollution intensity overlay
3. **Interpret**: Darker/redder areas = higher pollution
4. **Zoom** in/out to see regional patterns

### Map Controls
- **Zoom**: Use mouse wheel or +/- buttons
- **Pan**: Click and drag to move map
- **Reset**: Refresh page to reset view
- **Fullscreen**: Expand browser window for better view

---

## Machine Learning Models

### 1. Prophet Time Series Forecasting

**Purpose**: Predict future environmental trends

**How to Use**:
1. Select "Prophet Time Series Forecasting"
2. Choose variable to forecast (Temperature, AQI, Humidity, CO2)
3. Set forecast horizon (5-30 days)
4. View predictions with confidence intervals

**Interpreting Results**:
- **Blue line**: Historical data
- **Red dashed line**: Forecast
- **Shaded area**: Uncertainty range (95% confidence)
- **Components**: Shows daily and weekly patterns

**Best For**:
- Long-term trend analysis
- Planning and preparation
- Understanding seasonal patterns

---

### 2. LSTM Neural Network

**Purpose**: Deep learning for pollution prediction

**How to Use**:
1. Select "LSTM Neural Network Prediction"
2. Choose sequence length (3-10 days lookback)
3. Select prediction target (AQI, CO2, Temperature)
4. Wait for model training (30-60 seconds)
5. View predictions and performance metrics

**Interpreting Results**:
- **RMSE**: Lower is better (prediction error)
- **MAE**: Mean absolute error
- **R² Score**: Closer to 1.0 is better (0.8+ is good)
- **Training curves**: Should show decreasing loss

**Best For**:
- Short-term predictions
- Complex pattern recognition
- High-accuracy forecasting

---

### 3. K-Means Clustering

**Purpose**: Discover environmental patterns

**How to Use**:
1. Select "K-Means Environmental Clustering"
2. Choose features for clustering (2-6 features)
3. Set number of clusters (2-6)
4. View cluster visualizations

**Interpreting Results**:
- **Clusters**: Groups of similar environmental conditions
- **2D/3D plots**: Visual representation of clusters
- **Statistics**: Average values for each cluster
- **Distribution**: Number of days in each cluster

**Best For**:
- Pattern discovery
- Identifying typical weather conditions
- Understanding environmental regimes

---

### 4. Advanced Anomaly Detection

**Purpose**: Identify unusual environmental events

**How to Use**:
1. Select "Advanced Anomaly Detection"
2. Choose features to analyze
3. Set contamination rate (expected % of anomalies)
4. View detected anomalies

**Interpreting Results**:
- **Red points**: Anomalies detected
- **Blue points**: Normal conditions
- **Anomaly score**: More negative = more anomalous
- **Table**: List of anomalous days with values

**Best For**:
- Detecting pollution events
- Quality control
- Identifying data errors

---

### 5. Multi-Variable Prediction

**Purpose**: Predict one variable using multiple factors

**How to Use**:
1. Select "Multi-Variable Prediction"
2. Choose target variable to predict
3. Select predictor features
4. View feature importance and predictions

**Interpreting Results**:
- **Feature importance**: Which factors matter most
- **R² Score**: Model accuracy (0.7+ is good)
- **Scatter plot**: Predicted vs actual values
- **Residuals**: Prediction errors distribution

**Best For**:
- Understanding relationships
- Identifying key factors
- Making informed predictions

---

## Data Analysis

### CSV Upload & Analysis

1. **Navigate** to "📈 CSV Analysis" tab
2. **Click** "Upload a CSV file"
3. **Select** your environmental dataset
4. **View** automatic analysis:
   - Row and column counts
   - Data quality percentage
   - Missing value detection
   - Summary statistics

### Supported CSV Format
```csv
Date,Temperature,Humidity,AQI,CO2
2024-01-01,25.5,65,85,410
2024-01-02,26.2,62,92,415
...
```

### Image Analysis

1. **Navigate** to "🖼️ Image Analysis" tab
2. **Upload** environmental image (PNG, JPG, JPEG)
3. **View** metadata:
   - Resolution
   - File size
   - Format
   - Average RGB values

---

## Alerts & Notifications

### Configuring Alerts

1. **Open Sidebar** → "🔔 Alert Settings"
2. **Enable** "Enable Pollution Alerts"
3. **Set** AQI Alert Threshold (100-300)
4. **Monitor** alert history in main area

### Alert Types

#### Pollution Spike Alert
- Triggered when AQI increases by 50+ points
- Shows spike amount
- Displayed as red error message

#### High AQI Alert
- Triggered when AQI exceeds threshold
- Shows health recommendations
- Displayed as yellow warning

### Alert History
- **View** last 5 alerts in expandable section
- **Timestamp**: When alert occurred
- **Message**: Alert details
- **Severity**: Color-coded by importance

### Health Recommendations

Based on AQI levels:
- **0-50 (Good)**: No restrictions
- **51-100 (Moderate)**: Sensitive people should limit prolonged outdoor exertion
- **101-150 (Unhealthy for Sensitive)**: Sensitive groups should reduce outdoor activities
- **151-200 (Unhealthy)**: Everyone should reduce prolonged outdoor exertion
- **201-300 (Very Unhealthy)**: Everyone should avoid outdoor exertion
- **301+ (Hazardous)**: Everyone should remain indoors

---

## Tips & Best Practices

### For Daily Monitoring
1. Enable auto-refresh with 5-minute interval
2. Set AQI alert threshold to 150
3. Check alert history regularly
4. Monitor your city on the interactive map

### For Data Analysis
1. Disable auto-refresh to avoid interruptions
2. Upload historical CSV data for trends
3. Use Prophet for long-term forecasting
4. Run anomaly detection to find unusual events

### For ML Experiments
1. Start with Prophet (easiest to interpret)
2. Try different forecast horizons
3. Compare multiple models
4. Use feature importance to understand relationships

### Performance Tips
1. Close unused browser tabs
2. Disable heatmap when not needed
3. Use shorter time periods for faster ML training
4. Clear alert history periodically

### Troubleshooting

**Map not loading?**
- Check internet connection
- Refresh the page
- Try different browser

**ML model training slow?**
- Reduce sequence length (LSTM)
- Use fewer features (clustering)
- Close other applications

**Alerts not showing?**
- Ensure "Enable Pollution Alerts" is checked
- Verify AQI threshold is appropriate
- Check if auto-refresh is enabled

**Data not updating?**
- Click "🔄 Refresh Now" button
- Check "Last Update" time
- Verify auto-refresh is enabled

---

## Keyboard Shortcuts

- **Ctrl/Cmd + R**: Refresh page
- **Ctrl/Cmd + F**: Search in page
- **Ctrl/Cmd + +/-**: Zoom in/out
- **Esc**: Close popups/modals

---

## Getting Help

- **Documentation**: Check other docs in `/docs` folder
- **Issues**: Report bugs on GitHub
- **Questions**: Open a discussion on GitHub
- **Updates**: Check README for latest features

---

**Happy Monitoring! 🌍**
