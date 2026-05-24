import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'

const normalizeApiBaseUrl = () => {
  if (typeof window !== 'undefined' && window.location.hostname === 'terrapulse-ai.vercel.app') {
    return '/api'
  }

  const rawUrl = String(import.meta.env.VITE_API_URL || 'https://terrapulse-ai.onrender.com/api').trim()
  const withoutTrailingSlash = rawUrl.replace(/\/+$/, '')
  return withoutTrailingSlash.endsWith('/api')
    ? withoutTrailingSlash
    : `${withoutTrailingSlash}/api`
}

const API_BASE_URL = normalizeApiBaseUrl()

interface LoginRequest {
  username?: string
  email?: string
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
  sub?: string
  name?: string
  role?: string
  full_name?: string
  is_active: boolean
  is_admin: boolean
  created_at: string
}

interface JwtPayload {
  sub?: string
  username?: string
  email?: string
  full_name?: string
  name?: string
  role?: string
  is_admin?: boolean
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

interface CityStatistics {
  city: string
  avg_aqi: number
  max_aqi: number
  min_aqi: number
  avg_temperature: number
  avg_humidity: number
  data_points: number
  period_days: number
}

interface AirQualityHistory {
  id: number
  city: string
  aqi?: number
  co2?: number
  pm25?: number
  pm10?: number
  timestamp: string
}

interface HealthResponse {
  status: string
  version: string
  database: Record<string, unknown>
  timestamp: string
}

interface ApiErrorBody {
  detail?: string
  error?: string
}

interface CityRiskInsight {
  city: string
  current_aqi: number
  predicted_aqi_24h: number
  risk_score: number
  risk_level: 'Low' | 'Moderate' | 'High' | 'Critical'
  confidence: number
  recommendation: string
}

interface MLInsights {
  model_name: string
  model_version: string
  generated_at: string
  monitored_cities: number
  avg_current_aqi: number
  avg_predicted_aqi_24h: number
  high_risk_cities: number
  confidence: number
  trend: string
  insights: CityRiskInsight[]
}

interface MLTrainingMetrics {
  run_id?: string
  model_name: string
  model_version: string
  trained_at: string
  training_rows: number
  test_rows: number
  synthetic_rows_inserted: number
  validation_strategy?: string
  train_window_start?: string
  train_window_end?: string
  test_window_start?: string
  test_window_end?: string
  mae: number
  rmse: number
  r2: number
  features: string[]
  artifact_uri?: string
  model_artifact?: string
}

interface MLModelRunSummary {
  run_id: string
  model_name: string
  model_version: string
  trained_at: string
  validation_strategy: string
  training_rows: number
  test_rows: number
  mae: number
  rmse: number
  r2: number
  artifact_uri: string
}

interface MLDataQuality {
  total_records: number
  monitored_cities: number
  latest_timestamp?: string
  missing_aqi: number
  missing_weather: number
  missing_ratio: number
  freshness_status: 'fresh' | 'aging' | 'stale' | 'no_data'
  source_tracking_enabled: boolean
  synthetic_rows_last_run: number
}

interface FeatureImportanceItem {
  feature: string
  importance: number
}

interface EvaluationSample {
  sample: number
  actual_aqi: number
  predicted_aqi: number
  error: number
}

interface AQIForecast {
  city: string
  current_aqi: number
  predicted_aqi_24h: number
  change: number
  risk_level: string
  confidence: number
  generated_at: string
  data_sufficiency?: {
    is_sufficient: boolean
    warning?: string
  }
}

interface PredictionExplanationFactor {
  feature: string
  label: string
  value: number
  importance: number
  direction: string
  reason: string
}

interface AQIPredictionExplanation extends AQIForecast {
  explanation_summary: string
  factors: PredictionExplanationFactor[]
}

interface MLForecastAlert {
  alert_triggered: boolean
  email_sent: boolean
  city: string
  current_aqi: number
  predicted_aqi_24h: number
  threshold: number
  confidence: number
  message: string
}

const getApiErrorMessage = (error: unknown, fallback: string): string => {
  if (axios.isAxiosError<ApiErrorBody>(error)) {
    if (error.code === 'ERR_CANCELED' || error.code === 'ECONNABORTED') {
      return 'Request timed out. Backend is still waking up.'
    }

    if (!error.response) {
      return 'Cannot reach server. Please wait 30 seconds and retry.'
    }

    return error.response?.data?.detail || error.response?.data?.error || fallback
  }

  return fallback
}

const decodeJwtPayload = (token: string): JwtPayload | null => {
  try {
    const payload = token.split('.')[1]
    if (!payload) return null

    const normalizedPayload = payload.replace(/-/g, '+').replace(/_/g, '/')
    const decodedPayload = decodeURIComponent(
      atob(normalizedPayload)
        .split('')
        .map((char) => `%${`00${char.charCodeAt(0).toString(16)}`.slice(-2)}`)
        .join('')
    )
    return JSON.parse(decodedPayload) as JwtPayload
  } catch {
    return null
  }
}

const getUserFromToken = (token: string, fallbackUsername = 'User'): User => {
  const decoded = decodeJwtPayload(token)
  const username = decoded?.sub || decoded?.username || decoded?.email || decoded?.name || fallbackUsername

  return {
    id: 0,
    email: decoded?.email || '',
    username,
    sub: decoded?.sub,
    name: decoded?.name,
    role: decoded?.role || 'user',
    full_name: decoded?.full_name || decoded?.name || '',
    is_active: true,
    is_admin: Boolean(decoded?.is_admin || decoded?.role === 'admin'),
    created_at: '',
  }
}

const mergeUserWithToken = (user: User, token: string, fallbackUsername = 'User'): User => {
  const decodedUser = getUserFromToken(token, fallbackUsername)

  return {
    ...decodedUser,
    ...user,
    username: user.username || decodedUser.username,
    email: user.email || decodedUser.email,
    full_name: user.full_name || decodedUser.full_name,
    sub: user.sub || decodedUser.sub,
    name: user.name || decodedUser.name,
    role: user.role || decodedUser.role,
    is_active: user.is_active ?? decodedUser.is_active,
    is_admin: user.is_admin ?? decodedUser.is_admin,
    created_at: user.created_at || decodedUser.created_at,
  }
}

const getPersistedToken = () => {
  const token = localStorage.getItem('access_token')
  if (token) return token

  const authData = localStorage.getItem('terrapulse-auth')
  if (!authData) return null

  try {
    const parsed = JSON.parse(authData) as { state?: { token?: string } }
    return parsed.state?.token || null
  } catch {
    return null
  }
}

const saveAuthSnapshot = (token: string, user: User | null) => {
  localStorage.setItem(
    'terrapulse-auth',
    JSON.stringify({
      state: {
        token,
        user,
        isAuthenticated: true,
      },
    })
  )
}

const clearAuthStorage = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('terrapulse-auth')
}

