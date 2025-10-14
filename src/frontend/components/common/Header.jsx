import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import healthWebSocket from '../../services/healthWebSocket'
import platformService from '../../services/platformService'

function Header() {
  const [alerts, setAlerts] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [showNotifications, setShowNotifications] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
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

  useEffect(() => {
    // Only connect to WebSocket if there are connected platforms
    if (connectedPlatforms.length === 0) {
      // Disconnect if previously connected
      healthWebSocket.disconnect()
      setAlerts([])
      setUnreadCount(0)
      setIsConnected(false)
      return
    }

    // Connect to WebSocket
    healthWebSocket.connect()

    // Subscribe to connection events
    const unsubConnection = healthWebSocket.on('connection', () => {
      setIsConnected(true)
    })

    const unsubDisconnect = healthWebSocket.on('disconnect', () => {
      setIsConnected(false)
    })

    // Subscribe to health alerts
    const unsubAlert = healthWebSocket.on('health_alert', (alert) => {
      setAlerts(prev => [...prev, alert].slice(-10)) // Keep last 10 alerts
      setUnreadCount(prev => prev + 1)
    })

    // Subscribe to alert history
    const unsubHistory = healthWebSocket.on('history', (history) => {
      setAlerts(history.slice(-10)) // Keep last 10 alerts
      setUnreadCount(healthWebSocket.getUnreadAlertCount(30))
    })

    // Cleanup on unmount or when platforms change
    return () => {
      unsubConnection()
      unsubDisconnect()
      unsubAlert()
      unsubHistory()
    }
  }, [connectedPlatforms])

  const handleNotificationClick = () => {
    setShowNotifications(!showNotifications)
    if (!showNotifications) {
      setUnreadCount(0) // Mark as read
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-500'
      case 'warning': return 'bg-orange-500'
      case 'info': return 'bg-blue-500'
      default: return 'bg-gray-500'
    }
  }

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical': return '🔴'
      case 'warning': return '🟡'
      case 'info': return '🔵'
      default: return '⚪'
    }
  }

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMinutes = Math.floor((now - date) / 60000)

    if (diffMinutes < 1) return 'Just now'
    if (diffMinutes < 60) return `${diffMinutes}m ago`
    if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}h ago`
    return date.toLocaleDateString()
  }

  return (
    <div className="navbar bg-base-100 shadow-soft border-b border-base-300 header-height px-6">
      {/* Left section: Menu toggle and Logo */}
      <div className="navbar-start">
        <button className="btn btn-ghost btn-circle focus-primary" aria-label="Toggle sidebar">
          <span className="iconify" data-icon="heroicons:bars-3" data-width="24"></span>
        </button>
        <div className="flex items-center ml-4">
          <img alt="PostProber Logo" className="w-10 h-10 rounded-lg" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='8' fill='%233B82F6'/%3E%3Ctext x='20' y='26' text-anchor='middle' fill='white' font-family='sans-serif' font-size='16' font-weight='bold'%3EPP%3C/text%3E%3C/svg%3E" />
          <span className="ml-3 text-xl font-semibold text-primary hidden lg:block">PostProber</span>
        </div>
      </div>

      {/* Center section: Search and actions only */}
      <div className="navbar-center hidden xl:flex">
        {/* Removed duplicate navigation - handled by sidebar */}
      </div>

      {/* Right section: Search and notifications */}
      <div className="navbar-end">
        {/* Global search */}
        <div className="form-control hidden md:block mr-4">
          <div className="join">
            <input type="text" placeholder="Search posts..." className="input input-bordered input-sm join-item w-48 focus-primary" />
            <button className="btn btn-sm join-item btn-primary" aria-label="Search">
              <span className="iconify" data-icon="heroicons:magnifying-glass" data-width="16"></span>
            </button>
          </div>
        </div>

        {/* Dashboard button for mobile */}
        <Link to="/dashboard" className="btn btn-ghost btn-sm md:hidden focus-primary">
          <span className="iconify" data-icon="heroicons:home" data-width="20"></span>
          <span>Dashboard</span>
        </Link>

        {/* Health Notifications */}
        <div className="dropdown dropdown-end mr-2">
          <div tabIndex={0} className="indicator">
            {unreadCount > 0 && (
              <span className="indicator-item badge badge-error badge-sm">{unreadCount}</span>
            )}
            <button
              onClick={handleNotificationClick}
              className={`btn btn-ghost btn-circle focus-primary ${!isConnected ? 'opacity-50' : ''}`}
              aria-label="Health notifications"
            >
              <span className="iconify" data-icon="heroicons:bell" data-width="20"></span>
            </button>
          </div>

          {showNotifications && (
            <div
              tabIndex={0}
              className="dropdown-content card card-compact w-80 mt-3 shadow-lg bg-base-100 border border-base-300 z-50"
            >
              <div className="card-body">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-lg">Health Alerts</h3>
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></div>
                    <span className="text-xs text-gray-500">
                      {isConnected ? 'Live' : 'Disconnected'}
                    </span>
                  </div>
                </div>

                {connectedPlatforms.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <span className="iconify" data-icon="heroicons:bell-slash" data-width="48"></span>
                    <p className="mt-2 text-sm">No platforms connected</p>
                    <p className="text-xs mt-1">Connect platforms to receive health alerts</p>
                  </div>
                ) : alerts.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <span className="iconify" data-icon="heroicons:check-circle" data-width="48" style={{ color: 'var(--accent-green)' }}></span>
                    <p className="mt-2">All systems healthy!</p>
                  </div>
                ) : (
                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {alerts.slice().reverse().map((alert, index) => (
                      <div
                        key={`${alert.platform}-${alert.timestamp}-${index}`}
                        className={`p-3 rounded-lg border-l-4 ${
                          alert.severity === 'critical' ? 'border-red-500 bg-red-50' :
                          alert.severity === 'warning' ? 'border-orange-500 bg-orange-50' :
                          'border-blue-500 bg-blue-50'
                        }`}
                      >
                        <div className="flex items-start gap-2">
                          <span className="text-lg">{getSeverityIcon(alert.severity)}</span>
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-semibold text-sm capitalize">{alert.platform}</span>
                              <span className="text-xs text-gray-500">{formatTimestamp(alert.timestamp)}</span>
                            </div>
                            <p className="text-sm text-gray-700 mb-1">{alert.message}</p>
                            {alert.recommended_action && (
                              <p className="text-xs text-gray-600">
                                💡 {alert.recommended_action}
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {connectedPlatforms.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-base-300">
                    <Link
                      to="/health"
                      className="btn btn-sm btn-block btn-primary"
                      onClick={() => setShowNotifications(false)}
                    >
                      View Full Health Dashboard
                    </Link>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Header