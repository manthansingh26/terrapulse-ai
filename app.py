import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(page_title="TerraPulse AI", layout="wide")

# Thin and sleek style tweaks
st.markdown("""
<style>
    :root {
        --bg: #030712;
        --card-bg: rgba(10, 20, 40, 0.75);
        --panel-bg: rgba(5, 12, 30, 0.85);
        --accent: #00d2ff;
        --accent2: #007bff;
    }

    body {
        background: linear-gradient(140deg, #02060f, #071b3a 60%, #030a18 100%);
    }

    .main .block-container {
        max-width: 1320px;
        padding: 0.7rem 2rem 1.5rem;
        background: transparent;
    }

    .css-1d391kg .element-container,
    .css-18e3th9 {
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.45);
        border: 1px solid rgba(90, 170, 255, 0.24);
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border-radius: 18px;
    }

    .css-1v3fvcr {
        background: var(--panel-bg) !important;
        border-radius: 18px !important;
        border: 1px solid rgba(140, 150, 220, 0.30) !important;
    }

    .stSidebar {
        background: linear-gradient(170deg, #040814, #07172c 90%);
        border-right: 1px solid rgba(100, 150, 255, 0.14);
    }

    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #f3f9ff;
        font-family: 'Poppins', 'Segoe UI', sans-serif;
        font-weight: 800;
        letter-spacing: 0.02em;
    }

    .stMetric > div {
        border-radius: 14px;
        background: rgba(20, 40, 80, 0.6);
        border: 1px solid rgba(0, 220, 255, 0.22);
        transition: transform 0.24s ease, box-shadow 0.24s ease;
    }

    .stMetric:hover > div {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.52);
    }

    .stMetric .css-1nw1y2g {  /* metric value */
        color: #e7f5ff;
    }

    button[kind='primary'], .stButton>button {
        background: linear-gradient(120deg, #0078ff, #00f7ff);
        color: #02162f;
        font-weight: 700;
        border: none;
        box-shadow: 0 8px 20px rgba(0, 110, 255, 0.4);
        transition: transform 0.2s ease,
                    box-shadow 0.2s ease;
    }

    button[kind='primary']:hover, .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 26px rgba(0, 160, 255, 0.55);
    }

    .css-1q1n0ol {
        color: #98c5ff !important;
    }

    .stTabs [role='tab'] {
        border-radius: 12px;
        background: rgba(30, 60, 100, 0.35);
        border: 1px solid rgba(150, 190, 255, .18);
        color: #d7e9ff;
        margin-right: 6px;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected='true'] {
        background: linear-gradient(90deg, rgba(0, 188, 255, 0.7), rgba(0, 128, 255, 0.9));
        box-shadow: 0 8px 16px rgba(0, 112, 255, 0.45);
        color: #fff;
        border: 1px solid rgba(0, 255, 255, 0.35);
    }

    @keyframes glow-title {
        0% { text-shadow: 0 0 8px rgba(0,225,255,0.66), 0 0 18px rgba(0,130,255,0.4);}   
        50% { text-shadow: 0 0 14px rgba(0,255,255,0.86), 0 0 24px rgba(0,92,222,0.58);} 
        100% { text-shadow: 0 0 8px rgba(0,225,255,0.66), 0 0 18px rgba(0,130,255,0.4);}   
    }

    .css-1d391kg h1 {
        animation: glow-title 2.5s ease-in-out infinite;
    }

    .stDataFrame .dataframe {
        background-color: rgba(5,10,30,0.7) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(64, 120, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.title("🌍 TerraPulse AI")
st.subheader("AI-powered Earth Intelligence Dashboard")
st.write("Live environmental monitoring dashboard")

st.sidebar.title("Control Panel")
location = st.sidebar.selectbox("Select Location", ["Ahmedabad", "Surat", "Mumbai"])
days = st.sidebar.slider("Number of Days", 5, 30, 7)

temperature = np.random.randint(20, 40, days)
humidity = np.random.randint(40, 90, days)

sample_data = pd.DataFrame({
    "Day": list(range(1, days + 1)),
    "Temperature": temperature,
    "Humidity": humidity
})

col1, col2, col3 = st.columns(3)
col1.metric("📍 Location", location)
col2.metric("🌡 Avg Temperature", f"{sample_data['Temperature'].mean():.1f} °C")
col3.metric("💧 Avg Humidity", f"{sample_data['Humidity'].mean():.1f} %")

st.divider()

# Main Dashboard Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 CSV Analysis", "🖼️ Image Analysis"])

# ============ TAB 1: DASHBOARD ============
with tab1:
    st.subheader("Environmental Metrics")
    
    # Display data table
    st.write("Real-time environmental data:")
    st.dataframe(sample_data, use_container_width=True)
    
    # Chart
    st.line_chart(sample_data.set_index("Day")[["Temperature", "Humidity"]])

# ============ TAB 2: CSV ANALYSIS ============
with tab2:
    st.subheader("Upload & Analyze CSV Data")
    
    uploaded_csv = st.file_uploader("📂 Upload a CSV file", type=["csv"], key="csv_uploader")
    if uploaded_csv is not None:
        df = pd.read_csv(uploaded_csv)
        st.success("✓ CSV uploaded successfully")
        st.dataframe(df, use_container_width=True)
        
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
        
        # Download Report Section
        st.subheader("📥 Download Analysis Report")
        
        # Create analysis report
        report_data = {
            "Generated At": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total Rows": df.shape[0],
            "Total Columns": df.shape[1],
            "Data Quality %": f"{data_quality:.1f}%",
            "Numeric Columns": len(df.select_dtypes(include=np.number).columns),
            "Text Columns": len(df.select_dtypes(include='object').columns),
            "Missing Values": missing_cells
        }
        
        # Convert to CSV format
        report_str = "ANALYSIS REPORT\n"
        report_str += "=" * 40 + "\n\n"
        for key, value in report_data.items():
            report_str += f"{key}: {value}\n"
        report_str += "\n" + "=" * 40 + "\n"
        report_str += f"\nOriginal Data:\n{df.to_csv(index=False)}"
        
        # Download button
        st.download_button(
            label="⬇️ Download Analysis Report (CSV)",
            data=report_str,
            file_name=f"terrapulse_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
        st.success("✓ Report ready to download!")
        
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
            
            # ML Predictions Section
            st.subheader("🤖 AI Predictions & Anomaly Detection")
            
            # Trend prediction
            if len(df[selected_col]) >= 3:
                from sklearn.linear_model import LinearRegression
                
                # Prepare data
                X = np.arange(len(df[selected_col])).reshape(-1, 1)
                y = df[selected_col].values
                
                # Train simple linear regression
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict next 5 points
                future_X = np.arange(len(df[selected_col]), len(df[selected_col]) + 5).reshape(-1, 1)
                predictions = model.predict(future_X)
                
                st.write(f"**Trend Prediction (Next 5 values):**")
                pred_df = pd.DataFrame({
                    "Step": range(1, 6),
                    "Predicted Value": predictions.round(2)
                })
                st.dataframe(pred_df)
                
                # Anomaly Detection
                st.write(f"**Anomaly Detection:**")
                mean_val = y.mean()
                std_val = y.std()
                threshold = 2.5  # 2.5 standard deviations
                
                anomalies = np.abs(y - mean_val) > (threshold * std_val)
                anomaly_count = anomalies.sum()
                
                col1, col2 = st.columns(2)
                col1.metric("🔴 Anomalies Detected", anomaly_count)
                col2.metric("📊 Anomaly %", f"{(anomaly_count/len(y)*100):.1f}%")
                
                if anomaly_count > 0:
                    st.warning(f"⚠️ Found {anomaly_count} anomalous values (>2.5σ from mean)")
                    anomaly_indices = np.where(anomalies)[0]
                    anomaly_df = pd.DataFrame({
                        "Index": anomaly_indices,
                        "Value": y[anomalies],
                        "Deviation": (y[anomalies] - mean_val).round(2)
                    })
                    st.dataframe(anomaly_df)
                else:
                    st.success("✓ No anomalies detected - data looks clean!")
        
        else:
            st.warning("No numeric column available for analysis.")

# ============ TAB 3: IMAGE ANALYSIS ============
with tab3:
    st.subheader("Upload & Analyze Images")
    
    uploaded_image = st.file_uploader("📂 Upload an image", type=["png", "jpg", "jpeg"], key="image_uploader")
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.success("✓ Image uploaded successfully")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Image Metrics Cards
        st.subheader("📊 Image Properties")
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("📏 Resolution", f"{image.size[0]}×{image.size[1]}")
        
        file_size_kb = len(uploaded_image.getvalue()) / 1024
        col2.metric("📁 File Size", f"{file_size_kb:.1f} KB")
        
        col3.metric("🎨 Format", image.format if image.format else "Unknown")
        
        col4.metric("🖼️ Mode", image.mode)
        
        # Image Analysis
        st.subheader("🎨 Color & Brightness Analysis")
        
        img_array = np.array(image)
        
        # Calculate brightness
        if len(img_array.shape) == 3:
            brightness = img_array.mean()
        else:
            brightness = img_array.mean()
        
        st.metric("🌞 Average Brightness", f"{brightness:.0f}/255")
        
        # Color Channel Analysis
        if image.mode == 'RGB' or image.mode == 'RGBA':
            col1, col2, col3 = st.columns(3)
            
            r_avg = img_array[:,:,0].mean()
            g_avg = img_array[:,:,1].mean()
            b_avg = img_array[:,:,2].mean()
            
            col1.metric("🔴 Red Channel", f"{r_avg:.0f}")
            col2.metric("🟢 Green Channel", f"{g_avg:.0f}")
            col3.metric("🔵 Blue Channel", f"{b_avg:.0f}")
            
            # Create a simple color distribution chart
            st.write("Color Channel Distribution:")
            color_data = pd.DataFrame({
                "Channel": ["Red", "Green", "Blue"],
                "Average Value": [r_avg, g_avg, b_avg]
            })
            st.bar_chart(color_data.set_index("Channel"))
        
        elif image.mode == 'L':
            st.info("📉 Grayscale image detected - single tone channel only")
        
        # Image Quality Score
        st.subheader("✅ Image Quality Assessment")
        
        contrast = img_array.std()
        quality_score = min(100, (contrast / 256) * 100)
        
        st.metric("📈 Contrast Score", f"{quality_score:.1f}%")
        st.progress(quality_score / 100, text=f"Quality: {quality_score:.0f}%")
        
        # Additional info
        with st.expander("📋 Detailed Image Info"):
            st.write(f"**Filename:** {uploaded_image.name}")
            st.write(f"**Dimensions:** {image.size[0]} × {image.size[1]} pixels")
            st.write(f"**Total Pixels:** {image.size[0] * image.size[1]:,}")
            st.write(f"**File Size:** {file_size_kb:.2f} KB")
            st.write(f"**Image Mode:** {image.mode}")
            st.write(f"**Average Brightness:** {brightness:.2f}/255")
            st.write(f"**Contrast (Std Dev):** {contrast:.2f}")