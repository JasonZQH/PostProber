/**
 * Platform Connection Service
 *
 * Manages platform connections and OAuth flows
 */

import { BsTwitterX } from 'react-icons/bs'
import { FaLinkedin, FaInstagram, FaFacebookF } from 'react-icons/fa'

class PlatformService {
  constructor() {
    this.connectedPlatforms = []
    this.listeners = []
    this.apiBaseUrl = 'http://localhost:8000'
    this.isInitialized = false

    // Load platforms from backend on initialization
    this.loadPlatformsFromBackend()
  }

  /**
   * Load connected platforms from backend API
   */
  async loadPlatformsFromBackend() {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/auth/status`, {
        credentials: 'include' // Include cookies for session
      })

      if (response.ok) {
        const data = await response.json()
        this.connectedPlatforms = data.connected_platforms.map(platform => ({
          id: platform.id,
          name: this.getPlatformName(platform.id),
          icon: this.getPlatformIcon(platform.id),
          color: this.getPlatformColor(platform.id),
          connectedAt: platform.connected_at,
          status: 'connected',
          username: platform.username,
          userId: platform.user_id
        }))
        this.isInitialized = true
        this.notifyListeners()
      }
    } catch (error) {
      console.error('Failed to load platforms from backend:', error)
      this.isInitialized = true
    }
  }

  /**
   * Refresh platform status from backend
   */
  async refreshPlatforms() {
    await this.loadPlatformsFromBackend()
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
   * Connect a platform (initiates OAuth flow)
   */
  async connectPlatform(platformId) {
    try {
      // Redirect to OAuth login endpoint
      const loginUrl = `${this.apiBaseUrl}/api/auth/${platformId.toLowerCase()}/login`
      window.location.href = loginUrl
    } catch (error) {
      console.error(`Failed to connect ${platformId}:`, error)
      throw error
    }
  }

  /**
   * Disconnect a platform
   */
  async disconnectPlatform(platformId) {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/auth/${platformId.toLowerCase()}/disconnect`, {
        method: 'POST',
        credentials: 'include' // Include cookies for session
      })

      if (!response.ok) {
        throw new Error(`Failed to disconnect ${platformId}`)
      }

      // Remove from local state
      this.connectedPlatforms = this.connectedPlatforms.filter(
        p => p.id !== platformId.toLowerCase()
      )
      this.notifyListeners()

      return true
    } catch (error) {
      console.error(`Failed to disconnect ${platformId}:`, error)
      throw error
    }
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
      twitter: 'X (Twitter)',
      linkedin: 'LinkedIn',
      instagram: 'Instagram',
      facebook: 'Facebook'
    }
    return names[platformId.toLowerCase()] || platformId
  }

  /**
   * Helper: Get platform icon (React component)
   */
  getPlatformIcon(platformId) {
    const icons = {
      twitter: BsTwitterX,
      linkedin: FaLinkedin,
      instagram: FaInstagram,
      facebook: FaFacebookF
    }
    return icons[platformId.toLowerCase()] || null
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
