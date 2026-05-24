import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'

const Login: React.FC = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await login(username, password)
      navigate('/')
    } catch (err: any) {
      setIsLoading(false)
      
      // Detect backend status from error
      const isNetworkError = !err.response
      const isColdStart = [502, 503, 504].includes(err.response?.status)
      const isUnauthorized = err.response?.status === 401

      if (isNetworkError || isColdStart) {
        setError(
          'Server is still waking up. Please wait 30 seconds and try again, ' +
          'or click "Try Demo" to auto-retry.'
        )
      } else if (isUnauthorized) {
        setError('Invalid username or password. Demo credentials: demo / demo123')
      } else {
        setError(
          err.response?.data?.detail ||
          err.message ||
          'Login failed. Please try again.'
        )
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleTryDemo = async (e: React.MouseEvent) => {
    e.preventDefault()
    setUsername('demo')
    setPassword('demo123')
    setError('')
    
    // Auto-submit after a brief delay to ensure state is updated
    setTimeout(async () => {
      try {
        setIsLoading(true)
        await login('demo', 'demo123')
        navigate('/')
      } catch (err: any) {
        setIsLoading(false)
        const isNetworkError = !err.response
        const isColdStart = [502, 503, 504].includes(err.response?.status)
        
        if (isNetworkError || isColdStart) {
          setError(
            'Server is still waking up. Please wait 30 seconds and try again, ' +
            'or click "Try Demo" to auto-retry.'
          )
        } else {
          setError(err.response?.data?.detail || 'Demo login failed. Please try again.')
        }
      }
    }, 100)
  }

  const handleRetry = async (e: React.MouseEvent) => {
    e.preventDefault()
    // Create a synthetic form event
    const form = { preventDefault: () => {} } as React.FormEvent
    await handleSubmit(form)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-700 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Card */}
        <div className="bg-white rounded-lg shadow-xl p-8 card">
          {/* Logo */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-blue-900">TerraPulse AI</h1>
            <p className="text-gray-600 text-sm mt-2">Environmental Monitoring System</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="rounded-lg bg-red-50 border-l-4 border-red-500 px-4 py-3 text-sm text-red-800">
                <div className="flex items-start gap-3">
                  <span className="text-red-600 text-lg mt-0.5 flex-shrink-0">⚠</span>
                  <div className="flex-1">
                    <p className="font-medium">{error}</p>
                    {error.includes('waking up') && (
                      <button
                        type="button"
                        onClick={handleRetry}
                        className="mt-2 inline-block text-red-600 hover:text-red-700 underline text-xs font-semibold"
                      >
                        Try again now →
                      </button>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Username */}
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
                }}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none"
                placeholder="Enter your username"
                required
              />
            </div>

            {/* Password */}
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
                }}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none"
                placeholder="Enter your password"
                required
              />
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>

            {/* Try Demo Button */}
            <button
              type="button"
              onClick={handleTryDemo}
              disabled={isLoading}
              className="w-full border border-gray-400 text-gray-600 hover:bg-gray-100 rounded px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Trying demo...' : 'Try Demo'}
            </button>
          </form>

          {/* Helper text */}
          <p className="mt-4 text-center text-xs text-gray-500">
            No account? Click Try Demo to explore the dashboard.
          </p>

          {/* Footer */}
          <div className="mt-6 text-center">
            <p className="text-gray-600 text-sm">
              Do not have an account?{' '}
              <Link to="/register" className="text-blue-600 hover:underline font-semibold">
                Register here
              </Link>
            </p>
          </div>

          {/* Demo credentials */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg text-sm text-gray-700">
            <p className="font-semibold mb-2">Demo Credentials:</p>
            <p>Username: <code className="bg-white px-2 py-1 rounded">demo</code></p>
            <p>Password: <code className="bg-white px-2 py-1 rounded">demo123</code></p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
