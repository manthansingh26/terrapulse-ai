import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

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
    return error.response?.data?.detail || error.response?.data?.error || fallback
  }

  return fallback
}

class APIClient {
  private client: AxiosInstance

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

    // Handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true
          const refreshToken = localStorage.getItem('refresh_token')
          if (refreshToken) {
            try {
              const response = await this.client.post('/auth/refresh', {
                token: refreshToken,
              })
              const { access_token } = response.data
              localStorage.setItem('access_token', access_token)
              originalRequest.headers.Authorization = `Bearer ${access_token}`
              return this.client(originalRequest)
            } catch (err) {
              localStorage.removeItem('access_token')
              localStorage.removeItem('refresh_token')
            }
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
    return response.data
  }

  async getCity(city: string): Promise<City> {
    const response = await this.client.get(`/cities/${city}`)
    return response.data
  }

  async getCityCoordinates(): Promise<Record<string, { lat: number; lon: number }>> {
    const response = await this.client.get('/cities/coordinates/all')
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

  async getHistoricalData(city: string, days: number = 7): Promise<EnvironmentalData[]> {
    const response = await this.client.get(`/data/history/${city}`, {
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

  async getAllLatestData(): Promise<EnvironmentalData[]> {
    const response = await this.client.get('/data/all/latest')
    return response.data
  }

  async getMLInsights(): Promise<MLInsights> {
    const response = await this.client.get('/data/ml/insights')
    return response.data
  }

  // Machine learning endpoints
  async trainAQIModel(): Promise<MLTrainingMetrics> {
    const response = await this.client.post('/ml/train')
    return response.data
  }

  async getMLMetrics(): Promise<MLTrainingMetrics> {
    const response = await this.client.get('/ml/metrics')
    return response.data
  }

  async getMLRunHistory(): Promise<MLModelRunSummary[]> {
    const response = await this.client.get('/ml/runs')
    return response.data
  }

  async getMLRun(runId: string): Promise<MLTrainingMetrics> {
    const response = await this.client.get(`/ml/runs/${runId}`)
    return response.data
  }

  async getMLDataQuality(): Promise<MLDataQuality> {
    const response = await this.client.get('/ml/data-quality')
    return response.data
  }

  async getFeatureImportance(): Promise<FeatureImportanceItem[]> {
    const response = await this.client.get('/ml/feature-importance')
    return response.data
  }

  async getEvaluationSamples(): Promise<EvaluationSample[]> {
    const response = await this.client.get('/ml/evaluation-samples')
    return response.data
  }

  async getAllForecasts(): Promise<AQIForecast[]> {
    const response = await this.client.get('/ml/forecast/all')
    return response.data
  }

  async getTopForecastExplanations(limit: number = 5): Promise<AQIPredictionExplanation[]> {
    const response = await this.client.get('/ml/explain/top', {
      params: { limit },
    })
    return response.data
  }

  async checkAllMLForecastAlerts(): Promise<MLForecastAlert[]> {
    const response = await this.client.post('/alerts/ml/check-all')
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
