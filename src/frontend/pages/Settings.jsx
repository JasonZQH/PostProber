import React, { useState } from 'react'
import PlatformManagementCard from '../components/platforms/PlatformManagementCard'

function Settings() {
  const [activeTab, setActiveTab] = useState('platforms')

  const tabs = [
    { id: 'platforms', label: 'Platforms', icon: '🔗' },
    { id: 'profile', label: 'Profile', icon: '👤' },
    { id: 'ai', label: 'AI Settings', icon: '🤖' },
    { id: 'notifications', label: 'Notifications', icon: '🔔' },
    { id: 'privacy', label: 'Privacy', icon: '🔒' }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="fade-in">
        <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
          Settings ⚙️
        </h1>
        <p style={{ color: 'var(--gray-600)' }}>
          Customize your PostProber experience and preferences
        </p>
      </div>

      {/* Tabs */}
      <div className="card slide-up">
        <div className="card-content p-0">
          <div className="flex border-b" style={{ borderColor: 'var(--gray-200)' }}>
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-4 font-medium transition-colors flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'border-b-2 text-blue-600'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
                style={{
                  borderBottomColor: activeTab === tab.id ? 'var(--primary-blue)' : 'transparent'
                }}
              >
                <span className="text-lg">{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Platforms Tab */}
        {activeTab === 'platforms' && (
          <div className="card-content">
            <PlatformManagementCard />
          </div>
        )}

        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <div className="card-content space-y-6">
            <div className="flex items-center gap-6">
              <div
                className="w-20 h-20 rounded-full flex items-center justify-center text-white text-2xl font-bold"
                style={{ background: 'var(--gradient-primary)' }}
              >
                U
              </div>
              <div>
                <h3 className="text-xl font-bold" style={{ color: 'var(--gray-900)' }}>User Profile</h3>
                <p style={{ color: 'var(--gray-600)' }}>Manage your account information</p>
                <button
                  className="mt-2 text-sm font-semibold hover:underline"
                  style={{ color: 'var(--primary-blue)' }}
                >
                  Change Avatar
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="form-label">
                  Email Address
                </label>
                <input
                  type="email"
                  className="form-input"
                  defaultValue="demo@postprober.com"
                />
              </div>
              <div>
                <label className="form-label">
                  Display Name
                </label>
                <input
                  type="text"
                  className="form-input"
                  defaultValue="PostProber User"
                />
              </div>
            </div>

            <div>
              <label className="form-label">
                Bio
              </label>
              <textarea
                className="form-input resize-none"
                rows="3"
                placeholder="Tell us about yourself..."
              />
            </div>

            <button className="btn btn-primary">
              <span>💾</span>
              <span>Save Changes</span>
            </button>
          </div>
        )}

        {/* AI Settings Tab */}
        {activeTab === 'ai' && (
          <div className="card-content space-y-6">
            <div
              className="p-6 rounded-xl"
              style={{ background: 'var(--gradient-primary)', color: 'white' }}
            >
              <div className="text-center">
                <div className="text-3xl mb-2">🤖</div>
                <h3 className="text-xl font-bold">AI Assistant Configuration</h3>
                <p className="opacity-90">Customize your AI experience</p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="form-label">
                  AI Personality
                </label>
                <div className="grid grid-cols-3 gap-4">
                  {['Professional', 'Casual', 'Creative'].map(style => (
                    <button
                      key={style}
                      className="p-4 border-2 rounded-xl transition-all hover:bg-gray-50"
                      style={{
                        borderColor: 'var(--gray-200)',
                        ':hover': { borderColor: 'var(--primary-blue)' }
                      }}
                    >
                      <div className="text-center">
                        <div className="text-2xl mb-2">
                          {style === 'Professional' ? '💼' : style === 'Casual' ? '😊' : '🎨'}
                        </div>
                        <div className="font-semibold" style={{ color: 'var(--gray-800)' }}>{style}</div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="form-label">
                  Content Optimization
                </label>
                <div className="space-y-3">
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Auto-suggest hashtags</span>
                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                  </label>
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Optimize posting times</span>
                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                  </label>
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Content sentiment analysis</span>
                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                  </label>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Notifications Tab */}
        {activeTab === 'notifications' && (
          <div className="card-content space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold mb-4" style={{ color: 'var(--gray-900)' }}>Email Notifications</h3>
                <div className="space-y-3">
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Post published successfully</span>
                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                  </label>
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Post failed to publish</span>
                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                  </label>
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Weekly analytics report</span>
                    <input type="checkbox" className="w-5 h-5 rounded" />
                  </label>
                </div>
              </div>

              <div>
                <h3 className="font-semibold mb-4" style={{ color: 'var(--gray-900)' }}>Push Notifications</h3>
                <div className="space-y-3">
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Real-time engagement alerts</span>
                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                  </label>
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>AI optimization suggestions</span>
                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                  </label>
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Account connection issues</span>
                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                  </label>
                </div>
              </div>
            </div>

            <div className="border-t pt-6" style={{ borderColor: 'var(--gray-200)' }}>
              <h3 className="font-semibold mb-4" style={{ color: 'var(--gray-900)' }}>Notification Schedule</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="form-label">
                    Quiet Hours Start
                  </label>
                  <input
                    type="time"
                    className="form-input"
                    defaultValue="22:00"
                  />
                </div>
                <div>
                  <label className="form-label">
                    Quiet Hours End
                  </label>
                  <input
                    type="time"
                    className="form-input"
                    defaultValue="08:00"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Privacy Tab */}
        {activeTab === 'privacy' && (
          <div className="card-content space-y-6">
            <div
              className="border rounded-lg p-4"
              style={{
                background: 'rgba(239, 68, 68, 0.05)',
                borderColor: 'rgba(239, 68, 68, 0.2)'
              }}
            >
              <div className="flex items-center gap-2 mb-2">
                <span style={{ color: 'var(--danger-red)' }}>🔒</span>
                <h3 className="font-semibold" style={{ color: 'var(--danger-red)' }}>Data Privacy & Security</h3>
              </div>
              <p className="text-sm" style={{ color: 'var(--danger-red)' }}>
                Your data is encrypted and stored securely. We never share your personal information.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <h3 className="font-semibold mb-3" style={{ color: 'var(--gray-900)' }}>Data Collection</h3>
                <div className="space-y-3">
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Analytics and usage data</span>
                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                  </label>
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Performance monitoring</span>
                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                  </label>
                  <label className="flex items-center justify-between">
                    <span style={{ color: 'var(--gray-700)' }}>Crash reports</span>
                    <input type="checkbox" className="w-5 h-5 rounded" />
                  </label>
                </div>
              </div>

              <div>
                <h3 className="font-semibold mb-3" style={{ color: 'var(--gray-900)' }}>Account Security</h3>
                <div className="space-y-3">
                  <button
                    className="w-full p-4 border-2 rounded-xl transition-colors text-left hover:bg-gray-50"
                    style={{ borderColor: 'var(--gray-200)' }}
                  >
                    <div className="font-semibold" style={{ color: 'var(--gray-900)' }}>Change Password</div>
                    <div className="text-sm" style={{ color: 'var(--gray-600)' }}>Update your account password</div>
                  </button>
                  <button
                    className="w-full p-4 border-2 rounded-xl transition-colors text-left hover:bg-gray-50"
                    style={{ borderColor: 'var(--gray-200)' }}
                  >
                    <div className="font-semibold" style={{ color: 'var(--gray-900)' }}>Two-Factor Authentication</div>
                    <div className="text-sm" style={{ color: 'var(--gray-600)' }}>Add an extra layer of security</div>
                  </button>
                  <button
                    className="w-full p-4 border-2 rounded-xl transition-colors text-left hover:bg-gray-50"
                    style={{ borderColor: 'var(--gray-200)' }}
                  >
                    <div className="font-semibold" style={{ color: 'var(--gray-900)' }}>Active Sessions</div>
                    <div className="text-sm" style={{ color: 'var(--gray-600)' }}>Manage your login sessions</div>
                  </button>
                </div>
              </div>

              <div className="border-t pt-6" style={{ borderColor: 'var(--gray-200)' }}>
                <h3 className="font-semibold mb-3" style={{ color: 'var(--danger-red)' }}>Danger Zone</h3>
                <button
                  className="w-full p-4 border-2 rounded-xl transition-colors text-left"
                  style={{
                    borderColor: 'rgba(239, 68, 68, 0.2)',
                    ':hover': {
                      borderColor: 'var(--danger-red)',
                      background: 'rgba(239, 68, 68, 0.05)'
                    }
                  }}
                >
                  <div className="font-semibold" style={{ color: 'var(--danger-red)' }}>Delete Account</div>
                  <div className="text-sm" style={{ color: 'var(--danger-red)' }}>Permanently delete your account and all data</div>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Settings