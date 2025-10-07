# Project Structure & Organization

## Directory Layout

```
PostProber/
├── README.md                    # Project overview and quick start
├── package.json                 # Dependencies and scripts
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
├── vite.config.js              # Vite configuration
├── jest.config.js              # Testing configuration
├── docker-compose.yml          # Docker development setup
├── Dockerfile                  # Production container
│
├── src/                        # Source code
│   ├── frontend/               # React application
│   │   ├── index.html             # HTML entry point
│   │   ├── main.jsx               # React entry point
│   │   ├── App.jsx                # Main App component
│   │   ├── components/            # Reusable UI components
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.jsx        # User login interface
│   │   │   │   ├── AccountManager.jsx   # Social media account linking
│   │   │   │   └── ProtectedRoute.jsx   # Route protection
│   │   │   ├── composer/
│   │   │   │   ├── PostComposer.jsx     # Post creation interface
│   │   │   │   ├── PlatformSelector.jsx # Platform selection
│   │   │   │   ├── ContentOptimizer.jsx # AI-powered optimization
│   │   │   │   └── PreviewPanel.jsx     # Post preview
│   │   │   ├── monitoring/
│   │   │   │   ├── Dashboard.jsx        # Main monitoring view
│   │   │   │   ├── StepProgress.jsx     # Step-by-step progress
│   │   │   │   ├── AlertPanel.jsx       # Notifications panel
│   │   │   │   ├── MetricsChart.jsx     # Performance charts
│   │   │   │   └── LogViewer.jsx        # Detailed logs
│   │   │   └── common/
│   │   │       ├── Header.jsx           # Application header
│   │   │       ├── Sidebar.jsx          # Navigation sidebar
│   │   │       ├── LoadingSpinner.jsx   # Loading indicator
│   │   │       ├── ErrorBoundary.jsx    # Error handling
│   │   │       └── Toast.jsx            # Toast notifications
│   │   ├── pages/
│   │   │   ├── Home.jsx               # Landing page
│   │   │   ├── Login.jsx              # Login page
│   │   │   ├── Dashboard.jsx          # Main dashboard
│   │   │   ├── Compose.jsx            # Post composition page
│   │   │   ├── Monitor.jsx            # Monitoring page
│   │   │   ├── Settings.jsx           # User settings
│   │   │   └── NotFound.jsx           # 404 page
│   │   ├── hooks/
│   │   │   ├── useAuth.js             # Authentication state
│   │   │   ├── useRealTime.js         # WebSocket connection
│   │   │   ├── useMonitoring.js       # Monitoring data
│   │   │   ├── useLocalStorage.js     # Local storage helper
│   │   │   └── useApi.js              # API request helper
│   │   ├── utils/
│   │   │   ├── api.js                 # API client configuration
│   │   │   ├── constants.js           # Application constants
│   │   │   ├── helpers.js             # Utility functions
│   │   │   ├── validation.js          # Form validation
│   │   │   └── formatting.js          # Data formatting
│   │   ├── styles/
│   │   │   ├── globals.css            # Global styles
│   │   │   ├── components.css         # Component styles
│   │   │   └── utilities.css          # Utility classes
│   │   └── assets/
│   │       ├── images/                # Static images
│   │       ├── icons/                 # Icon files
│   │       └── fonts/                 # Custom fonts
│   │
│   ├── backend/                    # Node.js server
│   │   ├── server.js                  # Express server entry
│   │   ├── routes/
│   │   │   ├── index.js               # Route aggregation
│   │   │   ├── auth.js                # Authentication routes
│   │   │   ├── posts.js               # Post management
│   │   │   ├── accounts.js            # Account management
│   │   │   ├── monitoring.js          # Monitoring endpoints
│   │   │   └── health.js              # Health check
│   │   ├── controllers/
│   │   │   ├── AuthController.js      # Authentication logic
│   │   │   ├── PostController.js      # Post operations
│   │   │   ├── AccountController.js   # Account management
│   │   │   └── MonitorController.js   # Monitoring logic
│   │   ├── services/
│   │   │   ├── platforms/
│   │   │   │   ├── TwitterService.js    # Twitter API integration
│   │   │   │   ├── LinkedInService.js   # LinkedIn API
│   │   │   │   ├── InstagramService.js  # Instagram automation
│   │   │   │   └── PlatformFactory.js   # Platform abstraction
│   │   │   ├── AIAgentService.js        # OpenAI integration
│   │   │   ├── MonitoringService.js     # Monitoring orchestration
│   │   │   ├── NotificationService.js   # Alert system
│   │   │   ├── QueueService.js          # Job queue management
│   │   │   └── EncryptionService.js     # Data encryption
│   │   ├── models/
│   │   │   ├── index.js               # Model exports
│   │   │   ├── User.js                # User model
│   │   │   ├── Account.js             # Social media accounts
│   │   │   ├── Post.js                # Post records
│   │   │   ├── MonitoringLog.js       # Monitoring logs
│   │   │   └── Alert.js               # Alert records
│   │   ├── middleware/
│   │   │   ├── auth.js                # JWT authentication
│   │   │   ├── validation.js          # Request validation
│   │   │   ├── logging.js             # Request logging
│   │   │   ├── rateLimiting.js        # Rate limiting
│   │   │   └── errorHandler.js        # Error handling
│   │   └── utils/
│   │       ├── database.js            # Database connection
│   │       ├── logger.js              # Logging configuration
│   │       ├── config.js              # Configuration loader
│   │       └── helpers.js             # Utility functions
│   │
│   └── shared/                     # Shared code
│       ├── types.js                   # TypeScript types/JSDoc
│       ├── constants.js               # Shared constants
│       ├── validators.js              # Shared validation
│       └── utils.js                   # Shared utilities
│
├── config/                         # Configuration files
│   ├── database.js                    # Database configuration
│   ├── social-platforms.js           # Platform configurations
│   ├── ai-prompts.js                 # AI prompt templates
│   └── environments/                 # Environment-specific configs
│       ├── development.js
│       ├── production.js
│       └── test.js
│
├── data/                          # Data storage
│   ├── postprober.db                 # SQLite database
│   ├── logs/                         # Application logs
│   └── uploads/                      # File uploads
│
├── docs/                          # Documentation
│   ├── API.md                        # API documentation
│   ├── ARCHITECTURE.md               # System architecture
│   ├── SETUP.md                      # Setup guide
│   ├── TECH_STACK.md                 # Technology decisions
│   ├── DEPLOYMENT.md                 # Deployment guide
│   └── CONTRIBUTING.md               # Contribution guidelines
│
├── tests/                         # Test files
│   ├── frontend/                     # Frontend tests
│   │   ├── components/               # Component tests
│   │   ├── pages/                    # Page tests
│   │   ├── hooks/                    # Hook tests
│   │   └── utils/                    # Utility tests
│   ├── backend/                      # Backend tests
│   │   ├── routes/                   # Route tests
│   │   ├── controllers/              # Controller tests
│   │   ├── services/                 # Service tests
│   │   └── models/                   # Model tests
│   ├── integration/                  # Integration tests
│   │   ├── api.test.js               # API integration
│   │   ├── auth.test.js              # Authentication flow
│   │   └── monitoring.test.js        # Monitoring flow
│   ├── fixtures/                     # Test data
│   │   ├── users.json                # Sample users
│   │   ├── posts.json                # Sample posts
│   │   └── responses.json            # Mock API responses
│   └── helpers/                      # Test utilities
│       ├── setup.js                  # Test setup
│       ├── mocks.js                  # Mock functions
│       └── factories.js              # Test data factories
│
├── docker/                        # Docker configurations
│   ├── development.yml               # Development compose
│   ├── production.yml                # Production compose
│   ├── nginx.conf                    # Nginx configuration
│   └── scripts/                      # Docker scripts
│       ├── init-db.sh               # Database initialization
│       └── health-check.sh          # Health check script
│
└── scripts/                       # Build and utility scripts
    ├── build.sh                      # Production build
    ├── deploy.sh                     # Deployment script
    ├── db-migrate.js                 # Database migrations
    ├── seed-data.js                  # Seed sample data
    └── cleanup.sh                    # Cleanup script
```

