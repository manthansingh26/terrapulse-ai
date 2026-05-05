import React, { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, AreaChart, Area } from 'recharts'
import { apiClient, City } from '@/services/api'
import { AlertCircle, TrendingUp, Thermometer, Droplets, Wind, Calendar, Filter, BarChart3, Activity, LineChart as LineChartIcon } from 'lucide-react'
import DataSourceNotice from '@/components/DataSourceNotice'

type TabType = 'charts' | 'trends' | 'comparison'

const Analytics: React.FC = () => {
  const [cities, setCities] = useState<City[]>([])
  const [selectedCity, setSelectedCity] = useState<string>('')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<TabType>('charts')
  const [dateRange, setDateRange] = useState({ from: '', to: '' })

  useEffect(() => {
    const fetchCities = async () => {
      try {
        setIsLoading(true)
        const data = await apiClient.getAllCities()
        setCities(data)
        if (data.length > 0) {
          setSelectedCity(data[0].city)
        }
      } catch (err) {
        setError('Failed to load analytics data')
        console.error(err)
      } finally {
        setIsLoading(false)
      }
    }

    fetchCities()
  }, [])

  const selectedCityData = cities.find((c) => c.city === selectedCity)

  const lineChartData = [
    { time: '06:00', aqi: 85, temp: 24, humidity: 65 },
    { time: '09:00', aqi: 110, temp: 28, humidity: 58 },
    { time: '12:00', aqi: 145, temp: 32, humidity: 45 },
    { time: '15:00', aqi: 168, temp: 35, humidity: 38 },
    { time: '18:00', aqi: 142, temp: 30, humidity: 52 },
    { time: '21:00', aqi: 95, temp: 26, humidity: 62 },
    { time: '00:00', aqi: 78, temp: 23, humidity: 70 },
  ]

  const pieChartData = [
    { name: 'Good (0-50)', value: cities.filter((c) => c.current_aqi && c.current_aqi <= 50).length, color: '#10b981' },
    { name: 'Fair (51-100)', value: cities.filter((c) => c.current_aqi && c.current_aqi > 50 && c.current_aqi <= 100).length, color: '#fbbf24' },
    { name: 'Poor (101-200)', value: cities.filter((c) => c.current_aqi && c.current_aqi > 100 && c.current_aqi <= 200).length, color: '#f97316' },
    { name: 'Unhealthy (200+)', value: cities.filter((c) => c.current_aqi && c.current_aqi > 200).length, color: '#ef4444' },
  ]

  const scatterData = cities.filter((c) => c.current_temperature && c.current_humidity).map((c) => ({
    name: c.city,
    temp: c.current_temperature || 0,
    humidity: c.current_humidity || 0,
  }))

  const topCitiesData = cities
    .filter((c) => c.current_aqi)
    .sort((a, b) => (b.current_aqi || 0) - (a.current_aqi || 0))
    .slice(0, 5)
    .map((city) => ({
      name: city.city,
      aqi: city.current_aqi || 0,
      color: city.current_aqi! <= 50 ? '#10b981' : city.current_aqi! <= 100 ? '#fbbf24' : city.current_aqi! <= 200 ? '#f97316' : '#ef4444',
    }))

  const summaryStats = {
    highestAQI: Math.max(...cities.filter(c => c.current_aqi).map(c => c.current_aqi || 0)),
    lowestAQI: Math.min(...cities.filter(c => c.current_aqi).map(c => c.current_aqi || 0)),
    avgTemp: cities.filter(c => c.current_temperature).reduce((sum, c) => sum + (c.current_temperature || 0), 0) / cities.filter(c => c.current_temperature).length,
    avgHumidity: cities.filter(c => c.current_humidity).reduce((sum, c) => sum + (c.current_humidity || 0), 0) / cities.filter(c => c.current_humidity).length,
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8 animate-fade-in">
      <DataSourceNotice />

      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 flex items-center gap-3">
            <span className="text-3xl">📈</span> Analytics
          </h1>
          <p className="text-gray-600 mt-2">Detailed analysis of sample environmental records and demo trends</p>
        </div>

        {/* Date Range Picker */}
        <div className="flex items-center gap-4 bg-white rounded-xl px-4 py-2 shadow">
          <Calendar className="text-gray-400" size={20} />
          <input
            type="date"
            value={dateRange.from}
            onChange={(e) => setDateRange({ ...dateRange, from: e.target.value })}
            className="text-sm border-none outline-none text-gray-700"
          />
          <span className="text-gray-400">to</span>
          <input
            type="date"
            value={dateRange.to}
            onChange={(e) => setDateRange({ ...dateRange, to: e.target.value })}
            className="text-sm border-none outline-none text-gray-700"
          />
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle className="text-red-600" size={20} />
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Summary Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card p-5 bg-gradient-to-br from-red-50 to-orange-50 border border-red-100">
          <div className="flex items-center gap-2 text-red-600 mb-2">
            <Wind size={18} />
            <span className="text-sm font-medium">Highest demo AQI</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{summaryStats.highestAQI}</p>
          <p className="text-xs text-gray-500 mt-1">
            {cities.find(c => c.current_aqi === summaryStats.highestAQI)?.city}
          </p>
        </div>
        <div className="card p-5 bg-gradient-to-br from-green-50 to-emerald-50 border border-green-100">
          <div className="flex items-center gap-2 text-green-600 mb-2">
            <Activity size={18} />
            <span className="text-sm font-medium">Lowest demo AQI</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{summaryStats.lowestAQI}</p>
          <p className="text-xs text-gray-500 mt-1">
            {cities.find(c => c.current_aqi === summaryStats.lowestAQI)?.city}
          </p>
        </div>
        <div className="card p-5 bg-gradient-to-br from-orange-50 to-amber-50 border border-orange-100">
          <div className="flex items-center gap-2 text-orange-600 mb-2">
            <Thermometer size={18} />
            <span className="text-sm font-medium">Avg Temp</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{summaryStats.avgTemp.toFixed(1)}°C</p>
        </div>
        <div className="card p-5 bg-gradient-to-br from-cyan-50 to-blue-50 border border-cyan-100">
          <div className="flex items-center gap-2 text-cyan-600 mb-2">
            <Droplets size={18} />
            <span className="text-sm font-medium">Avg Humidity</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{summaryStats.avgHumidity.toFixed(0)}%</p>
        </div>
      </div>

      {/* Tab Buttons */}
      <div className="flex gap-2 border-b border-gray-200">
        <button
          onClick={() => setActiveTab('charts')}
          className={`tab-button flex items-center gap-2 ${activeTab === 'charts' ? 'tab-button-active' : ''}`}
        >
          <BarChart3 size={18} />
          Charts
        </button>
        <button
          onClick={() => setActiveTab('trends')}
          className={`tab-button flex items-center gap-2 ${activeTab === 'trends' ? 'tab-button-active' : ''}`}
        >
          <TrendingUp size={18} />
          Trends
        </button>
        <button
          onClick={() => setActiveTab('comparison')}
          className={`tab-button flex items-center gap-2 ${activeTab === 'comparison' ? 'tab-button-active' : ''}`}
        >
          <Filter size={18} />
          Comparison
        </button>
      </div>

      {/* City Selector */}
      <div className="card p-6">
        <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">Select City</h2>
            <select
              value={selectedCity}
              onChange={(e) => setSelectedCity(e.target.value)}
              className="px-6 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-cyan-500 focus:border-transparent outline-none text-lg font-medium bg-white shadow-sm"
            >
              {cities.map((city) => (
                <option key={city.city} value={city.city}>
                  {city.city}
                </option>
              ))}
            </select>
          </div>

          {selectedCityData && (
            <div className="flex gap-4">
              <div className="px-6 py-3 bg-gradient-to-br from-cyan-50 to-blue-50 rounded-xl border border-cyan-100">
                <p className="text-xs text-cyan-600 font-medium">Demo AQI</p>
                <p className="text-2xl font-bold text-gray-900">{selectedCityData.current_aqi || 'N/A'}</p>
              </div>
              <div className="px-6 py-3 bg-gradient-to-br from-orange-50 to-amber-50 rounded-xl border border-orange-100">
                <p className="text-xs text-orange-600 font-medium">Temperature</p>
                <p className="text-2xl font-bold text-gray-900">{selectedCityData.current_temperature?.toFixed(1)}°C</p>
              </div>
              <div className="px-6 py-3 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border border-purple-100">
                <p className="text-xs text-purple-600 font-medium">Humidity</p>
                <p className="text-2xl font-bold text-gray-900">{selectedCityData.current_humidity?.toFixed(0)}%</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'charts' && (
        <>
          {/* Time Series Chart */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
              <LineChartIcon className="text-cyan-600" size={20} />
              Demo AQI & Temperature Trend
            </h2>
            <ResponsiveContainer width="100%" height={350}>
              <AreaChart data={lineChartData}>
                <defs>
                  <linearGradient id="colorAqi" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="time" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'white',
                    borderRadius: '12px',
                    boxShadow: '0 4px 20px rgba(0,0,0,0.15)',
                    border: 'none',
                  }}
                />
                <Legend />
                <Area yAxisId="left" type="monotone" dataKey="aqi" stroke="#ef4444" fill="url(#colorAqi)" name="Demo AQI" strokeWidth={3} />
                <Area yAxisId="right" type="monotone" dataKey="temp" stroke="#f59e0b" fill="url(#colorTemp)" name="Temperature (°C)" strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* AQI Distribution & Top Cities */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-6">Demo AQI Status Distribution</h2>
              <div className="flex items-center justify-center">
                <ResponsiveContainer width="100%" height={280}>
                  <PieChart>
                    <Pie
                      data={pieChartData.filter((d) => d.value > 0)}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={4}
                      dataKey="value"
                      stroke="#ffffff"
                      strokeWidth={3}
                    >
                      {pieChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'white',
                        borderRadius: '12px',
                        boxShadow: '0 4px 20px rgba(0,0,0,0.15)',
                        border: 'none',
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex flex-wrap justify-center gap-4 mt-4">
                {pieChartData.map((item) => (
                  <div key={item.name} className="flex items-center gap-2">
                    <div className="w-4 h-4 rounded-full shadow" style={{ backgroundColor: item.color }} />
                    <span className="text-sm font-medium text-gray-700">{item.name}: {item.value}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="card p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-6">Top 5 Highest Demo AQI Cities</h2>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={topCitiesData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis type="number" />
                  <YAxis dataKey="name" type="category" width={80} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'white',
                      borderRadius: '12px',
                      boxShadow: '0 4px 20px rgba(0,0,0,0.15)',
                      border: 'none',
                    }}
                  />
                  <Bar dataKey="aqi" radius={[0, 8, 8, 0]}>
                    {topCitiesData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}

      {activeTab === 'trends' && (
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Temperature & Humidity Correlation</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b-2 border-gray-200">
                  <th className="text-left py-3 px-4 font-bold text-gray-700">City</th>
                  <th className="text-left py-3 px-4 font-bold text-gray-700">Temperature</th>
                  <th className="text-left py-3 px-4 font-bold text-gray-700">Humidity</th>
                  <th className="text-left py-3 px-4 font-bold text-gray-700">Heat Index</th>
                </tr>
              </thead>
              <tbody>
                {scatterData.map((row) => (
                  <tr key={row.name} className="border-b border-gray-100 hover:bg-cyan-50 transition-colors">
                    <td className="py-3 px-4 font-semibold text-gray-900">{row.name}</td>
                    <td className="py-3 px-4">
                      <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full font-medium">{row.temp.toFixed(1)}°C</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-3 py-1 bg-cyan-100 text-cyan-700 rounded-full font-medium">{row.humidity.toFixed(0)}%</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-3 py-1 rounded-full font-medium ${
                        (row.temp / row.humidity) > 0.5 ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
                      }`}>
                        {(row.temp / row.humidity).toFixed(2)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'comparison' && (
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">City Comparison</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {cities
              .sort((a, b) => (b.current_aqi || 0) - (a.current_aqi || 0))
              .slice(0, 9)
              .map((city) => (
                <div
                  key={city.city}
                  className="p-4 rounded-xl border-2 transition-all hover:shadow-lg hover:scale-105"
                  style={{
                    borderColor: city.current_aqi! <= 50 ? '#10b981' :
                      city.current_aqi! <= 100 ? '#fbbf24' :
                      city.current_aqi! <= 200 ? '#f97316' : '#ef4444'
                  }}
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-bold text-gray-900">{city.city}</span>
                    <span className="text-2xl font-bold" style={{
                      color: city.current_aqi! <= 50 ? '#10b981' :
                        city.current_aqi! <= 100 ? '#fbbf24' :
                        city.current_aqi! <= 200 ? '#f97316' : '#ef4444'
                    }}>
                      {city.current_aqi}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>🌡️ {city.current_temperature?.toFixed(1)}°C</span>
                    <span>💧 {city.current_humidity?.toFixed(0)}%</span>
                  </div>
                  <div className="mt-3 h-2 rounded-full bg-gray-200 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all"
                      style={{
                        width: `${Math.min(((city.current_aqi || 0) / 300) * 100, 100)}%`,
                        backgroundColor: city.current_aqi! <= 50 ? '#10b981' :
                          city.current_aqi! <= 100 ? '#fbbf24' :
                          city.current_aqi! <= 200 ? '#f97316' : '#ef4444'
                      }}
                    />
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Analytics
