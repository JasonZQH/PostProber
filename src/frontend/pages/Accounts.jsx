import React, { useState } from 'react'

function Accounts() {
  const [activeTab, setActiveTab] = useState('connected')

  const connectedAccounts = [
    {
      id: 1,
      platform: 'Twitter',
      icon: '🐦',
      username: '@postprober',
      displayName: 'PostProber',
      followers: '12.4K',
      status: 'active',
      lastSync: '2 minutes ago',
      color: '#1DA1F2',
      posts: 247,
      engagement: '8.2%'
    },
    {
      id: 2,
      platform: 'LinkedIn',
      icon: '💼',
      username: 'postprober-company',
      displayName: 'PostProber Inc.',
      followers: '8.9K',
      status: 'active',
      lastSync: '5 minutes ago',
      color: '#0077B5',
      posts: 156,
      engagement: '9.1%'
    },
    {
      id: 3,
      platform: 'Instagram',
      icon: '📷',
      username: '@postprober.app',
      displayName: 'PostProber',
      followers: '5.2K',
      status: 'warning',
      lastSync: '2 hours ago',
      color: '#E4405F',
      posts: 89,
      engagement: '7.8%'
    }
  ]

  const availablePlatforms = [
    {
      platform: 'Facebook',
      icon: '📘',
      description: 'Connect your Facebook Page to schedule and manage posts',
      color: '#1877F2',
      features: ['Page posting', 'Story scheduling', 'Audience insights'],
      isPopular: false
    },
    {
      platform: 'TikTok',
      icon: '🎵',
      description: 'Share engaging short-form videos with your TikTok audience',
      color: '#000000',
      features: ['Video scheduling', 'Hashtag suggestions', 'Trend analysis'],
      isPopular: true
    },
    {
      platform: 'YouTube',
      icon: '📺',
      description: 'Manage your YouTube channel and video content',
      color: '#FF0000',
      features: ['Video uploads', 'Community posts', 'Analytics'],
      isPopular: false
    },
    {
      platform: 'Pinterest',
      icon: '📌',
      description: 'Pin your content and reach Pinterest\'s visual audience',
      color: '#BD081C',
      features: ['Pin scheduling', 'Board management', 'Idea pins'],
      isPopular: false
    }
  ]

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

  const handleConnect = (platform) => {
    console.log(`Connecting to ${platform}...`)
  }

  const handleDisconnect = (accountId) => {
    console.log(`Disconnecting account ${accountId}...`)
  }

  const handleRefresh = (accountId) => {
    console.log(`Refreshing account ${accountId}...`)
  }

  return (
    <div className="space-y-6">
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
                  {connectedAccounts.reduce((sum, acc) => sum + parseFloat(acc.followers.replace('K', '')) * 1000, 0) / 1000}K
                </div>
                <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                  Total Followers
                </div>
              </div>
              <div
                className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-xl"
                style={{ background: 'var(--accent-green)' }}
              >
                👥
              </div>
            </div>
          </div>
        </div>

        <div className="card slide-up">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                  {connectedAccounts.filter(acc => acc.status === 'active').length}/{connectedAccounts.length}
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
          {connectedAccounts.map((account, index) => (
            <div key={account.id} className="card slide-up" style={{ animationDelay: `${index * 100}ms` }}>
              <div className="card-content">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-4">
                    <div
                      className="w-16 h-16 rounded-xl flex items-center justify-center text-white text-2xl"
                      style={{ background: account.color }}
                    >
                      {account.icon}
                    </div>
                    <div>
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                          {account.displayName}
                        </h3>
                        {getStatusBadge(account.status)}
                      </div>
                      <p className="text-sm mb-1" style={{ color: 'var(--gray-600)' }}>
                        {account.platform} • {account.username}
                      </p>
                      <p className="text-sm" style={{ color: 'var(--gray-500)' }}>
                        Last synced {account.lastSync}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleRefresh(account.id)}
                      className="btn btn-ghost btn-sm"
                    >
                      🔄 Refresh
                    </button>
                    <button
                      onClick={() => handleDisconnect(account.id)}
                      className="btn btn-outline btn-sm text-red-600 border-red-300 hover:bg-red-50"
                    >
                      🔌 Disconnect
                    </button>
                  </div>
                </div>

                <div className="mt-6 grid grid-cols-3 gap-6 pt-4 border-t" style={{ borderColor: 'var(--gray-200)' }}>
                  <div className="text-center">
                    <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                      {account.followers}
                    </div>
                    <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                      Followers
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                      {account.posts}
                    </div>
                    <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                      Posts
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                      {account.engagement}
                    </div>
                    <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                      Engagement
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Available Platforms Tab */}
      {activeTab === 'available' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {availablePlatforms.map((platform, index) => (
            <div key={platform.platform} className="card slide-up" style={{ animationDelay: `${index * 100}ms` }}>
              <div className="card-content">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-4">
                    <div
                      className="w-14 h-14 rounded-xl flex items-center justify-center text-white text-xl"
                      style={{ background: platform.color }}
                    >
                      {platform.icon}
                    </div>
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                          {platform.platform}
                        </h3>
                        {platform.isPopular && (
                          <span
                            className="px-2 py-1 rounded-full text-xs font-medium"
                            style={{
                              background: 'var(--accent-green)',
                              color: 'white'
                            }}
                          >
                            🔥 Popular
                          </span>
                        )}
                      </div>
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
                  onClick={() => handleConnect(platform.platform)}
                  className="w-full btn btn-primary"
                >
                  <span>🔗</span>
                  <span>Connect {platform.platform}</span>
                </button>
              </div>
            </div>
          ))}
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