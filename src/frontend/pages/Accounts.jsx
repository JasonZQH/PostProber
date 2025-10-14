import React, { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import platformService from '../services/platformService'
import { BsTwitterX } from 'react-icons/bs'
import { FaLinkedin, FaInstagram, FaFacebookF } from 'react-icons/fa'

function Accounts() {
  const [activeTab, setActiveTab] = useState('connected')
  const [connectedAccounts, setConnectedAccounts] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchParams, setSearchParams] = useSearchParams()
  const [notification, setNotification] = useState(null)

  // All supported platforms with descriptions
  const allPlatforms = [
    {
      id: 'twitter',
      platform: 'X (Twitter)',
      icon: BsTwitterX,
      description: 'Connect to post and monitor engagement',
      color: '#000000',
      features: ['Post scheduling', 'Engagement tracking', 'Trend analysis']
    },
    {
      id: 'linkedin',
      platform: 'LinkedIn',
      icon: FaLinkedin,
      description: 'Share professional content and insights',
      color: '#0077B5',
      features: ['Professional networking', 'Company updates', 'Article publishing']
    },
    {
      id: 'instagram',
      platform: 'Instagram',
      icon: FaInstagram,
      description: 'Post photos, stories, and reels',
      color: '#E4405F',
      features: ['Photo & video posts', 'Stories', 'Reels scheduling']
    },
    {
      id: 'facebook',
      platform: 'Facebook',
      icon: FaFacebookF,
      description: 'Manage your Facebook page posts',
      color: '#1877F2',
      features: ['Page posting', 'Story scheduling', 'Audience insights']
    }
  ]

  // Handle OAuth callback
  useEffect(() => {
    const connected = searchParams.get('connected')
    const error = searchParams.get('error')

    if (connected) {
      setNotification({
        type: 'success',
        message: `Successfully connected ${connected}! 🎉`
      })

      // Refresh platforms after connection
      platformService.refreshPlatforms()

      // Clear query params
      setSearchParams({})

      // Auto-hide notification after 5 seconds
      setTimeout(() => setNotification(null), 5000)
    }

    if (error) {
      setNotification({
        type: 'error',
        message: `Failed to connect: ${error}`
      })

      // Clear query params
      setSearchParams({})

      // Auto-hide notification after 8 seconds
      setTimeout(() => setNotification(null), 8000)
    }
  }, [searchParams, setSearchParams])

  // Load connected platforms
  useEffect(() => {
    const platforms = platformService.getConnectedPlatforms()
    setConnectedAccounts(platforms)
    setIsLoading(false)

    const unsubscribe = platformService.subscribe((platforms) => {
      setConnectedAccounts(platforms)
      setIsLoading(false)
    })

    return unsubscribe
  }, [])

  // Get available platforms (not yet connected)
  const availablePlatforms = allPlatforms.filter(
    platform => !connectedAccounts.some(acc => acc.id === platform.id)
  )

  const getStatusBadge = (status) => {
    switch (status) {
      case 'active':
        return <span className="status-indicator status-success">🟢 Active</span>
      case 'warning':
        return <span className="status-indicator status-warning">🟡 Needs Attention</span>
      case 'error':
        return <span className="status-indicator status-danger">🔴 Error</span>
      case 'syncing':
        return <span className="status-indicator status-info">🔄 Syncing</span>
      default:
        return <span className="status-indicator">{status}</span>
    }
  }

  const handleConnect = async (platformId) => {
    try {
      // Initiate OAuth flow (will redirect to platform)
      await platformService.connectPlatform(platformId)
    } catch (error) {
      console.error(`Failed to connect ${platformId}:`, error)
      setNotification({
        type: 'error',
        message: `Failed to connect ${platformId}: ${error.message}`
      })
    }
  }

  const handleDisconnect = async (accountId) => {
    if (confirm(`Are you sure you want to disconnect this account?`)) {
      try {
        await platformService.disconnectPlatform(accountId)
        setNotification({
          type: 'success',
          message: `Successfully disconnected ${accountId}!`
        })
        setTimeout(() => setNotification(null), 5000)
      } catch (error) {
        console.error(`Failed to disconnect ${accountId}:`, error)
        setNotification({
          type: 'error',
          message: `Failed to disconnect ${accountId}: ${error.message}`
        })
      }
    }
  }

  const formatDate = (isoString) => {
    const date = new Date(isoString)
    const now = new Date()
    const diffMinutes = Math.floor((now - date) / 60000)

    if (diffMinutes < 1) return 'Just now'
    if (diffMinutes < 60) return `${diffMinutes} ${diffMinutes === 1 ? 'minute' : 'minutes'} ago`
    if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)} ${Math.floor(diffMinutes / 60) === 1 ? 'hour' : 'hours'} ago`
    return date.toLocaleDateString()
  }

  return (
    <div className="space-y-6">
      {/* Notification Banner */}
      {notification && (
        <div
          className={`card fade-in ${
            notification.type === 'success' ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
          }`}
          style={{ borderWidth: '1px' }}
        >
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-2xl">
                  {notification.type === 'success' ? '✅' : '❌'}
                </span>
                <p
                  className="font-medium"
                  style={{ color: notification.type === 'success' ? 'var(--accent-green)' : 'var(--error-red)' }}
                >
                  {notification.message}
                </p>
              </div>
              <button
                onClick={() => setNotification(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="fade-in">
        <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
          Social Media Accounts 🔗
        </h1>
        <p style={{ color: 'var(--gray-600)' }}>
          Manage your connected social media platforms and add new accounts
        </p>
      </div>

      {/* Account Summary */}
      {connectedAccounts.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card slide-up">
            <div className="card-content">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                    {connectedAccounts.length}
                  </div>
                  <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                    Connected Accounts
                  </div>
                </div>
                <div
                  className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-xl"
                  style={{ background: 'var(--primary-blue)' }}
                >
                  🔗
                </div>
              </div>
            </div>
          </div>

          <div className="card slide-up">
            <div className="card-content">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                    {allPlatforms.length}
                  </div>
                  <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                    Available Platforms
                  </div>
                </div>
                <div
                  className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-xl"
                  style={{ background: 'var(--accent-green)' }}
                >
                  ➕
                </div>
              </div>
            </div>
          </div>

          <div className="card slide-up">
            <div className="card-content">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                    {connectedAccounts.filter(acc => acc.status === 'connected').length}/{connectedAccounts.length}
                  </div>
                  <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                    Healthy Connections
                  </div>
                </div>
                <div
                  className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-xl"
                  style={{ background: 'var(--warning-orange)' }}
                >
                  ✅
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab Navigation */}
      <div className="card slide-up">
        <div className="card-content p-0">
          <div className="flex border-b" style={{ borderColor: 'var(--gray-200)' }}>
            <button
              onClick={() => setActiveTab('connected')}
              className={`px-6 py-4 font-medium transition-colors ${
                activeTab === 'connected'
                  ? 'border-b-2 text-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
              style={{
                borderBottomColor: activeTab === 'connected' ? 'var(--primary-blue)' : 'transparent'
              }}
            >
              🔗 Connected Accounts ({connectedAccounts.length})
            </button>
            <button
              onClick={() => setActiveTab('available')}
              className={`px-6 py-4 font-medium transition-colors ${
                activeTab === 'available'
                  ? 'border-b-2 text-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
              style={{
                borderBottomColor: activeTab === 'available' ? 'var(--primary-blue)' : 'transparent'
              }}
            >
              ➕ Add Platform ({availablePlatforms.length})
            </button>
          </div>
        </div>
      </div>

      {/* Connected Accounts Tab */}
      {activeTab === 'connected' && (
        <div className="space-y-4">
          {connectedAccounts.length === 0 ? (
            <div className="card">
              <div className="card-content">
                <div className="text-center py-16">
                  <div className="text-6xl mb-4">🔗</div>
                  <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
                    No Connected Accounts
                  </h2>
                  <p className="mb-6" style={{ color: 'var(--gray-600)' }}>
                    Connect your social media platforms to start managing your content
                  </p>
                  <button
                    onClick={() => setActiveTab('available')}
                    className="btn btn-primary"
                  >
                    <span>➕</span>
                    <span>Add Platform</span>
                  </button>
                </div>
              </div>
            </div>
          ) : (
            connectedAccounts.map((account, index) => (
              <div key={account.id} className="card slide-up" style={{ animationDelay: `${index * 100}ms` }}>
                <div className="card-content">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-4">
                      <div
                        className="w-16 h-16 rounded-xl flex items-center justify-center text-white"
                        style={{ background: account.color }}
                      >
                        {account.icon && <account.icon size={32} />}
                      </div>
                      <div>
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                            {account.name}
                          </h3>
                          {getStatusBadge(account.status)}
                        </div>
                        <p className="text-sm mb-1" style={{ color: 'var(--gray-600)' }}>
                          {account.username}
                        </p>
                        <p className="text-sm" style={{ color: 'var(--gray-500)' }}>
                          Connected {formatDate(account.connectedAt)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleDisconnect(account.id)}
                        className="btn btn-outline btn-sm text-red-600 border-red-300 hover:bg-red-50"
                      >
                        <span>🔌</span>
                        <span>Disconnect</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Available Platforms Tab */}
      {activeTab === 'available' && (
        <div>
          {availablePlatforms.length === 0 ? (
            <div className="card">
              <div className="card-content">
                <div className="text-center py-16">
                  <div className="text-6xl mb-4">🎉</div>
                  <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
                    All Platforms Connected!
                  </h2>
                  <p style={{ color: 'var(--gray-600)' }}>
                    You've connected all available platforms. Great job!
                  </p>
                </div>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {availablePlatforms.map((platform, index) => (
                <div key={platform.id} className="card slide-up" style={{ animationDelay: `${index * 100}ms` }}>
                  <div className="card-content">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-4">
                        <div
                          className="w-14 h-14 rounded-xl flex items-center justify-center text-white"
                          style={{ background: platform.color }}
                        >
                          <platform.icon size={28} />
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold mb-1" style={{ color: 'var(--gray-900)' }}>
                            {platform.platform}
                          </h3>
                          <p className="text-sm" style={{ color: 'var(--gray-600)' }}>
                            {platform.description}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="mb-4">
                      <h4 className="text-sm font-medium mb-2" style={{ color: 'var(--gray-700)' }}>
                        Features:
                      </h4>
                      <div className="space-y-1">
                        {platform.features.map((feature, idx) => (
                          <div key={idx} className="flex items-center gap-2 text-sm">
                            <span style={{ color: 'var(--accent-green)' }}>✓</span>
                            <span style={{ color: 'var(--gray-600)' }}>{feature}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <button
                      onClick={() => handleConnect(platform.id)}
                      className="w-full btn btn-primary"
                      style={{ background: platform.color, borderColor: platform.color }}
                    >
                      <span>🔗</span>
                      <span>Connect {platform.platform}</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Account Health Tips */}
      <div
        className="card slide-up"
        style={{ background: 'var(--gradient-cool)', color: 'white' }}
      >
        <div className="card-content">
          <div className="text-center">
            <div className="text-3xl mb-3">💡</div>
            <h3 className="font-semibold mb-2">Account Health Tips</h3>
            <div className="space-y-2 text-sm opacity-90">
              <p>• Keep your accounts active by posting regularly</p>
              <p>• Check connection status daily to avoid missed posts</p>
              <p>• Refresh tokens when you see warning indicators</p>
              <p>• Monitor engagement rates across all platforms</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Accounts