import React, { useState } from 'react'

function Health() {
  const [selectedTimeRange, setSelectedTimeRange] = useState('24h')

  const timeRanges = [
    { value: '1h', label: '1 Hour' },
    { value: '24h', label: '24 Hours' },
    { value: '7d', label: '7 Days' },
    { value: '30d', label: '30 Days' }
  ]

  // Platform Health Status
  const platformHealth = [
    {
      platform: 'Twitter',
      icon: '🐦',
      status: 'healthy',
      uptime: '99.8%',
      responseTime: '245ms',
      apiCalls: 1247,
      rateLimit: { used: 850, limit: 1500, percentage: 56.7 },
      lastCheck: '2 minutes ago',
      color: '#1DA1F2'
    },
    {
      platform: 'LinkedIn',
      icon: '💼',
      status: 'healthy',
      uptime: '99.9%',
      responseTime: '189ms',
      apiCalls: 892,
      rateLimit: { used: 450, limit: 1000, percentage: 45.0 },
      lastCheck: '1 minute ago',
      color: '#0077B5'
    },
    {
      platform: 'Instagram',
      icon: '📷',
      status: 'warning',
      uptime: '98.5%',
      responseTime: '567ms',
      apiCalls: 634,
      rateLimit: { used: 890, limit: 1000, percentage: 89.0 },
      lastCheck: '3 minutes ago',
      color: '#E4405F'
    },
    {
      platform: 'Facebook',
      icon: '📘',
      status: 'critical',
      uptime: '95.2%',
      responseTime: '1.2s',
      apiCalls: 423,
      rateLimit: { used: 950, limit: 1000, percentage: 95.0 },
      lastCheck: '5 minutes ago',
      color: '#1877F2'
    }
  ]

  // Reliability Metrics
  const reliabilityMetrics = [
    {
      label: 'Post Success Rate',
      value: '98.4%',
      target: '99.0%',
      status: 'warning',
      icon: '📝',
      color: 'var(--warning-orange)',
      trend: '-0.6%'
    },
    {
      label: 'Platform Availability',
      value: '99.1%',
      target: '99.5%',
      status: 'warning',
      icon: '🌐',
      color: 'var(--warning-orange)',
      trend: '-0.4%'
    },
    {
      label: 'Error Rate',
      value: '1.6%',
      target: '< 1.0%',
      status: 'critical',
      icon: '⚠️',
      color: 'var(--danger-red)',
      trend: '+0.6%'
    },
    {
      label: 'Avg Response Time',
      value: '423ms',
      target: '< 500ms',
      status: 'healthy',
      icon: '⚡',
      color: 'var(--accent-green)',
      trend: '-12ms'
    }
  ]

  // Active Alerts
  const activeAlerts = [
    {
      id: 1,
      type: 'critical',
      platform: 'Facebook',
      message: 'API rate limit exceeded (95%)',
      time: '5 minutes ago',
      acknowledged: false
    },
    {
      id: 2,
      type: 'warning',
      platform: 'Instagram',
      message: 'High response time detected (567ms)',
      time: '12 minutes ago',
      acknowledged: false
    },
    {
      id: 3,
      type: 'info',
      platform: 'Twitter',
      message: 'Scheduled maintenance in 2 hours',
      time: '1 hour ago',
      acknowledged: true
    }
  ]

  // SLI/SLO Tracking
  const sloTracking = [
    {
      name: 'Post Delivery SLO',
      target: '99.0%',
      current: '98.4%',
      errorBudget: '60%',
      status: 'at-risk',
      timeRemaining: '23 days'
    },
    {
      name: 'Platform Uptime SLO',
      target: '99.5%',
      current: '99.1%',
      errorBudget: '20%',
      status: 'critical',
      timeRemaining: '23 days'
    },
    {
      name: 'Response Time SLO',
      target: '< 500ms',
      current: '423ms',
      errorBudget: '85%',
      status: 'healthy',
      timeRemaining: '23 days'
    }
  ]

  // Recent Incidents
  const recentIncidents = [
    {
      id: 1,
      title: 'Facebook API Rate Limit Breach',
      status: 'investigating',
      severity: 'critical',
      startTime: '2 hours ago',
      affectedPosts: 23,
      retryCount: 3
    },
    {
      id: 2,
      title: 'Instagram Connection Timeout',
      status: 'resolved',
      severity: 'warning',
      startTime: '6 hours ago',
      duration: '45 minutes',
      affectedPosts: 12,
      retryCount: 5
    },
    {
      id: 3,
      title: 'LinkedIn Authentication Failure',
      status: 'resolved',
      severity: 'warning',
      startTime: '1 day ago',
      duration: '1.2 hours',
      affectedPosts: 8,
      retryCount: 2
    }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy': return 'var(--accent-green)'
      case 'warning': return 'var(--warning-orange)'
      case 'critical': return 'var(--danger-red)'
      default: return 'var(--gray-500)'
    }
  }

  const getStatusBadge = (status) => {
    const colors = {
      healthy: { bg: 'rgba(0, 210, 91, 0.1)', text: 'var(--accent-green)', icon: '✅' },
      warning: { bg: 'rgba(255, 140, 0, 0.1)', text: 'var(--warning-orange)', icon: '⚠️' },
      critical: { bg: 'rgba(239, 68, 68, 0.1)', text: 'var(--danger-red)', icon: '🚨' },
      'at-risk': { bg: 'rgba(255, 140, 0, 0.1)', text: 'var(--warning-orange)', icon: '⚠️' }
    }

    const color = colors[status] || colors.healthy

    return (
      <span
        className="px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1"
        style={{ background: color.bg, color: color.text }}
      >
        <span>{color.icon}</span>
        <span className="capitalize">{status.replace('-', ' ')}</span>
      </span>
    )
  }

  const getRateLimitColor = (percentage) => {
    if (percentage >= 90) return 'var(--danger-red)'
    if (percentage >= 75) return 'var(--warning-orange)'
    return 'var(--accent-green)'
  }

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

      {/* Time Range Filter */}
      <div className="card slide-up">
        <div className="card-content">
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium" style={{ color: 'var(--gray-700)' }}>
              Time Range:
            </label>
            <select
              value={selectedTimeRange}
              onChange={(e) => setSelectedTimeRange(e.target.value)}
              className="form-input w-auto"
            >
              {timeRanges.map(range => (
                <option key={range.value} value={range.value}>
                  {range.label}
                </option>
              ))}
            </select>
            <button className="btn btn-outline ml-auto">
              <span>🔄</span>
              <span>Refresh</span>
            </button>
          </div>
        </div>
      </div>

      {/* Top Section: Stats + Active Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Section: Stats + SLO Tracking */}
        <div className="lg:col-span-2 flex flex-col h-full">
          {/* Reliability Metrics - 4 stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-6">
            {reliabilityMetrics.map((metric, index) => (
              <div key={metric.label} className="card slide-up" style={{ animationDelay: `${index * 100}ms` }}>
                <div className="card-content">
                  <div className="flex items-center justify-between mb-4">
                    <div
                      className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-xl"
                      style={{ background: metric.color }}
                    >
                      {metric.icon}
                    </div>
                    {getStatusBadge(metric.status)}
                  </div>
                  <div className="text-2xl font-bold mb-1" style={{ color: 'var(--gray-900)' }}>
                    {metric.value}
                  </div>
                  <div className="text-sm mb-2" style={{ color: 'var(--gray-600)' }}>
                    {metric.label}
                  </div>
                  <div className="flex justify-between text-xs">
                    <span style={{ color: 'var(--gray-500)' }}>Target: {metric.target}</span>
                    <span style={{ color: metric.trend.startsWith('+') ? 'var(--danger-red)' : 'var(--accent-green)' }}>
                      {metric.trend}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* SLO Tracking - Fills remaining space */}
          <div className="card slide-up flex-1 flex flex-col">
            <div className="card-header">
              <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                SLO Tracking
              </h3>
            </div>
            <div className="card-content flex-1 flex items-center">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 w-full">
                {sloTracking.map((slo) => (
                  <div key={slo.name} className="p-4 border rounded-lg" style={{ borderColor: 'var(--gray-200)' }}>
                    <div className="flex items-center justify-between mb-3">
                      <div className="text-sm font-medium" style={{ color: 'var(--gray-800)' }}>
                        {slo.name}
                      </div>
                      {getStatusBadge(slo.status)}
                    </div>
                    <div className="text-sm space-y-2" style={{ color: 'var(--gray-600)' }}>
                      <div className="flex justify-between">
                        <span>Current:</span>
                        <span className="font-medium">{slo.current}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Target:</span>
                        <span className="font-medium">{slo.target}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Error Budget:</span>
                        <span className="font-medium">{slo.errorBudget}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Active Alerts - Right side */}
        <div className="lg:col-span-1">
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
                    {!alert.acknowledged && (
                      <button className="mt-2 text-xs text-blue-600 hover:text-blue-800">
                        Acknowledge
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
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
                    <span style={{ color: 'var(--gray-600)' }}>Uptime:</span>
                    <span className="font-medium" style={{ color: 'var(--gray-800)' }}>{platform.uptime}</span>
                  </div>
                  <div className="flex justify-between">
                    <span style={{ color: 'var(--gray-600)' }}>Response Time:</span>
                    <span className="font-medium" style={{ color: 'var(--gray-800)' }}>{platform.responseTime}</span>
                  </div>
                  <div className="flex justify-between">
                    <span style={{ color: 'var(--gray-600)' }}>API Calls:</span>
                    <span className="font-medium" style={{ color: 'var(--gray-800)' }}>{platform.apiCalls}</span>
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
        </div>
      </div>

      {/* Incident Management */}
      <div className="card slide-up">
        <div className="card-header">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold" style={{ color: 'var(--gray-900)' }}>
              Incident Management
            </h2>
            <button className="btn btn-outline btn-sm">View All Incidents</button>
          </div>
        </div>
        <div className="card-content">
          <div className="space-y-4">
            {recentIncidents.map((incident) => (
              <div key={incident.id} className="p-4 border rounded-lg" style={{ borderColor: 'var(--gray-200)' }}>
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="font-medium mb-1" style={{ color: 'var(--gray-800)' }}>
                      {incident.title}
                    </div>
                    <div className="flex items-center gap-4 text-sm" style={{ color: 'var(--gray-600)' }}>
                      <span>Started: {incident.startTime}</span>
                      {incident.duration && <span>Duration: {incident.duration}</span>}
                      <span>Affected Posts: {incident.affectedPosts}</span>
                      <span>Retries: {incident.retryCount}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {getStatusBadge(incident.severity)}
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        incident.status === 'resolved' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'
                      }`}
                    >
                      {incident.status}
                    </span>
                  </div>
                </div>
                {incident.status === 'investigating' && (
                  <div className="flex gap-2">
                    <button className="btn btn-sm btn-outline">Retry Failed Posts</button>
                    <button className="btn btn-sm btn-outline">Manual Rollback</button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Health