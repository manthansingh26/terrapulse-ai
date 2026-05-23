import { Database, Wifi } from 'lucide-react'

const DataSourceNotice = () => (
  <div className="rounded-lg border border-emerald-200 bg-emerald-50/80 backdrop-blur-sm p-4 text-sm text-emerald-950 shadow-sm transition-all hover:shadow-md">
    <div className="flex items-start gap-3">
      <div className="relative mt-1 shrink-0 flex h-3 w-3">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
        <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
      </div>
      <div>
        <p className="font-bold flex items-center gap-2 text-emerald-900">
          Live Environmental Ingestion Pipeline Active
          <span className="text-xs bg-emerald-100 text-emerald-800 font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider">WAQI Real-time</span>
        </p>
        <p className="mt-1.5 leading-relaxed text-emerald-800">
          This system is directly connected to the <strong>World Air Quality Index (WAQI)</strong> API. Environmental telemetries—including real-time AQI levels, pollutant counts, temperature, wind speed, and humidity—are synchronized automatically every 30 minutes via background scheduling daemons to support continuous ML prediction.
        </p>
      </div>
    </div>
  </div>
)

export default DataSourceNotice
