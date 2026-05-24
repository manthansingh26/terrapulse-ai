import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'

export function WakingUpBanner() {
  const [visible, setVisible] = useState(false)
  const [attempt, setAttempt] = useState(0)
  const [failed, setFailed] = useState(false)
  const location = useLocation()

  const isAuthPage = location.pathname === '/login' || location.pathname === '/register'

  useEffect(() => {
    const onWaking = (event: Event) => {
      setVisible(true)
      setFailed(false)
      setAttempt((event as CustomEvent).detail.attempt)
    }

    const onFailed = () => {
      setVisible(true)
      setFailed(true)
    }

    window.addEventListener('backend:waking', onWaking)
    window.addEventListener('backend:failed', onFailed)
    return () => {
      window.removeEventListener('backend:waking', onWaking)
      window.removeEventListener('backend:failed', onFailed)
    }
  }, [])

  if (!visible || isAuthPage) return null

  return (
    <div className="fixed bottom-4 left-1/2 z-50 w-[min(680px,calc(100%-2rem))] -translate-x-1/2 rounded-lg border border-yellow-300 bg-yellow-50 px-5 py-3 text-sm text-yellow-800 shadow-md">
      {failed ? (
        <div className="flex items-center justify-between gap-3 w-full flex-wrap">
          <div className="flex items-center gap-2">
            <span className="font-bold">!</span>
            <div>
              <p className="font-medium text-sm">
                Server could not be reached after 4 attempts.
              </p>
              <p className="text-xs opacity-75">
                Render free tier takes 60s on cold start. Please wait and reload.
              </p>
            </div>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-1.5 bg-amber-700 hover:bg-amber-800 text-white rounded-lg text-xs font-semibold whitespace-nowrap transition-colors"
          >
            Reload page
          </button>
        </div>
      ) : (
        <div className="flex items-center gap-3">
          <span className="h-4 w-4 animate-spin rounded-full border-2 border-yellow-300 border-t-yellow-700" />
          <span>Backend is waking up (attempt {attempt}/4) - this takes about 30s on first load.</span>
        </div>
      )}
    </div>
  )
}
