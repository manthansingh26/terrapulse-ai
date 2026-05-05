import React, { useState } from 'react'
import { Outlet, Link, useNavigate } from 'react-router-dom'
import { BarChart3, FlaskConical, LineChart, LogOut, Map, Menu, UserCircle, X } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'

const Layout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = [
    { path: '/', label: 'Dashboard', icon: BarChart3 },
    { path: '/map', label: 'Map', icon: Map },
    { path: '/analytics', label: 'Analytics', icon: LineChart },
    { path: '/model-lab', label: 'Model Lab', icon: FlaskConical },
    { path: '/profile', label: 'Profile', icon: UserCircle },
  ]

  return (
    <div className="flex h-screen bg-slate-50">
      <aside
        className={`${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } fixed inset-y-0 left-0 z-50 w-64 bg-slate-950 text-white shadow-lg transform transition-transform duration-200 lg:translate-x-0 lg:static`}
      >
        <div className="flex h-full flex-col">
          <div className="flex items-center justify-between border-b border-white/10 p-6">
            <div>
              <h1 className="text-xl font-bold">TerraPulse AI</h1>
              <p className="text-xs font-semibold text-cyan-300">ML Operations Console</p>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="text-white hover:text-slate-300 lg:hidden"
              aria-label="Close sidebar"
            >
              <X size={24} />
            </button>
          </div>

          <nav className="flex-1 overflow-y-auto py-6">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className="flex items-center gap-3 px-6 py-3 text-sm font-medium text-slate-200 transition-colors hover:bg-white/10"
                  onClick={() => setSidebarOpen(false)}
                >
                  <Icon size={18} className="text-cyan-300" />
                  <span>{item.label}</span>
                </Link>
              )
            })}
          </nav>

          <div className="border-t border-white/10 p-6">
            <p className="text-xs font-medium uppercase tracking-wide text-slate-500">Signed in as</p>
            <p className="mt-1 truncate text-sm font-semibold text-white">{user?.username}</p>
          </div>
        </div>
      </aside>

      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="border-b border-slate-200 bg-white">
          <div className="flex items-center justify-between px-4 py-4 sm:px-6">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-slate-500 hover:text-slate-700 lg:hidden"
              aria-label="Open sidebar"
            >
              <Menu size={24} />
            </button>

            <div className="ml-auto flex items-center gap-4">
              <div className="hidden text-sm text-slate-600 sm:block">
                Welcome, <span className="font-semibold">{user?.full_name || user?.username}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-red-600 transition-colors hover:bg-red-50"
              >
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto">
          <div className="mx-auto max-w-[1500px] px-4 py-6 sm:px-6 lg:px-8">
            <Outlet />
          </div>
        </main>
      </div>

      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}

export default Layout