const isAuthRoute = (url?: string) =>
  Boolean(url?.includes('/auth/login') || url?.includes('/auth/register') || url?.includes('/auth/refresh'))

class APIClient {
  private client: AxiosInstance
  // @ts-expect-error -- state is set internally and consumed by external event listeners
  private _isWakingUp: boolean = false

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 60000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add token to requests
    this.client.interceptors.request.use((config) => {
      const token = getPersistedToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config
        if (error.response?.status === 401 && originalRequest && !originalRequest._retry && !isAuthRoute(originalRequest.url)) {
          originalRequest._retry = true
          const refreshToken = localStorage.getItem('refresh_token')
          if (refreshToken) {
            try {
              const response = await this.client.post('/auth/refresh', {
                token: refreshToken,
              })
              const { access_token } = response.data
              localStorage.setItem('access_token', access_token)
              saveAuthSnapshot(access_token, getUserFromToken(access_token))
              originalRequest.headers.Authorization = `Bearer ${access_token}`
              return this.client(originalRequest)
            } catch (err) {
              clearAuthStorage()
            }
          }
        }

        if (error.response?.status === 401 && !isAuthRoute(originalRequest?.url)) {
          clearAuthStorage()
          if (window.location.pathname !== '/login') {
            window.location.href = '/login'
          }
        }

        return Promise.reject(error)
      }
    )

    // Retry logic with exponential backoff for Render cold-start (502/503) and network errors
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const config = error.config
        if (!config || config._retryCount >= 4) {
          if (config?._retryCount >= 4) {
            this._isWakingUp = false
            window.dispatchEvent(new CustomEvent('backend:failed'))
          }
          return Promise.reject(error)
        }

        // Retry on network errors or 502/503 (Render cold start)
        const isNetworkError = !error.response
        const isColdStart = error.response?.status === 502 || error.response?.status === 503

        if (isNetworkError || isColdStart) {
          config._retryCount = (config._retryCount || 0) + 1
          this._isWakingUp = true
          window.dispatchEvent(
            new CustomEvent('backend:waking', { detail: { attempt: config._retryCount } })
          )

          const delay = Math.min(1000 * Math.pow(2, config._retryCount), 15000) // exp backoff, max 15s
          await new Promise((res) => setTimeout(res, delay))

          if (config._retryCount >= 4) {
            this._isWakingUp = false
            window.dispatchEvent(new CustomEvent('backend:failed'))
          }

          return this.client(config)
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
    try {
      await axios.get(`${API_BASE_URL}/health`, { timeout: 5000 })
    } catch {
      // Ignore the wake-up ping failure; the login request below has the long timeout.
    }

    const response = await this.client.post('/auth/login', data, { timeout: 65000 })
    return response.data
  }

