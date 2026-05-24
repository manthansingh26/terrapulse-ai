import React, { useEffect, useRef, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'

const getErrorStatus = (error: unknown) => {
  if (typeof error === 'object' && error !== null && 'response' in error) {
    return (error as { response?: { status?: number } }).response?.status
  }

  return undefined
}

const getErrorMessage = (error: unknown) => {
  if (typeof error === 'object' && error !== null) {
    const apiError = error as { response?: { data?: { detail?: string } }; message?: string }
    return apiError.response?.data?.detail || apiError.message
  }

  return undefined
}

const isWakeUpError = (error: unknown) => {
  const status = getErrorStatus(error)
  const hasResponse = Boolean(
    typeof error === 'object' &&
      error !== null &&
      'response' in error &&
      (error as { response?: unknown }).response
  )

  return !hasResponse || [502, 503, 504].includes(status || 0)
}

const Login: React.FC = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [countdown, setCountdown] = useState<number | null>(null)
  const retryTimerRef = useRef<number | null>(null)
  const { login } = useAuth()
  const navigate = useNavigate()

  const clearCountdown = () => {
    if (retryTimerRef.current !== null) {
      window.clearInterval(retryTimerRef.current)
      retryTimerRef.current = null
    }
    setCountdown(null)
  }

  const runLogin = async (loginUsername: string, loginPassword: string) => {
    setError('')
    setIsLoading(true)

    try {
      await login(loginUsername, loginPassword)
      clearCountdown()
      navigate('/')
    } catch (err: unknown) {
      const status = getErrorStatus(err)

      if (isWakeUpError(err)) {
        setError('Server is still waking up. Please wait 30 seconds and try again, or click "Try again now".')
        scheduleAutoRetry(loginUsername, loginPassword)
      } else if (status === 401) {
        clearCountdown()
        setError('Invalid username or password. Demo credentials: demo / demo123')
      } else {
        clearCountdown()
        setError(getErrorMessage(err) || 'Login failed. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const scheduleAutoRetry = (retryUsername: string, retryPassword: string) => {
    clearCountdown()
    setCountdown(30)

    retryTimerRef.current = window.setInterval(() => {
      setCountdown((prev) => {
        if (prev === null) return null

        if (prev <= 1) {
          if (retryTimerRef.current !== null) {
            window.clearInterval(retryTimerRef.current)
            retryTimerRef.current = null
          }
          window.setTimeout(() => {
            void runLogin(retryUsername, retryPassword)
          }, 0)
          return null
        }

        return prev - 1
      })
    }, 1000)
  }

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault()
    clearCountdown()
    await runLogin(username, password)
  }

  const handleTryDemo = async (e: React.MouseEvent) => {
    e.preventDefault()
    clearCountdown()
    setUsername('demo')
    setPassword('demo123')
    setError('')
    await runLogin('demo', 'demo123')
  }

  const handleRetry = async (e: React.MouseEvent) => {
    e.preventDefault()
    clearCountdown()
    await runLogin(username, password)
  }

  useEffect(() => clearCountdown, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-700 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-xl p-8 card">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-blue-900">TerraPulse AI</h1>
            <p className="text-gray-600 text-sm mt-2">Environmental Monitoring System</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="rounded-lg bg-red-50 border-l-4 border-red-500 px-4 py-3 text-sm text-red-800">
                <div className="flex items-start gap-3">
                  <span className="text-red-600 text-lg mt-0.5 flex-shrink-0">!</span>
                  <div className="flex-1">
                    <p className="font-medium">{error}</p>
                    {error.includes('waking up') && (
                      <>
                        <button
                          type="button"
                          onClick={handleRetry}
                          className="mt-2 inline-block text-red-600 hover:text-red-700 underline text-xs font-semibold"
                        >
                          Try again now
                        </button>
                        {countdown !== null && (
                          <div className="mt-2">
                            <div className="flex justify-between text-xs text-gray-500 mb-1">
                              <span>Auto-retrying...</span>
                              <span>{countdown}s</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-1">
                              <div
                                className="bg-blue-500 h-1 rounded-full transition-all"
                                style={{ width: `${((30 - countdown) / 30) * 100}%` }}
                              />
                            </div>
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Username or Email
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => {
                  setUsername(e.target.value)
                  setError('')
                  clearCountdown()
                }}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none"
                placeholder="Enter your username"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value)
                  setError('')
                  clearCountdown()
                }}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none"
                placeholder="Enter your password"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>

            <button
              type="button"
              onClick={handleTryDemo}
              disabled={isLoading}
              className="w-full border border-gray-400 text-gray-600 hover:bg-gray-100 rounded px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Trying demo...' : 'Try Demo'}
            </button>
          </form>

          <p className="mt-4 text-center text-xs text-gray-500">
            No account? Click Try Demo to explore the dashboard.
          </p>

          <div className="mt-6 text-center">
            <p className="text-gray-600 text-sm">
              Do not have an account?{' '}
              <Link to="/register" className="text-blue-600 hover:underline font-semibold">
                Register here
              </Link>
            </p>
          </div>

          <div className="mt-6 p-4 bg-blue-50 rounded-lg text-sm text-gray-700">
            <p className="font-semibold mb-2">Demo Credentials:</p>
            <p>
              Username: <code className="bg-white px-2 py-1 rounded">demo</code>
            </p>
            <p>
              Password: <code className="bg-white px-2 py-1 rounded">demo123</code>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
