import express from 'express'

const router = express.Router()

// Placeholder auth routes
router.post('/login', (req, res) => {
res.json({ message: 'Login endpoint - coming soon!' })
})

router.post('/logout', (req, res) => {
res.json({ message: 'Logout endpoint - coming soon!' })
})

router.get('/me', (req, res) => {
res.json({ message: 'User profile endpoint - coming soon!' })
})

export default router