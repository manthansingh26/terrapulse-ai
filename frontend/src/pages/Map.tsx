import React, { useEffect, useMemo, useState } from 'react'
import { CircleMarker, MapContainer, Popup, TileLayer, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { apiClient, City } from '@/services/api'
import DataSourceNotice from '@/components/DataSourceNotice'
import {
  AlertCircle,
  Building2,
  CloudSun,
  Crosshair,
  Droplets,
  LocateFixed,
  MapPin,
  Radio,
  Search,
  ShieldAlert,
  Thermometer,
  Wind,
  X,
  Zap,
} from 'lucide-react'

type RiskFilter = 'all' | 'elevated' | 'critical'

const mapTileLayer = {
  url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  attribution: '&copy; OpenStreetMap contributors',
}

const getAQIMarkerColor = (aqi?: number) => {
  if (!aqi) return '#64748b'
  if (aqi <= 50) return '#10b981'
  if (aqi <= 100) return '#f59e0b'
  if (aqi <= 200) return '#f97316'
  if (aqi <= 300) return '#ef4444'
  return '#7f1d1d'
}

const getAQILabel = (aqi?: number) => {
  if (!aqi) return 'No Data'
  if (aqi <= 50) return 'Good'
  if (aqi <= 100) return 'Fair'
  if (aqi <= 200) return 'Poor'
  if (aqi <= 300) return 'Unhealthy'
  return 'Severe'
}

const getRiskFilterMatch = (city: City, filter: RiskFilter) => {
  const aqi = city.current_aqi || 0
  if (filter === 'critical') return aqi > 200
  if (filter === 'elevated') return aqi > 100
  return true
}

const getMarkerRadius = (aqi?: number, selected = false) => {
  const base = selected ? 13 : 9
  if (!aqi) return base
  return Math.min(base + aqi / 55, selected ? 20 : 16)
}

const MapViewport: React.FC<{ cities: City[]; selectedCity: City | null }> = ({ cities, selectedCity }) => {
  const map = useMap()

  useEffect(() => {
    if (selectedCity) {
      map.flyTo([selectedCity.latitude, selectedCity.longitude], 7, { duration: 0.8 })
      return
    }

    if (cities.length > 0) {
      const bounds = L.latLngBounds(cities.map((city) => [city.latitude, city.longitude] as [number, number]))
      map.fitBounds(bounds, { padding: [44, 44] })
    }
  }, [cities, map, selectedCity])

  return null
}

const MapMarkers: React.FC<{
  cities: City[]
  selectedCity: City | null
  onCitySelect: (city: City) => void
}> = ({ cities, selectedCity, onCitySelect }) => (
  <>
    {cities.map((city) => {
      const color = getAQIMarkerColor(city.current_aqi)
      const isSelected = selectedCity?.city === city.city
      const radius = getMarkerRadius(city.current_aqi, isSelected)

      return (
        <React.Fragment key={city.city}>
          <CircleMarker
            center={[city.latitude, city.longitude]}
            radius={radius * 2.1}
            fillColor={color}
            color={color}
            opacity={0.12}
            fillOpacity={0.12}
            weight={1}
            interactive={false}
          />
          <CircleMarker
            center={[city.latitude, city.longitude]}
            radius={radius}
            fillColor={color}
            color={isSelected ? '#ffffff' : '#0f172a'}
            weight={isSelected ? 4 : 2}
            opacity={1}
            fillOpacity={0.92}
            eventHandlers={{ click: () => onCitySelect(city) }}
          >
            <Popup>
              <div className="min-w-56 p-2">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="text-base font-bold text-slate-950">{city.city}</h3>
                    <p className="text-xs font-medium text-slate-500">{getAQILabel(city.current_aqi)} demo AQI</p>
                  </div>
                  <span className="rounded-md px-2 py-1 text-sm font-bold text-white" style={{ backgroundColor: color }}>
                    {city.current_aqi || 'N/A'}
                  </span>
                </div>
                <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
                  <div className="rounded-md bg-slate-50 p-2">
                    <p className="text-slate-500">Temperature</p>
                    <p className="font-bold text-slate-950">{city.current_temperature?.toFixed(1) || '0.0'} C</p>
                  </div>
                  <div className="rounded-md bg-slate-50 p-2">
                    <p className="text-slate-500">Humidity</p>
                    <p className="font-bold text-slate-950">{city.current_humidity?.toFixed(0) || '0'}%</p>
                  </div>
                </div>
              </div>
            </Popup>
          </CircleMarker>
        </React.Fragment>
      )
    })}
  </>
)

const Map: React.FC = () => {
  const [cities, setCities] = useState<City[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedCity, setSelectedCity] = useState<City | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [riskFilter, setRiskFilter] = useState<RiskFilter>('all')
  const [lastUpdated, setLastUpdated] = useState('')

  useEffect(() => {
    const fetchCities = async () => {
      try {
        setIsLoading(true)
        const data = await apiClient.getAllCities()
        setCities(data)
        setLastUpdated(new Date().toLocaleTimeString())
      } catch (err) {
        setError('Failed to load map intelligence. Check backend and database connection.')
        console.error(err)
      } finally {
        setIsLoading(false)
      }
    }

    fetchCities()
  }, [])

  const filteredCities = useMemo(
    () =>
      cities.filter((city) => {
        const matchesSearch = city.city.toLowerCase().includes(searchQuery.toLowerCase())
        return matchesSearch && getRiskFilterMatch(city, riskFilter)
      }),
    [cities, riskFilter, searchQuery]
  )

  const sortedCities = useMemo(
    () => [...filteredCities].sort((a, b) => (b.current_aqi || 0) - (a.current_aqi || 0)),
    [filteredCities]
  )

  const topRiskCity = sortedCities[0] || null
  const unhealthyCities = cities.filter((city) => (city.current_aqi || 0) > 150)
  const criticalCities = cities.filter((city) => (city.current_aqi || 0) > 200)
  const avgAQI = cities.length
    ? Math.round(cities.reduce((sum, city) => sum + (city.current_aqi || 0), 0) / cities.length)
    : 0

  const handleFocusRisk = () => {
    setRiskFilter('elevated')
    setSearchQuery('')
    if (unhealthyCities.length > 0) setSelectedCity(unhealthyCities[0])
  }

  const handleResetView = () => {
    setSelectedCity(null)
    setRiskFilter('all')
    setSearchQuery('')
  }

  const metricCards = [
    { label: 'Cities online', value: cities.length, icon: Radio, tone: 'text-cyan-600 bg-cyan-50' },
    { label: 'Avg AQI', value: avgAQI, icon: CloudSun, tone: 'text-slate-700 bg-slate-100' },
    { label: 'Elevated risk', value: unhealthyCities.length, icon: ShieldAlert, tone: 'text-orange-600 bg-orange-50' },
    { label: 'Critical zones', value: criticalCities.length, icon: Zap, tone: 'text-red-600 bg-red-50' },
  ]

  if (isLoading) {
    return (
      <div className="space-y-5">
        <div className="h-24 rounded-lg bg-slate-200 animate-pulse" />
        <div className="h-[680px] rounded-lg bg-slate-200 animate-pulse" />
      </div>
    )
  }

  return (
    <div className="space-y-5 animate-fade-in">
      <DataSourceNotice />

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-5 xl:flex-row xl:items-end xl:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full bg-slate-950 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-cyan-300">
              <LocateFixed size={14} />
              Geospatial monitoring
            </div>
            <h1 className="mt-4 text-3xl font-bold text-slate-950 lg:text-4xl">Demo AQI map intelligence</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
              Explore city-level sample air quality across India with risk filters, demo readings,
              and operational context for each monitored location.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 xl:min-w-[560px]">
            {metricCards.map((metric) => {
              const Icon = metric.icon
              return (
                <div key={metric.label} className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                  <div className={`inline-flex rounded-md p-2 ${metric.tone}`}>
                    <Icon size={18} />
                  </div>
                  <p className="mt-3 text-2xl font-bold text-slate-950">{metric.value}</p>
                  <p className="text-xs font-medium text-slate-500">{metric.label}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {error && (
        <div className="flex items-center gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      <section className="grid grid-cols-1 gap-5 xl:grid-cols-[1fr_360px]">
        <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
          <div className="flex flex-col gap-3 border-b border-slate-200 p-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="relative min-w-0 flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
              <input
                type="text"
                placeholder="Search a city"
                value={searchQuery}
                onChange={(event) => setSearchQuery(event.target.value)}
                className="h-11 w-full rounded-md border border-slate-200 bg-slate-50 pl-10 pr-10 text-sm outline-none transition focus:border-cyan-500 focus:bg-white focus:ring-2 focus:ring-cyan-100"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                  aria-label="Clear search"
                >
                  <X size={17} />
                </button>
              )}
            </div>

            <div className="flex flex-wrap gap-2">
              {(['all', 'elevated', 'critical'] as RiskFilter[]).map((filter) => (
                <button
                  key={filter}
                  onClick={() => setRiskFilter(filter)}
                  className={`rounded-md px-3 py-2 text-sm font-semibold capitalize transition ${
                    riskFilter === filter
                      ? 'bg-slate-950 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {filter}
                </button>
              ))}
            </div>

            <button
              onClick={handleFocusRisk}
              className="inline-flex items-center justify-center gap-2 rounded-md bg-orange-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-orange-700"
            >
              <Crosshair size={17} />
              Focus risk
            </button>
          </div>

          <div className="relative h-[720px] bg-slate-100">
            <MapContainer
              center={[22.8, 78.9]}
              zoom={5}
              style={{ height: '100%', width: '100%' }}
              zoomControl={false}
            >
              <TileLayer
                url={mapTileLayer.url}
                attribution={mapTileLayer.attribution}
              />
              <MapViewport cities={filteredCities} selectedCity={selectedCity} />
              <MapMarkers cities={filteredCities} selectedCity={selectedCity} onCitySelect={setSelectedCity} />
            </MapContainer>

            <div className="absolute left-4 top-4 z-[900] rounded-lg border border-white/80 bg-white/95 px-4 py-3 shadow-lg backdrop-blur">
              <div className="flex items-center gap-3">
                <div className="relative flex h-10 w-10 items-center justify-center rounded-full bg-cyan-50 text-cyan-700">
                  <span className="absolute h-10 w-10 animate-ping rounded-full bg-cyan-300/30" />
                  <Radio size={18} />
                </div>
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Demo city map</p>
                  <p className="text-sm font-semibold text-slate-950">Sample AQI overlay active</p>
                </div>
              </div>
            </div>

            <div className="absolute bottom-4 left-4 z-[900] w-[min(430px,calc(100%-2rem))] rounded-lg border border-white/70 bg-white/95 p-4 shadow-lg backdrop-blur">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Network status</p>
                  <p className="mt-1 text-sm font-semibold text-slate-950">
                    Showing {filteredCities.length} of {cities.length} monitored cities
                  </p>
                </div>
                <button onClick={handleResetView} className="rounded-md bg-slate-100 px-3 py-2 text-xs font-bold text-slate-700 hover:bg-slate-200">
                  Reset
                </button>
              </div>
              <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-100">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-emerald-500 via-orange-500 to-red-600"
                  style={{ width: `${Math.min((avgAQI / 220) * 100, 100)}%` }}
                />
              </div>
              <div className="mt-3 flex flex-wrap gap-3 text-xs font-medium text-slate-500">
                <span>Last refresh: {lastUpdated || 'loading'}</span>
                <span>Highest risk: {topRiskCity?.city || 'N/A'}</span>
              </div>
            </div>

            {selectedCity && (
              <div className="absolute right-4 top-4 z-[900] w-[min(360px,calc(100%-2rem))] rounded-lg border border-white/70 bg-white/95 p-5 shadow-xl backdrop-blur">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Selected city</p>
                    <h2 className="mt-1 text-2xl font-bold text-slate-950">{selectedCity.city}</h2>
                  </div>
                  <button
                    onClick={() => setSelectedCity(null)}
                    className="rounded-md p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
                    aria-label="Close city panel"
                  >
                    <X size={18} />
                  </button>
                </div>

                <div className="mt-5 rounded-lg p-4 text-white" style={{ backgroundColor: getAQIMarkerColor(selectedCity.current_aqi) }}>
                  <div className="flex items-end justify-between">
                    <div>
                      <p className="text-sm font-semibold opacity-90">Sample AQI</p>
                      <p className="mt-1 text-4xl font-bold">{selectedCity.current_aqi || 'N/A'}</p>
                    </div>
                    <p className="rounded-md bg-white/20 px-3 py-2 text-sm font-bold">{getAQILabel(selectedCity.current_aqi)}</p>
                  </div>
                </div>

                <div className="mt-4 grid grid-cols-2 gap-3">
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                    <div className="flex items-center gap-2 text-orange-600">
                      <Thermometer size={16} />
                      <span className="text-xs font-bold uppercase">Temp</span>
                    </div>
                    <p className="mt-2 text-xl font-bold text-slate-950">{selectedCity.current_temperature?.toFixed(1) || '0.0'} C</p>
                  </div>
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                    <div className="flex items-center gap-2 text-cyan-600">
                      <Droplets size={16} />
                      <span className="text-xs font-bold uppercase">Humidity</span>
                    </div>
                    <p className="mt-2 text-xl font-bold text-slate-950">{selectedCity.current_humidity?.toFixed(0) || '0'}%</p>
                  </div>
                </div>

                <div className="mt-4 rounded-lg border border-slate-200 p-3">
                  <div className="flex items-center gap-2 text-slate-500">
                    <MapPin size={16} />
                    <span className="text-xs font-bold uppercase">Coordinates</span>
                  </div>
                  <p className="mt-2 font-mono text-sm text-slate-700">
                    {selectedCity.latitude.toFixed(4)}, {selectedCity.longitude.toFixed(4)}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        <aside className="space-y-5">
          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-950">Risk queue</h2>
                <p className="text-sm text-slate-500">Highest AQI locations first.</p>
              </div>
              <Building2 className="text-slate-400" size={22} />
            </div>

            <div className="mt-4 space-y-3">
              {sortedCities.slice(0, 8).map((city, index) => (
                <button
                  key={city.city}
                  onClick={() => setSelectedCity(city)}
                  className={`w-full rounded-lg border p-3 text-left transition hover:border-cyan-300 hover:bg-cyan-50 ${
                    selectedCity?.city === city.city ? 'border-cyan-400 bg-cyan-50' : 'border-slate-200 bg-white'
                  }`}
                >
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex min-w-0 items-center gap-3">
                      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-slate-100 text-sm font-bold text-slate-700">
                        {index + 1}
                      </span>
                      <div className="min-w-0">
                        <p className="truncate font-bold text-slate-950">{city.city}</p>
                        <p className="text-xs font-medium text-slate-500">{getAQILabel(city.current_aqi)}</p>
                      </div>
                    </div>
                    <span className="rounded-md px-2 py-1 text-sm font-bold text-white" style={{ backgroundColor: getAQIMarkerColor(city.current_aqi) }}>
                      {city.current_aqi || 'N/A'}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-bold text-slate-950">Demo AQI legend</h2>
            <div className="mt-4 space-y-3">
              {[
                { label: 'Good', range: '0-50', color: '#10b981' },
                { label: 'Fair', range: '51-100', color: '#f59e0b' },
                { label: 'Poor', range: '101-200', color: '#f97316' },
                { label: 'Unhealthy', range: '201-300', color: '#ef4444' },
                { label: 'Severe', range: '300+', color: '#7f1d1d' },
              ].map((item) => (
                <div key={item.label} className="flex items-center justify-between rounded-md bg-slate-50 p-3">
                  <div className="flex items-center gap-3">
                    <span className="h-4 w-4 rounded-full" style={{ backgroundColor: item.color }} />
                    <span className="font-semibold text-slate-800">{item.label}</span>
                  </div>
                  <span className="text-xs font-bold text-slate-500">{item.range}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-lg border border-slate-200 bg-slate-950 p-5 text-white shadow-sm">
            <div className="flex items-center gap-3">
              <Wind className="text-cyan-300" size={22} />
              <h2 className="text-lg font-bold">Operational note</h2>
            </div>
            <p className="mt-3 text-sm leading-6 text-slate-300">
              Use the risk filters to inspect the demo scenario, then select a marker to review
              sample city conditions before moving into analytics or alert workflows.
            </p>
          </div>
        </aside>
      </section>
    </div>
  )
}

export default Map
