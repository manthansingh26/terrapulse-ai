import { Database } from 'lucide-react'

const DataSourceNotice = () => (
  <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
    <div className="flex items-start gap-3">
      <Database className="mt-0.5 shrink-0 text-amber-700" size={18} />
      <div>
        <p className="font-bold">Demo data notice</p>
        <p className="mt-1 leading-6">
          AQI, weather, and forecast values are sample records generated for the portfolio demo.
          They are not official real-time city AQI readings. Real-time ingestion from WAQI,
          CPCB, or another verified provider is listed as a production upgrade.
        </p>
      </div>
    </div>
  </div>
)

export default DataSourceNotice
