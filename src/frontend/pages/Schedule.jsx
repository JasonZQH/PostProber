import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import platformService from '../services/platformService'

function Schedule() {
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

  const scheduledPosts = [
    {
      id: 1,
      content: 'Weekly analytics report: Our reach increased by 24% this week! 📊',
      scheduledFor: '2024-01-15T14:00:00',
      platforms: ['LinkedIn', 'Twitter'],
      status: 'scheduled'
    },
    {
      id: 2,
      content: 'Behind the scenes: Building the future of social media management ✨',
      scheduledFor: '2024-01-15T18:30:00',
      platforms: ['Instagram', 'Facebook'],
      status: 'scheduled'
    },
    {
      id: 3,
      content: 'Monday motivation: Start your week with purpose and passion! 💪',
      scheduledFor: '2024-01-16T09:00:00',
      platforms: ['Twitter', 'LinkedIn'],
      status: 'scheduled'
    }
  ]

  const formatDateTime = (dateString) => {
    const date = new Date(dateString)
    return {
      date: date.toLocaleDateString(),
      time: date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  }

  // Check if no platforms connected
  if (connectedPlatforms.length === 0) {
    return (
      <div className="space-y-6">
        <div className="fade-in">
          <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
            Scheduled Posts 📅
          </h1>
          <p style={{ color: 'var(--gray-600)' }}>
            Manage your upcoming posts and publishing schedule
          </p>
        </div>

        <div className="card">
          <div className="card-content">
            <div className="text-center py-16">
              <div className="text-6xl mb-4">📅</div>
              <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
                No Schedule Available
              </h2>
              <p className="mb-6" style={{ color: 'var(--gray-600)' }}>
                Connect your social media platforms to start scheduling posts
              </p>
              <Link to="/settings" className="btn btn-primary">
                <span>🔗</span>
                <span>Connect Platforms</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="fade-in">
        <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
          Scheduled Posts 📅
        </h1>
        <p style={{ color: 'var(--gray-600)' }}>
          Manage your upcoming posts and publishing schedule
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card slide-up">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                  {scheduledPosts.length}
                </div>
                <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                  Scheduled Posts
                </div>
              </div>
              <div
                className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-xl"
                style={{ background: 'var(--primary-blue)' }}
              >
                📅
              </div>
            </div>
          </div>
        </div>

        <div className="card slide-up">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                  2
                </div>
                <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                  Posts Today
                </div>
              </div>
              <div
                className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-xl"
                style={{ background: 'var(--accent-green)' }}
              >
                🎯
              </div>
            </div>
          </div>
        </div>

        <div className="card slide-up">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                  7
                </div>
                <div className="text-sm" style={{ color: 'var(--gray-600)' }}>
                  Posts This Week
                </div>
              </div>
              <div
                className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-xl"
                style={{ background: 'var(--warning-orange)' }}
              >
                📊
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scheduled Posts List */}
      <div className="card slide-up">
        <div className="card-header">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold" style={{ color: 'var(--gray-900)' }}>
              Upcoming Posts
            </h2>
            <Link to="/compose" className="btn btn-primary">
              <span>✍️</span>
              <span>Schedule New Post</span>
            </Link>
          </div>
        </div>
        <div className="card-content">
          {scheduledPosts.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-4xl mb-4">📝</div>
              <h3 className="text-lg font-semibold mb-2" style={{ color: 'var(--gray-900)' }}>
                No Scheduled Posts
              </h3>
              <p className="mb-4" style={{ color: 'var(--gray-600)' }}>
                Start scheduling your content to maintain a consistent posting schedule
              </p>
              <Link to="/compose" className="btn btn-primary">
                <span>✍️</span>
                <span>Create Your First Post</span>
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {scheduledPosts.map((post, index) => {
              const { date, time } = formatDateTime(post.scheduledFor)

              return (
                <div
                  key={post.id}
                  className="p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                  style={{ borderColor: 'var(--gray-200)' }}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <p className="font-medium mb-2" style={{ color: 'var(--gray-800)' }}>
                        {post.content}
                      </p>
                      <div className="flex items-center gap-4 text-sm" style={{ color: 'var(--gray-600)' }}>
                        <div className="flex items-center gap-1">
                          <span>📅</span>
                          <span>{date}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <span>⏰</span>
                          <span>{time}</span>
                        </div>
                      </div>
                    </div>
                    <span className="status-indicator status-info">⏰ Scheduled</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {post.platforms.map((platform) => (
                        <span
                          key={platform}
                          className="px-2 py-1 rounded text-xs font-medium"
                          style={{
                            color: 'var(--primary-blue)',
                            background: 'rgba(0, 102, 255, 0.1)'
                          }}
                        >
                          {platform}
                        </span>
                      ))}
                    </div>
                    <div className="flex items-center gap-2">
                      <button className="btn btn-ghost btn-sm">Edit</button>
                      <button className="btn btn-outline btn-sm">Reschedule</button>
                      <button
                        className="btn btn-sm"
                        style={{
                          background: 'var(--danger-red)',
                          color: 'white',
                          border: 'none'
                        }}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                </div>
              )
              })}
            </div>
          )}
        </div>
      </div>

      {/* Calendar View Placeholder */}
      <div
        className="card slide-up"
        style={{ background: 'var(--gradient-primary)', color: 'white' }}
      >
        <div className="card-content">
          <div className="text-center">
            <div className="text-3xl mb-3">📅</div>
            <h3 className="font-semibold mb-2">Calendar View</h3>
            <p className="text-sm opacity-90 mb-4">
              Visual calendar integration coming soon
            </p>
            <button className="btn" style={{ background: 'white', color: 'var(--primary-blue)' }}>
              Preview Calendar
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Schedule