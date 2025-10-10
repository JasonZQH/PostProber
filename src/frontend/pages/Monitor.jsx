import React from 'react'

function Monitor() {
  const activePosts = [
    {
      id: 1,
      content: "🚀 Just launched our new AI-powered social media tool!",
      platforms: ['Twitter', 'LinkedIn'],
      status: 'posted',
      steps: [
        { name: 'Authentication', status: 'completed', time: '2:00 PM' },
        { name: 'Content Analysis', status: 'completed', time: '2:01 PM' },
        { name: 'Publishing', status: 'completed', time: '2:02 PM' },
        { name: 'Verification', status: 'completed', time: '2:03 PM' },
        { name: 'Engagement Tracking', status: 'active', time: 'Now' }
      ],
      metrics: {
        views: 1247,
        likes: 89,
        shares: 23,
        comments: 12
      }
    },
    {
      id: 2,
      content: "Behind the scenes of building PostProber ✨",
      platforms: ['Instagram', 'Twitter'],
      status: 'posting',
      steps: [
        { name: 'Authentication', status: 'completed', time: '3:15 PM' },
        { name: 'Content Analysis', status: 'completed', time: '3:16 PM' },
        { name: 'Publishing', status: 'active', time: 'Now' },
        { name: 'Verification', status: 'pending', time: 'Waiting' },
        { name: 'Engagement Tracking', status: 'pending', time: 'Waiting' }
      ],
      metrics: {
        views: 45,
        likes: 3,
        shares: 0,
        comments: 1
      }
    }
  ]

  const getStepIcon = (status) => {
    switch (status) {
      case 'completed': return '✅'
      case 'active': return '🔄'
      case 'pending': return '⏳'
      case 'failed': return '❌'
      default: return '⏳'
    }
  }

  const getStepStatus = (status) => {
    switch (status) {
      case 'completed': return 'text-green-600'
      case 'active': return 'text-blue-600'
      case 'pending': return 'text-gray-500'
      case 'failed': return 'text-red-600'
      default: return 'text-gray-500'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="slide-in-up">
        <h1 className="text-3xl font-bold gradient-text mb-2">
          📊 Real-Time Monitoring
        </h1>
        <p className="text-gray-600">
          Track your posts across all platforms in real-time
        </p>
      </div>

      {/* Live Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Active Posts', value: '2', icon: '🚀', color: 'purple' },
          { label: 'Total Views', value: '1.2K', icon: '👀', color: 'blue' },
          { label: 'Engagement Rate', value: '8.4%', icon: '❤️', color: 'pink' },
          { label: 'Success Rate', value: '98%', icon: '✅', color: 'green' }
        ].map((stat, index) => (
          <div
            key={stat.label}
            className="card hover-lift slide-in-up"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl bounce-soft">{stat.icon}</span>
              <div className="text-right">
                <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                <div className="text-sm text-gray-600">{stat.label}</div>
              </div>
            </div>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '70%' }}></div>
            </div>
          </div>
        ))}
      </div>

      {/* Active Posts Monitoring */}
      <div className="space-y-6">
        {activePosts.map((post, index) => (
          <div
            key={post.id}
            className="card hover-lift slide-in-up"
            style={{ animationDelay: `${index * 0.2}s` }}
          >
            {/* Post Header */}
            <div className="flex items-start justify-between mb-6">
              <div className="flex-1">
                <p className="text-lg font-semibold text-gray-900 mb-2">
                  {post.content}
                </p>
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    {post.platforms.map(platform => (
                      <span
                        key={platform}
                        className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium"
                      >
                        {platform}
                      </span>
                    ))}
                  </div>
                  <div className={`status-dot ${post.status === 'posted' ? 'status-success' : 'status-pending'}`}></div>
                  <span className="text-sm font-semibold">
                    {post.status === 'posted' ? '✅ Posted' : '🚀 Posting'}
                  </span>
                </div>
              </div>
              <button className="btn btn-ghost text-sm">
                View Details
              </button>
            </div>

            {/* Progress Steps */}
            <div className="mb-6">
              <h4 className="font-semibold text-gray-900 mb-4">Publishing Progress</h4>
              <div className="space-y-3">
                {post.steps.map((step, stepIndex) => (
                  <div key={stepIndex} className="flex items-center space-x-4">
                    <div className={`text-xl ${step.status === 'active' ? 'bounce-soft' : ''}`}>
                      {getStepIcon(step.status)}
                    </div>
                    <div className="flex-1">
                      <div className={`font-medium ${getStepStatus(step.status)}`}>
                        {step.name}
                      </div>
                      <div className="text-sm text-gray-500">{step.time}</div>
                    </div>
                    {step.status === 'active' && (
                      <div className="text-blue-600 typing-indicator font-medium">
                        Processing
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Metrics */}
            <div className="border-t border-gray-100 pt-4">
              <h4 className="font-semibold text-gray-900 mb-3">Engagement Metrics</h4>
              <div className="grid grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">{post.metrics.views}</div>
                  <div className="text-sm text-gray-600">Views</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-pink-600">{post.metrics.likes}</div>
                  <div className="text-sm text-gray-600">Likes</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{post.metrics.shares}</div>
                  <div className="text-sm text-gray-600">Shares</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{post.metrics.comments}</div>
                  <div className="text-sm text-gray-600">Comments</div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* AI Monitoring Insights */}
      <div className="card card-gradient slide-in-up">
        <div className="text-center mb-4">
          <div className="text-3xl mb-2 float">🤖</div>
          <h3 className="text-xl font-bold text-white">AI Monitoring Insights</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white bg-opacity-20 rounded-lg p-4">
            <div className="text-white font-semibold mb-2">Performance Alert</div>
            <div className="text-sm text-white opacity-90">
              Your LinkedIn post is performing 34% better than average! 📈
            </div>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-4">
            <div className="text-white font-semibold mb-2">Optimization Tip</div>
            <div className="text-sm text-white opacity-90">
              Post on Twitter in 2 hours for maximum engagement ⏰
            </div>
          </div>
        </div>

        <button className="w-full mt-4 bg-white text-purple-600 py-3 rounded-lg font-semibold hover-scale">
          Get More AI Insights
        </button>
      </div>
    </div>
  )
}

export default Monitor