  async getCurrentUser(config?: AxiosRequestConfig): Promise<User> {
    const response = await this.client.get('/auth/me', config)
    return response.data
  }

  // Cities endpoints
  async getAllCities(config?: AxiosRequestConfig): Promise<City[]> {
    const response = await this.client.get('/cities/all', config)
    return response.data
  }

  async getCity(city: string, config?: AxiosRequestConfig): Promise<City> {
    const response = await this.client.get(`/cities/${city}`, config)
    return response.data
  }

  async getCityCoordinates(config?: AxiosRequestConfig): Promise<Record<string, { lat: number; lon: number }>> {
    const response = await this.client.get('/cities/coordinates/all', config)
    return response.data
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

  async getHistoricalData(city: string, days: number = 7, config?: AxiosRequestConfig): Promise<EnvironmentalData[]> {
    const response = await this.client.get(`/data/history/${city}`, {
      ...config,
      params: { days },
    })
    return response.data
  }

  async getCityStatistics(city: string, days: number = 7): Promise<CityStatistics> {
    const response = await this.client.get(`/data/statistics/${city}`, {
      params: { days },
    })
    return response.data
  }

  async getAirQualityHistory(city: string, days: number = 7): Promise<AirQualityHistory[]> {
    const response = await this.client.get(`/data/air-quality/${city}`, {
      params: { days },
    })
    return response.data
  }

  async getAllLatestData(config?: AxiosRequestConfig): Promise<EnvironmentalData[]> {
    const response = await this.client.get('/data/all/latest', config)
    return response.data
  }

  async getMLInsights(config?: AxiosRequestConfig): Promise<MLInsights> {
    const response = await this.client.get('/data/ml/insights', config)
    return response.data
  }

  // Machine learning endpoints
  async trainAQIModel(config?: AxiosRequestConfig): Promise<MLTrainingMetrics> {
    const response = await this.client.post('/ml/train', undefined, config)
    return response.data
  }

  async getMLMetrics(config?: AxiosRequestConfig): Promise<MLTrainingMetrics> {
    const response = await this.client.get('/ml/metrics', config)
    return response.data
  }

  async getMLRunHistory(config?: AxiosRequestConfig): Promise<MLModelRunSummary[]> {
    const response = await this.client.get('/ml/runs', config)
    return response.data
  }

  async getMLRun(runId: string, config?: AxiosRequestConfig): Promise<MLTrainingMetrics> {
    const response = await this.client.get(`/ml/runs/${runId}`, config)
    return response.data
  }

  async getMLDataQuality(config?: AxiosRequestConfig): Promise<MLDataQuality> {
    const response = await this.client.get('/ml/data-quality', config)
    return response.data
  }

  async getFeatureImportance(config?: AxiosRequestConfig): Promise<FeatureImportanceItem[]> {
    const response = await this.client.get('/ml/feature-importance', config)
    return response.data
  }

  async getEvaluationSamples(config?: AxiosRequestConfig): Promise<EvaluationSample[]> {
    const response = await this.client.get('/ml/evaluation-samples', config)
    return response.data
  }

  async getAllForecasts(config?: AxiosRequestConfig): Promise<AQIForecast[]> {
    const response = await this.client.get('/ml/forecast/all', config)
    return response.data
  }

  async getTopForecastExplanations(limit: number = 5, config?: AxiosRequestConfig): Promise<AQIPredictionExplanation[]> {
    const response = await this.client.get('/ml/explain/top', {
      ...config,
      params: { limit },
    })
    return response.data
  }

  async checkAllMLForecastAlerts(config?: AxiosRequestConfig): Promise<MLForecastAlert[]> {
    const response = await this.client.post('/alerts/ml/check-all', undefined, config)
    return response.data
  }

  // Health endpoint
  async getHealth(): Promise<HealthResponse> {
    const response = await this.client.get('/health')
    return response.data
  }
}

export const apiClient = new APIClient()
export type {
  User,
  City,
  EnvironmentalData,
  CityStatistics,
  AirQualityHistory,
  HealthResponse,
  Token,
  CityRiskInsight,
  MLInsights,
  MLTrainingMetrics,
  MLModelRunSummary,
  MLDataQuality,
  FeatureImportanceItem,
  EvaluationSample,
  AQIForecast,
  PredictionExplanationFactor,
  AQIPredictionExplanation,
  MLForecastAlert,
}
export { getApiErrorMessage }
export { API_BASE_URL, getUserFromToken, mergeUserWithToken, saveAuthSnapshot, clearAuthStorage }
