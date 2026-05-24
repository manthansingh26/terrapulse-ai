import React, { createContext, useState, useCallback, useEffect } from 'react'
import {
  apiClient,
  clearAuthStorage,
  getApiErrorMessage,
  getUserFromToken,
  mergeUserWithToken,
  saveAuthSnapshot,
  User,
} from '@/services/api'

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
        const tokenUser = getUserFromToken(token)
        setUser(tokenUser)
        try {
          const currentUser = await apiClient.getCurrentUser()
          const mergedUser = mergeUserWithToken(currentUser, token)
          setUser(mergedUser)
          saveAuthSnapshot(token, mergedUser)
        } catch (err) {
          saveAuthSnapshot(token, tokenUser)
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

      const fallbackUser = getUserFromToken(response.access_token, username || 'User')
      setUser(fallbackUser)
      saveAuthSnapshot(response.access_token, fallbackUser)

      try {
        const currentUser = await apiClient.getCurrentUser()
        const mergedUser = mergeUserWithToken(currentUser, response.access_token, username || 'User')
        setUser(mergedUser)
        saveAuthSnapshot(response.access_token, mergedUser)
      } catch {
        // Login succeeded; keep the decoded token user if the profile endpoint is still waking up.
      }
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
    clearAuthStorage()
  }, [])

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, isLoading, error, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
