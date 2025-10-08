export default {
    testEnvironment: 'node',
    transform: {},
    extensionsToTreatAsEsm: ['.js'],
    testMatch: ['**/tests/**/*.test.js'],
    collectCoverageFrom: [
      'src/**/*.js',
      '!src/frontend/main.jsx'
    ]
  }