# 🚨 Email Alert System - Setup & Testing Guide

## Overview

This guide walks you through setting up and testing the TerraPulse AI email alert system that sends notifications when city AQI exceeds 200 (Unhealthy level).

---

## 📋 Prerequisites

- PostgreSQL database running on `localhost:5432`
- Python 3.11+ with backend dependencies installed
- Gmail account for sending alerts
- Backend server running on `localhost:8000`

---

## 🔧 Step 1: Configure Gmail SMTP

### Get Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Select **Security** from the left menu
3. Enable **2-Step Verification** (if not already enabled)
4. Go back to Security → **App passwords**
5. Click **App passwords**
6. Select app: **Mail**
7. Select device: **Other (Custom name)** → Enter "TerraPulse"
8. Click **Generate**
9. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)
10. Remove spaces: `abcdefghijklmnop`

### Update .env File

Edit `backend/.env`:

```bash
# Replace with YOUR Gmail address
SMTP_USER=your-email@gmail.com

# Replace with YOUR App Password (no spaces)
SMTP_PASSWORD=abcdefghijklmnop

# Email that receives alerts
ALERT_EMAIL=admin@terrapulse.com

# AQI threshold for alerts (default: 200)
AQI_ALERT_THRESHOLD=200
```

---

## 🧪 Step 2: Run Test Script

### Option A: PowerShell (Windows)

```powershell
cd D:\Projects\terrapulse-ai\backend
python test_alerts.py
```

### Option B: Bash (Linux/Mac/WSL)

```bash
cd /d/Projects/terrapulse-ai/backend
python test_alerts.py
```

### Expected Output

```
============================================================
           🧪 TerraPulse AI - Email Alert Test Suite
============================================================

ℹ️  Timestamp: 2026-04-19 10:30:45
ℹ️  Database: localhost:5432/terrapulse_db

Test: 1. Database Connection
ℹ️  Connecting to: localhost:5432/terrapulse_db
✅ 1. Database Connection - PASSED

Test: 2. .env File Exists
✅ .env file found at D:\Projects\terrapulse-ai\backend\.env
✅ 2. .env File Exists - PASSED

Test: 3. AlertHistory Table Exists
ℹ️  Checking for AlertHistory table...
ℹ️  Table 'alert_history' found
✅ 3. AlertHistory Table Exists - PASSED

Test: 4. Email Configuration
ℹ️  Checking email configuration...
ℹ️  SMTP Host: smtp.gmail.com
ℹ️  SMTP Port: 587
ℹ️  SMTP User: your-email@gmail.com
ℹ️  Alert Email: admin@terrapulse.com
ℹ️  AQI Threshold: 200
✅ 4. Email Configuration - PASSED

Test: 5. Send Test Email
ℹ️  Sending test email to admin@terrapulse.com...
✅ Alert email sent to admin@terrapulse.com for Test City (AQI: 250)
✅ Email sent successfully to admin@terrapulse.com
✅ 5. Send Test Email - PASSED

Test: 6. Log Alert to Database
ℹ️  Creating test alert record in database...
✅ Alert record created with ID: 1
✅ Alert record retrieved: City=Test City, AQI=250
✅ 6. Log Alert to Database - PASSED

============================================================
                      📊 Test Summary
============================================================
Passed: 6
Failed: 0
Total:  6

✅ 🎉 All tests passed! Email alert system is ready.
```

---

## 🌐 Step 3: Test API Endpoint

### Start Backend Server

```powershell
cd D:\Projects\terrapulse-ai\backend
python -m uvicorn app.main:app --reload
```

### Test Alert Endpoint (No Auth Required)

**PowerShell:**

```powershell
$body = @{
    city = "Ahmedabad"
    aqi_value = 250
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/alerts/test" -Method Post -Body $body -ContentType "application/json"
```

**cURL (Bash):**

```bash
curl -X POST http://localhost:8000/api/alerts/test \
  -H "Content-Type: application/json" \
  -d '{"city": "Ahmedabad", "aqi_value": 250}'
```

**Expected Response:**

```json
{
  "alert_triggered": true,
  "email_sent": true,
  "city": "Ahmedabad",
  "aqi_value": 250,
  "threshold": 200,
  "message": "Test alert processed. Email SENT to admin@terrapulse.com"
}
```

---

## 📧 Step 4: Verify Email Received

