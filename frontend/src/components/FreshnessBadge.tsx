interface FreshnessBadgeProps {
  lastFetchedAt: string | null | undefined; // ISO datetime string
}

export function FreshnessBadge({ lastFetchedAt }: FreshnessBadgeProps) {
  if (!lastFetchedAt) {
    return (
      <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-gray-100 text-gray-700">
        📭 No data
      </span>
    )
  }

  const minutesAgo = Math.floor(
    (Date.now() - new Date(lastFetchedAt).getTime()) / 60000
  )

  const isStale = minutesAgo > 60
  const label =
    minutesAgo < 1 ? 'Just now' :
    minutesAgo < 60 ? `${minutesAgo}m ago` :
    `${Math.floor(minutesAgo / 60)}h ago`

  return (
    <span
      className={`text-xs px-2 py-0.5 rounded-full font-medium ${
        isStale
          ? 'bg-red-100 text-red-700'
          : 'bg-green-100 text-green-700'
      }`}
      title={`Data fetched: ${new Date(lastFetchedAt).toLocaleString()}`}
    >
      {isStale ? '⚠️ ' : '🟢 '}{label}
    </span>
  )
}
