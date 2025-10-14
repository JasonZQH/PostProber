import React, { useState } from 'react'
import platformService from '../../services/platformService'

function PlatformConnectionModal({ isOpen, onClose, onComplete }) {
  const [selectedPlatform, setSelectedPlatform] = useState(null)
  const [isConnecting, setIsConnecting] = useState(false)
  const [connectedPlatforms, setConnectedPlatforms] = useState([])
  const [error, setError] = useState(null)

  const platforms = [
    { id: 'twitter', name: 'Twitter', icon: '🐦', color: '#1DA1F2', description: 'Connect to post tweets and monitor engagement' },
    { id: 'linkedin', name: 'LinkedIn', icon: '💼', color: '#0077B5', description: 'Share professional content and insights' },
    { id: 'instagram', name: 'Instagram', icon: '📷', color: '#E4405F', description: 'Post photos, stories, and reels' },
    { id: 'facebook', name: 'Facebook', icon: '📘', color: '#1877F2', description: 'Manage your Facebook page posts' }
  ]

  const handleConnectPlatform = async (platform) => {
    setSelectedPlatform(platform.id)
    setIsConnecting(true)
    setError(null)

    try {
      // Simulate OAuth flow
      await platformService.connectPlatform(platform.id, {
        username: `demo_user@${platform.id}`
      })

      setConnectedPlatforms(prev => [...prev, platform.id])
      setSelectedPlatform(null)
    } catch (err) {
      setError(`Failed to connect ${platform.name}. Please try again.`)
    } finally {
      setIsConnecting(false)
    }
  }

  const handleContinue = () => {
    if (connectedPlatforms.length > 0) {
      platformService.completeOnboarding()
      onComplete()
      onClose()
    }
  }

  const handleSkip = () => {
    platformService.completeOnboarding()
    onComplete()
    onClose()
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="p-8 border-b" style={{ borderColor: 'var(--gray-200)' }}>
          <h2 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
            Welcome to PostProber! 🚀
          </h2>
          <p style={{ color: 'var(--gray-600)' }}>
            Connect your social media platforms to get started. You can add more platforms later.
          </p>
        </div>

        {/* Platform Grid */}
        <div className="p-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {platforms.map((platform) => {
              const isConnected = connectedPlatforms.includes(platform.id)
              const isConnecting = selectedPlatform === platform.id

              return (
                <div
                  key={platform.id}
                  className="border rounded-xl p-6 transition-all hover:shadow-lg"
                  style={{
                    borderColor: isConnected ? platform.color : 'var(--gray-200)',
                    borderWidth: isConnected ? '2px' : '1px',
                    opacity: isConnecting ? 0.6 : 1
                  }}
                >
                  <div className="flex items-start gap-4 mb-4">
                    <div
                      className="w-14 h-14 rounded-xl flex items-center justify-center text-2xl text-white"
                      style={{ background: platform.color }}
                    >
                      {platform.icon}
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold mb-1" style={{ color: 'var(--gray-900)' }}>
                        {platform.name}
                      </h3>
                      <p className="text-sm" style={{ color: 'var(--gray-600)' }}>
                        {platform.description}
                      </p>
                    </div>
                  </div>

                  <button
                    className="btn btn-primary w-full"
                    style={{
                      background: isConnected ? 'var(--accent-green)' : platform.color,
                      borderColor: isConnected ? 'var(--accent-green)' : platform.color
                    }}
                    onClick={() => handleConnectPlatform(platform)}
                    disabled={isConnected || isConnecting}
                  >
                    {isConnecting ? (
                      <>
                        <div className="spinner"></div>
                        <span>Connecting...</span>
                      </>
                    ) : isConnected ? (
                      <>
                        <span>✓</span>
                        <span>Connected</span>
                      </>
                    ) : (
                      <>
                        <span>Connect {platform.name}</span>
                      </>
                    )}
                  </button>
                </div>
              )
            })}
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          {/* Connection Status */}
          {connectedPlatforms.length > 0 && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm text-green-700">
                ✓ {connectedPlatforms.length} {connectedPlatforms.length === 1 ? 'platform' : 'platforms'} connected successfully!
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-8 border-t bg-gray-50" style={{ borderColor: 'var(--gray-200)' }}>
          <div className="flex justify-between items-center">
            <button
              className="btn btn-ghost"
              onClick={handleSkip}
              disabled={isConnecting}
            >
              Skip for now
            </button>
            <button
              className="btn btn-primary"
              onClick={handleContinue}
              disabled={connectedPlatforms.length === 0 || isConnecting}
            >
              Continue to Dashboard
            </button>
          </div>
          <p className="text-xs text-center mt-4" style={{ color: 'var(--gray-500)' }}>
            You can connect or disconnect platforms anytime from Settings
          </p>
        </div>
      </div>
    </div>
  )
}

export default PlatformConnectionModal
