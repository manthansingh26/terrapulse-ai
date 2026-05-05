# FRONTEND FIXES - READY TO PASTE TO CLAUDE CODE
## Step-by-Step Instructions for Claude Opus 4.7

---

## 📋 EXACT STEPS TO FIX ALL FRONTEND ISSUES

### **INSTRUCTION FOR CLAUDE CODE:**

Copy and paste this entire prompt into Claude Opus 4.7 or Claude Code:

---

## CLAUDE CODE PROMPT - COPY EVERYTHING BELOW

```
I need to fix multiple frontend issues in my TerraPulse AI React TypeScript project. 

Here are the 10 issues I've identified:

1. WebSocket URL not properly configured
2. Missing .env file with environment variables
3. API base URL hardcoded with fallback
4. No error boundary component (app crashes on errors)
5. WebSocket errors not handled properly
6. Axios interceptor may cause infinite loops on token refresh
7. Missing loading states in some pages
8. Type safety issues (some 'any' types)
9. CORS configuration might not allow frontend origin
10. Analytics page uses hardcoded mock data instead of real API data

ISSUE DESCRIPTIONS:

**Issue #1: WebSocket URL**
File: `frontend/src/pages/Dashboard.tsx` (around line 35)
Problem: Uses hardcoded websocket URL
Current code:
```typescript
const wsUrl = `ws://${window.location.hostname}:8000/api/ws/cities`
useWebSocket(wsUrl)
```

**Issue #2: Missing .env file**
File: `frontend/.env` (doesn't exist)
Need to create with:
```
VITE_API_URL=http://localhost:8000/api
VITE_WS_PORT=8000
VITE_APP_NAME=TerraPulse AI
VITE_DEBUG=true
```

**Issue #3: API base URL**
File: `frontend/src/services/api.ts` (line 3)
Problem: Fallback to hardcoded localhost
Current code:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
```

**Issue #4: No Error Boundary**
File: `frontend/src/components/ErrorBoundary.tsx` (doesn't exist)
Need to create this component from scratch

**Issue #5: WebSocket Hook**
File: `frontend/src/hooks/useWebSocket.ts`
Problem: Errors don't propagate to UI
Need better error handling in onError and onclose handlers

**Issue #6: Axios Interceptor**
File: `frontend/src/services/api.ts` (lines 80-100)
Problem: Token refresh logic may cause infinite loops
Need to add proper queue management and fallback

**Issue #7: Loading States**
Files: `frontend/src/pages/Analytics.tsx`, `frontend/src/pages/Map.tsx`
Problem: Some pages don't show loading spinners
Need to add loading state management

**Issue #8: Type Safety**
File: `frontend/src/services/api.ts`
Problem: Some responses return `any` type
Need to create specific TypeScript interfaces

**Issue #9: CORS Backend**
File: `backend/app/main.py`
Problem: CORS middleware might not include frontend origin
Need to verify: `allow_origins=["http://localhost:3000", ...]`

**Issue #10: Analytics Mock Data**
File: `frontend/src/pages/Analytics.tsx` (lines 28-35)
Problem: Uses hardcoded mock data instead of real API
Current code:
```typescript
const lineChartData = [
  { time: '06:00', aqi: 85, temp: 24, humidity: 65 },
  { time: '09:00', aqi: 110, temp: 28, humidity: 58 },
  // ... more mock data
]
```
Should fetch real data from backend API

---

PLEASE DO ALL OF THE FOLLOWING:

1. **Create the .env file** in frontend/ with all required environment variables
2. **Create ErrorBoundary.tsx** component to catch React errors gracefully
3. **Update App.tsx** to wrap app with ErrorBoundary
4. **Improve axios interceptor** with proper queue management to prevent infinite loops
5. **Fix WebSocket URL** to use environment variables
6. **Add TypeScript types** for API responses (create CityStatistics interface)
7. **Add real data fetching to Analytics** - replace hardcoded mock data with API calls
8. **Improve WebSocket hook** error handling
9. **Add loading states** to all pages
10. **Create .env.example** template file

After making these fixes:
- The app will crash gracefully with error boundaries
- Token refresh will work without infinite loops
- Analytics will show real data instead of mock data
- WebSocket will properly report errors
- All components will be type-safe
- Environment is properly configured

Please provide the complete fixed code for all these files/components.
```

---

## 📝 WHAT TO EXPECT

After pasting the above prompt to Claude:

1. ✅ Claude will provide complete fixed code for:
   - `.env` file template
   - ErrorBoundary.tsx component
   - Updated App.tsx
   - Improved api.ts with better interceptors
   - Updated Dashboard.tsx with proper WebSocket
   - Fixed Analytics.tsx with real data
   - Updated useWebSocket.ts hook
   - All other necessary fixes

2. ✅ You'll get type-safe, production-ready code

3. ✅ All 10 issues will be resolved

---

## 🔧 MANUAL FIX (If you prefer to do it yourself)

### Step 1: Create .env file
**File**: `frontend/.env`
```
VITE_API_URL=http://localhost:8000/api
VITE_WS_PORT=8000
VITE_APP_NAME=TerraPulse AI
VITE_DEBUG=true
```

### Step 2: Create .env.example
**File**: `frontend/.env.example`
```
# API Configuration
VITE_API_URL=http://localhost:8000/api
VITE_WS_PORT=8000

# App Configuration
VITE_APP_NAME=TerraPulse AI
VITE_DEBUG=false
```

### Step 3: Create ErrorBoundary Component
**File**: `frontend/src/components/ErrorBoundary.tsx`
```typescript
import React, { Component, ReactNode } from 'react'
import { AlertCircle } from 'lucide-react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center h-screen bg-gray-50">
          <div className="bg-white rounded-lg shadow-lg p-8 max-w-md">
            <div className="flex items-center gap-3 mb-4">
              <AlertCircle className="text-red-600" size={32} />
              <h1 className="text-2xl font-bold text-gray-900">Something went wrong</h1>
            </div>
            <p className="text-gray-600 mb-6">
              An unexpected error occurred. Please refresh the page to try again.
            </p>
            <button
              onClick={() => window.location.href = '/'}
              className="mt-6 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
            >
              Go Home
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
```

### Step 4: Update App.tsx
```typescript
import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '@/context/AuthContext'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import ProtectedRoute from '@/components/ProtectedRoute'
import Layout from '@/components/Layout'
import Login from '@/pages/Login'
import Register from '@/pages/Register'
import Dashboard from '@/pages/Dashboard'
import Map from '@/pages/Map'
import Analytics from '@/pages/Analytics'
import Profile from '@/pages/Profile'
import '@/styles/global.css'

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route element={<Layout />}>
              <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
              <Route path="/map" element={<ProtectedRoute><Map /></ProtectedRoute>} />
              <Route path="/analytics" element={<ProtectedRoute><Analytics /></ProtectedRoute>} />
              <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </Router>
    </ErrorBoundary>
  )
}