Check the inbox of `ALERT_EMAIL` (default: `admin@terrapulse.com`).

### Expected Email Content

**Subject:** 🚨 Air Quality Alert: Ahmedabad - AQI 250

**Body:**

> ⚠️ **Unhealthy Air Quality Alert**
>
> - **City:** Ahmedabad
> - **AQI Level:** 250
> - **Time:** 2026-04-19 10:30:45
>
> **Health Recommendations:**
> - Avoid outdoor activities
> - Keep windows closed
> - Use air purifiers indoors
> - Wear N95 masks if going outside
> - Monitor symptoms if you have respiratory conditions

---

## 🖥️ Step 5: Test Frontend Alert Display

### Start Frontend

```powershell
cd D:\Projects\terrapulse-ai\frontend
npm run dev
```

### Access Dashboard

Open browser: http://localhost:3000

### Expected Behavior

When any city has AQI > 200, a **red pulsing alert banner** appears at the top of the Dashboard showing:

- 🚨 Unhealthy Air Quality Alert header
- List of affected cities with their AQI values
- Health safety recommendations

---

## 🔍 Troubleshooting

### Problem: "SMTP Authentication Failed"

**Solution:**
1. Make sure you're using an **App Password**, not your regular Gmail password
2. Ensure 2-Step Verification is enabled on your Google Account
3. Check for typos in the email address

### Problem: "Connection Refused"

**Solution:**
```powershell
# Check if PostgreSQL is running
Get-Service postgresql*

# Start if stopped
Start-Service postgresql-x64-15
```

### Problem: "Table alert_history does not exist"

**Solution:**

The table is created automatically on backend startup. If it doesn't exist:

```powershell
# Run the test script (creates tables automatically)
python test_alerts.py
```

Or manually create it:

```python
from app.db.database import engine, Base
from app.models.models import AlertHistory

Base.metadata.create_all(bind=engine)
```

### Problem: Email not received

**Solution:**
1. Check spam/junk folder
2. Verify SMTP credentials in `.env`
3. Test with a different recipient email
4. Check Gmail sending limits (500 emails/day)

---

## 📊 API Endpoints Reference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/alerts/test` | POST | ❌ | Send test alert (no auth) |
| `/api/alerts/check` | POST | ✅ | Check & send alert for city |
| `/api/alerts/check-all` | POST | ✅ | Check multiple cities |
| `/api/alerts/history` | GET | ✅ | Get alert history (7 days) |
| `/api/alerts/history/{city}` | GET | ✅ | Get city-specific history |

---

## 🎯 Quick Command Reference

### Run All Tests

```powershell
cd D:\Projects\terrapulse-ai\backend
python test_alerts.py
```

### Start Backend

```powershell
cd D:\Projects\terrapulse-ai\backend
python -m uvicorn app.main:app --reload
```

### Test Alert API

```powershell
$body = @{city="Ahmedabad"; aqi_value=250} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/alerts/test" -Method Post -Body $body -ContentType "application/json"
```

### Check Database

```powershell
# Connect to PostgreSQL
psql -U postgres -d terrapulse_db

# Query alert history
SELECT * FROM alert_history ORDER BY last_alert_time DESC LIMIT 10;
```

---

## ✅ Verification Checklist

- [ ] `.env` file configured with Gmail credentials
- [ ] Test script passes all 6 tests
- [ ] Backend starts without errors
- [ ] AlertHistory table exists in database
- [ ] Test email received at admin@terrapulse.com
- [ ] API endpoint `/api/alerts/test` returns success
- [ ] Frontend Dashboard shows red alert banner when AQI > 200
- [ ] Alert logged to database after sending

---

## 📝 Files Modified/Created

| File | Purpose |
|------|---------|
| `backend/app/models/models.py` | Added `AlertHistory` model |
| `backend/app/core/config.py` | Added email configuration |
| `backend/app/core/email.py` | Email sending service |
| `backend/app/api/endpoints/alerts.py` | Alert endpoints (+ test endpoint) |
| `backend/app/api/endpoints/data.py` | Auto-alert on data save |
| `backend/app/main.py` | Registered alerts router |
| `backend/.env` | Email configuration |
| `backend/test_alerts.py` | Test script |
| `frontend/src/pages/Dashboard.tsx` | Alert banner UI |

---

**🎉 Your email alert system is now fully operational!**
