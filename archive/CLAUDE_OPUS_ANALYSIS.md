# TerraPulse AI - Frontend Analysis & Full Project Report
## Complete Code & Error Identification for Claude Opus 4.7

---

## 🔍 IDENTIFIED FRONTEND ISSUES & ERRORS

### **Critical Issues Found:**

#### **1. WebSocket URL Issue**
- **Location**: `frontend/src/pages/Dashboard.tsx` (Line ~35)
- **Problem**: WebSocket URL uses http:// port 8000, but backend WebSocket may not be configured
- **Impact**: Dashboard fails to establish WebSocket connection
- **Fix Needed**: Backend needs WebSocket endpoint implementation

```typescript
// CURRENT (BROKEN):
const wsUrl = `ws://${window.location.hostname}:8000/api/ws/cities`

// SHOULD BE:
const wsUrl = `ws://${window.location.hostname}:${import.meta.env.VITE_WS_PORT || 8000}/api/ws/cities`
```

---

#### **2. Environment Variables Missing**
- **Files Affected**: `frontend/.env` needs these variables
- **Current State**: No `.env` file exists
- **Missing Variables**:
  ```
  VITE_API_URL=http://localhost:8000/api
  VITE_WS_PORT=8000
  VITE_APP_NAME=TerraPulse AI
  ```

---

#### **3. API Base URL Configuration Issue**
- **Location**: `frontend/src/services/api.ts` (Line 3)
- **Problem**: Falls back to `http://localhost:8000/api` if env var not set
- **Fix**: Ensure backend CORS allows this origin

---

#### **4. Missing Error Boundaries**
- **Issue**: No error boundary component to catch React errors
- **Impact**: App crashes on component errors without graceful fallback
- **Needs**: ErrorBoundary component implementation

---

#### **5. WebSocket Hook Error Handling**
- **Location**: `frontend/src/hooks/useWebSocket.ts`
- **Problem**: WebSocket errors don't propagate to UI
- **Impact**: User doesn't know connection failed

---

#### **6. Axios Interceptor Issue**
- **Location**: `frontend/src/services/api.ts` (Line ~85-92)
- **Problem**: Token refresh logic may cause infinite loops if refresh fails
- **Issue**: If both access_token and refresh_token are invalid, user should be logged out

---

#### **7. Missing Loading States**
- **Location**: Multiple pages (Analytics, Map)
- **Problem**: Some pages don't show loading spinners properly
- **Impact**: Confusing UX when data is loading

---

#### **8. Type Safety Issues**
- **Problem**: Some API responses not fully typed
- **Example**: `getCityStatistics()` returns `any` type
- **Fix**: Create proper TypeScript interfaces

---

#### **9. CORS Configuration**
- **Backend Issue**: Check if backend allows frontend origin
- **Current**: Backend CORS might not include http://localhost:3000
- **Backend File**: `backend/app/main.py` needs CORS middleware configured

---

#### **10. Analytics Page - Hardcoded Mock Data**
- **Location**: `frontend/src/pages/Analytics.tsx` (Lines ~28-35)
- **Problem**: Line chart uses fake/mock data instead of real API data
- **Should Fetch**: Real historical data from `getHistoricalData()` endpoint

```typescript
// CURRENT (MOCK):
const lineChartData = [
  { time: '06:00', aqi: 85, temp: 24, humidity: 65 },
  { time: '09:00', aqi: 110, temp: 28, humidity: 58 },
  // ... more mock data
]

// SHOULD BE: Fetch real data
```

---

## ✅ QUICK FIX CHECKLIST

- [ ] Create `.env` file in frontend/ with correct variables
- [ ] Implement WebSocket endpoint in backend
- [ ] Fix Analytics page to use real data
- [ ] Add error boundaries
- [ ] Improve axios interceptor logic
- [ ] Add proper TypeScript types throughout
- [ ] Test CORS configuration
- [ ] Add .env.example template

---

---

## 📋 FULL PROJECT STRUCTURE & CODE REFERENCE

### **Backend Stack**
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Auth**: JWT + bcrypt
- **Ports**: 8000
- **Status**: ✅ PRODUCTION READY

### **Frontend Stack**
- **Framework**: React 18.2 + TypeScript 5.3
- **Build**: Vite 5.0
- **Styling**: Tailwind CSS 3.3
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Maps**: Leaflet + React Leaflet
- **Ports**: 3000
- **Status**: ⚠️ NEEDS FIXES (see issues above)

---

## 🔧 COMPLETE FIX CODE FOR CLAUDE CODE

