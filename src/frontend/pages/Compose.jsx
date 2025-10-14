import React, { useState } from 'react'
import aiService from '../services/aiService'

function Compose() {
  const [postContent, setPostContent] = useState('')
  const [selectedPlatforms, setSelectedPlatforms] = useState([])
  const [isScheduled, setIsScheduled] = useState(false)
  const [scheduleDate, setScheduleDate] = useState('')
  const [scheduleTime, setScheduleTime] = useState('')
  const [isAIOptimizing, setIsAIOptimizing] = useState(false)
  const [aiSuggestions, setAiSuggestions] = useState(null)
  const [aiError, setAiError] = useState(null)

  const platforms = [
    { id: 'twitter', name: 'Twitter', icon: '🐦', limit: 280, connected: true },
    { id: 'linkedin', name: 'LinkedIn', icon: '💼', limit: 3000, connected: true },
    { id: 'instagram', name: 'Instagram', icon: '📷', limit: 2200, connected: false },
    { id: 'facebook', name: 'Facebook', icon: '📘', limit: 63206, connected: false }
  ]

  const handlePlatformToggle = (platformId) => {
    setSelectedPlatforms(prev =>
      prev.includes(platformId)
        ? prev.filter(p => p !== platformId)
        : [...prev, platformId]
    )
  }

  const handleAIOptimize = async () => {
    // Clear previous errors
    setAiError(null)
    setIsAIOptimizing(true)

    try {
      // Get the first selected platform (or default to twitter)
      const targetPlatform = selectedPlatforms.length > 0
        ? selectedPlatforms[0]
        : 'twitter'

      // Call AI service to optimize content AND generate hashtags
      const response = await aiService.optimizeWithHashtags(postContent, targetPlatform)

      if (response.success) {
        const { optimization, hashtags } = response.result

        // Format AI suggestions for the UI
        setAiSuggestions({
          optimizedContent: optimization.optimized_content,
          score: optimization.score,
          improvements: optimization.improvements,
          hashtags: hashtags.hashtags.map(h => h.tag),
          hashtagsWithMeta: hashtags.hashtags, // Keep full metadata
          processingTime: response.processing_time
        })
      } else {
        throw new Error('AI optimization failed')
      }

    } catch (error) {
      console.error('AI optimization error:', error)
      setAiError(error.message || 'Failed to optimize content. Please try again.')
    } finally {
      setIsAIOptimizing(false)
    }
  }

  const getCharacterCount = (platformId) => {
    const platform = platforms.find(p => p.id === platformId)
    if (!platform) return 0
    return Math.min(postContent.length, platform.limit)
  }

  const getCharacterPercentage = (platformId) => {
    const platform = platforms.find(p => p.id === platformId)
    if (!platform) return 0
    return (postContent.length / platform.limit) * 100
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="fade-in">
        <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
          Create New Post ✍️
        </h1>
        <p style={{ color: 'var(--gray-600)' }}>
          Craft engaging content for your social media platforms
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Composer */}
        <div className="lg:col-span-2 space-y-6">
          {/* Content Input */}
          <div className="card slide-up">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold" style={{ color: 'var(--gray-900)' }}>
                  Post Content
                </h2>
                <button
                  onClick={handleAIOptimize}
                  disabled={!postContent.trim() || isAIOptimizing}
                  className="btn btn-outline btn-sm"
                  style={{ borderColor: 'var(--accent-green)', color: 'var(--accent-green)' }}
                >
                  {isAIOptimizing ? (
                    <>
                      <div className="spinner"></div>
                      <span>AI Optimizing...</span>
                    </>
                  ) : (
                    <>
                      <span>🤖</span>
                      <span>AI Optimize</span>
                    </>
                  )}
                </button>
              </div>
            </div>
            <div className="card-content">
              <textarea
                value={postContent}
                onChange={(e) => setPostContent(e.target.value)}
                placeholder="What's on your mind? Share your thoughts with the world..."
                className="form-input resize-none"
                rows="6"
              />

              {/* Character Counters */}
              {selectedPlatforms.length > 0 && (
                <div className="mt-4 space-y-3">
                  <h4 className="text-sm font-medium" style={{ color: 'var(--gray-700)' }}>
                    Character Limits
                  </h4>
                  {selectedPlatforms.map(platformId => {
                    const platform = platforms.find(p => p.id === platformId)
                    const count = getCharacterCount(platformId)
                    const percentage = getCharacterPercentage(platformId)
                    const isOverLimit = count >= platform.limit

                    return (
                      <div key={platformId} className="flex items-center gap-3">
                        <span className="text-lg">{platform.icon}</span>
                        <span className="text-sm font-medium w-20">{platform.name}</span>
                        <div className="flex-1">
                          <div className="progress-bar">
                            <div
                              className="progress-fill"
                              style={{
                                width: `${Math.min(percentage, 100)}%`,
                                background: isOverLimit ? 'var(--danger-red)' : 'var(--gradient-primary)'
                              }}
                            />
                          </div>
                        </div>
                        <span
                          className={`text-sm font-medium ${isOverLimit ? 'text-red-600' : ''}`}
                          style={{ color: isOverLimit ? 'var(--danger-red)' : 'var(--gray-600)' }}
                        >
                          {count}/{platform.limit}
                        </span>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          </div>

          {/* Platform Selection */}
          <div className="card slide-up">
            <div className="card-header">
              <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                Select Platforms
              </h3>
            </div>
            <div className="card-content">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {platforms.map(platform => (
                  <div
                    key={platform.id}
                    className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                      !platform.connected ? 'opacity-50 cursor-not-allowed' : ''
                    } ${
                      selectedPlatforms.includes(platform.id) && platform.connected
                        ? 'border-blue-400 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => platform.connected && handlePlatformToggle(platform.id)}
                  >
                    <div className="text-center">
                      <div className="text-3xl mb-2">{platform.icon}</div>
                      <div className="font-medium text-sm" style={{ color: 'var(--gray-800)' }}>
                        {platform.name}
                      </div>
                      {platform.connected ? (
                        selectedPlatforms.includes(platform.id) ? (
                          <div className="mt-2">
                            <span className="status-indicator status-success">✓ Selected</span>
                          </div>
                        ) : (
                          <div className="text-xs mt-1" style={{ color: 'var(--gray-500)' }}>
                            Click to select
                          </div>
                        )
                      ) : (
                        <div className="mt-2">
                          <span className="status-indicator status-warning">Not Connected</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Scheduling */}
          <div className="card slide-up">
            <div className="card-header">
              <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                Scheduling Options
              </h3>
            </div>
            <div className="card-content">
              <div className="flex items-center gap-6 mb-4">
                <label className="flex items-center gap-2">
                  <input
                    type="radio"
                    name="postTiming"
                    checked={!isScheduled}
                    onChange={() => setIsScheduled(false)}
                    className="w-4 h-4"
                  />
                  <span>Post Now</span>
                </label>
                <label className="flex items-center gap-2">
                  <input
                    type="radio"
                    name="postTiming"
                    checked={isScheduled}
                    onChange={() => setIsScheduled(true)}
                    className="w-4 h-4"
                  />
                  <span>Schedule for Later</span>
                </label>
              </div>

              {isScheduled && (
                <div className="grid grid-cols-2 gap-4 scale-in">
                  <div>
                    <label className="form-label">Date</label>
                    <input
                      type="date"
                      value={scheduleDate}
                      onChange={(e) => setScheduleDate(e.target.value)}
                      className="form-input"
                      min={new Date().toISOString().split('T')[0]}
                    />
                  </div>
                  <div>
                    <label className="form-label">Time</label>
                    <input
                      type="time"
                      value={scheduleTime}
                      onChange={(e) => setScheduleTime(e.target.value)}
                      className="form-input"
                    />
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* AI Error Display */}
          {aiError && (
            <div
              className="card slide-up"
              style={{ borderColor: 'var(--danger-red)', background: 'rgba(255, 0, 0, 0.05)' }}
            >
              <div className="card-content">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">⚠️</span>
                  <div>
                    <h4 className="font-semibold mb-1" style={{ color: 'var(--danger-red)' }}>
                      AI Optimization Failed
                    </h4>
                    <p className="text-sm" style={{ color: 'var(--gray-700)' }}>
                      {aiError}
                    </p>
                    <button
                      onClick={() => setAiError(null)}
                      className="btn btn-sm btn-outline mt-2"
                      style={{ borderColor: 'var(--danger-red)', color: 'var(--danger-red)' }}
                    >
                      Dismiss
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* AI Suggestions */}
          {aiSuggestions && (
            <div
              className="card slide-up"
              style={{ borderColor: 'var(--accent-green)', background: 'rgba(0, 210, 91, 0.05)' }}
            >
              <div className="card-header">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">🤖</span>
                  <h3 className="text-lg font-semibold" style={{ color: 'var(--accent-green-dark)' }}>
                    AI Optimization Complete
                  </h3>
                  <span
                    className="px-2 py-1 rounded-full text-xs font-bold text-white"
                    style={{ background: 'var(--accent-green)' }}
                  >
                    Score: {aiSuggestions.score}/100
                  </span>
                </div>
              </div>
              <div className="card-content">
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2" style={{ color: 'var(--gray-800)' }}>
                      Optimized Content:
                    </h4>
                    <div
                      className="p-3 rounded-lg border"
                      style={{ background: 'white', borderColor: 'var(--accent-green)' }}
                    >
                      {aiSuggestions.optimizedContent}
                    </div>
                    <button
                      onClick={() => setPostContent(aiSuggestions.optimizedContent)}
                      className="btn btn-success btn-sm mt-2"
                    >
                      Use This Version
                    </button>
                  </div>

                  <div>
                    <h4 className="font-medium mb-2" style={{ color: 'var(--gray-800)' }}>
                      Suggested Hashtags:
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {aiSuggestions.hashtags.map(tag => (
                        <button
                          key={tag}
                          onClick={() => setPostContent(prev => prev + ' ' + tag)}
                          className="px-3 py-1 rounded-full text-sm border hover:bg-gray-50"
                          style={{ borderColor: 'var(--accent-green)', color: 'var(--accent-green-dark)' }}
                        >
                          {tag}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Publish Actions */}
          <div className="card slide-up">
            <div className="card-content">
              <div className="space-y-3">
                <button
                  className="w-full btn btn-primary btn-lg"
                  disabled={!postContent.trim() || selectedPlatforms.length === 0}
                >
                  {isScheduled ? (
                    <>
                      <span>📅</span>
                      <span>Schedule Post</span>
                    </>
                  ) : (
                    <>
                      <span>🚀</span>
                      <span>Publish Now</span>
                    </>
                  )}
                </button>
                <button className="w-full btn btn-outline">
                  <span>💾</span>
                  <span>Save as Draft</span>
                </button>
              </div>
            </div>
          </div>

          {/* Best Times to Post */}
          <div
            className="card slide-up"
            style={{ background: 'var(--gradient-cool)', color: 'white' }}
          >
            <div className="card-content">
              <div className="text-center">
                <div className="text-2xl mb-3">⏰</div>
                <h3 className="font-semibold mb-2">Best Times to Post</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Today</span>
                    <span>2:00 PM - 4:00 PM</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Tomorrow</span>
                    <span>10:00 AM - 12:00 PM</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Content Tips */}
          <div className="card slide-up">
            <div className="card-header">
              <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
                Content Tips
              </h3>
            </div>
            <div className="card-content">
              <div className="space-y-3 text-sm">
                <div className="flex items-start gap-2">
                  <span style={{ color: 'var(--accent-green)' }}>✓</span>
                  <span>Add emojis to increase engagement</span>
                </div>
                <div className="flex items-start gap-2">
                  <span style={{ color: 'var(--accent-green)' }}>✓</span>
                  <span>Include relevant hashtags</span>
                </div>
                <div className="flex items-start gap-2">
                  <span style={{ color: 'var(--accent-green)' }}>✓</span>
                  <span>Ask questions to encourage comments</span>
                </div>
                <div className="flex items-start gap-2">
                  <span style={{ color: 'var(--warning-orange)' }}>•</span>
                  <span>Post when your audience is most active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Compose