/**
 * Health WebSocket Service
 *
 * Manages WebSocket connection for real-time health monitoring alerts.
 * Features:
 * - Auto-reconnection on disconnect
 * - Event-based message handling
 * - Alert history management
 * - Connection state tracking
 */

class HealthWebSocketService {
  constructor() {
    this.ws = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 3000 // 3 seconds
    this.isConnected = false
    this.listeners = {
      health_alert: [],
      health_update: [],
      connection: [],
      history: [],
      disconnect: [],
      error: []
    }

    // Store recent alerts
    this.alertHistory = []
    this.maxHistorySize = 50

    // WebSocket URL (adjust port if needed)
    this.wsUrl = 'ws://localhost:8000/ws/health'
  }

  /**
   * Connect to WebSocket server
   */
  connect() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected')
      return
    }

    console.log('🔌 Connecting to health monitoring WebSocket...')

    try {
      this.ws = new WebSocket(this.wsUrl)

      this.ws.onopen = () => {
        console.log('✅ WebSocket connected')
        this.isConnected = true
        this.reconnectAttempts = 0
        this._emit('connection', { status: 'connected' })
      }

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          this._handleMessage(data)
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      this.ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
        this._emit('error', error)
      }

      this.ws.onclose = () => {
        console.log('🔌 WebSocket disconnected')
        this.isConnected = false
        this._emit('disconnect', {})
        this._attemptReconnect()
      }

    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
      this._attemptReconnect()
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect() {
    if (this.ws) {
      console.log('🔌 Disconnecting WebSocket...')
      this.reconnectAttempts = this.maxReconnectAttempts // Prevent auto-reconnect
      this.ws.close()
      this.ws = null
      this.isConnected = false
    }
  }

  /**
   * Attempt to reconnect to WebSocket
   */
  _attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached')
      return
    }

    this.reconnectAttempts++
    console.log(`⏳ Reconnecting... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`)

    setTimeout(() => {
      this.connect()
    }, this.reconnectDelay * this.reconnectAttempts) // Exponential backoff
  }

  /**
   * Handle incoming WebSocket messages
   */
  _handleMessage(data) {
    const { type } = data

    switch (type) {
      case 'connection':
        console.log('🎉 Connection confirmed:', data.message)
        this._emit('connection', data)
        break

      case 'health_alert':
        console.log('🚨 Health alert received:', data.alert)
        this._addToHistory(data.alert)
        this._emit('health_alert', data.alert)
        break

      case 'health_update':
        console.log('📊 Health update received')
        this._emit('health_update', data.platforms)
        break

      case 'history':
        console.log('📚 Alert history received:', data.alerts.length, 'alerts')
        this.alertHistory = data.alerts
        this._emit('history', data.alerts)
        break

      case 'ping':
        // Respond to ping with pong
        this._sendPong()
        break

      case 'stats':
        console.log('📊 WebSocket stats:', data.data)
        break

      default:
        console.warn('Unknown message type:', type)
    }
  }

  /**
   * Add alert to history
   */
  _addToHistory(alert) {
    this.alertHistory.push(alert)

    // Keep only last N alerts
    if (this.alertHistory.length > this.maxHistorySize) {
      this.alertHistory = this.alertHistory.slice(-this.maxHistorySize)
    }
  }

  /**
   * Send pong response to server
   */
  _sendPong() {
    if (this.isConnected && this.ws) {
      this.ws.send(JSON.stringify({ type: 'pong' }))
    }
  }

  /**
   * Request alert history from server
   */
  requestHistory() {
    if (this.isConnected && this.ws) {
      this.ws.send(JSON.stringify({ type: 'get_history' }))
    }
  }

  /**
   * Request WebSocket stats from server
   */
  requestStats() {
    if (this.isConnected && this.ws) {
      this.ws.send(JSON.stringify({ type: 'get_stats' }))
    }
  }

  /**
   * Subscribe to WebSocket events
   *
   * @param {string} event - Event type (health_alert, health_update, connection, etc.)
   * @param {function} callback - Callback function
   * @returns {function} Unsubscribe function
   */
  on(event, callback) {
    if (!this.listeners[event]) {
      console.warn(`Unknown event type: ${event}`)
      return () => {}
    }

    this.listeners[event].push(callback)

    // Return unsubscribe function
    return () => {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback)
    }
  }

  /**
   * Emit event to all listeners
   */
  _emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => {
        try {
          callback(data)
        } catch (error) {
          console.error(`Error in ${event} listener:`, error)
        }
      })
    }
  }

  /**
   * Get alert history
   */
  getAlertHistory() {
    return this.alertHistory
  }

  /**
   * Get unread alert count (alerts from last N minutes)
   */
  getUnreadAlertCount(minutesAgo = 30) {
    const cutoffTime = new Date()
    cutoffTime.setMinutes(cutoffTime.getMinutes() - minutesAgo)

    return this.alertHistory.filter(alert => {
      const alertTime = new Date(alert.timestamp)
      return alertTime >= cutoffTime
    }).length
  }

  /**
   * Get connection status
   */
  getConnectionStatus() {
    return {
      connected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      alertHistoryCount: this.alertHistory.length
    }
  }

  /**
   * Clear alert history
   */
  clearHistory() {
    this.alertHistory = []
  }
}

// Export singleton instance
const healthWebSocket = new HealthWebSocketService()
export default healthWebSocket
