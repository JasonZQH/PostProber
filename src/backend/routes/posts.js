import express from 'express'

const router = express.Router()

// Get all posts
router.get('/', (req, res) => {
res.json({
  message: 'Posts list endpoint - coming soon!',
  posts: []
})
})

// Create new post
router.post('/', (req, res) => {
res.json({ message: 'Create post endpoint - coming soon!' })
})

// Get specific post
router.get('/:id', (req, res) => {
res.json({
  message: `Get post ${req.params.id} endpoint - coming soon!`,
  postId: req.params.id
})
})

export default router