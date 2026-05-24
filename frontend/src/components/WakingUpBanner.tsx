import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'

export function WakingUpBanner() {
  const [visible, setVisible] = useState(false)
  const [attempt, setAttempt] = useState(0)
  const [failed, setFailed] = useState(false)
  const location = useLocation()

  // Don't show on login/register pages (they handle their own errors)
  const isAuthPage = location.pathname === '/login' || location.pathname === '/register'

  useEffect(() => {
    const onWaking = (e: Event) => {
      setVisible(true)
      setFailed(false)
      setAttempt((e as CustomEvent).detail.attempt)
    }
    const onFailed = () => {
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
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 bg-yellow-50 border border-yellow-300 text-yellow-800 px-5 py-3 rounded-lg shadow-md text-sm flex items-center gap-3">
      {!failed ? (
        <>
          <span className="animate-spin">⏳</span>
          <span>Backend is waking up (attempt {attempt}/4) — this takes ~30s on first load…</span>
        </>
      ) : (
        <div className="flex items-center gap-3 w-full">
          <span>❌</span>
          <div>
            <p className="font-medium">Server took too long to respond.</p>
            <p className="text-xs mt-0.5 opacity-80">
              The backend is still waking up. Wait 30 seconds and:
            </p>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="ml-auto px-3 py-1 bg-amber-700 text-white rounded-lg text-xs font-medium
                       hover:bg-amber-800 whitespace-nowrap"
          >
            Reload page
          </button>
        </div>
      )}
    </div>
  )
}
