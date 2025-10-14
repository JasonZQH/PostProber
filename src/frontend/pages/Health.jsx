import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import healthWebSocket from '../services/healthWebSocket'
import platformService from '../services/platformService'

function Health() {
  const [platformHealth, setPlatformHealth] = useState([])
  const [activeAlerts, setActiveAlerts] = useState([])
  const [isConnected, setIsConnected] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(null)
  const [connectedPlatforms, setConnectedPlatforms] = useState([])

  // Helper functions
  const getPlatformIcon = (platform) => {
    const icons = {
      twitter: '🐦',
      linkedin: '💼',
      instagram: '📷',
      facebook: '📘'
    }
    return icons[platform.toLowerCase()] || '📱'
  }

  const getPlatformColor = (platform) => {
    const colors = {
      twitter: '#1DA1F2',
      linkedin: '#0077B5',
      instagram: '#E4405F',
      facebook: '#1877F2'
    }
    return colors[platform.toLowerCase()] || '#6B7280'
  }

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMinutes = Math.floor((now - date) / 60000)

    if (diffMinutes < 1) return 'Just now'
    if (diffMinutes < 60) return `${diffMinutes} ${diffMinutes === 1 ? 'minute' : 'minutes'} ago`
    if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)} ${Math.floor(diffMinutes / 60) === 1 ? 'hour' : 'hours'} ago`
    return date.toLocaleDateString()
  }

  const getStatusBadge = (status) => {
    const colors = {
      healthy: { bg: 'rgba(0, 210, 91, 0.1)', text: 'var(--accent-green)', icon: '✅' },
      warning: { bg: 'rgba(255, 140, 0, 0.1)', text: 'var(--warning-orange)', icon: '⚠️' },
      critical: { bg: 'rgba(239, 68, 68, 0.1)', text: 'var(--danger-red)', icon: '🚨' }
    }

    const color = colors[status] || colors.healthy

    return (
      <span
        className="px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1"
        style={{ background: color.bg, color: color.text }}
      >
        <span>{color.icon}</span>
        <span className="capitalize">{status}</span>
      </span>
    )
  }

  const getRateLimitColor = (percentage) => {
    if (percentage >= 90) return 'var(--danger-red)'
    if (percentage >= 75) return 'var(--warning-orange)'
    return 'var(--accent-green)'
  }

  // Fetch health data
  const fetchHealthData = async () => {
    if (connectedPlatforms.length === 0) {
      setIsLoading(false)
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/health/status')
      const data = await response.json()

      if (data.success) {
        // Filter to only show connected platforms
        const connectedPlatformIds = connectedPlatforms.map(p => p.id)
        const filteredData = data.platforms.filter(platform =>
          connectedPlatformIds.includes(platform.platform.toLowerCase())
        )

        const transformedData = filteredData.map(platform => ({
          platform: platform.platform.charAt(0).toUpperCase() + platform.platform.slice(1),
          icon: getPlatformIcon(platform.platform),
          status: platform.status,
          responseTime: `${platform.response_time}ms`,
          rateLimit: {
            used: platform.rate_limit_used,
            limit: platform.rate_limit_total,
            percentage: (platform.rate_limit_used / platform.rate_limit_total) * 100
          },
          lastCheck: formatTimestamp(platform.last_check),
          color: getPlatformColor(platform.platform)
        }))

        setPlatformHealth(transformedData)
        setLastUpdate(new Date())
      }
    } catch (error) {
      console.error('Failed to fetch health data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Load connected platforms
  useEffect(() => {
    const platforms = platformService.getConnectedPlatforms()
    setConnectedPlatforms(platforms)

    const unsubscribe = platformService.subscribe((platforms) => {
      setConnectedPlatforms(platforms)
    })

    return unsubscribe
  }, [])

  // Fetch data when connected platforms change
  useEffect(() => {
    fetchHealthData()
  }, [connectedPlatforms])

  // WebSocket for real-time updates
  useEffect(() => {
    if (connectedPlatforms.length === 0) return

    healthWebSocket.connect()

    const unsubConnection = healthWebSocket.on('connection', () => {
      setIsConnected(true)
    })

    const unsubDisconnect = healthWebSocket.on('disconnect', () => {
      setIsConnected(false)
    })

    const unsubUpdate = healthWebSocket.on('health_update', (platforms) => {
      const connectedPlatformIds = connectedPlatforms.map(p => p.id)
      const filteredPlatforms = platforms.filter(p =>
        connectedPlatformIds.includes(p.platform.toLowerCase())
      )

      const transformedData = filteredPlatforms.map(platform => ({
        platform: platform.platform.charAt(0).toUpperCase() + platform.platform.slice(1),
        icon: getPlatformIcon(platform.platform),
        status: platform.status,
        responseTime: `${platform.response_time}ms`,
        rateLimit: {
          used: platform.rate_limit_used,
          limit: platform.rate_limit_total,
          percentage: (platform.rate_limit_used / platform.rate_limit_total) * 100
        },
        lastCheck: formatTimestamp(platform.last_check),
        color: getPlatformColor(platform.platform)
      }))

      setPlatformHealth(transformedData)
      setLastUpdate(new Date())
    })

    const unsubAlert = healthWebSocket.on('health_alert', (alert) => {
      setActiveAlerts(prev => {
        const newAlerts = [{
          id: Date.now(),
          type: alert.severity,
          platform: alert.platform.charAt(0).toUpperCase() + alert.platform.slice(1),
          message: alert.message,
          time: formatTimestamp(alert.timestamp),
          acknowledged: false
        }, ...prev]
        return newAlerts.slice(0, 10)
      })
    })

    return () => {
      unsubConnection()
      unsubDisconnect()
      unsubUpdate()
      unsubAlert()
    }
  }, [connectedPlatforms])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="fade-in">
        <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
          Health Check Dashboard 🩺
        </h1>
        <p style={{ color: 'var(--gray-600)' }}>
          Monitor system health, platform connectivity, and reliability metrics
        </p>
      </div>

      {/* Check for connected platforms */}
      {connectedPlatforms.length === 0 ? (
        <div className="card">
          <div className="card-content">
            <div className="text-center py-16">
              <div className="text-6xl mb-4">🔗</div>
              <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
                No Platforms Connected
              </h2>
              <p className="mb-6" style={{ color: 'var(--gray-600)' }}>
                Connect your social media platforms to monitor their health and performance
              </p>
              <Link to="/settings" className="btn btn-primary">
                <span>Connect Platforms</span>
              </Link>
            </div>
          </div>
        </div>
      ) : (
        <>
          {/* Status Bar */}
          <div className="card slide-up">
            <div className="card-content">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></div>
                    <span className="text-sm" style={{ color: 'var(--gray-600)' }}>
                      {isConnected ? 'Live Updates' : 'Disconnected'}
                    </span>
                  </div>
                  {lastUpdate && (
                    <span className="text-sm" style={{ color: 'var(--gray-600)' }}>
                      Updated: {lastUpdate.toLocaleTimeString()}
                    </span>
                  )}
                </div>
                <button
                  className="btn btn-outline btn-sm"
                  onClick={fetchHealthData}
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <div className="spinner"></div>
                      <span>Refreshing...</span>
                    </>
                  ) : (
                    <>
                      <span>🔄</span>
                      <span>Refresh</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Active Alerts */}
          <div className="card slide-up">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                  Active Alerts
                </h3>
                <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
                  {activeAlerts.filter(alert => !alert.acknowledged).length}
                </span>
              </div>
            </div>
            <div className="card-content">
              {activeAlerts.length === 0 ? (
                <div className="text-center py-8" style={{ color: 'var(--gray-600)' }}>
                  <div className="text-4xl mb-2">✅</div>
                  <p>All systems healthy</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {activeAlerts.map((alert) => (
                    <div key={alert.id} className={`p-3 border rounded-lg ${alert.acknowledged ? 'opacity-50' : ''}`} style={{ borderColor: 'var(--gray-200)' }}>
                      <div className="flex items-start justify-between mb-2">
                        {getStatusBadge(alert.type)}
                        <span className="text-xs" style={{ color: 'var(--gray-500)' }}>{alert.time}</span>
                      </div>
                      <div className="text-sm font-medium mb-1" style={{ color: 'var(--gray-800)' }}>
                        {alert.platform}
                      </div>
                      <div className="text-xs" style={{ color: 'var(--gray-600)' }}>
                        {alert.message}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Platform Health Status */}
          <div className="card slide-up">
            <div className="card-header">
              <h2 className="text-xl font-semibold" style={{ color: 'var(--gray-900)' }}>
                Platform Health Status
              </h2>
            </div>
            <div className="card-content">
              {isLoading ? (
                <div className="text-center py-12">
                  <div className="spinner mx-auto mb-4"></div>
                  <p style={{ color: 'var(--gray-600)' }}>Loading health data...</p>
                </div>
              ) : platformHealth.length === 0 ? (
                <div className="text-center py-12">
                  <p style={{ color: 'var(--gray-600)' }}>No health data available</p>
                  <button onClick={fetchHealthData} className="btn btn-primary mt-4">
                    Try Again
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {platformHealth.map((platform) => (
                    <div key={platform.platform} className="p-4 border rounded-lg" style={{ borderColor: 'var(--gray-200)' }}>
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <div
                            className="w-10 h-10 rounded-lg flex items-center justify-center text-white text-lg"
                            style={{ background: platform.color }}
                          >
                            {platform.icon}
                          </div>
                          <div>
                            <div className="font-medium" style={{ color: 'var(--gray-800)' }}>
                              {platform.platform}
                            </div>
                            <div className="text-xs" style={{ color: 'var(--gray-500)' }}>
                              Last check: {platform.lastCheck}
                            </div>
                          </div>
                        </div>
                        {getStatusBadge(platform.status)}
                      </div>

                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span style={{ color: 'var(--gray-600)' }}>Response Time:</span>
                          <span className="font-medium" style={{ color: 'var(--gray-800)' }}>{platform.responseTime}</span>
                        </div>

                        {/* Rate Limit Bar */}
                        <div className="mt-3">
                          <div className="flex justify-between text-xs mb-1">
                            <span style={{ color: 'var(--gray-600)' }}>Rate Limit</span>
                            <span style={{ color: getRateLimitColor(platform.rateLimit.percentage) }}>
                              {platform.rateLimit.used}/{platform.rateLimit.limit} ({platform.rateLimit.percentage.toFixed(1)}%)
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="h-2 rounded-full transition-all"
                              style={{
                                width: `${platform.rateLimit.percentage}%`,
                                background: getRateLimitColor(platform.rateLimit.percentage)
                              }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default Health