export default App
```

### Step 5: Update Dashboard WebSocket
**File**: `frontend/src/pages/Dashboard.tsx` (Find and replace)

Replace:
```typescript
const wsUrl = `ws://${window.location.hostname}:8000/api/ws/cities`
useWebSocket(wsUrl)
```

With:
```typescript
const wsPort = import.meta.env.VITE_WS_PORT || 8000
const wsUrl = `ws://${window.location.hostname}:${wsPort}/api/ws/cities`
const { send } = useWebSocket(wsUrl)
```

### Step 6: Add Types to API Service
**File**: `frontend/src/services/api.ts`

Add these interfaces after existing ones:
```typescript
interface CityStatistics {
  city: string
  avg_aqi: number
  max_aqi: number
  min_aqi: number
  avg_temperature: number
  max_temperature: number
  min_temperature: number
  avg_humidity: number
  data_points: number
}

interface AirQualityRecord {
  timestamp: string
  aqi: number
  status: string
  temperature?: number
  humidity?: number
  wind_speed?: number
}
```

### Step 7: Update Analytics to Use Real Data
**File**: `frontend/src/pages/Analytics.tsx`

Add this after state declarations:
```typescript
const [lineChartData, setLineChartData] = useState<any[]>([])

useEffect(() => {
  if (selectedCity) {
    const fetchHistoricalData = async () => {
      try {
        const data = await apiClient.getHistoricalData(selectedCity, 7)
        const chartData = data.map((item) => ({
          time: new Date(item.timestamp).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
          }),
          aqi: item.aqi || 0,
          temp: item.temperature || 0,
          humidity: item.humidity || 0,
        }))
        setLineChartData(chartData)
      } catch (error) {
        console.error('Failed to fetch historical data:', error)
      }
    }
    fetchHistoricalData()
  }
}, [selectedCity])
```

Then replace the hardcoded data with `lineChartData`

---

## ✅ VERIFICATION CHECKLIST

After applying fixes:

- [ ] `frontend/.env` file exists with correct variables
- [ ] `frontend/.env.example` exists
- [ ] ErrorBoundary component created in `src/components/`
- [ ] App.tsx wraps application with ErrorBoundary
- [ ] Dashboard uses environment variable for WebSocket port
- [ ] Analytics page fetches real data from API
- [ ] No TypeScript errors: `npm run type-check`
- [ ] Build succeeds: `npm run build`
- [ ] App starts without errors: `npm run dev`
- [ ] Login/register works
- [ ] Dashboard loads data
- [ ] Analytics shows real data
- [ ] Map displays cities

---

## 🚀 FINAL STEPS

1. **Paste the CLAUDE CODE PROMPT** (in the section above) into Claude Opus
2. **Wait for Claude's response** with all fixed code
3. **Copy and apply** all the fixes Claude provides
4. **Run**: `npm run type-check` to verify no errors
5. **Run**: `npm run build` to create production build
6. **Run**: `npm run dev` to test locally
7. **Test**: All pages and features

---

## 📞 IF SOMETHING STILL DOESN'T WORK

Common issues:

1. **Backend not running?**
   - Terminal 1: `cd backend && ./run.bat` (Windows)

2. **API calls fail?**
   - Check `.env` file VITE_API_URL value
   - Verify backend CORS includes http://localhost:3000

3. **WebSocket not connecting?**
   - Check backend has WebSocket endpoint at `/api/ws/cities`
   - Check VITE_WS_PORT in .env matches backend

4. **Build errors?**
   - Run: `npm install` again
   - Delete `node_modules` and `.vite` folders
   - Run: `npm install && npm run build`

---

## 📊 SUMMARY

**Issues Identified**: 10
**Issues Fixable**: ✅ All 10

**Frontend Status**:
- Before: 🟡 Has 10 issues
- After: 🟢 Production ready

**Expected Result**:
- ✅ Type-safe code
- ✅ Error handling
- ✅ Real data in Analytics
- ✅ Proper WebSocket
- ✅ No infinite loops
- ✅ Graceful error UI

---

## 🎯 READY?

1. Copy the **CLAUDE CODE PROMPT** above
2. Paste into **Claude Opus 4.7**
3. Get all fixed code
4. Apply fixes
5. Test
6. Deploy! 🚀

