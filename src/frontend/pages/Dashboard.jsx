import React from 'react'

function Dashboard() {
  const stats = [
    {
      label: 'Total Posts',
      value: '2,847',
      change: '+12%',
      changeType: 'positive',
      icon: '📝',
      color: 'var(--primary-blue)'
    },
    {
      label: 'Total Reach',
      value: '1.2M',
      change: '+18%',
      changeType: 'positive',
      icon: '👥',
      color: 'var(--accent-green)'
    },
    {
      label: 'Engagement Rate',
      value: '8.4%',
      change: '+2.1%',
      changeType: 'positive',
      icon: '❤️',
      color: 'var(--warning-orange)'
    },
    {
      label: 'Scheduled Posts',
      value: '24',
      change: '+5',
      changeType: 'positive',
      icon: '📅',
      color: 'var(--primary-blue)'
    }
  ]

  const recentPosts = [
    {
      id: 1,
      content: 'Just launched our new AI-powered social media tool! 🚀 #AI #SocialMedia',
      platforms: ['Twitter', 'LinkedIn'],
      status: 'published',
      engagement: { likes: 156, comments: 23, shares: 12 },
      publishedAt: '2 hours ago'
    },
    {
      id: 2,
      content: 'Behind the scenes of building PostProber ✨ The future of social media management',
      platforms: ['Instagram', 'Twitter'],
      status: 'scheduled',
      scheduledFor: 'Today at 3:00 PM',
      publishedAt: null
    },
    {
      id: 3,
      content: 'Top 5 social media trends that will dominate 2024 📈 Thread below 👇',
      platforms: ['Twitter'],
      status: 'published',
      engagement: { likes: 89, comments: 15, shares: 8 },
      publishedAt: '5 hours ago'
    },
    {
      id: 4,
      content: 'Customer success story: How @CompanyName increased engagement by 300% using our platform 📊✨',
      platforms: ['LinkedIn', 'Facebook'],
      status: 'published',
      engagement: { likes: 234, comments: 45, shares: 18 },
      publishedAt: '8 hours ago'
    },
    {
      id: 5,
      content: 'Monday motivation: Consistency is key to social media success! What\'s your posting strategy? 💪',
      platforms: ['Instagram', 'Twitter'],
      status: 'published',
      engagement: { likes: 127, comments: 32, shares: 9 },
      publishedAt: '1 day ago'
    }
  ]

  const upcomingPosts = [
    { time: '2:00 PM', content: 'Weekly analytics report', platform: 'LinkedIn' },
    { time: '4:30 PM', content: 'Product update announcement', platform: 'Twitter' },
    { time: '6:00 PM', content: 'Team showcase Friday', platform: 'Instagram' }
  ]

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
      case 'twitter': return 'var(--primary-blue)'
      case 'linkedin': return '#0077B5'
      case 'instagram': return '#E4405F'
      case 'facebook': return '#1877F2'
      default: return 'var(--gray-500)'
    }
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
                    <div
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        stat.changeType === 'positive' ? 'text-green-700 bg-green-100' : 'text-red-700 bg-red-100'
                      }`}
                    >
                      {stat.change}
                    </div>
                  </div>
                  <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                    {stat.value}
                  </div>
                  <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                    {stat.label}
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
              <div className="space-y-4">
                {recentPosts.map((post) => (
                  <div
                    key={post.id}
                    className="p-4 border rounded-lg transition-colors hover:bg-gray-50"
                    style={{ borderColor: 'var(--gray-200)' }}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <p className="text-sm mb-2" style={{ color: 'var(--gray-800)' }}>
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
                      <div className="flex items-center gap-4 text-sm" style={{ color: 'var(--gray-600)' }}>
                        <span>❤️ {post.engagement.likes}</span>
                        <span>💬 {post.engagement.comments}</span>
                        <span>🔄 {post.engagement.shares}</span>
                        <span className="ml-auto">{post.publishedAt}</span>
                      </div>
                    )}
                    {post.scheduledFor && (
                      <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                        Scheduled for {post.scheduledFor}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          {/* All Systems Online */}
          <div
            className="card slide-up"
            style={{ background: 'var(--gradient-primary)', color: 'white' }}
          >
            <div className="card-content">
              <div className="text-center">
                <div className="text-3xl mb-3">🚀</div>
                <h3 className="font-semibold mb-2">All Systems Online</h3>
                <p className="text-sm opacity-90 mb-4">
                  All your connected accounts are working perfectly
                </p>
                <div className="flex justify-center gap-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
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
                <button className="w-full btn btn-primary justify-start">
                  <span>✍️</span>
                  <span>Create New Post</span>
                </button>
                <button className="w-full btn btn-outline justify-start">
                  <span>📅</span>
                  <span>Schedule Post</span>
                </button>
                <button className="w-full btn btn-outline justify-start">
                  <span>📊</span>
                  <span>View Analytics</span>
                </button>
                <button className="w-full btn btn-outline justify-start">
                  <span>🔗</span>
                  <span>Add Account</span>
                </button>
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
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard