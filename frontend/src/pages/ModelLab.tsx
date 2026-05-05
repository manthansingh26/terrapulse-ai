import React, { useEffect, useMemo, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import {
  Activity,
  AlertCircle,
  Brain,
  CheckCircle2,
  Cpu,
  Database,
  FlaskConical,
  Gauge,
  GitBranch,
  Layers,
  Lightbulb,
  Radio,
  RefreshCw,
  Server,
  Sigma,
  Target,
  Timer,
  TrendingUp,
  Zap,
} from 'lucide-react'
import {
  apiClient,
  AQIPredictionExplanation,
  AQIForecast,
  EvaluationSample,
  FeatureImportanceItem,
  MLDataQuality,
  MLForecastAlert,
  MLModelRunSummary,
  MLTrainingMetrics,
} from '@/services/api'
import DataSourceNotice from '@/components/DataSourceNotice'

const riskClass = {
  Good: 'border-emerald-200 bg-emerald-50 text-emerald-700',
  Fair: 'border-amber-200 bg-amber-50 text-amber-700',
  Poor: 'border-orange-200 bg-orange-50 text-orange-700',
  Unhealthy: 'border-red-200 bg-red-50 text-red-700',
  Severe: 'border-red-300 bg-red-100 text-red-800',
}

const formatFeatureName = (feature: string) =>
  feature
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')

const pipelineSteps = [
  { label: 'Load dataset', icon: Database },
  { label: 'Build features', icon: Layers },
  { label: 'Train forest', icon: Cpu },
  { label: 'Evaluate holdout', icon: Target },
  { label: 'Register run', icon: GitBranch },
]

const freshnessClass = {
  fresh: 'bg-emerald-100 text-emerald-700',
  aging: 'bg-amber-100 text-amber-700',
  stale: 'bg-red-100 text-red-700',
  no_data: 'bg-slate-100 text-slate-700',
}

const ModelLab: React.FC = () => {
  const [metrics, setMetrics] = useState<MLTrainingMetrics | null>(null)
  const [featureImportance, setFeatureImportance] = useState<FeatureImportanceItem[]>([])
  const [evaluationSamples, setEvaluationSamples] = useState<EvaluationSample[]>([])
  const [forecasts, setForecasts] = useState<AQIForecast[]>([])
  const [forecastExplanations, setForecastExplanations] = useState<AQIPredictionExplanation[]>([])
  const [modelRuns, setModelRuns] = useState<MLModelRunSummary[]>([])
  const [dataQuality, setDataQuality] = useState<MLDataQuality | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isTraining, setIsTraining] = useState(false)
  const [isCheckingAlerts, setIsCheckingAlerts] = useState(false)
  const [alertResults, setAlertResults] = useState<MLForecastAlert[]>([])
  const [error, setError] = useState<string | null>(null)

  const loadModelLab = async () => {
    try {
      setError(null)
      const [metricsData, runsData, qualityData, importanceData, evaluationData, forecastData, explanationData] = await Promise.all([
        apiClient.getMLMetrics(),
        apiClient.getMLRunHistory(),
        apiClient.getMLDataQuality(),
        apiClient.getFeatureImportance(),
        apiClient.getEvaluationSamples(),
        apiClient.getAllForecasts(),
        apiClient.getTopForecastExplanations(5),
      ])
      setMetrics(metricsData)
      setModelRuns(runsData)
      setDataQuality(qualityData)
      setFeatureImportance(importanceData)
      setEvaluationSamples(evaluationData)
      setForecasts(forecastData)
      setForecastExplanations(explanationData)
    } catch (err) {
      setError('Unable to load model artifacts. Train the model or check backend status.')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadModelLab()
  }, [])

  const handleRetrain = async () => {
    try {
      setIsTraining(true)
      setError(null)
      const updatedMetrics = await apiClient.trainAQIModel()
      setMetrics(updatedMetrics)
      const [runsData, qualityData, importanceData, evaluationData, forecastData, explanationData] = await Promise.all([
        apiClient.getMLRunHistory(),
        apiClient.getMLDataQuality(),
        apiClient.getFeatureImportance(),
        apiClient.getEvaluationSamples(),
        apiClient.getAllForecasts(),
        apiClient.getTopForecastExplanations(5),
      ])
      setModelRuns(runsData)
      setDataQuality(qualityData)
      setFeatureImportance(importanceData)
      setEvaluationSamples(evaluationData)
      setForecasts(forecastData)
      setForecastExplanations(explanationData)
    } catch (err) {
      setError('Model retraining failed. Check backend logs and data availability.')
      console.error(err)
    } finally {
      setIsTraining(false)
    }
  }

  const handleCheckAlerts = async () => {
    try {
      setIsCheckingAlerts(true)
      setError(null)
      const results = await apiClient.checkAllMLForecastAlerts()
      setAlertResults(results)
    } catch (err) {
      setError('ML alert check failed. Confirm backend authentication and model artifacts are available.')
      console.error(err)
    } finally {
      setIsCheckingAlerts(false)
    }
  }

  const topFeatures = useMemo(
    () =>
      featureImportance.slice(0, 8).map((item) => ({
        feature: formatFeatureName(item.feature),
        importance: Number(Math.max(item.importance, 0).toFixed(4)),
      })),
    [featureImportance]
  )

  const forecastSummary = useMemo(() => {
    const avgPredicted = forecasts.length
      ? forecasts.reduce((sum, item) => sum + item.predicted_aqi_24h, 0) / forecasts.length
      : 0
    const highRisk = forecasts.filter((item) => ['Unhealthy', 'Severe'].includes(item.risk_level)).length
    const improving = forecasts.filter((item) => item.change < 0).length
    return {
      avgPredicted: Math.round(avgPredicted),
      highRisk,
      improving,
    }
  }, [forecasts])

  const evaluationSummary = useMemo(() => {
    const averageError = evaluationSamples.length
      ? evaluationSamples.reduce((sum, item) => sum + Math.abs(item.error), 0) / evaluationSamples.length
      : 0
    const maxError = evaluationSamples.length
      ? Math.max(...evaluationSamples.map((item) => Math.abs(item.error)))
      : 0
    return {
      averageError: Number(averageError.toFixed(1)),
      maxError,
    }
  }, [evaluationSamples])

  const alertSummary = useMemo(() => {
    const triggered = alertResults.filter((item) => item.alert_triggered).length
    const emailsSent = alertResults.filter((item) => item.email_sent).length
    return { triggered, emailsSent }
  }, [alertResults])

  const runComparison = useMemo(() => {
    const current = modelRuns[0]
    const previous = modelRuns[1]
    if (!current || !previous) {
      return null
    }

    return {
      maeDelta: Number((current.mae - previous.mae).toFixed(2)),
      rmseDelta: Number((current.rmse - previous.rmse).toFixed(2)),
      r2Delta: Number((current.r2 - previous.r2).toFixed(3)),
    }
  }, [modelRuns])

  const modelHealthCards = [
    {
      label: 'Model status',
      value: metrics ? 'Ready' : 'Offline',
      detail: metrics?.run_id || 'No registered run',
      icon: CheckCircle2,
      tone: 'text-emerald-700 bg-emerald-50 border-emerald-200',
    },
    {
      label: 'Data freshness',
      value: dataQuality ? formatFeatureName(dataQuality.freshness_status) : 'Unknown',
      detail: dataQuality?.latest_timestamp
        ? `Latest ${new Date(dataQuality.latest_timestamp).toLocaleString()}`
        : 'No timestamp available',
      icon: Radio,
      tone:
        dataQuality?.freshness_status === 'fresh'
          ? 'text-emerald-700 bg-emerald-50 border-emerald-200'
          : dataQuality?.freshness_status === 'aging'
            ? 'text-amber-700 bg-amber-50 border-amber-200'
            : 'text-red-700 bg-red-50 border-red-200',
    },
    {
      label: 'Validation',
      value: metrics?.validation_strategy ? formatFeatureName(metrics.validation_strategy) : 'Pending',
      detail: 'Forecast-safe holdout',
      icon: Server,
      tone: 'text-cyan-700 bg-cyan-50 border-cyan-200',
    },
    {
      label: 'Registered runs',
      value: modelRuns.length.toString(),
      detail: metrics?.artifact_uri || 'No artifact URI',
      icon: GitBranch,
      tone: 'text-violet-700 bg-violet-50 border-violet-200',
    },
  ]

  const metricCards = [
    {
      label: 'R2 Score',
      value: metrics?.r2.toFixed(3) || '0.000',
      detail: 'explained variance',
      icon: Target,
      tone: 'from-emerald-500 to-teal-500',
    },
    {
      label: 'MAE',
      value: metrics?.mae.toFixed(2) || '0.00',
      detail: 'AQI points average error',
      icon: Gauge,
      tone: 'from-cyan-500 to-sky-500',
    },
    {
      label: 'RMSE',
      value: metrics?.rmse.toFixed(2) || '0.00',
      detail: 'penalizes large errors',
      icon: Sigma,
      tone: 'from-violet-500 to-fuchsia-500',
    },
    {
      label: 'Training Rows',
      value: metrics?.training_rows.toLocaleString() || '0',
      detail: `${metrics?.test_rows.toLocaleString() || '0'} test rows`,
      icon: Database,
      tone: 'from-slate-700 to-slate-950',
    },
  ]

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="h-44 rounded-lg bg-slate-200 animate-pulse" />
        <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
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
        <div className="grid grid-cols-1 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="p-6 lg:p-8">
            <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 text-xs font-bold uppercase tracking-wide text-cyan-300">
              <FlaskConical size={14} />
              Model Lab
            </div>
            <h1 className="mt-5 text-3xl font-bold leading-tight lg:text-5xl">
              Demo AQI forecasting model workspace
            </h1>
            <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-300 lg:text-base">
              Inspect the trained Random Forest pipeline behind TerraPulse AI. This page exposes
              training quality, feature importance, retraining, and city-level 24-hour forecasts
              built from demo AQI records.
            </p>

            <div className="mt-7 flex flex-wrap gap-3 text-sm">
              <span className="rounded-md bg-white px-3 py-2 font-bold text-slate-950">
                {metrics?.model_name || 'Model unavailable'}
              </span>
              <span className="rounded-md border border-white/20 px-3 py-2 text-slate-200">
                {metrics?.model_version || 'version pending'}
              </span>
              {metrics?.run_id && (
                <span className="rounded-md border border-cyan-300/30 px-3 py-2 font-mono text-xs text-cyan-200">
                  {metrics.run_id}
                </span>
              )}
              <span className="rounded-md border border-white/20 px-3 py-2 text-slate-200">
                Trained {metrics ? new Date(metrics.trained_at).toLocaleString() : 'not yet'}
              </span>
            </div>
          </div>

          <div className="border-t border-white/10 bg-white/[0.04] p-6 lg:border-l lg:border-t-0 lg:p-8">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-400">Model readiness</p>
                <p className="mt-1 text-3xl font-bold">{metrics ? 'Production Demo' : 'Offline'}</p>
              </div>
              <div className="rounded-lg bg-cyan-400/10 p-3 text-cyan-300">
                <Brain size={28} />
              </div>
            </div>

            <div className="mt-6 grid grid-cols-3 gap-3">
              <div className="rounded-lg border border-white/10 bg-white/5 p-3">
                <p className="text-xs text-slate-400">Forecast avg</p>
                <p className="mt-1 text-2xl font-bold">{forecastSummary.avgPredicted}</p>
              </div>
              <div className="rounded-lg border border-white/10 bg-white/5 p-3">
                <p className="text-xs text-slate-400">High risk</p>
                <p className="mt-1 text-2xl font-bold">{forecastSummary.highRisk}</p>
              </div>
              <div className="rounded-lg border border-white/10 bg-white/5 p-3">
                <p className="text-xs text-slate-400">Improving</p>
                <p className="mt-1 text-2xl font-bold">{forecastSummary.improving}</p>
              </div>
            </div>

            <button
              onClick={handleRetrain}
              disabled={isTraining}
              className="mt-6 inline-flex w-full items-center justify-center gap-2 rounded-md bg-cyan-400 px-4 py-3 text-sm font-bold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <RefreshCw size={18} className={isTraining ? 'animate-spin' : ''} />
              {isTraining ? 'Training model...' : 'Retrain model'}
            </button>
            <button
              onClick={handleCheckAlerts}
              disabled={isCheckingAlerts}
              className="mt-3 inline-flex w-full items-center justify-center gap-2 rounded-md border border-white/20 px-4 py-3 text-sm font-bold text-white transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <AlertCircle size={18} className={isCheckingAlerts ? 'animate-pulse' : ''} />
              {isCheckingAlerts ? 'Checking forecasts...' : 'Check ML alerts'}
            </button>
          </div>
        </div>
      </section>

      {error && (
        <div className="flex items-center gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        {modelHealthCards.map((card, index) => {
          const Icon = card.icon
          return (
            <div
              key={card.label}
              className={`ml-health-card ${card.tone}`}
              style={{ animationDelay: `${index * 90}ms` }}
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide opacity-75">{card.label}</p>
                  <p className="mt-2 text-2xl font-black">{card.value}</p>
                </div>
                <div className="rounded-lg bg-white/70 p-2">
                  <Icon size={20} />
                </div>
              </div>
              <p className="mt-4 truncate text-xs font-semibold opacity-80">{card.detail}</p>
            </div>
          )
        })}
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-950">Training pipeline</h2>
              <p className="text-sm text-slate-500">
                Operational view of the retraining workflow.
              </p>
            </div>
            <span className={`rounded-full px-3 py-1 text-xs font-bold ${isTraining ? 'bg-cyan-100 text-cyan-700' : 'bg-emerald-100 text-emerald-700'}`}>
              {isTraining ? 'Running' : 'Idle'}
            </span>
          </div>

          <div className={`ml-pipeline mt-6 ${isTraining ? 'ml-pipeline-running' : ''}`}>
            {pipelineSteps.map((step, index) => {
              const Icon = step.icon
              return (
                <div key={step.label} className="ml-pipeline-step" style={{ animationDelay: `${index * 120}ms` }}>
                  <div className="ml-pipeline-node">
                    <Icon size={18} />
                  </div>
                  <p>{step.label}</p>
                </div>
              )
            })}
          </div>
        </div>

        <div className="rounded-lg border border-slate-200 bg-slate-950 p-5 text-white shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold">Run comparison</h2>
              <p className="text-sm text-slate-400">Current run vs previous registered run.</p>
            </div>
            <Zap className="text-cyan-300" size={22} />
          </div>

          {runComparison ? (
            <div className="mt-5 grid grid-cols-3 gap-3">
              <div className="rounded-lg border border-white/10 bg-white/5 p-3">
                <p className="text-xs text-slate-400">MAE delta</p>
                <p className={`mt-1 text-2xl font-bold ${runComparison.maeDelta <= 0 ? 'text-emerald-300' : 'text-red-300'}`}>
                  {runComparison.maeDelta > 0 ? '+' : ''}
                  {runComparison.maeDelta}
                </p>
              </div>
              <div className="rounded-lg border border-white/10 bg-white/5 p-3">
                <p className="text-xs text-slate-400">RMSE delta</p>
                <p className={`mt-1 text-2xl font-bold ${runComparison.rmseDelta <= 0 ? 'text-emerald-300' : 'text-red-300'}`}>
                  {runComparison.rmseDelta > 0 ? '+' : ''}
                  {runComparison.rmseDelta}
                </p>
              </div>
              <div className="rounded-lg border border-white/10 bg-white/5 p-3">
                <p className="text-xs text-slate-400">R2 delta</p>
                <p className={`mt-1 text-2xl font-bold ${runComparison.r2Delta >= 0 ? 'text-emerald-300' : 'text-red-300'}`}>
                  {runComparison.r2Delta > 0 ? '+' : ''}
                  {runComparison.r2Delta}
                </p>
              </div>
            </div>
          ) : (
            <div className="mt-5 rounded-lg border border-white/10 bg-white/5 p-4">
              <p className="text-sm font-semibold text-slate-200">No previous run yet</p>
              <p className="mt-2 text-sm leading-6 text-slate-400">
                Retrain once more to compare MAE, RMSE, and R2 against the prior registered run.
              </p>
            </div>
          )}
        </div>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-950">Training data quality</h2>
            <p className="text-sm text-slate-500">
              Dataset completeness and freshness signals used before model training.
            </p>
          </div>
          <span className={`rounded-full px-3 py-1 text-xs font-bold ${freshnessClass[dataQuality?.freshness_status || 'no_data']}`}>
            {dataQuality ? formatFeatureName(dataQuality.freshness_status) : 'Unknown'}
          </span>
        </div>

        <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Records</p>
            <p className="mt-2 text-2xl font-black text-slate-950">{dataQuality?.total_records.toLocaleString() || '0'}</p>
          </div>
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Cities</p>
            <p className="mt-2 text-2xl font-black text-slate-950">{dataQuality?.monitored_cities || 0}</p>
          </div>
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Missing AQI</p>
            <p className="mt-2 text-2xl font-black text-slate-950">{dataQuality?.missing_aqi || 0}</p>
          </div>
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Missing weather</p>
            <p className="mt-2 text-2xl font-black text-slate-950">{dataQuality?.missing_weather || 0}</p>
          </div>
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Missing ratio</p>
            <p className="mt-2 text-2xl font-black text-slate-950">
              {dataQuality ? `${(dataQuality.missing_ratio * 100).toFixed(1)}%` : '0.0%'}
            </p>
          </div>
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Synthetic rows</p>
            <p className="mt-2 text-2xl font-black text-slate-950">{dataQuality?.synthetic_rows_last_run || 0}</p>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        {metricCards.map((metric) => {
          const Icon = metric.icon
          return (
            <div key={metric.label} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <div className={`inline-flex rounded-lg bg-gradient-to-br ${metric.tone} p-3 text-white`}>
                <Icon size={22} />
              </div>
              <p className="mt-5 text-sm font-medium text-slate-500">{metric.label}</p>
              <p className="mt-1 text-3xl font-bold text-slate-950">{metric.value}</p>
              <p className="mt-2 text-sm text-slate-500">{metric.detail}</p>
            </div>
          )
        })}
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-950">Prediction quality</h2>
            <p className="text-sm text-slate-500">
              Actual AQI vs predicted AQI from the model test split.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-3 sm:min-w-[280px]">
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Avg error</p>
              <p className="mt-1 text-2xl font-bold text-slate-950">{evaluationSummary.averageError}</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Max error</p>
              <p className="mt-1 text-2xl font-bold text-slate-950">{evaluationSummary.maxError}</p>
            </div>
          </div>
        </div>

        <div className="mt-6 h-[340px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={evaluationSamples} margin={{ top: 10, right: 18, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="sample" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} width={42} />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="actual_aqi"
                name="Actual AQI"
                stroke="#0f172a"
                strokeWidth={3}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="predicted_aqi"
                name="Predicted AQI"
                stroke="#06b6d4"
                strokeWidth={3}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-[1fr_0.9fr]">
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-950">Feature importance</h2>
              <p className="text-sm text-slate-500">Permutation importance from the trained model.</p>
            </div>
            <GitBranch className="text-slate-400" size={22} />
          </div>

          <div className="mt-6 h-[360px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topFeatures} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis type="number" />
                <YAxis dataKey="feature" type="category" width={120} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="importance" radius={[0, 8, 8, 0]} fill="#0f172a" name="Importance" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-950">Training contract</h2>
              <p className="text-sm text-slate-500">Inputs used by the AQI forecasting pipeline.</p>
            </div>
            <Timer className="text-slate-400" size={22} />
          </div>

          <div className="mt-5 grid grid-cols-2 gap-3">
            {(metrics?.features || []).map((feature) => (
              <div key={feature} className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                <p className="text-sm font-bold text-slate-800">{formatFeatureName(feature)}</p>
                <p className="mt-1 text-xs text-slate-500">model feature</p>
              </div>
            ))}
          </div>

          <div className="mt-5 rounded-lg border border-cyan-200 bg-cyan-50 p-4">
            <div className="flex items-center gap-2 text-cyan-700">
              <Activity size={18} />
              <p className="text-sm font-bold">Pipeline note</p>
            </div>
            <p className="mt-2 text-sm leading-6 text-cyan-800">
              The current model trains from PostgreSQL demo records. Synthetic hourly history is used
              until a larger verified AQI ingestion pipeline is connected.
            </p>
          </div>

          {metrics?.validation_strategy && (
            <div className="mt-4 rounded-lg border border-slate-200 bg-white p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Validation strategy</p>
              <p className="mt-1 text-sm font-bold text-slate-900">
                {formatFeatureName(metrics.validation_strategy)}
              </p>
              {metrics.test_window_start && metrics.test_window_end && (
                <p className="mt-2 text-xs leading-5 text-slate-500">
                  Test window: {new Date(metrics.test_window_start).toLocaleDateString()} to{' '}
                  {new Date(metrics.test_window_end).toLocaleDateString()}
                </p>
              )}
            </div>
          )}
        </div>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-950">Prediction explanations</h2>
            <p className="text-sm text-slate-500">
              Top forecast drivers for the highest-risk city predictions.
            </p>
          </div>
          <div className="inline-flex items-center gap-2 rounded-md bg-cyan-50 px-3 py-2 text-sm font-bold text-cyan-700">
            <Lightbulb size={16} />
            Explainability layer
          </div>
        </div>

        <div className="mt-5 grid grid-cols-1 gap-4 xl:grid-cols-2">
          {forecastExplanations.map((item, index) => {
            const riskTone = riskClass[item.risk_level as keyof typeof riskClass] || riskClass.Fair
            return (
              <div
                key={item.city}
                className="ml-explanation-card rounded-lg border border-slate-200 bg-slate-50 p-4"
                style={{ animationDelay: `${index * 110}ms` }}
              >
                <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="text-lg font-black text-slate-950">{item.city}</h3>
                      <span className={`rounded-full border px-3 py-1 text-xs font-bold ${riskTone}`}>
                        {item.risk_level}
                      </span>
                    </div>
                    <p className="mt-2 text-sm leading-6 text-slate-600">{item.explanation_summary}</p>
                  </div>
                  <div className="rounded-lg bg-white px-4 py-3 text-right shadow-sm">
                    <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Predicted AQI</p>
                    <p className="text-2xl font-black text-slate-950">{item.predicted_aqi_24h}</p>
                  </div>
                </div>

                <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-2">
                  {item.factors.map((factor) => (
                    <div key={`${item.city}-${factor.feature}`} className="rounded-lg border border-slate-200 bg-white p-3">
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <p className="text-sm font-black text-slate-900">{factor.label}</p>
                          <p className="mt-1 text-xs leading-5 text-slate-500">{factor.reason}</p>
                        </div>
                        <span
                          className={`rounded-full px-2 py-1 text-[11px] font-bold ${
                            factor.direction === 'increases_risk'
                              ? 'bg-red-50 text-red-700'
                              : factor.direction === 'reduces_risk'
                                ? 'bg-emerald-50 text-emerald-700'
                                : 'bg-slate-100 text-slate-700'
                          }`}
                        >
                          {formatFeatureName(factor.direction)}
                        </span>
                      </div>
                      <div className="mt-3 flex items-center justify-between text-xs font-semibold text-slate-500">
                        <span>Value {factor.value}</span>
                        <span>Importance {factor.importance.toFixed(3)}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-950">Model run history</h2>
            <p className="text-sm text-slate-500">
              Recent retraining runs tracked by the local artifact registry.
            </p>
          </div>
          <div className="inline-flex items-center gap-2 rounded-md bg-slate-100 px-3 py-2 text-sm font-bold text-slate-700">
            <Database size={16} />
            {modelRuns.length} runs
          </div>
        </div>

        <div className="mt-5 overflow-x-auto">
          <table className="w-full min-w-[860px] text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-left text-xs uppercase tracking-wide text-slate-500">
                <th className="px-3 py-3">Run ID</th>
                <th className="px-3 py-3">Trained</th>
                <th className="px-3 py-3">Validation</th>
                <th className="px-3 py-3">Rows</th>
                <th className="px-3 py-3">MAE</th>
                <th className="px-3 py-3">RMSE</th>
                <th className="px-3 py-3">R2</th>
              </tr>
            </thead>
            <tbody>
              {modelRuns.slice(0, 8).map((run) => (
                <tr key={run.run_id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-4 font-mono text-xs font-bold text-slate-950">{run.run_id}</td>
                  <td className="px-3 py-4 text-slate-700">{new Date(run.trained_at).toLocaleString()}</td>
                  <td className="px-3 py-4 text-slate-700">{formatFeatureName(run.validation_strategy)}</td>
                  <td className="px-3 py-4 text-slate-700">
                    {run.training_rows.toLocaleString()} / {run.test_rows.toLocaleString()}
                  </td>
                  <td className="px-3 py-4 font-semibold text-slate-950">{run.mae.toFixed(2)}</td>
                  <td className="px-3 py-4 font-semibold text-slate-950">{run.rmse.toFixed(2)}</td>
                  <td className="px-3 py-4 font-semibold text-slate-950">{run.r2.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {alertResults.length > 0 && (
        <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-950">ML early-warning alert run</h2>
              <p className="text-sm text-slate-500">
                Forecast alerts are triggered only when predicted AQI crosses the configured threshold.
              </p>
            </div>
            <div className="flex flex-wrap gap-2 text-sm font-bold">
              <span className="rounded-md bg-orange-50 px-3 py-2 text-orange-700">
                {alertSummary.triggered} triggered
              </span>
              <span className="rounded-md bg-emerald-50 px-3 py-2 text-emerald-700">
                {alertSummary.emailsSent} emails sent
              </span>
            </div>
          </div>

          <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3">
            {alertResults.slice(0, 6).map((result) => (
              <div key={result.city} className="rounded-lg border border-slate-200 bg-slate-50 p-4">
                <div className="flex items-center justify-between gap-3">
                  <h3 className="font-bold text-slate-950">{result.city}</h3>
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-bold ${
                      result.alert_triggered
                        ? 'bg-orange-100 text-orange-700'
                        : 'bg-emerald-100 text-emerald-700'
                    }`}
                  >
                    {result.alert_triggered ? 'Triggered' : 'Clear'}
                  </span>
                </div>
                <p className="mt-2 text-sm text-slate-600">
                  Current {result.current_aqi} / predicted {result.predicted_aqi_24h}
                </p>
                <p className="mt-2 text-xs leading-5 text-slate-500">{result.message}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-950">24-hour city forecasts</h2>
            <p className="text-sm text-slate-500">Predictions generated by the saved model artifact.</p>
          </div>
          <div className="inline-flex items-center gap-2 rounded-md bg-slate-100 px-3 py-2 text-sm font-bold text-slate-700">
            <TrendingUp size={16} />
            {forecasts.length} forecasts
          </div>
        </div>

        <div className="mt-5 overflow-x-auto">
          <table className="w-full min-w-[860px] text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-left text-xs uppercase tracking-wide text-slate-500">
                <th className="px-3 py-3">City</th>
                <th className="px-3 py-3">Sample AQI</th>
                <th className="px-3 py-3">Predicted AQI</th>
                <th className="px-3 py-3">Change</th>
                <th className="px-3 py-3">Risk</th>
                <th className="px-3 py-3">Confidence</th>
              </tr>
            </thead>
            <tbody>
              {forecasts.map((forecast) => {
                const riskTone = riskClass[forecast.risk_level as keyof typeof riskClass] || riskClass.Fair
                return (
                  <tr key={forecast.city} className="border-b border-slate-100 hover:bg-slate-50">
                    <td className="px-3 py-4 font-bold text-slate-950">{forecast.city}</td>
                    <td className="px-3 py-4 text-slate-700">{forecast.current_aqi}</td>
                    <td className="px-3 py-4 font-bold text-slate-950">{forecast.predicted_aqi_24h}</td>
                    <td className={`px-3 py-4 font-semibold ${forecast.change >= 0 ? 'text-red-600' : 'text-emerald-600'}`}>
                      {forecast.change >= 0 ? '+' : ''}
                      {forecast.change}
                    </td>
                    <td className="px-3 py-4">
                      <span className={`rounded-full border px-3 py-1 text-xs font-bold ${riskTone}`}>
                        {forecast.risk_level}
                      </span>
                    </td>
                    <td className="px-3 py-4 text-slate-700">{Math.round(forecast.confidence * 100)}%</td>
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

export default ModelLab
