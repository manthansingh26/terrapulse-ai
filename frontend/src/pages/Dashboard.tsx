import React, { useEffect, useMemo, useState } from 'react'
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import {
  Activity,
  AlertTriangle,
  Brain,
  CloudSun,
  Database,
  Gauge,
  MapPin,
  Radio,
  ShieldAlert,
  Target,
  TrendingUp,
  Wind,
} from 'lucide-react'
import { apiClient, City, MLInsights } from '@/services/api'
import { useWebSocket } from '@/hooks/useWebSocket'
import DataSourceNotice from '@/components/DataSourceNotice'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
const wsUrl = API_BASE_URL.replace(/^http/, 'ws').replace(/\/api\/?$/, '/api/ws/cities')

const riskColor = {
  Low: '#10b981',
  Moderate: '#f59e0b',
  High: '#f97316',
  Critical: '#ef4444',
}

const riskBadgeClass = {
  Low: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  Moderate: 'bg-amber-50 text-amber-700 border-amber-200',
  High: 'bg-orange-50 text-orange-700 border-orange-200',
  Critical: 'bg-red-50 text-red-700 border-red-200',
}

const modelSignals = [
  { name: 'AQI', weight: 42 },
  { name: 'Humidity', weight: 18 },
  { name: 'Temp', weight: 16 },
  { name: 'Wind', weight: 14 },
  { name: 'History', weight: 10 },
]

