import React, { useState, useEffect } from 'react'
import platformService from '../../services/platformService'

function PlatformManagementCard() {
  const [platforms, setPlatforms] = useState([])
  const [isConnecting, setIsConnecting] = useState(null)
  const [isDisconnecting, setIsDisconnecting] = useState(null)

  useEffect(() => {
    loadPlatforms()

    // Subscribe to platform changes
    const unsubscribe = platformService.subscribe(() => {
      loadPlatforms()
    })

    return unsubscribe
  }, [])

  const loadPlatforms = () => {
    setPlatforms(platformService.getAllPlatforms())
  }

  const handleConnect = async (platform) => {
    setIsConnecting(platform.id)
    try {
      await platformService.connectPlatform(platform.id, {
        username: `demo_user@${platform.id}`
      })
    } catch (error) {
      console.error('Failed to connect platform:', error)
    } finally {
      setIsConnecting(null)
    }
  }

  const handleDisconnect = (platformId) => {
    if (confirm(`Are you sure you want to disconnect ${platformService.getPlatformName(platformId)}?`)) {
      setIsDisconnecting(platformId)
      platformService.disconnectPlatform(platformId)
      setIsDisconnecting(null)
    }
  }

  const connectedCount = platforms.filter(p => p.status === 'connected').length

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold" style={{ color: 'var(--gray-900)' }}>
              Connected Platforms
            </h3>
            <p className="text-sm" style={{ color: 'var(--gray-600)' }}>
              {connectedCount} of 4 platforms connected
            </p>
          </div>
        </div>
      </div>
      <div className="card-content">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {platforms.map((platform) => {
            const isConnected = platform.status === 'connected'
            const isProcessing = isConnecting === platform.id || isDisconnecting === platform.id

            return (
              <div
                key={platform.id}
                className="p-4 border rounded-lg transition-all"
                style={{
                  borderColor: isConnected ? platform.color : 'var(--gray-200)',
                  borderWidth: isConnected ? '2px' : '1px',
                  opacity: isProcessing ? 0.6 : 1
                }}
              >
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
                        {platform.name}
                      </div>
                      {isConnected && platform.username && (
                        <div className="text-xs" style={{ color: 'var(--gray-500)' }}>
                          @{platform.username}
                        </div>
                      )}
                    </div>
                  </div>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      isConnected
                        ? 'bg-green-100 text-green-700'
                        : 'bg-gray-100 text-gray-700'
                    }`}
                  >
                    {isConnected ? '✓ Connected' : 'Not connected'}
                  </span>
                </div>

                {isConnected ? (
                  <button
                    className="btn btn-outline btn-sm w-full"
                    style={{ borderColor: 'var(--danger-red)', color: 'var(--danger-red)' }}
                    onClick={() => handleDisconnect(platform.id)}
                    disabled={isProcessing}
                  >
                    {isDisconnecting === platform.id ? (
                      <>
                        <div className="spinner"></div>
                        <span>Disconnecting...</span>
                      </>
                    ) : (
                      'Disconnect'
                    )}
                  </button>
                ) : (
                  <button
                    className="btn btn-primary btn-sm w-full"
                    style={{ background: platform.color, borderColor: platform.color }}
                    onClick={() => handleConnect(platform)}
                    disabled={isProcessing}
                  >
                    {isConnecting === platform.id ? (
                      <>
                        <div className="spinner"></div>
                        <span>Connecting...</span>
                      </>
                    ) : (
                      `Connect ${platform.name}`
                    )}
                  </button>
                )}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default PlatformManagementCard
