import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import { initializeDatabase } from '../../config/database.js'

// Import routes
import apiRoutes from './routes/index.js'
import authRoutes from './routes/auth.js'
import postRoutes from './routes/posts.js'

dotenv.config()

// Initialize database
initializeDatabase()

const app = express()
const PORT = process.env.PORT || 3001

// Middleware
app.use(cors())
app.use(express.json())

// Use routes
app.use('/api', apiRoutes)
app.use('/api/auth', authRoutes)
app.use('/api/posts', postRoutes)

app.listen(PORT, () => {
console.log(`🚀 PostProber backend running on http://localhost:${PORT}`)
console.log(`📊 Health check: http://localhost:${PORT}/api/health`)
})