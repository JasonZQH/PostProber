/**
 * AI Service
 *
 * Frontend service for AI-powered features:
 * - Content optimization
 * - Hashtag generation
 * - Combined optimization + hashtags
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class AIService {
    /**
     * Optimize social media content for maximum engagement
     *
     * @param {string} content - Post content to optimize
     * @param {string} platform - Target platform (twitter, linkedin, instagram, facebook)
     * @returns {Promise<Object>} Optimization result with score and improvements
     */
    async optimizeContent(content, platform) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/optimize-content`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content,
                    platform: platform.toLowerCase()
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Content optimization failed');
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Content optimization error:', error);
            throw error;
        }
    }

    /**
     * Generate strategic hashtags for content
     *
     * @param {string} content - Post content to analyze
     * @param {string} platform - Target platform
     * @returns {Promise<Object>} Hashtag generation result
     */
    async generateHashtags(content, platform) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/generate-hashtags`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content,
                    platform: platform.toLowerCase()
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Hashtag generation failed');
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Hashtag generation error:', error);
            throw error;
        }
    }

    /**
     * Optimize content AND generate hashtags in one call
     *
     * More efficient than calling both endpoints separately.
     *
     * @param {string} content - Post content
     * @param {string} platform - Target platform
     * @returns {Promise<Object>} Combined optimization and hashtag results
     */
    async optimizeWithHashtags(content, platform) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/optimize-with-hashtags`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content,
                    platform: platform.toLowerCase()
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'AI optimization failed');
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Combined optimization error:', error);
            throw error;
        }
    }

    /**
     * Check if AI API is healthy and available
     *
     * @returns {Promise<Object>} Health status
     */
    async checkHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/health/status`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('AI API health check failed:', error);
            return {
                status: 'unhealthy',
                error: error.message
            };
        }
    }
}

// Export singleton instance
export default new AIService();
