/**
 * Platform Connection Service
 *
 * Manages platform connections and OAuth flows
 */

class PlatformService {
  constructor() {
    this.connectedPlatforms = this.loadConnectedPlatforms()
    this.listeners = []
  }

  /**
   * Load connected platforms from localStorage
   */
  loadConnectedPlatforms() {
    try {
      const stored = localStorage.getItem('connectedPlatforms')
      return stored ? JSON.parse(stored) : []
    } catch (error) {
      console.error('Failed to load connected platforms:', error)
      return []
    }
  }

  /**
   * Save connected platforms to localStorage
   */
  saveConnectedPlatforms() {
    try {
      localStorage.setItem('connectedPlatforms', JSON.stringify(this.connectedPlatforms))
      this.notifyListeners()
    } catch (error) {
      console.error('Failed to save connected platforms:', error)
    }
  }

  /**
   * Get all connected platforms
   */
  getConnectedPlatforms() {
    return this.connectedPlatforms
  }

  /**
   * Check if a platform is connected
   */
  isPlatformConnected(platform) {
    return this.connectedPlatforms.some(p => p.id === platform.toLowerCase())
  }

  /**
   * Connect a platform (simulated OAuth flow)
   */
  async connectPlatform(platformId, credentials = {}) {
    return new Promise((resolve, reject) => {
      // Simulate OAuth flow delay
      setTimeout(() => {
        const platform = {
          id: platformId.toLowerCase(),
          name: this.getPlatformName(platformId),
          icon: this.getPlatformIcon(platformId),
          color: this.getPlatformColor(platformId),
          connectedAt: new Date().toISOString(),
          status: 'connected',
          // Simulated OAuth tokens
          accessToken: `mock_token_${platformId}_${Date.now()}`,
          refreshToken: `mock_refresh_${platformId}_${Date.now()}`,
          expiresAt: new Date(Date.now() + 3600000).toISOString(), // 1 hour
          username: credentials.username || `user@${platformId}`,
          userId: `user_${Date.now()}`
        }

        // Check if already connected
        const existingIndex = this.connectedPlatforms.findIndex(p => p.id === platform.id)
        if (existingIndex >= 0) {
          // Update existing connection
          this.connectedPlatforms[existingIndex] = platform
        } else {
          // Add new connection
          this.connectedPlatforms.push(platform)
        }

        this.saveConnectedPlatforms()
        resolve(platform)
      }, 1500) // Simulate network delay
    })
  }

  /**
   * Disconnect a platform
   */
  disconnectPlatform(platformId) {
    this.connectedPlatforms = this.connectedPlatforms.filter(
      p => p.id !== platformId.toLowerCase()
    )
    this.saveConnectedPlatforms()
  }

  /**
   * Get platform details
   */
  getPlatform(platformId) {
    return this.connectedPlatforms.find(p => p.id === platformId.toLowerCase())
  }

  /**
   * Subscribe to platform changes
   */
  subscribe(listener) {
    this.listeners.push(listener)
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener)
    }
  }

  /**
   * Notify all listeners of changes
   */
  notifyListeners() {
    this.listeners.forEach(listener => {
      listener(this.connectedPlatforms)
    })
  }

  /**
   * Helper: Get platform name
   */
  getPlatformName(platformId) {
    const names = {
      twitter: 'Twitter',
      linkedin: 'LinkedIn',
      instagram: 'Instagram',
      facebook: 'Facebook'
    }
    return names[platformId.toLowerCase()] || platformId
  }

  /**
   * Helper: Get platform icon
   */
  getPlatformIcon(platformId) {
    const icons = {
      twitter: '🐦',
      linkedin: '💼',
      instagram: '📷',
      facebook: '📘'
    }
    return icons[platformId.toLowerCase()] || '📱'
  }

  /**
   * Helper: Get platform color
   */
  getPlatformColor(platformId) {
    const colors = {
      twitter: '#1DA1F2',
      linkedin: '#0077B5',
      instagram: '#E4405F',
      facebook: '#1877F2'
    }
    return colors[platformId.toLowerCase()] || '#6B7280'
  }

  /**
   * Get all available platforms (connected and unconnected)
   */
  getAllPlatforms() {
    const allPlatformIds = ['twitter', 'linkedin', 'instagram', 'facebook']

    return allPlatformIds.map(id => {
      const connected = this.getPlatform(id)
      if (connected) {
        return connected
      }

      return {
        id,
        name: this.getPlatformName(id),
        icon: this.getPlatformIcon(id),
        color: this.getPlatformColor(id),
        status: 'disconnected'
      }
    })
  }

  /**
   * Check if this is first time user (no platforms connected)
   */
  isFirstTimeUser() {
    return this.connectedPlatforms.length === 0
  }

  /**
   * Mark onboarding as complete
   */
  completeOnboarding() {
    localStorage.setItem('onboardingComplete', 'true')
  }

  /**
   * Check if onboarding is complete
   */
  isOnboardingComplete() {
    return localStorage.getItem('onboardingComplete') === 'true'
  }
}

// Export singleton instance
const platformService = new PlatformService()
export default platformService
