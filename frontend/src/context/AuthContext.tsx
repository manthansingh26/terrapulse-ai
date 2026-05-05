import React, { createContext, useState, useCallback, useEffect } from 'react'
import { apiClient, getApiErrorMessage, User } from '@/services/api'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  login: (username: string, password: string) => Promise<void>
  register: (email: string, username: string, password: string, fullName?: string) => Promise<void>
  logout: () => void
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Check if already logged in
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token')
      if (token) {
        try {
          const currentUser = await apiClient.getCurrentUser()
          setUser(currentUser)
        } catch (err) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        }
      }
      setIsLoading(false)
    }

    checkAuth()
  }, [])

  const login = useCallback(async (username: string, password: string) => {
    try {
      setError(null)
      const loginField = username.includes('@')
        ? { email: username, password }
        : { username, password }
      const response = await apiClient.login(loginField)
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)
      
      const currentUser = await apiClient.getCurrentUser()
      setUser(currentUser)
    } catch (err: unknown) {
      const message = getApiErrorMessage(err, 'Login failed')
      setError(message)
      throw err
    }
  }, [])

  const register = useCallback(async (email: string, username: string, password: string, fullName?: string) => {
    try {
      setError(null)
      await apiClient.register({ email, username, password, full_name: fullName })
      // Auto-login after registration
      await login(username, password)
    } catch (err: unknown) {
      const message = getApiErrorMessage(err, 'Registration failed')
      setError(message)
      throw err
    }
  }, [login])

  const logout = useCallback(() => {
    setUser(null)
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }, [])

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, isLoading, error, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
