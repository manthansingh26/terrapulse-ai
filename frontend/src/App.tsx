import { lazy, Suspense } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '@/context/AuthContext'
import AppIntro from '@/components/AppIntro'
import ProtectedRoute from '@/components/ProtectedRoute'
import Layout from '@/components/Layout'
import { WakingUpBanner } from '@/components/WakingUpBanner'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import Login from '@/pages/Login'
import Register from '@/pages/Register'
import '@/styles/global.css'

const Dashboard = lazy(() => import('@/pages/Dashboard'))
const Map = lazy(() => import('@/pages/Map'))
const Analytics = lazy(() => import('@/pages/Analytics'))
const ModelLab = lazy(() => import('@/pages/ModelLab'))
const Profile = lazy(() => import('@/pages/Profile'))

const PageLoader = () => (
  <div className="flex h-screen items-center justify-center bg-slate-50">
    <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-cyan-500" />
  </div>
)

function App() {
  return (
    <Router>
      <AuthProvider>
        <WakingUpBanner />
        <AppIntro />
        <Suspense fallback={<PageLoader />}>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected routes */}
            <Route element={<Layout />}>
              <Route path="/" element={<ProtectedRoute><ErrorBoundary pageName="Dashboard"><Dashboard /></ErrorBoundary></ProtectedRoute>} />
              <Route path="/map" element={<ProtectedRoute><ErrorBoundary pageName="Map"><Map /></ErrorBoundary></ProtectedRoute>} />
              <Route path="/analytics" element={<ProtectedRoute><ErrorBoundary pageName="Analytics"><Analytics /></ErrorBoundary></ProtectedRoute>} />
              <Route path="/model-lab" element={<ProtectedRoute><ErrorBoundary pageName="ModelLab"><ModelLab /></ErrorBoundary></ProtectedRoute>} />
              <Route path="/profile" element={<ProtectedRoute><ErrorBoundary pageName="Profile"><Profile /></ErrorBoundary></ProtectedRoute>} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </AuthProvider>
    </Router>
  )
}

export default App
