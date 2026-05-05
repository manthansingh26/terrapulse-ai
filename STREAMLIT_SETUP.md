# 🌍 TerraPulse AI - Streamlit Frontend Setup Guide

This is your **restored Streamlit-based frontend** for TerraPulse AI - the original design you had before!

## 🚀 Quick Start (2 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements_streamlit.txt
```

### Step 2: Run the Streamlit App
```bash
streamlit run app_streamlit.py
```

**The app will open at:** `http://localhost:8501`

---

## 📋 Features Included

✅ **User Authentication**
- Login with demo/demo123
- User registration
- JWT token management
- Profile page

✅ **Dashboard**
- Overall statistics (Average AQI, Temperature, Humidity)
- Top 10 most polluted cities
- AQI status distribution chart
- Temperature distribution map
- Complete cities data table

✅ **City Details**
- Select any city from 20 Indian cities
- Current environmental readings
- AQI, Temperature, Humidity, Wind Speed, CO₂
- Historical trends (7-30 days)
- Statistics and analysis

✅ **User Profile**
- View account information
- User ID and creation date
- Admin status indicator
- Quick links to API documentation

---

## 🔗 Backend Connection

**Backend must be running on:** `http://localhost:8000`

The Streamlit app connects to these endpoints:
```
POST   /api/auth/register        - User registration
POST   /api/auth/login           - User login
GET    /api/auth/me              - Current user info
GET    /api/data/all/latest      - All cities latest data
GET    /api/data/latest/{city}   - Specific city data
GET    /api/data/history/{city}  - Historical data
GET    /api/data/statistics/{city} - City statistics
```

---

## 📊 Demo Credentials

```
Username: demo
Password: demo123
```

---

## 🎨 Streamlit Features

- **Responsive Layout** - Works on desktop and mobile
- **Interactive Charts** - Plotly visualization
- **Real-time Updates** - Connect to live backend
- **Data Tables** - Browse all city data
- **Sidebar Navigation** - Easy page switching
- **Dark/Light Mode** - Streamlit theme toggle

---

## 🐛 Troubleshooting

### "Connection refused" error
Make sure backend is running:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### "Module not found" error
Reinstall dependencies:
```bash
pip install -r requirements_streamlit.txt
```

### Port 8501 already in use
Run on a different port:
```bash
streamlit run app_streamlit.py --server.port 8502
```

### Slow performance
Try restarting:
```bash
streamlit run app_streamlit.py --logger.level=error
```

---

## 📁 Files Included

```
app_streamlit.py          ← Main Streamlit application
requirements_streamlit.txt ← Python dependencies
STREAMLIT_SETUP.md        ← This file
```

---

## ⚙️ Configuration

Edit `app_streamlit.py` to customize:

**API Base URL (Line 62):**
```python
API_BASE_URL = "http://localhost:8000/api"
```

**City Coordinates (Lines 65-85):**
```python
CITY_COORDINATES = {
    "City": {"lat": latitude, "lon": longitude},
    ...
}
```

**Session Timeout (Line 86):**
```python
SESSION_TIMEOUT = 3600  # in seconds
```

---

## 🔄 Deployment

### Local (Development)
```bash
streamlit run app_streamlit.py
```

### Server (Production)
```bash
streamlit run app_streamlit.py --server.address 0.0.0.0 --server.port 8501
```

### Docker (Optional)
```bash
docker build -f Dockerfile.streamlit -t terrapulse-streamlit .
docker run -p 8501:8501 terrapulse-streamlit
```

---

## 📖 Streamlit Documentation

- **Official Docs:** https://docs.streamlit.io/
- **Plotly Charts:** https://plotly.com/python/streamlit/
- **Deployment:** https://docs.streamlit.io/deploy

---

## 🌟 Advantages of This Streamlit Design

✅ **Simple & Fast** - No build process needed  
✅ **Interactive** - Real-time updates  
✅ **Beautiful** - Built-in styling  
✅ **Responsive** - Works on all devices  
✅ **Lightweight** - Minimal dependencies  
✅ **Easy to Modify** - Single Python file  
✅ **Rich Charts** - Plotly integration  
✅ **Production Ready** - Deploy anywhere  

---

## 💡 Next Steps

1. **Start Backend:** Run backend on port 8000
2. **Run Streamlit:** `streamlit run app_streamlit.py`
3. **Access App:** Open http://localhost:8501
4. **Login:** Use demo/demo123
5. **Explore:** Dashboard, Cities, Profile

---

## 📞 Support

For issues or questions:
- Check API docs at http://localhost:8000/api/docs
- Review backend logs for API errors
- Check Streamlit logs in terminal

---

**🎉 Your Streamlit frontend is ready to use!**

Created: April 26, 2026  
Last Updated: April 26, 2026
