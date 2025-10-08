 import sqlite3 from 'sqlite3'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const dbPath = join(__dirname, '..', 'data', 'postprober.db')

export const db = new sqlite3.Database(dbPath, (err) => {
if (err) {
  console.error('Error opening database:', err)
} else {
  console.log('Connected to SQLite database')
}
})

// Initialize database schema
export const initializeDatabase = () => {
const tables = [
  `CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`,

  `CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    platform VARCHAR(50) NOT NULL,
    account_name VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at DATETIME,
    is_active BOOLEAN DEFAULT true,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`,

  `CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    platforms TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    ai_suggestions TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    posted_at DATETIME
  )`,

  `CREATE TABLE IF NOT EXISTS monitoring_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER REFERENCES posts(id),
    platform VARCHAR(50),
    step VARCHAR(100),
    status VARCHAR(50),
    details TEXT,
    ai_analysis TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
  )`
]

tables.forEach(sql => {
  db.run(sql, (err) => {
    if (err) console.error('Error creating table:', err)
  })
})
}