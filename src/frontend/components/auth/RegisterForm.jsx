import React, { useState } from 'react'

function RegisterForm({ onRegister, onSwitchToLogin, isLoading }) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [errors, setErrors] = useState({})

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrors({})

    // Validation
    const newErrors = {}
    if (!formData.email) newErrors.email = 'Email is required'
    if (!formData.password) newErrors.password = 'Password is required'
    if (formData.password.length < 6) newErrors.password = 'Password must be at least 6 characters'
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    await onRegister({
      email: formData.email,
      password: formData.password
    })
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    if (errors[e.target.name]) {
      setErrors({
        ...errors,
        [e.target.name]: ''
      })
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Background Animation */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 w-full max-w-md">
        {/* Logo Section */}
        <div className="text-center mb-8 slide-in-up">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl gradient-animated float"></div>
          <h1 className="text-4xl font-bold gradient-text mb-2">Join PostProber</h1>
          <p className="text-gray-600">Start your social media success journey!</p>
          <div className="mt-2">
            <span className="sparkle">🌟</span>
          </div>
        </div>

        {/* Register Form */}
        <div className="card hover-lift slide-in-up">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all ${
                  errors.email
                    ? 'border-red-300 bg-red-50'
                    : 'border-gray-200 focus:border-purple-300'
                }`}
                placeholder="your@email.com"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600 slide-in-right">{errors.email}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all ${
                  errors.password
                    ? 'border-red-300 bg-red-50'
                    : 'border-gray-200 focus:border-purple-300'
                }`}
                placeholder="Create a strong password"
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600 slide-in-right">{errors.password}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Confirm Password
              </label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all ${
                  errors.confirmPassword
                    ? 'border-red-300 bg-red-50'
                    : 'border-gray-200 focus:border-purple-300'
                }`}
                placeholder="Confirm your password"
              />
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600 slide-in-right">{errors.confirmPassword}</p>
              )}
            </div>

            <div className="flex items-start space-x-2">
              <input
                type="checkbox"
                id="terms"
                className="w-4 h-4 mt-1 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                required
              />
              <label htmlFor="terms" className="text-sm text-gray-600">
                I agree to the{' '}
                <button type="button" className="text-purple-600 hover:text-purple-500">
                  Terms of Service
                </button>{' '}
                and{' '}
                <button type="button" className="text-purple-600 hover:text-purple-500">
                  Privacy Policy
                </button>
              </label>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full btn btn-primary text-lg py-4 hover-scale"
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="spinner"></div>
                  <span>Creating account<span className="typing-indicator"></span></span>
                </div>
              ) : (
                <div className="flex items-center justify-center space-x-2">
                  <span>Create Account</span>
                  <span>✨</span>
                </div>
              )}
            </button>

            <div className="text-center">
              <span className="text-gray-600">Already have an account? </span>
              <button
                type="button"
                onClick={onSwitchToLogin}
                className="text-purple-600 hover:text-purple-500 font-semibold"
              >
                Sign in
              </button>
            </div>
          </form>
        </div>

        {/* Features Preview */}
        <div className="mt-6 slide-in-up">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="p-3 bg-white rounded-xl border border-gray-100 hover-lift">
              <div className="text-2xl mb-1">🤖</div>
              <div className="text-xs text-gray-600">AI Powered</div>
            </div>
            <div className="p-3 bg-white rounded-xl border border-gray-100 hover-lift">
              <div className="text-2xl mb-1">📊</div>
              <div className="text-xs text-gray-600">Analytics</div>
            </div>
            <div className="p-3 bg-white rounded-xl border border-gray-100 hover-lift">
              <div className="text-2xl mb-1">🚀</div>
              <div className="text-xs text-gray-600">Multi-Platform</div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes blob {
          0%, 100% { transform: translate(0px, 0px) scale(1); }
          33% { transform: translate(30px, -50px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        .animate-blob {
          animation: blob 7s infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  )
}

export default RegisterForm