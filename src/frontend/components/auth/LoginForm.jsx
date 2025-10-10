import React, { useState } from 'react'

function LoginForm({ onLogin, onSwitchToRegister, isLoading }) {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [errors, setErrors] = useState({})

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrors({})

    // Basic validation
    const newErrors = {}
    if (!formData.email) newErrors.email = 'Email is required'
    if (!formData.password) newErrors.password = 'Password is required'

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    await onLogin(formData)
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    // Clear error when user starts typing
    if (errors[e.target.name]) {
      setErrors({
        ...errors,
        [e.target.name]: ''
      })
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50">
      {/* Background Animation */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 w-full max-w-md">
        {/* Logo Section */}
        <div className="text-center mb-8 slide-in-up">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl gradient-animated float"></div>
          <h1 className="text-4xl font-bold gradient-text mb-2">PostProber</h1>
          <p className="text-gray-600">Welcome back to your social media command center!</p>
          <div className="mt-2">
            <span className="sparkle">✨</span>
          </div>
        </div>

        {/* Login Form */}
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
                placeholder="Enter your password"
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600 slide-in-right">{errors.password}</p>
              )}
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input type="checkbox" className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500" />
                <span className="ml-2 text-sm text-gray-600">Remember me</span>
              </label>
              <button type="button" className="text-sm text-purple-600 hover:text-purple-500">
                Forgot password?
              </button>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full btn btn-primary text-lg py-4 hover-scale"
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="spinner"></div>
                  <span>Logging in<span className="typing-indicator"></span></span>
                </div>
              ) : (
                <div className="flex items-center justify-center space-x-2">
                  <span>Log In</span>
                  <span>🚀</span>
                </div>
              )}
            </button>

            <div className="text-center">
              <span className="text-gray-600">Don't have an account? </span>
              <button
                type="button"
                onClick={onSwitchToRegister}
                className="text-purple-600 hover:text-purple-500 font-semibold"
              >
                Sign up for free
              </button>
            </div>
          </form>
        </div>

        {/* Social Login (Future Enhancement) */}
        <div className="mt-6 text-center slide-in-up">
          <p className="text-sm text-gray-500 mb-4">Or continue with</p>
          <div className="flex justify-center space-x-4">
            <button className="p-3 border-2 border-gray-200 rounded-xl hover:border-purple-300 hover:bg-purple-50 transition-all hover-scale">
              <span className="text-xl">🐦</span>
            </button>
            <button className="p-3 border-2 border-gray-200 rounded-xl hover:border-purple-300 hover:bg-purple-50 transition-all hover-scale">
              <span className="text-xl">💼</span>
            </button>
            <button className="p-3 border-2 border-gray-200 rounded-xl hover:border-purple-300 hover:bg-purple-50 transition-all hover-scale">
              <span className="text-xl">📷</span>
            </button>
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

export default LoginForm