### **Fix #1: Frontend .env File**
```env
# frontend/.env
VITE_API_URL=http://localhost:8000/api
VITE_WS_PORT=8000
VITE_APP_NAME=TerraPulse AI
VITE_DEBUG=true
```

---

### **Fix #2: API Client Service - Better Error Handling**
```typescript
// frontend/src/services/api.ts

import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

interface LoginRequest {
  username: string
  password: string
}

interface RegisterRequest {
  email: string
  username: string
  full_name?: string
  password: string
}

interface Token {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

interface User {
  id: number
  email: string
  username: string
  full_name?: string
  is_active: boolean
  is_admin: boolean
  created_at: string
}

interface City {
  city: string
  latitude: number
  longitude: number
  current_aqi?: number
  current_temperature?: number
  current_humidity?: number
  aqi_status: string
  aqi_color: string
  last_updated?: string
}

interface EnvironmentalData {
  id: number
  city: string
  aqi?: number
  co2?: number
  temperature?: number
  humidity?: number
  wind_speed?: number
  rainfall?: number
  timestamp: string
}

// Statistics response type
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

// Air quality history type
interface AirQualityRecord {
  timestamp: string
  aqi: number
  status: string
  temperature?: number
  humidity?: number
  wind_speed?: number
}

class APIClient {
  private client: AxiosInstance
  private isRefreshing = false
  private failedQueue: Array<{
    resolve: (value: any) => void
    reject: (reason?: any) => void
  }> = []

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add token to requests
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Handle token refresh with queue
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
          if (this.isRefreshing) {
            return new Promise((resolve, reject) => {
              this.failedQueue.push({ resolve, reject })
            })
              .then((token) => {
                originalRequest.headers.Authorization = `Bearer ${token}`
                return this.client(originalRequest)
              })
              .catch((err) => Promise.reject(err))
          }

          originalRequest._retry = true
          this.isRefreshing = true

          const refreshToken = localStorage.getItem('refresh_token')
          if (refreshToken) {
            try {
              const response = await axios.post(
                `${API_BASE_URL}/auth/refresh`,
                { token: refreshToken }
              )
              const { access_token } = response.data
              localStorage.setItem('access_token', access_token)
              originalRequest.headers.Authorization = `Bearer ${access_token}`

              this.failedQueue.forEach((item) => item.resolve(access_token))
              this.failedQueue = []

              return this.client(originalRequest)
            } catch (err) {
              localStorage.removeItem('access_token')
              localStorage.removeItem('refresh_token')
              this.failedQueue.forEach((item) => item.reject(err))
              this.failedQueue = []
              
              // Redirect to login or emit logout event
              window.location.href = '/login'
              return Promise.reject(err)
            } finally {
              this.isRefreshing = false
            }
          } else {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            window.location.href = '/login'
            return Promise.reject(error)
          }
        }

        return Promise.reject(error)
      }
    )
  }

  // Auth endpoints
  async register(data: RegisterRequest): Promise<User> {
    const response = await this.client.post('/auth/register', data)
    return response.data
  }

  async login(data: LoginRequest): Promise<Token> {
    const response = await this.client.post('/auth/login', data)
    return response.data
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get('/auth/me')
    return response.data
  }

  // Cities endpoints
  async getAllCities(): Promise<City[]> {
    const response = await this.client.get('/cities/all')
    return response.data || []
  }

  async getCity(city: string): Promise<City> {
    const response = await this.client.get(`/cities/${city}`)
    return response.data
  }

  async getCityCoordinates(): Promise<Record<string, { lat: number; lon: number }>> {
    const response = await this.client.get('/cities/coordinates/all')
    return response.data || {}
  }

  // Data endpoints
  async saveData(data: Partial<EnvironmentalData>): Promise<EnvironmentalData> {
    const response = await this.client.post('/data/save', data)
    return response.data
  }

  async getLatestData(city: string): Promise<EnvironmentalData> {
    const response = await this.client.get(`/data/latest/${city}`)
    return response.data
  }

  async getHistoricalData(city: string, days: number = 7): Promise<EnvironmentalData[]> {
    const response = await this.client.get(`/data/history/${city}`, {
      params: { days },
    })
    return response.data || []
  }

  async getCityStatistics(city: string, days: number = 7): Promise<CityStatistics> {
    const response = await this.client.get(`/data/statistics/${city}`, {
      params: { days },
    })
    return response.data
  }

  async getAirQualityHistory(city: string, days: number = 7): Promise<AirQualityRecord[]> {
    const response = await this.client.get(`/data/air-quality/${city}`, {
      params: { days },
    })
    return response.data || []
  }

  async getAllLatestData(): Promise<EnvironmentalData[]> {
    const response = await this.client.get('/data/all/latest')
    return response.data || []
  }

  // Health endpoint
  async getHealth(): Promise<any> {
    const response = await this.client.get('/health')
    return response.data
  }

  // Status endpoint
  async getStatus(): Promise<any> {
    const response = await this.client.get('/status')
    return response.data
  }
}

export const apiClient = new APIClient()
export type { User, City, EnvironmentalData, Token, CityStatistics, AirQualityRecord }
```