## File Naming Conventions

### Frontend Components
```javascript
// PascalCase for React components
LoginForm.jsx
PostComposer.jsx
AlertPanel.jsx

// camelCase for utilities and hooks
useAuth.js
apiClient.js
validationHelpers.js

// kebab-case for CSS files
login-form.css
post-composer.css
```

### Backend Files
```javascript
// PascalCase for classes and models
UserController.js
PostService.js
TwitterService.js

// camelCase for utilities and configs
database.js
authMiddleware.js
rateLimiting.js

// kebab-case for route files
auth-routes.js
post-routes.js
```

## Import/Export Patterns

### Frontend Module Structure
```javascript
// Component exports
export default LoginForm;
export { LoginForm, LoginFormValidator };

// Hook exports
export const useAuth = () => { /* ... */ };
export const useRealTime = () => { /* ... */ };

// Utility exports
export const formatDate = (date) => { /* ... */ };
export const validateEmail = (email) => { /* ... */ };

// Centralized exports
// src/frontend/components/index.js
export { default as LoginForm } from './auth/LoginForm';
export { default as PostComposer } from './composer/PostComposer';
export { default as Dashboard } from './monitoring/Dashboard';
```

### Backend Module Structure
```javascript
// Controller exports
class AuthController {
  static async login(req, res) { /* ... */ }
  static async logout(req, res) { /* ... */ }
}
module.exports = AuthController;

// Service exports
class TwitterService {
  constructor(credentials) { /* ... */ }
  async postTweet(content) { /* ... */ }
}
module.exports = TwitterService;

// Middleware exports
const authMiddleware = (req, res, next) => { /* ... */ };
module.exports = authMiddleware;
```

