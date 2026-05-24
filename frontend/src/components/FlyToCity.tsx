import { useState } from 'react'
import { useMap } from 'react-leaflet'
import { City } from '@/services/api'
import { Search, X } from 'lucide-react'

interface FlyToCityProps {
  cities: City[]
}

export function FlyToCity({ cities }: FlyToCityProps) {
  const map = useMap()
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState<City[]>([])
  const [isOpen, setIsOpen] = useState(false)

  const handleSearch = (value: string) => {
    setQuery(value)
    if (value.length > 0) {
      setSuggestions(
        cities
          .filter((c) => c.city.toLowerCase().includes(value.toLowerCase()))
          .slice(0, 6)
      )
      setIsOpen(true)
    } else {
      setSuggestions([])
      setIsOpen(false)
    }
  }

  const selectCity = (city: City) => {
    map.flyTo([city.latitude, city.longitude], 11, { duration: 1.2 })
    setQuery(city.city)
    setSuggestions([])
    setIsOpen(false)
  }

  const getAQIColor = (aqi?: number) => {
    if (!aqi) return 'bg-gray-100 text-gray-700'
    if (aqi <= 50) return 'bg-green-100 text-green-700'
    if (aqi <= 100) return 'bg-yellow-100 text-yellow-700'
    if (aqi <= 200) return 'bg-orange-100 text-orange-700'
    if (aqi <= 300) return 'bg-red-100 text-red-700'
    return 'bg-purple-100 text-purple-700'
  }

  return (
    <div className="w-full max-w-sm">
      <div className="relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input
            type="text"
            value={query}
            onChange={(e) => handleSearch(e.target.value)}
            onFocus={() => query.length > 0 && setIsOpen(true)}
            placeholder="Search city…"
            className="w-full pl-10 pr-9 py-2.5 rounded-lg border border-gray-300 shadow-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition"
          />
          {query && (
            <button
              onClick={() => {
                setQuery('')
                setSuggestions([])
                setIsOpen(false)
              }}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              <X size={18} />
            </button>
          )}
        </div>

        {isOpen && suggestions.length > 0 && (
          <ul className="absolute top-full mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden z-50">
            {suggestions.map((c) => (
              <li key={c.city}>
                <button
                  onClick={() => selectCity(c)}
                  className="w-full px-4 py-2.5 text-sm hover:bg-blue-50 text-left flex items-center justify-between transition"
                >
                  <span className="font-medium text-gray-900">{c.city}</span>
                  <span
                    className={`text-xs font-semibold px-2.5 py-1 rounded-full ${getAQIColor(
                      c.current_aqi
                    )}`}
                  >
                    AQI {c.current_aqi || 'N/A'}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