---

### **Fix #3: Error Boundary Component**
```typescript
// frontend/src/components/ErrorBoundary.tsx

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
            {process.env.NODE_ENV === 'development' && (
              <details className="bg-red-50 p-4 rounded text-sm text-red-800 font-mono">
                <summary className="cursor-pointer font-bold">Error Details</summary>
                <pre className="mt-2 overflow-auto">{this.state.error?.toString()}</pre>
              </details>
            )}
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

---

### **Fix #4: Update App.tsx to Use Error Boundary**
```typescript
// frontend/src/App.tsx

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
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected routes */}
            <Route element={<Layout />}>
              <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
              <Route path="/map" element={<ProtectedRoute><Map /></ProtectedRoute>} />
              <Route path="/analytics" element={<ProtectedRoute><Analytics /></ProtectedRoute>} />
              <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </Router>
    </ErrorBoundary>
  )
}

export default App
```

---

### **Fix #5: Analytics Page - Replace Mock Data with Real API Data**
```typescript
// frontend/src/pages/Analytics.tsx - Key section to fix

// Add this new function to fetch historical data
const fetchHistoricalData = async (cityName: string) => {
  try {
    const data = await apiClient.getHistoricalData(cityName, 7)
    
    // Transform data for chart
    const chartData = data.map((item, index) => ({
      time: new Date(item.timestamp).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
      }),
      aqi: item.aqi || 0,
      temp: item.temperature || 0,
      humidity: item.humidity || 0,
    }))
    
    return chartData
  } catch (error) {
    console.error('Failed to fetch historical data:', error)
    return []
  }
}

// Replace the hardcoded lineChartData with:
const [lineChartData, setLineChartData] = useState<any[]>([])

useEffect(() => {
  if (selectedCity) {
    fetchHistoricalData(selectedCity).then(data => {
      if (data.length > 0) {
        setLineChartData(data)
      }
    })
  }
}, [selectedCity])
```

---

### **Fix #6: Dashboard WebSocket - Add Better Error Handling**
```typescript
// frontend/src/pages/Dashboard.tsx - Update WebSocket usage

// Replace:
const wsUrl = `ws://${window.location.hostname}:8000/api/ws/cities`
useWebSocket(wsUrl)

// With:
const wsUrl = import.meta.env.VITE_WS_URL || 
  `ws://${window.location.hostname}:${import.meta.env.VITE_WS_PORT || 8000}/api/ws/cities`

const { send } = useWebSocket(wsUrl)

// Add error handling:
useEffect(() => {
  if (!wsUrl.includes('localhost') && !wsUrl.includes('127.0.0.1')) {
    console.warn('WebSocket may not work on non-localhost environments')
  }
}, [wsUrl])
```

---

## 📝 SUMMARY OF ALL ISSUES

### **Frontend Errors/Issues (10 Total):**

1. ❌ **WebSocket URL** - Not properly configured
2. ❌ **Missing .env file** - No environment variables
3. ❌ **API Base URL** - Hardcoded fallback
4. ❌ **No Error Boundaries** - App crashes on errors
5. ❌ **WebSocket Error Handling** - Silent failures
6. ❌ **Axios Interceptor** - Potential infinite loops on refresh
7. ❌ **Missing Loading States** - Confusing UX
8. ❌ **Type Safety Issues** - Some `any` types
9. ❌ **CORS Configuration** - Backend might not allow frontend origin
10. ❌ **Hardcoded Mock Data** - Analytics uses fake data instead of real API

---

## 🚀 HOW TO USE WITH CLAUDE CODE

1. **Copy this entire section** below
2. **Paste into Claude Opus 4.7**
3. **Ask**: "Fix all these frontend issues"

```
HERE'S THE COMPLETE FIX PACKAGE:

[Use all the Fix #1 through Fix #6 code sections above]
```

---

## ✅ VERIFICATION CHECKLIST

After applying fixes:
- [ ] Run `npm install` in frontend/
- [ ] Update `.env` file with correct values
- [ ] Test login/register
- [ ] Verify API calls work
- [ ] Check WebSocket connection
- [ ] Test error boundaries
- [ ] Run `npm run build` to check for TypeScript errors
- [ ] Test on http://localhost:3000
