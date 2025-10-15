import React, { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import platformService from '../services/platformService'

function Dashboard() {
  const [connectedPlatforms, setConnectedPlatforms] = useState([])

  // Load connected platforms
  useEffect(() => {
    const platforms = platformService.getConnectedPlatforms()
    setConnectedPlatforms(platforms)

    const unsubscribe = platformService.subscribe((platforms) => {
      setConnectedPlatforms(platforms)
    })

    return unsubscribe
  }, [])
  const formatRelativeTime = (isoString) => {
    if (!isoString) return 'Not available'
    const date = new Date(isoString)
    if (Number.isNaN(date.getTime())) return 'Not available'

    const diffMs = Date.now() - date.getTime()
    const diffMinutes = Math.floor(diffMs / 60000)

    if (diffMinutes < 1) return 'Just now'
    if (diffMinutes < 60) return `${diffMinutes} minute${diffMinutes === 1 ? '' : 's'} ago`
    const diffHours = Math.floor(diffMinutes / 60)
    if (diffHours < 24) return `${diffHours} hour${diffHours === 1 ? '' : 's'} ago`
    const diffDays = Math.floor(diffHours / 24)
    return `${diffDays} day${diffDays === 1 ? '' : 's'} ago`
  }

  const latestConnection = useMemo(() => {
    const sorted = connectedPlatforms
      .filter(platform => platform.connectedAt)
      .sort((a, b) => new Date(b.connectedAt) - new Date(a.connectedAt))
    return sorted[0]
  }, [connectedPlatforms])

  const stats = useMemo(() => [
    {
      label: 'Connected Platforms',
      value: connectedPlatforms.length.toString(),
      icon: '🔗',
      color: 'var(--primary-blue)',
      description: connectedPlatforms.length
        ? connectedPlatforms.map(p => p.name).join(', ')
        : 'Link a platform to unlock analytics and posting tools.'
    },
    {
      label: 'Latest Connection',
      value: latestConnection ? latestConnection.name : '—',
      icon: '🆕',
      color: 'var(--accent-green)',
      description: latestConnection
        ? `Linked ${formatRelativeTime(latestConnection.connectedAt)}`
        : 'No platforms connected yet.'
    },
    {
      label: 'AI Health Monitoring',
      value: connectedPlatforms.length ? 'Active' : 'Idle',
      icon: '🩺',
      color: 'var(--warning-orange)',
      description: connectedPlatforms.length
        ? 'Monitoring connected APIs every few minutes.'
        : 'Connect a platform to enable live health checks.'
    },
    {
      label: 'Posting Activity',
      value: '—',
      icon: '📝',
      color: 'var(--primary-blue)',
      description: 'Publishing history will appear once posting integration is enabled.'
    }
  ], [connectedPlatforms, latestConnection])

  const recentPosts = []
  const upcomingPosts = []

  const getStatusBadge = (status) => {
    switch (status) {
      case 'published':
        return <span className="status-indicator status-success">✅ Published</span>
      case 'scheduled':
        return <span className="status-indicator status-info">⏰ Scheduled</span>
      case 'draft':
        return <span className="status-indicator status-warning">📝 Draft</span>
      default:
        return <span className="status-indicator">{status}</span>
    }
  }

  const getPlatformColor = (platform) => {
    switch (platform.toLowerCase()) {
      case 'twitter': return '#000000'
      case 'x (twitter)': return '#000000'
      case 'linkedin': return '#0077B5'
      case 'instagram': return '#E4405F'
      case 'facebook': return '#1877F2'
      default: return 'var(--gray-500)'
    }
  }

  // Check if no platforms connected
  if (connectedPlatforms.length === 0) {
    return (
      <div className="space-y-6">
        <div className="fade-in">
          <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
            Welcome to PostProber! 👋
          </h1>
          <p style={{ color: 'var(--gray-600)' }}>
            Get started by connecting your social media accounts
          </p>
        </div>

        <div className="card">
          <div className="card-content">
            <div className="text-center py-16">
              <div className="text-6xl mb-4">🚀</div>
              <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
                Let's Get Started!
              </h2>
              <p className="mb-6" style={{ color: 'var(--gray-600)' }}>
                Connect your social media platforms to start managing your content, scheduling posts, and tracking analytics
              </p>
              <Link to="/settings" className="btn btn-primary">
                <span>🔗</span>
                <span>Connect Your First Platform</span>
              </Link>
            </div>
          </div>
        </div>

        {/* Feature highlights for new users */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card">
            <div className="card-content text-center">
              <div className="text-4xl mb-3">✍️</div>
              <h3 className="font-semibold mb-2" style={{ color: 'var(--gray-900)' }}>
                Create & Schedule
              </h3>
              <p className="text-sm" style={{ color: 'var(--gray-600)' }}>
                Compose posts and schedule them across all your platforms
              </p>
            </div>
          </div>
          <div className="card">
            <div className="card-content text-center">
              <div className="text-4xl mb-3">📊</div>
              <h3 className="font-semibold mb-2" style={{ color: 'var(--gray-900)' }}>
                Track Analytics
              </h3>
              <p className="text-sm" style={{ color: 'var(--gray-600)' }}>
                Monitor performance and get AI-powered insights
              </p>
            </div>
          </div>
          <div className="card">
            <div className="card-content text-center">
              <div className="text-4xl mb-3">🩺</div>
              <h3 className="font-semibold mb-2" style={{ color: 'var(--gray-900)' }}>
                Health Monitoring
              </h3>
              <p className="text-sm" style={{ color: 'var(--gray-600)' }}>
                Stay informed about platform status and rate limits
              </p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="fade-in">
        <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
          Welcome back! 👋
        </h1>
        <p style={{ color: 'var(--gray-600)' }}>
          Here's what's happening with your social media accounts today.
        </p>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Section: Stats + Recent Posts */}
        <div className="lg:col-span-2 space-y-6">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <div key={stat.label} className="card slide-up" style={{ animationDelay: `${index * 100}ms` }}>
                <div className="card-content">
                  <div className="flex items-center justify-between mb-4">
                    <div
                      className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-xl"
                      style={{ background: stat.color }}
                    >
                      {stat.icon}
                    </div>
                  </div>
                  <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                    {stat.value}
                  </div>
                  <div className="text-sm font-medium mb-1" style={{ color: 'var(--gray-700)' }}>
                    {stat.label}
                  </div>
                  <div className="text-xs" style={{ color: 'var(--gray-600)' }}>
                    {stat.description}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Recent Posts */}
          <div className="card slide-up">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold" style={{ color: 'var(--gray-900)' }}>
                  Recent Posts
                </h2>
                <button className="btn btn-outline btn-sm">View All</button>
              </div>
            </div>
            <div className="card-content">
              {recentPosts.length === 0 ? (
                <div className="p-6 text-center text-sm" style={{ color: 'var(--gray-600)' }}>
                  No recent publishing data yet. Once posting integrations are connected,
                  new activity will appear here automatically.
                </div>
              ) : (
                <div className="space-y-4">
                  {recentPosts.map((post) => (
                    <div
                      key={post.id}
                      className="p-4 border rounded-lg transition-colors hover:bg-white group cursor-pointer"
                      style={{ borderColor: 'var(--gray-200)' }}
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <p className="text-sm mb-2 group-hover:!text-black" style={{ color: 'var(--gray-800)' }}>
                            {post.content}
                          </p>
                          <div className="flex items-center gap-2 mb-2">
                            {post.platforms.map((platform) => (
                              <span
                                key={platform}
                                className="px-2 py-1 rounded text-xs font-medium"
                                style={{
                                  color: getPlatformColor(platform),
                                  background: `${getPlatformColor(platform)}15`
                                }}
                              >
                                {platform}
                              </span>
                            ))}
                          </div>
                        </div>
                        {getStatusBadge(post.status)}
                      </div>
                      {post.engagement && (
                        <div className="flex items-center gap-4 text-sm group-hover:!text-black" style={{ color: 'var(--gray-600)' }}>
                          <span>❤️ {post.engagement.likes}</span>
                          <span>💬 {post.engagement.comments}</span>
                          <span>🔄 {post.engagement.shares}</span>
                          <span className="ml-auto">{post.publishedAt}</span>
                        </div>
                      )}
                      {post.scheduledFor && (
                        <div className="text-sm group-hover:!text-black" style={{ color: 'var(--gray-600)' }}>
                          Scheduled for {post.scheduledFor}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          {/* Connected Platforms Status */}
          <div
            className="card slide-up"
            style={{ background: 'var(--gradient-primary)', color: 'white' }}
          >
            <div className="card-content">
              <div className="text-center">
                <div className="text-3xl mb-3">🚀</div>
                <h3 className="font-semibold mb-2">{connectedPlatforms.length} Platform{connectedPlatforms.length !== 1 ? 's' : ''} Connected</h3>
                <p className="text-sm opacity-90 mb-4">
                  {connectedPlatforms.map(p => p.name).join(', ')}
                </p>
                <div className="flex justify-center gap-2">
                  {connectedPlatforms.map((platform, idx) => (
                    <div key={platform.id} className="w-2 h-2 bg-green-400 rounded-full"></div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="card slide-up">
            <div className="card-header">
              <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                Quick Actions
              </h3>
            </div>
            <div className="card-content">
              <div className="space-y-3">
                <Link to="/compose" className="w-full btn btn-primary justify-start">
                  <span>✍️</span>
                  <span>Create New Post</span>
                </Link>
                <Link to="/schedule" className="w-full btn btn-outline justify-start">
                  <span>📅</span>
                  <span>Schedule Post</span>
                </Link>
                <Link to="/analytics" className="w-full btn btn-outline justify-start">
                  <span>📊</span>
                  <span>View Analytics</span>
                </Link>
                <Link to="/settings" className="w-full btn btn-outline justify-start">
                  <span>🔗</span>
                  <span>Manage Accounts</span>
                </Link>
              </div>
            </div>
          </div>

          {/* Today's Schedule */}
          <div className="card slide-up">
            <div className="card-header">
              <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                Today's Schedule
              </h3>
            </div>
            <div className="card-content">
              {upcomingPosts.length === 0 ? (
                <div className="text-sm text-center" style={{ color: 'var(--gray-600)' }}>
                  Scheduling data is not yet available. Use the Schedule page to plan posts once
                  your automation workflow is connected.
                </div>
              ) : (
                <div className="space-y-3">
                  {upcomingPosts.map((post, index) => (
                    <div key={index} className="flex items-center gap-3">
                      <div
                        className="w-2 h-2 rounded-full"
                        style={{ background: getPlatformColor(post.platform) }}
                      ></div>
                      <div className="flex-1">
                        <div className="text-sm font-medium" style={{ color: 'var(--gray-800)' }}>
                          {post.time}
                        </div>
                        <div className="text-xs" style={{ color: 'var(--gray-600)' }}>
                          {post.content} • {post.platform}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
