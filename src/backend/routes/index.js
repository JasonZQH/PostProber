import express from 'express'

const router = express.Router()

// Health check
router.get('/health', (req, res) => {
res.json({
  status: 'ok',
  message: 'PostProber API is healthy!',
  timestamp: new Date().toISOString(),
  database: 'connected'
})
})

// Basic info
router.get('/', (req, res) => {
res.json({
  name: 'PostProber API',
  version: '1.0.0',
  description: 'AI Agent powered Social Media Reliability Monitor'
})
})

export default router