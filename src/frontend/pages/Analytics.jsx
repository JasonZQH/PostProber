import React, { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import analyticsService from '../services/analyticsService'
import platformService from '../services/platformService'

function Analytics() {
  const [selectedPeriod, setSelectedPeriod] = useState('7d')
  const [selectedPlatform, setSelectedPlatform] = useState('')
  const [aiInsights, setAiInsights] = useState(null)
  const [isLoadingInsights, setIsLoadingInsights] = useState(false)
  const [showAiInsights, setShowAiInsights] = useState(false)
  const [connectedPlatforms, setConnectedPlatforms] = useState([])

  const periods = [
    { value: '24h', label: '24 Hours' },
    { value: '7d', label: '7 Days' },
    { value: '30d', label: '30 Days' },
    { value: '90d', label: '90 Days' }
  ]

  // Load connected platforms
  useEffect(() => {
    const platforms = platformService.getConnectedPlatforms()
    setConnectedPlatforms(platforms)

    // Set default platform to first connected platform
    if (platforms.length > 0 && !selectedPlatform) {
      setSelectedPlatform(platforms[0].id)
    }

    const unsubscribe = platformService.subscribe((platforms) => {
      setConnectedPlatforms(platforms)
      // If current selected platform is disconnected, switch to first available
      if (platforms.length > 0 && !platforms.some(p => p.id === selectedPlatform)) {
        setSelectedPlatform(platforms[0].id)
      } else if (platforms.length === 0) {
        setSelectedPlatform('')
      }
    })

    return unsubscribe
  }, [])

  // Build platform selector options from connected platforms
  const platformOptions = [
    ...(connectedPlatforms.length > 1 ? [{ value: 'all', label: 'All Platforms', icon: '📊' }] : []),
    ...connectedPlatforms.map(platform => ({
      value: platform.id,
      label: platform.name,
      icon: platform.icon
    }))
  ]

  const summaryCards = useMemo(() => {
    if (aiInsights && showAiInsights) {
      const topFormats = aiInsights.trending?.top_formats?.slice(0, 2).join(', ') || '—'
      const topTopics = aiInsights.trending?.top_topics?.slice(0, 2).join(', ') || '—'
      const bestAdvice = aiInsights.best_times?.general_advice || 'Use the recommendations below to choose posting windows.'
      const score = aiInsights.performance?.overall_score

      return [
        {
          label: 'Overall Performance Score',
          value: typeof score === 'number' ? `${score}/100` : '—',
          icon: '🎯',
          description: 'AI benchmarking based on trending engagement.'
        },
        {
          label: 'Trending Formats',
          value: topFormats,
          icon: '📋',
          description: 'Formats most likely to perform well right now.'
        },
        {
          label: 'Hot Topics',
          value: topTopics,
          icon: '🔥',
          description: 'Themes driving the highest engagement this week.'
        },
        {
          label: 'Posting Guidance',
          value: aiInsights.best_times?.timezone || 'Local Time',
          icon: '⏰',
          description: bestAdvice
        }
      ]
    }

    if (connectedPlatforms.length > 0) {
      return [
        {
          label: 'Analysis Status',
          value: 'Awaiting AI Insights',
          icon: '🕒',
          description: 'Run “Get AI Insights” to analyze your connected platform.'
        },
        {
          label: 'Connected Platforms',
          value: connectedPlatforms.map(p => p.name).join(', '),
          icon: '🔗',
          description: 'Insights are specific to the platform you select above.'
        }
      ]
    }

    return []
  }, [aiInsights, showAiInsights, connectedPlatforms])


  // Load AI insights
  const loadAIInsights = async () => {
    if (selectedPlatform === 'all') {
      alert('Please select a specific platform to get AI insights')
      return
    }

    setIsLoadingInsights(true)
    try {
      const dashboard = await analyticsService.getAnalyticsDashboard(selectedPlatform)
      if (dashboard.success) {
        setAiInsights(dashboard.result)
        setShowAiInsights(true)
      }
    } catch (error) {
      console.error('Failed to load AI insights:', error)
      alert('Failed to load AI insights. Make sure the backend is running.')
    } finally {
      setIsLoadingInsights(false)
    }
  }

  // Check if no platforms connected
  if (connectedPlatforms.length === 0) {
    return (
      <div className="space-y-6">
        <div className="fade-in">
          <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
            Analytics Dashboard 📊
          </h1>
          <p style={{ color: 'var(--gray-600)' }}>
            Track your social media performance and growth metrics
          </p>
        </div>

        <div className="card">
          <div className="card-content">
            <div className="text-center py-16">
              <div className="text-6xl mb-4">📊</div>
              <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
                No Analytics Data Available
              </h2>
              <p className="mb-6" style={{ color: 'var(--gray-600)' }}>
                Connect your social media platforms to start tracking your performance
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
          Analytics Dashboard 📊
        </h1>
        <p style={{ color: 'var(--gray-600)' }}>
          Track your social media performance and growth metrics
        </p>
      </div>

      {/* Filters */}
      <div className="card slide-up">
        <div className="card-content">
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex items-center gap-2">
              <label className="text-sm font-medium" style={{ color: 'var(--gray-700)' }}>
                Time Period:
              </label>
              <select
                value={selectedPeriod}
                onChange={(e) => setSelectedPeriod(e.target.value)}
                className="form-input w-auto"
              >
                {periods.map(period => (
                  <option key={period.value} value={period.value}>
                    {period.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-center gap-2">
              <label className="text-sm font-medium" style={{ color: 'var(--gray-700)' }}>
                Platform:
              </label>
              <select
                value={selectedPlatform}
                onChange={(e) => setSelectedPlatform(e.target.value)}
                className="form-input w-auto"
              >
                {platformOptions.map(platform => (
                  <option key={platform.value} value={platform.value}>
                    {platform.icon} {platform.label}
                  </option>
                ))}
              </select>
            </div>
            <button
              onClick={loadAIInsights}
              disabled={isLoadingInsights || selectedPlatform === 'all'}
              className="btn btn-primary"
              style={{ background: 'var(--accent-green)', borderColor: 'var(--accent-green)' }}
            >
              {isLoadingInsights ? (
                <>
                  <div className="spinner"></div>
                  <span>Loading AI Insights...</span>
                </>
              ) : (
                <>
                  <span>🤖</span>
                  <span>Get AI Insights</span>
                </>
              )}
            </button>
            <button className="btn btn-outline">
              <span>📤</span>
              <span>Export Report</span>
            </button>
          </div>
      </div>
    </div>

      {/* Summary Cards */}
      {summaryCards.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
          {summaryCards.map((card, index) => (
            <div key={card.label} className="card slide-up" style={{ animationDelay: `${index * 80}ms` }}>
              <div className="card-content">
                <div className="flex items-center gap-3 mb-3">
                  <div
                    className="w-10 h-10 rounded-lg flex items-center justify-center text-xl text-white"
                    style={{ background: 'var(--primary-blue)' }}
                  >
                    {card.icon}
                  </div>
                  <div>
                    <div className="text-sm font-semibold" style={{ color: 'var(--gray-700)' }}>
                      {card.label}
                    </div>
                    <div className="text-2xl font-bold" style={{ color: 'var(--gray-900)' }}>
                      {card.value}
                    </div>
                  </div>
                </div>
                <p className="text-xs" style={{ color: 'var(--gray-600)' }}>
                  {card.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* AI Insights Section */}
      {showAiInsights && aiInsights && (
        <div className="space-y-6 slide-up">
          {/* Trending Insights */}
          <div className="card" style={{ borderColor: 'var(--accent-green)', borderWidth: '2px' }}>
            <div className="card-header">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">🔥</span>
                  <h2 className="text-xl font-semibold" style={{ color: 'var(--gray-900)' }}>
                    Trending on {selectedPlatform.charAt(0).toUpperCase() + selectedPlatform.slice(1)}
                  </h2>
                </div>
                <button
                  onClick={() => setShowAiInsights(false)}
                  className="btn btn-sm btn-ghost"
                >
                  ✕
                </button>
              </div>
            </div>
            <div className="card-content">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Top Formats */}
                <div>
                  <h4 className="font-semibold mb-3" style={{ color: 'var(--gray-800)' }}>
                    📋 Top Formats
                  </h4>
                  <div className="space-y-2">
                    {aiInsights.trending?.top_formats?.slice(0, 5).map((format, idx) => (
                      <div key={idx} className="flex items-center gap-2">
                        <span className="text-sm px-2 py-1 rounded-full" style={{ background: 'var(--accent-green)', color: 'white' }}>
                          {idx + 1}
                        </span>
                        <span className="text-sm">{format}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Top Topics */}
                <div>
                  <h4 className="font-semibold mb-3" style={{ color: 'var(--gray-800)' }}>
                    💡 Top Topics
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {aiInsights.trending?.top_topics?.map((topic, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 rounded-full text-sm"
                        style={{ background: 'rgba(0, 210, 91, 0.1)', color: 'var(--accent-green-dark)' }}
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Engagement Drivers */}
                <div>
                  <h4 className="font-semibold mb-3" style={{ color: 'var(--gray-800)' }}>
                    🚀 Engagement Drivers
                  </h4>
                  <div className="space-y-2">
                    {aiInsights.trending?.engagement_drivers?.map((driver, idx) => (
                      <div key={idx} className="flex items-start gap-2">
                        <span style={{ color: 'var(--accent-green)' }}>✓</span>
                        <span className="text-sm">{driver}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Posting Advice */}
              {aiInsights.trending?.posting_advice && (
                <div className="mt-6 p-4 rounded-lg" style={{ background: 'rgba(0, 210, 91, 0.05)' }}>
                  <h4 className="font-semibold mb-2" style={{ color: 'var(--gray-800)' }}>
                    💬 AI Recommendation
                  </h4>
                  <p className="text-sm" style={{ color: 'var(--gray-700)' }}>
                    {aiInsights.trending.posting_advice}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Best Times to Post */}
          {aiInsights.best_times && (
            <div className="card">
              <div className="card-header">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">⏰</span>
                  <h2 className="text-xl font-semibold" style={{ color: 'var(--gray-900)' }}>
                    Best Times to Post
                  </h2>
                </div>
              </div>
              <div className="card-content">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {aiInsights.best_times.recommendations?.map((rec, idx) => (
                    <div key={idx} className="p-4 border rounded-lg" style={{ borderColor: 'var(--gray-200)' }}>
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-semibold" style={{ color: 'var(--gray-800)' }}>
                          📅 {rec.day}
                        </h4>
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium`}
                          style={{
                            background: rec.confidence === 'high' ? 'rgba(0, 210, 91, 0.1)' : 'rgba(255, 140, 0, 0.1)',
                            color: rec.confidence === 'high' ? 'var(--accent-green)' : 'var(--warning-orange)'
                          }}
                        >
                          {rec.confidence} confidence
                        </span>
                      </div>
                      <div className="space-y-2">
                        {rec.time_slots?.map((slot, sidx) => (
                          <div key={sidx} className="text-sm px-3 py-2 rounded" style={{ background: 'var(--gray-100)' }}>
                            🕐 {slot}
                          </div>
                        ))}
                      </div>
                      <p className="mt-3 text-xs" style={{ color: 'var(--gray-600)' }}>
                        {rec.reason}
                      </p>
                    </div>
                  ))}
                </div>
                {aiInsights.best_times.general_advice && (
                  <div className="mt-4 p-3 rounded-lg" style={{ background: 'var(--gray-100)' }}>
                    <p className="text-sm" style={{ color: 'var(--gray-700)' }}>
                      💡 <strong>Tip:</strong> {aiInsights.best_times.general_advice}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Performance Comparison */}
          {aiInsights.performance && (
            <div className="card">
              <div className="card-header">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">📊</span>
                  <h2 className="text-xl font-semibold" style={{ color: 'var(--gray-900)' }}>
                    Performance Insights
                  </h2>
                </div>
              </div>
              <div className="card-content">
                <div className="flex items-center gap-4 mb-6">
                  <div className="text-center">
                    <div className="text-4xl font-bold mb-1" style={{ color: 'var(--accent-green)' }}>
                      {aiInsights.performance.overall_score}
                    </div>
                    <div className="text-sm" style={{ color: 'var(--gray-600)' }}>Overall Score</div>
                  </div>
                  <div className="flex-1">
                    <div className="space-y-3">
                      {aiInsights.performance.insights?.map((insight, idx) => (
                        <div key={idx} className="flex items-start gap-2">
                          <span style={{ color: 'var(--accent-green)' }}>•</span>
                          <span className="text-sm" style={{ color: 'var(--gray-700)' }}>{insight}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Action Plan */}
                {aiInsights.performance.action_plan && (
                  <div className="p-4 rounded-lg" style={{ background: 'rgba(0, 210, 91, 0.05)' }}>
                    <h4 className="font-semibold mb-3" style={{ color: 'var(--gray-800)' }}>
                      🎯 Action Plan
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {aiInsights.performance.action_plan.map((action, idx) => (
                        <div key={idx} className="flex items-start gap-2">
                          <span className="text-sm font-bold" style={{ color: 'var(--accent-green)' }}>
                            {idx + 1}.
                          </span>
                          <span className="text-sm" style={{ color: 'var(--gray-700)' }}>{action}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Historical analytics placeholder */}
      <div className="card slide-up">
        <div className="card-content">
          <div className="flex items-start gap-4">
            <div className="text-3xl">🗂️</div>
            <div>
              <h3 className="font-semibold mb-2" style={{ color: 'var(--gray-900)' }}>
                Historical Analytics Coming Soon
              </h3>
              <p className="text-sm" style={{ color: 'var(--gray-600)' }}>
                Detailed post histories, scheduling analytics, and engagement breakdowns will appear here once the
                LinkedIn Publishing API access is granted. For now, run the AI insights above to explore trending patterns
                and recommended actions tailored to your connected platform.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Analytics
