export function AQICardSkeleton() {
  return (
    <div className="animate-pulse rounded-xl border border-gray-200 bg-white p-4 space-y-3">
      {/* Header with city name and badge */}
      <div className="flex justify-between items-start">
        <div className="h-5 bg-gray-200 rounded w-32" />
        <div className="h-5 bg-gray-200 rounded-full w-20" />
      </div>

      {/* Large AQI number */}
      <div className="h-12 bg-gray-200 rounded w-16" />

      {/* Status bar */}
      <div className="h-8 bg-gray-100 rounded w-full" />

      {/* Weather row */}
      <div className="flex gap-2">
        <div className="h-4 bg-gray-200 rounded flex-1" />
        <div className="h-4 bg-gray-200 rounded flex-1" />
      </div>

      {/* Advisory section */}
      <div className="space-y-2">
        <div className="h-3 bg-gray-100 rounded w-full" />
        <div className="h-3 bg-gray-100 rounded w-5/6" />
      </div>
    </div>
  )
}
