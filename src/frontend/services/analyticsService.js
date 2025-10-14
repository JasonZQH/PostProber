/**
 * Analytics Service
 *
 * Handles API calls for trending analysis and analytics insights
 */

const API_BASE_URL = 'http://localhost:8000'

class AnalyticsService {
  /**
   * Get trending content analysis for a platform
   */
  async getTrendingAnalysis(platform, category = null) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/trending/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          platform: platform.toLowerCase(),
          category
        })
      })

      if (!response.ok) {
        throw new Error('Failed to fetch trending analysis')
      }

      return await response.json()
    } catch (error) {
      console.error('Trending analysis error:', error)
      throw error
    }
  }

  /**
   * Get best posting times for a platform
   */
  async getBestPostingTimes(platform) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/trending/best-times/${platform.toLowerCase()}`)

      if (!response.ok) {
        throw new Error('Failed to fetch best posting times')
      }

      return await response.json()
    } catch (error) {
      console.error('Best posting times error:', error)
      throw error
    }
  }

  /**
   * Analyze user content against trending patterns
   */
  async analyzeContent(content, platform) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analytics/analyze-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          platform: platform.toLowerCase()
        })
      })

      if (!response.ok) {
        throw new Error('Failed to analyze content')
      }

      return await response.json()
    } catch (error) {
      console.error('Content analysis error:', error)
      throw error
    }
  }

  /**
   * Generate content ideas based on trending patterns
   */
  async generateContentIdeas(platform, category) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analytics/content-ideas`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          platform: platform.toLowerCase(),
          category: category.toLowerCase()
        })
      })

      if (!response.ok) {
        throw new Error('Failed to generate content ideas')
      }

      return await response.json()
    } catch (error) {
      console.error('Content ideas error:', error)
      throw error
    }
  }

  /**
   * Compare user performance with benchmarks
   */
  async comparePerformance(platform, userPosts = []) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analytics/performance-comparison`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          platform: platform.toLowerCase(),
          user_posts: userPosts
        })
      })

      if (!response.ok) {
        throw new Error('Failed to compare performance')
      }

      return await response.json()
    } catch (error) {
      console.error('Performance comparison error:', error)
      throw error
    }
  }

  /**
   * Get complete analytics dashboard data
   */
  async getAnalyticsDashboard(platform) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analytics/dashboard/${platform.toLowerCase()}`)

      if (!response.ok) {
        throw new Error('Failed to fetch analytics dashboard')
      }

      return await response.json()
    } catch (error) {
      console.error('Analytics dashboard error:', error)
      throw error
    }
  }
}

// Export singleton instance
const analyticsService = new AnalyticsService()
export default analyticsService
