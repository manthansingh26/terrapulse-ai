import { API_BASE_URL } from '@/services/api'

/**
 * Pings the backend every 14 minutes to reduce Render free tier cold starts.
 */
export function startKeepAlive() {
  const ping = async () => {
    const controller = new AbortController()
    const timeout = window.setTimeout(() => controller.abort(), 5000)

    try {
      await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        signal: controller.signal,
      })
    } catch {
      // The next user-initiated API call still handles wake-up and retry UI.
    } finally {
      window.clearTimeout(timeout)
    }
  }

  void ping()

  const interval = window.setInterval(() => {
    void ping()
  }, 14 * 60 * 1000)

  return () => window.clearInterval(interval)
}
