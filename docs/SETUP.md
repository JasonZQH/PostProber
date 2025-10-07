# Development Environment Setup Guide

## Prerequisites

### Required Software
```bash
# Node.js (v18.0.0 or higher)
node --version  # Should output v18.x.x or higher
npm --version   # Should output v9.x.x or higher

# Git (for version control)
git --version   # Any recent version

# Optional but recommended
# VS Code with extensions:
# - ES7+ React/Redux/React-Native snippets
# - Prettier - Code formatter
# - ESLint
```

### Installation Steps

#### 1. Install Node.js
```bash
# macOS (using Homebrew)
brew install node

# Windows (using Chocolatey)
choco install nodejs

# Linux (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version && npm --version
```

#### 2. Clone and Setup Project
```bash
# Clone the repository
git clone <repository-url>
cd PostProber

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Initialize database
npm run db:init
```

## Environment Configuration

### Required Environment Variables
Create a `.env` file in the project root:

```bash
# Application
NODE_ENV=development
PORT=3001
FRONTEND_URL=http://localhost:5173

# Database
DATABASE_URL=./data/postprober.db

# JWT Authentication
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRES_IN=24h

# OpenAI API (for AI agent)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Social Media APIs
# Twitter/X API v2
TWITTER_CLIENT_ID=your-twitter-client-id
TWITTER_CLIENT_SECRET=your-twitter-client-secret

# LinkedIn API
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret

# Instagram Basic Display API (if using official API)
INSTAGRAM_CLIENT_ID=your-instagram-client-id
INSTAGRAM_CLIENT_SECRET=your-instagram-client-secret

# Email Notifications (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# Monitoring & Alerts
ALERT_WEBHOOK_URL=https://hooks.slack.com/services/your/slack/webhook
```

### API Key Setup Instructions

#### OpenAI API Key
1. Visit [OpenAI API Platform](https://platform.openai.com)
2. Create account or sign in
3. Navigate to API Keys section
4. Create new secret key
5. Copy key to `OPENAI_API_KEY` in `.env`

#### Twitter/X API Setup
1. Visit [Twitter Developer Portal](https://developer.twitter.com)
2. Create a new project/app
3. Generate API keys and tokens
4. Enable OAuth 2.0 with PKCE
5. Set redirect URI: `http://localhost:3001/auth/twitter/callback`

#### LinkedIn API Setup
1. Visit [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
2. Create new application
3. Add "Sign In with LinkedIn" product
4. Set redirect URI: `http://localhost:3001/auth/linkedin/callback`
5. Note: LinkedIn API has limited post capabilities

## Development Workflow

### Starting the Development Server
```bash
# Start both frontend and backend simultaneously
npm run dev

# Or start individually
npm run dev:backend   # Starts Node.js server on port 3001
npm run dev:frontend  # Starts Vite dev server on port 5173
```

### Available Scripts
```bash
# Development
npm run dev              # Start full development environment
npm run dev:backend      # Backend only (Node.js + Express)
npm run dev:frontend     # Frontend only (React + Vite)

# Database
npm run db:init          # Initialize SQLite database
npm run db:seed          # Seed with sample data
npm run db:reset         # Reset database (caution: deletes all data)

# Testing
npm test                 # Run all tests
npm run test:backend     # Backend tests only
npm run test:frontend    # Frontend tests only
npm run test:watch       # Run tests in watch mode

# Code Quality
npm run lint             # Run ESLint
npm run lint:fix         # Fix ESLint issues automatically
npm run format           # Format code with Prettier
npm run typecheck        # TypeScript type checking

# Production
npm run build            # Build for production
npm start                # Start production server
npm run preview          # Preview production build
```

## Project Structure Setup

```bash
# Create the complete project structure
mkdir -p src/{frontend,backend,shared}
mkdir -p src/frontend/{components,pages,hooks,utils,assets}
mkdir -p src/frontend/components/{auth,composer,monitoring,common}
mkdir -p src/backend/{routes,controllers,services,models,middleware}
mkdir -p src/backend/services/platforms
mkdir -p config data docs tests
mkdir -p tests/{frontend,backend,integration}

# Create essential files
touch src/backend/server.js
touch src/frontend/App.jsx
touch src/frontend/index.html
touch src/shared/types.js
touch config/database.js
touch .env.example
touch .gitignore
```

## Database Setup

### SQLite Initialization
```bash
# Create database directory
mkdir -p data

# Initialize database with schema
npm run db:init

# Verify database creation
ls -la data/
# Should show: postprober.db
```

### Database Management Commands
```bash
# View database schema
sqlite3 data/postprober.db ".schema"

# Connect to database for manual queries
sqlite3 data/postprober.db

# Backup database
cp data/postprober.db data/postprober.backup.db

# Reset database (development only)
rm data/postprober.db && npm run db:init
```

## Development Tools Setup

### VS Code Extensions
Install these recommended extensions:
```json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-json",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense"
  ]
}
```

### VS Code Settings
Create `.vscode/settings.json`:
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "eslint.workingDirectories": ["src"],
  "files.exclude": {
    "node_modules": true,
    "data/*.db": false
  }
}
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 3001
lsof -ti:3001

# Kill process
kill $(lsof -ti:3001)

# Or change port in .env
PORT=3002
```

#### Database Connection Issues
```bash
# Check if database file exists
ls -la data/postprober.db

# Reset database
npm run db:reset

# Check permissions
chmod 644 data/postprober.db
```

#### API Key Issues
```bash
# Verify environment variables are loaded
node -e "console.log(process.env.OPENAI_API_KEY ? 'OpenAI key loaded' : 'OpenAI key missing')"

# Test API connection
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

#### Node.js Version Issues
```bash
# Check current version
node --version

# Install correct version with nvm
nvm install 18
nvm use 18
```

### Performance Optimization

#### Development Mode Optimizations
```bash
# Increase Node.js memory limit for large projects
export NODE_OPTIONS="--max-old-space-size=4096"

# Use faster source maps in development
# Add to vite.config.js:
# build: { sourcemap: 'eval-cheap-module-source-map' }
```

## Next Steps

After completing the setup:

1. **Verify Installation**: Run `npm run dev` and check both frontend (port 5173) and backend (port 3001)
2. **Test Database**: Navigate to `/api/health` to verify database connection
3. **Configure APIs**: Set up at least one social media API for testing
4. **Run Tests**: Execute `npm test` to ensure everything is working
5. **Start Development**: Begin with authentication implementation

## Production Deployment Notes

### Environment Differences
- Use PostgreSQL instead of SQLite
- Set `NODE_ENV=production`
- Use strong JWT secrets
- Enable HTTPS/SSL
- Configure proper CORS origins
- Set up proper logging and monitoring

### Docker Deployment
```dockerfile
# Basic Dockerfile structure
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3001
CMD ["npm", "start"]
```

This setup provides a complete development environment ready for building the PostProber application.