## Code Organization Principles

### Component Responsibility
```javascript
// ✅ Single Responsibility
const PostComposer = () => {
  // Only handles post composition logic
};

// ✅ Separation of Concerns
const usePostComposer = () => {
  // Only handles post state management
};

// ✅ Presentation vs Logic
const PostComposerUI = ({ onSubmit, content }) => {
  // Only handles UI rendering
};
```

### Service Layer Pattern
```javascript
// ✅ Abstract platform differences
class SocialMediaService {
  static getService(platform) {
    switch (platform) {
      case 'twitter': return new TwitterService();
      case 'linkedin': return new LinkedInService();
      case 'instagram': return new InstagramService();
    }
  }
}

// ✅ Consistent interface
class TwitterService {
  async authenticate(credentials) { /* ... */ }
  async createPost(content) { /* ... */ }
  async getPostStatus(postId) { /* ... */ }
}
```

### Configuration Management
```javascript
// config/environments/development.js
module.exports = {
  database: {
    type: 'sqlite',
    path: './data/postprober.db'
  },
  ai: {
    provider: 'openai',
    model: 'gpt-3.5-turbo'
  },
  platforms: {
    twitter: {
      apiVersion: 'v2',
      rateLimit: 300
    }
  }
};
```

## Dependency Management

### Frontend Dependencies
```json
{
  "dependencies": {
    "react": "^18.2.0",           // UI framework
    "react-router-dom": "^6.8.0", // Routing
    "axios": "^1.3.0",            // HTTP client
    "socket.io-client": "^4.6.0", // WebSocket client
    "recharts": "^2.5.0"          // Charts
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0", // Vite React plugin
    "eslint": "^8.36.0",              // Linting
    "prettier": "^2.8.0"              // Code formatting
  }
}
```

### Backend Dependencies
```json
{
  "dependencies": {
    "express": "^4.18.0",      // Web framework
    "jsonwebtoken": "^9.0.0",  // Authentication
    "bcryptjs": "^2.4.0",      // Password hashing
    "sqlite3": "^5.1.0",       // Database
    "socket.io": "^4.6.0",     // WebSocket server
    "winston": "^3.8.0",       // Logging
    "openai": "^3.2.0",        // AI integration
    "puppeteer": "^19.7.0"     // Browser automation
  },
  "devDependencies": {
    "nodemon": "^2.0.0",       // Development server
    "jest": "^29.4.0",         // Testing framework
    "supertest": "^6.3.0"      // API testing
  }
}
```

This structure provides clear separation of concerns, maintainable code organization, and scalable architecture patterns while keeping the project approachable for development and demonstration purposes.