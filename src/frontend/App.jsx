import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/common/Layout'
import Dashboard from './pages/Dashboard'
import Compose from './pages/Compose'
import Schedule from './pages/Schedule'
import Analytics from './pages/Analytics'
import Health from './pages/Health'
import Accounts from './pages/Accounts'
import Settings from './pages/Settings'
import PlatformConnectionModal from './components/platforms/PlatformConnectionModal'
import platformService from './services/platformService'

function App() {
  const [showConnectionModal, setShowConnectionModal] = useState(false)
  const [isCheckingFirstTime, setIsCheckingFirstTime] = useState(true)

  useEffect(() => {
    // Check if this is first time user
    const checkFirstTime = () => {
      const isFirstTime = platformService.isFirstTimeUser() && !platformService.isOnboardingComplete()
      setShowConnectionModal(isFirstTime)
      setIsCheckingFirstTime(false)
    }

    checkFirstTime()
  }, [])

  const handleModalComplete = () => {
    setShowConnectionModal(false)
  }

  if (isCheckingFirstTime) {
    // Show loading state while checking
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p style={{ color: 'var(--gray-600)' }}>Loading PostProber...</p>
        </div>
      </div>
    )
  }

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/compose" element={<Compose />} />
          <Route path="/schedule" element={<Schedule />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/health" element={<Health />} />
          <Route path="/accounts" element={<Accounts />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Layout>

      {/* Platform Connection Modal */}
      <PlatformConnectionModal
        isOpen={showConnectionModal}
        onClose={() => setShowConnectionModal(false)}
        onComplete={handleModalComplete}
      />
    </Router>
  )
}

export default App