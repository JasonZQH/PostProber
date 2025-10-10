import React, { useState } from 'react'

function Analytics() {
  const [selectedPeriod, setSelectedPeriod] = useState('7d')
  const [selectedPlatform, setSelectedPlatform] = useState('all')

  const periods = [
    { value: '24h', label: '24 Hours' },
    { value: '7d', label: '7 Days' },
    { value: '30d', label: '30 Days' },
    { value: '90d', label: '90 Days' }
  ]

  const platforms = [
    { value: 'all', label: 'All Platforms', icon: '📊' },
    { value: 'twitter', label: 'Twitter', icon: '🐦' },
    { value: 'linkedin', label: 'LinkedIn', icon: '💼' },
    { value: 'instagram', label: 'Instagram', icon: '📷' },
    { value: 'facebook', label: 'Facebook', icon: '📘' }
  ]

  const overviewStats = [
    {
      label: 'Total Impressions',
      value: '487K',
      change: '+24%',
      changeType: 'positive',
      icon: '👁️',
      color: 'var(--primary-blue)',
      chart: [45, 52, 38, 67, 73, 89, 56]
    },
    {
      label: 'Engagement Rate',
      value: '8.4%',
      change: '+2.1%',
      changeType: 'positive',
      icon: '❤️',
      color: 'var(--accent-green)',
      chart: [3.2, 4.1, 5.8, 6.2, 7.1, 8.4, 8.0]
    },
    {
      label: 'Click-through Rate',
      value: '3.2%',
      change: '+0.8%',
      changeType: 'positive',
      icon: '🔗',
      color: 'var(--warning-orange)',
      chart: [2.1, 2.4, 2.8, 3.0, 3.2, 3.1, 3.2]
    },
    {
      label: 'Follower Growth',
      value: '+1,247',
      change: '+18%',
      changeType: 'positive',
      icon: '📈',
      color: 'var(--primary-blue)',
      chart: [156, 203, 178, 245, 289, 334, 267]
    }
  ]

  const topPosts = [
    {
      id: 1,
      content: 'Just launched our new AI-powered social media tool! 🚀 #AI #SocialMedia',
      platform: 'Twitter',
      impressions: '45.2K',
      engagement: '3.8K',
      engagementRate: '8.4%',
      publishedAt: '2 days ago',
      performance: 'excellent'
    },
    {
      id: 2,
      content: 'Behind the scenes: Building the future of social media management ✨',
      platform: 'LinkedIn',
      impressions: '28.9K',
      engagement: '2.1K',
      engagementRate: '7.3%',
      publishedAt: '4 days ago',
      performance: 'good'
    },
    {
      id: 3,
      content: 'Top 5 social media trends that will dominate 2024 📈 Thread below 👇',
      platform: 'Twitter',
      impressions: '31.7K',
      engagement: '1.9K',
      engagementRate: '6.0%',
      publishedAt: '6 days ago',
      performance: 'good'
    },
    {
      id: 4,
      content: 'How we increased our client\'s reach by 300% in just 30 days 📊 Case study inside!',
      platform: 'LinkedIn',
      impressions: '38.5K',
      engagement: '2.8K',
      engagementRate: '7.3%',
      publishedAt: '1 week ago',
      performance: 'excellent'
    },
    {
      id: 5,
      content: 'Friday feature spotlight: AI-powered content suggestions are live! 🤖✨ #ProductUpdate',
      platform: 'Instagram',
      impressions: '22.1K',
      engagement: '1.7K',
      engagementRate: '7.7%',
      publishedAt: '1 week ago',
      performance: 'good'
    }
  ]

  const platformStats = [
    {
      platform: 'Twitter',
      icon: '🐦',
      followers: '12.4K',
      posts: 45,
      engagement: '8.2%',
      reach: '156K',
      growth: '+12%',
      color: '#1DA1F2'
    },
    {
      platform: 'LinkedIn',
      icon: '💼',
      followers: '8.9K',
      posts: 23,
      engagement: '9.1%',
      reach: '89K',
      growth: '+18%',
      color: '#0077B5'
    },
    {
      platform: 'Instagram',
      icon: '📷',
      followers: '5.2K',
      posts: 31,
      engagement: '7.8%',
      reach: '67K',
      growth: '+8%',
      color: '#E4405F'
    }
  ]

  const getPerformanceColor = (performance) => {
    switch (performance) {
      case 'excellent': return 'var(--accent-green)'
      case 'good': return 'var(--warning-orange)'
      case 'average': return 'var(--gray-500)'
      case 'poor': return 'var(--danger-red)'
      default: return 'var(--gray-500)'
    }
  }

  const getPerformanceBadge = (performance) => {
    const colors = {
      excellent: { bg: 'rgba(0, 210, 91, 0.1)', text: 'var(--accent-green)' },
      good: { bg: 'rgba(255, 140, 0, 0.1)', text: 'var(--warning-orange)' },
      average: { bg: 'rgba(107, 114, 128, 0.1)', text: 'var(--gray-500)' },
      poor: { bg: 'rgba(239, 68, 68, 0.1)', text: 'var(--danger-red)' }
    }

    const color = colors[performance] || colors.average

    return (
      <span
        className="px-2 py-1 rounded-full text-xs font-medium capitalize"
        style={{ background: color.bg, color: color.text }}
      >
        {performance}
      </span>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="fade-in">
        <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
          Analytics Dashboard 📊
        </h1>
        <p style={{ color: 'var(--gray-600)' }}>
          Track your social media performance and growth metrics
        </p>
      </div>

      {/* Filters */}
      <div className="card slide-up">
        <div className="card-content">
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex items-center gap-2">
              <label className="text-sm font-medium" style={{ color: 'var(--gray-700)' }}>
                Time Period:
              </label>
              <select
                value={selectedPeriod}
                onChange={(e) => setSelectedPeriod(e.target.value)}
                className="form-input w-auto"
              >
                {periods.map(period => (
                  <option key={period.value} value={period.value}>
                    {period.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-center gap-2">
              <label className="text-sm font-medium" style={{ color: 'var(--gray-700)' }}>
                Platform:
              </label>
              <select
                value={selectedPlatform}
                onChange={(e) => setSelectedPlatform(e.target.value)}
                className="form-input w-auto"
              >
                {platforms.map(platform => (
                  <option key={platform.value} value={platform.value}>
                    {platform.icon} {platform.label}
                  </option>
                ))}
              </select>
            </div>
            <button className="btn btn-outline ml-auto">
              <span>📤</span>
              <span>Export Report</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Section: Stats + Top Performing Posts */}
        <div className="lg:col-span-2 space-y-6">
          {/* Overview Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            {overviewStats.map((stat, index) => (
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

          {/* Top Performing Posts */}
          <div className="card slide-up">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold" style={{ color: 'var(--gray-900)' }}>
                  Top Performing Posts
                </h2>
                <button className="btn btn-outline btn-sm">View All Posts</button>
              </div>
            </div>
            <div className="card-content">
              <div className="space-y-4">
                {topPosts.map((post) => (
                  <div
                    key={post.id}
                    className="p-4 border rounded-lg transition-colors hover:bg-gray-50"
                    style={{ borderColor: 'var(--gray-200)' }}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <p className="font-medium mb-2" style={{ color: 'var(--gray-800)' }}>
                          {post.content}
                        </p>
                        <div className="flex items-center gap-4 text-sm" style={{ color: 'var(--gray-600)' }}>
                          <span>📍 {post.platform}</span>
                          <span>👁️ {post.impressions}</span>
                          <span>❤️ {post.engagement}</span>
                          <span>📊 {post.engagementRate}</span>
                        </div>
                      </div>
                      {getPerformanceBadge(post.performance)}
                    </div>
                    <div className="text-sm" style={{ color: 'var(--gray-500)' }}>
                      Published {post.publishedAt}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="lg:col-span-1">
          {/* Engagement Trends - aligned with stats */}
          <div>
            <div
              className="card slide-up"
              style={{ background: 'var(--gradient-cool)', color: 'white' }}
            >
              <div className="card-content">
                <div className="text-center">
                  <div className="text-3xl mb-3">📈</div>
                  <h3 className="font-semibold mb-2">Engagement Trending Up</h3>
                  <p className="text-sm opacity-90 mb-4">
                    Your content is performing 24% better than last month
                  </p>
                  <div className="flex justify-center gap-2">
                    <div className="w-2 h-2 bg-white rounded-full opacity-60"></div>
                    <div className="w-2 h-2 bg-white rounded-full"></div>
                    <div className="w-2 h-2 bg-white rounded-full opacity-60"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Platform Performance - aligned with Top Performing Posts */}
          <div className="card slide-up">
            <div className="card-header">
              <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                Platform Performance
              </h3>
            </div>
            <div className="card-content">
              <div className="space-y-4">
                {platformStats.map((platform) => (
                  <div key={platform.platform} className="p-4 border rounded-lg" style={{ borderColor: 'var(--gray-200)' }}>
                    <div className="flex items-center gap-3 mb-3">
                      <div
                        className="w-10 h-10 rounded-lg flex items-center justify-center text-white text-lg"
                        style={{ background: platform.color }}
                      >
                        {platform.icon}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium" style={{ color: 'var(--gray-800)' }}>
                          {platform.platform}
                        </div>
                        <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                          {platform.followers} followers
                        </div>
                      </div>
                      <span
                        className="px-2 py-1 rounded-full text-xs font-medium text-green-700"
                        style={{ background: 'rgba(0, 210, 91, 0.1)' }}
                      >
                        {platform.growth}
                      </span>
                    </div>
                    <div className="grid grid-cols-3 gap-3 text-center text-sm">
                      <div>
                        <div className="font-medium" style={{ color: 'var(--gray-800)' }}>
                          {platform.posts}
                        </div>
                        <div style={{ color: 'var(--gray-600)' }}>Posts</div>
                      </div>
                      <div>
                        <div className="font-medium" style={{ color: 'var(--gray-800)' }}>
                          {platform.engagement}
                        </div>
                        <div style={{ color: 'var(--gray-600)' }}>Engagement</div>
                      </div>
                      <div>
                        <div className="font-medium" style={{ color: 'var(--gray-800)' }}>
                          {platform.reach}
                        </div>
                        <div style={{ color: 'var(--gray-600)' }}>Reach</div>
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

export default Analytics