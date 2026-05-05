import React from 'react'
import { useAuth } from '@/hooks/useAuth'
import { Mail, User, Calendar, Shield } from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
const API_DOCS_URL = API_BASE_URL.replace(/\/api\/?$/, '/api/docs')

const Profile: React.FC = () => {
  const { user } = useAuth()

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900">Profile</h1>
        <p className="text-gray-600 mt-2">Manage your account information</p>
      </div>

      {/* Profile Card */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Profile */}
        <div className="lg:col-span-2 card p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Account Information</h2>

          <div className="space-y-6">
            {/* Username */}
            <div>
              <div className="flex items-center gap-3 mb-2">
                <User className="text-blue-600" size={20} />
                <label className="block text-sm font-semibold text-gray-700">Username</label>
              </div>
              <p className="bg-gray-100 px-4 py-3 rounded-lg text-gray-900 font-mono">{user?.username}</p>
            </div>

            {/* Email */}
            <div>
              <div className="flex items-center gap-3 mb-2">
                <Mail className="text-blue-600" size={20} />
                <label className="block text-sm font-semibold text-gray-700">Email Address</label>
              </div>
              <p className="bg-gray-100 px-4 py-3 rounded-lg text-gray-900">{user?.email}</p>
            </div>

            {/* Full Name */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
              <p className="bg-gray-100 px-4 py-3 rounded-lg text-gray-900">{user?.full_name || 'Not set'}</p>
            </div>

            {/* Account Status */}
            <div>
              <div className="flex items-center gap-3 mb-2">
                <Shield className="text-blue-600" size={20} />
                <label className="block text-sm font-semibold text-gray-700">Account Status</label>
              </div>
              <div className="flex gap-3">
                <span className={`px-4 py-2 rounded-lg font-semibold badge ${user?.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                  {user?.is_active ? 'Active' : 'Inactive'}
                </span>
                {user?.is_admin && <span className="px-4 py-2 rounded-lg font-semibold badge bg-blue-100 text-blue-800">Admin</span>}
              </div>
            </div>

            {/* Member Since */}
            <div>
              <div className="flex items-center gap-3 mb-2">
                <Calendar className="text-blue-600" size={20} />
                <label className="block text-sm font-semibold text-gray-700">Member Since</label>
              </div>
              <p className="bg-gray-100 px-4 py-3 rounded-lg text-gray-900">{formatDate(user?.created_at)}</p>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* User Avatar */}
          <div className="card p-6 text-center">
            <div className="w-24 h-24 mx-auto bg-gradient-to-br from-blue-600 to-blue-900 rounded-full flex items-center justify-center">
              <span className="text-4xl text-white font-bold">{(user?.username || 'U')[0].toUpperCase()}</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mt-4">{user?.full_name || user?.username}</h3>
            <p className="text-gray-600 text-sm mt-1">@{user?.username}</p>
          </div>

          {/* Quick Stats */}
          <div className="card p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Account Stats</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">User ID</span>
                <span className="font-mono font-semibold text-gray-900">{user?.id}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Account Type</span>
                <span className="font-semibold text-gray-900">{user?.is_admin ? 'Administrator' : 'Regular User'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Last Updated</span>
                <span className="font-semibold text-gray-900">{formatDate(user?.created_at)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* API Information */}
      <div className="card p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">API Information</h2>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">API Endpoint</h3>
              <code className="bg-white px-4 py-2 rounded-lg text-sm block text-gray-700 break-all">
                {API_BASE_URL}
              </code>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">API Documentation</h3>
              <a
                href={API_DOCS_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline text-sm"
              >
                View Swagger Documentation →
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Security Warning */}
      <div className="border-t pt-8">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h3 className="font-semibold text-yellow-900 mb-2">🔒 Security Tips</h3>
          <ul className="list-disc list-inside text-sm text-yellow-800 space-y-1">
            <li>Never share your login credentials</li>
            <li>Change your password regularly</li>
            <li>Log out when using shared computers</li>
            <li>Keep your email address up to date</li>
            <li>Use a strong, unique password</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Profile