const Dashboard: React.FC = () => {
  const [cities, setCities] = useState<City[]>([])
  const [mlInsights, setMlInsights] = useState<MLInsights | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdated, setLastUpdated] = useState('')

  useWebSocket(wsUrl)

  const loadDashboard = async (showLoader = false) => {
    try {
      if (showLoader) setIsLoading(true)
      setError(null)
      const [cityData, insights] = await Promise.all([
        apiClient.getAllCities(),
        apiClient.getMLInsights(),
      ])
      setCities(cityData)
      setMlInsights(insights)
      setLastUpdated(new Date().toLocaleTimeString())
    } catch (err) {
      setError('Unable to load demo model intelligence. Check backend and database connection.')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadDashboard(true)
    const interval = window.setInterval(() => loadDashboard(false), 30000)
    return () => window.clearInterval(interval)
  }, [])

  const validAQI = cities.filter((city) => city.current_aqi)
  const avgAQI = validAQI.length
    ? Math.round(validAQI.reduce((sum, city) => sum + (city.current_aqi || 0), 0) / validAQI.length)
    : 0

  const avgTemperature = cities.filter((city) => city.current_temperature).length
    ? (
        cities
          .filter((city) => city.current_temperature)
          .reduce((sum, city) => sum + (city.current_temperature || 0), 0) /
        cities.filter((city) => city.current_temperature).length
      ).toFixed(1)
    : '0.0'

  const criticalAlerts = mlInsights?.insights.filter((item) => item.risk_level === 'Critical').length || 0
  const topRisks = mlInsights?.insights.slice(0, 6) || []

  const forecastData = useMemo(
    () =>
      (mlInsights?.insights.slice(0, 8) || []).map((item) => ({
        city: item.city.replace('-Chinchwad', ''),
        current: item.current_aqi,
        predicted: item.predicted_aqi_24h,
        risk: item.risk_score,
      })),
    [mlInsights]
  )

  const riskDistribution = useMemo(() => {
    const levels = ['Low', 'Moderate', 'High', 'Critical'] as const
    return levels.map((level) => ({
      name: level,
      value: mlInsights?.insights.filter((item) => item.risk_level === level).length || 0,
      color: riskColor[level],
    }))
  }, [mlInsights])

  const systemMetrics = [
    {
      label: 'Avg AQI',
      value: avgAQI,
      detail: `avg temp ${avgTemperature} C`,
      icon: Gauge,
      tone: 'from-sky-500 to-cyan-500',
    },
    {
      label: '24h Forecast',
      value: mlInsights?.avg_predicted_aqi_24h.toFixed(0) || '0',
      detail: `${mlInsights?.trend || 'stable'} trajectory`,
      icon: TrendingUp,
      tone: 'from-violet-500 to-fuchsia-500',
    },
    {
      label: 'High Risk Cities',
      value: mlInsights?.high_risk_cities || 0,
      detail: `${criticalAlerts} critical alerts`,
      icon: ShieldAlert,
      tone: 'from-orange-500 to-red-500',
    },
    {
      label: 'Confidence',
      value: `${Math.round((mlInsights?.confidence || 0) * 100)}%`,
      detail: mlInsights?.model_version || 'model offline',
      icon: Brain,
      tone: 'from-emerald-500 to-teal-500',
    },
  ]

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="h-40 rounded-lg bg-slate-200 animate-pulse" />
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((item) => (
            <div key={item} className="h-32 rounded-lg bg-slate-200 animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <DataSourceNotice />

      <section className="overflow-hidden rounded-lg border border-slate-200 bg-slate-950 text-white shadow-xl">
        <div className="grid grid-cols-1 lg:grid-cols-[1.4fr_0.9fr]">
          <div className="p-6 lg:p-8">
            <div className="flex flex-wrap items-center gap-3 text-sm text-cyan-100">
              <span className="inline-flex items-center gap-2 rounded-full border border-cyan-400/40 bg-cyan-400/10 px-3 py-1">
                <Radio size={14} />
                Demo inference system
              </span>
              <span className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-3 py-1">
                <Database size={14} />
                {mlInsights?.monitored_cities || cities.length} city demo records
              </span>
            </div>

            <div className="mt-8 max-w-3xl">
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-cyan-300">
                TerraPulse AI
              </p>
              <h1 className="mt-3 text-3xl font-bold leading-tight text-white lg:text-5xl">
                Environmental intelligence command center
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
                A machine learning dashboard that converts city-level sample AQI readings into
                24-hour AQI forecasts, risk scores, model confidence, and operational actions.
              </p>
            </div>

            <div className="mt-8 flex flex-wrap gap-3 text-sm">
              <span className="rounded-md bg-white px-3 py-2 font-semibold text-slate-950">
                Model: {mlInsights?.model_name || 'AQI Risk Forecaster'}
              </span>
              <span className="rounded-md border border-white/20 px-3 py-2 text-slate-200">
                Updated {lastUpdated || 'just now'}
              </span>
            </div>
          </div>

          <div className="border-t border-white/10 bg-white/[0.04] p-6 lg:border-l lg:border-t-0 lg:p-8">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-400">Top predicted risk</p>
                <h2 className="mt-1 text-2xl font-bold text-white">{topRisks[0]?.city || 'No data'}</h2>
              </div>
              <div className="rounded-lg bg-red-500/15 p-3 text-red-200">
                <AlertTriangle size={24} />
              </div>
            </div>

            <div className="mt-6">
              <div className="flex items-end justify-between">
                <div>
                  <p className="text-5xl font-bold">{topRisks[0]?.risk_score || 0}</p>
                  <p className="mt-1 text-sm text-slate-400">risk score</p>
                </div>
                <span className="rounded-md bg-white px-3 py-2 text-sm font-bold text-slate-950">
                  {topRisks[0]?.risk_level || 'Low'}
                </span>
              </div>
              <div className="mt-5 h-2 rounded-full bg-white/10">
                <div
                  className="h-2 rounded-full bg-red-400"
                  style={{ width: `${topRisks[0]?.risk_score || 0}%` }}
                />
              </div>
              <p className="mt-5 text-sm leading-6 text-slate-300">
                {topRisks[0]?.recommendation || 'Waiting for model output.'}
              </p>
            </div>
          </div>
        </div>
      </section>

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">
          {error}
        </div>
      )}

      <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        {systemMetrics.map((metric) => {
          const Icon = metric.icon
          return (
            <div key={metric.label} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center justify-between">
                <div className={`rounded-lg bg-gradient-to-br ${metric.tone} p-3 text-white`}>
                  <Icon size={22} />
                </div>
                <Activity className="text-slate-300" size={18} />
              </div>
              <p className="mt-5 text-sm font-medium text-slate-500">{metric.label}</p>
              <p className="mt-1 text-3xl font-bold text-slate-950">{metric.value}</p>
              <p className="mt-2 text-sm text-slate-500">{metric.detail}</p>
            </div>
          )
        })}
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-[1.45fr_0.9fr]">
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-950">Forecast vs sample AQI</h2>
              <p className="text-sm text-slate-500">Top cities ranked by predicted risk score.</p>
            </div>
            <span className="rounded-md bg-slate-100 px-3 py-2 text-sm font-semibold text-slate-600">
              24 hour horizon
            </span>
          </div>
          <div className="mt-6 h-[360px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={forecastData}>
                <defs>
                  <linearGradient id="currentAqi" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0.02} />
                  </linearGradient>
                  <linearGradient id="predictedAqi" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0.02} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="city" tick={{ fontSize: 12 }} interval={0} angle={-20} textAnchor="end" height={70} />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="current" stroke="#0ea5e9" fill="url(#currentAqi)" strokeWidth={3} name="Sample AQI" />
                <Area type="monotone" dataKey="predicted" stroke="#ef4444" fill="url(#predictedAqi)" strokeWidth={3} name="Predicted AQI" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div>
            <h2 className="text-lg font-bold text-slate-950">Risk distribution</h2>
            <p className="text-sm text-slate-500">City clusters by model risk level.</p>
          </div>
          <div className="mt-6 h-[240px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={riskDistribution.filter((item) => item.value > 0)}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={58}
                  outerRadius={92}
                  paddingAngle={4}
                >
                  {riskDistribution.map((entry) => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {riskDistribution.map((item) => (
              <div key={item.name} className="rounded-md border border-slate-200 p-3">
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-sm font-semibold text-slate-700">{item.name}</span>
                </div>
                <p className="mt-2 text-2xl font-bold text-slate-950">{item.value}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-[1fr_1fr]">
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-950">Model feature impact</h2>
              <p className="text-sm text-slate-500">Explainability layer for portfolio storytelling.</p>
            </div>
            <Target className="text-slate-400" size={22} />
          </div>
          <div className="mt-6 h-[280px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={modelSignals} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis type="number" domain={[0, 50]} />
                <YAxis dataKey="name" type="category" width={80} />
                <Tooltip />
                <Bar dataKey="weight" radius={[0, 8, 8, 0]} fill="#0f172a" name="Feature weight %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-950">Priority action queue</h2>
              <p className="text-sm text-slate-500">Automatically generated from forecasted AQI risk.</p>
            </div>
            <Wind className="text-slate-400" size={22} />
          </div>

          <div className="mt-5 space-y-3">
            {topRisks.slice(0, 5).map((item, index) => (
              <div key={item.city} className="rounded-lg border border-slate-200 p-4">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div className="flex items-center gap-3">
                    <span className="flex h-9 w-9 items-center justify-center rounded-md bg-slate-100 text-sm font-bold text-slate-700">
                      {index + 1}
                    </span>
                    <div>
                      <h3 className="font-bold text-slate-950">{item.city}</h3>
                      <p className="text-sm text-slate-500">
                        AQI {item.current_aqi} to {item.predicted_aqi_24h} forecast
                      </p>
                    </div>
                  </div>
                  <span className={`w-fit rounded-full border px-3 py-1 text-xs font-bold ${riskBadgeClass[item.risk_level]}`}>
                    {item.risk_level}
                  </span>
                </div>
                <p className="mt-3 text-sm leading-6 text-slate-600">{item.recommendation}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-950">Demo city intelligence</h2>
            <p className="text-sm text-slate-500">Sample city readings combined with model outputs.</p>
          </div>
          <div className="flex items-center gap-2 rounded-md bg-emerald-50 px-3 py-2 text-sm font-semibold text-emerald-700">
            <CloudSun size={16} />
            Database connected
          </div>
        </div>

        <div className="mt-5 overflow-x-auto">
          <table className="w-full min-w-[760px] text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-left text-xs uppercase tracking-wide text-slate-500">
                <th className="px-3 py-3">City</th>
                <th className="px-3 py-3">Sample AQI</th>
                <th className="px-3 py-3">Predicted AQI</th>
                <th className="px-3 py-3">Risk</th>
                <th className="px-3 py-3">Confidence</th>
                <th className="px-3 py-3">Weather</th>
              </tr>
            </thead>
            <tbody>
              {(mlInsights?.insights || []).map((item) => {
                const city = cities.find((entry) => entry.city === item.city)
                return (
                  <tr key={item.city} className="border-b border-slate-100 hover:bg-slate-50">
                    <td className="px-3 py-4 font-semibold text-slate-950">
                      <span className="inline-flex items-center gap-2">
                        <MapPin size={15} className="text-slate-400" />
                        {item.city}
                      </span>
                    </td>
                    <td className="px-3 py-4 text-slate-700">{item.current_aqi}</td>
                    <td className="px-3 py-4 font-semibold text-slate-950">{item.predicted_aqi_24h}</td>
                    <td className="px-3 py-4">
                      <span className={`rounded-full border px-3 py-1 text-xs font-bold ${riskBadgeClass[item.risk_level]}`}>
                        {item.risk_level}
                      </span>
                    </td>
                    <td className="px-3 py-4 text-slate-700">{Math.round(item.confidence * 100)}%</td>
                    <td className="px-3 py-4 text-slate-700">
                      {city?.current_temperature?.toFixed(1) || '0.0'} C / {city?.current_humidity?.toFixed(0) || '0'}%
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

export default Dashboard
