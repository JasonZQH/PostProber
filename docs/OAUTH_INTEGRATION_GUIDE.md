# OAuth Integration Guide for PostProber

This document provides a comprehensive guide on implementing OAuth 2.0 authentication for connecting to social media platforms (X/Twitter, Instagram, LinkedIn, Facebook).

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [X (Twitter) Integration](#x-twitter-integration)
4. [Instagram Integration](#instagram-integration)
5. [LinkedIn Integration](#linkedin-integration)
6. [Facebook Integration](#facebook-integration)
7. [Implementation Architecture](#implementation-architecture)
8. [Security Best Practices](#security-best-practices)
9. [Token Management](#token-management)

---

## Overview

### What is OAuth 2.0?

OAuth 2.0 is an industry-standard authorization protocol that allows applications to obtain limited access to user accounts on HTTP services. It works by delegating user authentication to the service that hosts the user account and authorizing third-party applications to access that account.

### Why OAuth?

- **Secure**: Users never share their passwords with your application
- **Granular Permissions**: Request only the access you need (scopes)
- **Token-based**: Access tokens can be revoked without changing passwords
- **Industry Standard**: Widely adopted and well-documented

---

## Prerequisites

### General Requirements

1. **Developer Accounts**: Create developer accounts on each platform:
   - X: https://developer.x.com
   - Meta (Instagram/Facebook): https://developers.facebook.com
   - LinkedIn: https://developer.linkedin.com

2. **SSL/HTTPS**: Your application must use HTTPS for OAuth callbacks
   - For local development, use tools like `ngrok` or `localhost.run`
   - For production, ensure valid SSL certificates

3. **Redirect URIs**: Register your application's callback URLs with each platform

4. **Environment Variables**: Store credentials securely
   ```bash
   # .env file
   # X/Twitter
   X_CLIENT_ID=your_client_id
   X_CLIENT_SECRET=your_client_secret
   X_CALLBACK_URL=https://yourdomain.com/api/auth/x/callback

   # Instagram/Facebook
   FB_APP_ID=your_app_id
   FB_APP_SECRET=your_app_secret
   FB_CALLBACK_URL=https://yourdomain.com/api/auth/instagram/callback

   # LinkedIn
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   LINKEDIN_CALLBACK_URL=https://yourdomain.com/api/auth/linkedin/callback
   ```

---

## X (Twitter) Integration

### Authentication Method

X uses **OAuth 2.0 Authorization Code Flow with PKCE** (Proof Key for Code Exchange).

### Step 1: Register Your Application

1. Go to https://developer.x.com
2. Create a new project and app
3. Navigate to "User authentication settings"
4. Set App permissions (read, write, direct messages)
5. Add callback URL: `https://yourdomain.com/api/auth/x/callback`
6. Note your **Client ID** and **Client Secret**

### Step 2: Required Scopes

Common scopes for PostProber:
- `tweet.read` - Read tweets
- `tweet.write` - Create and delete tweets
- `users.read` - Read user profile information
- `offline.access` - Get refresh tokens (token stays valid beyond 2 hours)

### Step 3: Implementation Flow

#### 3.1 Generate Code Verifier and Challenge (PKCE)

```javascript
// Generate code verifier (random string)
function generateCodeVerifier() {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64URLEncode(array);
}

// Generate code challenge from verifier
async function generateCodeChallenge(verifier) {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return base64URLEncode(new Uint8Array(digest));
}
```

#### 3.2 Authorization URL

```javascript
const authorizationUrl = new URL('https://twitter.com/i/oauth2/authorize');
authorizationUrl.searchParams.append('response_type', 'code');
authorizationUrl.searchParams.append('client_id', process.env.X_CLIENT_ID);
authorizationUrl.searchParams.append('redirect_uri', process.env.X_CALLBACK_URL);
authorizationUrl.searchParams.append('scope', 'tweet.read tweet.write users.read offline.access');
authorizationUrl.searchParams.append('state', generateRandomState()); // CSRF protection
authorizationUrl.searchParams.append('code_challenge', codeChallenge);
authorizationUrl.searchParams.append('code_challenge_method', 'S256');

// Redirect user to authorizationUrl
```

#### 3.3 Exchange Authorization Code for Access Token

```javascript
// After user authorizes, X redirects to your callback with code
const tokenResponse = await fetch('https://api.twitter.com/2/oauth2/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authorizationCode,
    redirect_uri: process.env.X_CALLBACK_URL,
    client_id: process.env.X_CLIENT_ID,
    code_verifier: codeVerifier, // From step 3.1
  }),
});

const tokens = await tokenResponse.json();
// tokens.access_token - Use for API calls
// tokens.refresh_token - Use to get new access token (if offline.access scope)
// tokens.expires_in - Token lifetime in seconds (7200 = 2 hours)
```

#### 3.4 Making API Calls

```javascript
// Post a tweet
const response = await fetch('https://api.twitter.com/2/tweets', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'Hello from PostProber!'
  }),
});
```

#### 3.5 Refresh Access Token

```javascript
const refreshResponse = await fetch('https://api.twitter.com/2/oauth2/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: storedRefreshToken,
    client_id: process.env.X_CLIENT_ID,
  }),
});
```

### Key Points

- Access tokens expire in **2 hours** by default
- Use `offline.access` scope to get refresh tokens
- PKCE is **required** for security
- Only works with **X API v2** endpoints
- Rate limit: 900 requests per 15 minutes with OAuth 2.0

---

## Instagram Integration

### Authentication Method

Instagram uses **Facebook Login** and the **Instagram Graph API** (OAuth 2.0 Authorization Code Flow).

### Step 1: Register Your Application

1. Go to https://developers.facebook.com
2. Create a new app (Business or Consumer type)
3. Add **Instagram Basic Display** or **Instagram Graph API** product
4. Configure OAuth Redirect URIs
5. Note your **App ID** and **App Secret**

### Step 2: Required Permissions

For Instagram Graph API (business accounts):
- `instagram_basic` - Read profile info
- `instagram_content_publish` - Publish posts
- `pages_show_list` - List Facebook Pages
- `pages_read_engagement` - Read Page engagement

For Instagram Basic Display (personal accounts):
- `user_profile` - Read profile
- `user_media` - Read media

### Step 3: Implementation Flow

#### 3.1 Authorization URL

```javascript
const authorizationUrl = new URL('https://www.facebook.com/v18.0/dialog/oauth');
authorizationUrl.searchParams.append('client_id', process.env.FB_APP_ID);
authorizationUrl.searchParams.append('redirect_uri', process.env.FB_CALLBACK_URL);
authorizationUrl.searchParams.append('scope', 'instagram_basic,instagram_content_publish,pages_show_list');
authorizationUrl.searchParams.append('state', generateRandomState());

// Redirect user to authorizationUrl
```

#### 3.2 Exchange Code for Access Token

```javascript
const tokenResponse = await fetch('https://graph.facebook.com/v18.0/oauth/access_token', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  },
  params: {
    client_id: process.env.FB_APP_ID,
    client_secret: process.env.FB_APP_SECRET,
    redirect_uri: process.env.FB_CALLBACK_URL,
    code: authorizationCode,
  },
});

const tokens = await tokenResponse.json();
// tokens.access_token - Short-lived token (1-2 hours)
```

#### 3.3 Exchange for Long-Lived Token

```javascript
// Convert short-lived token to long-lived (60 days)
const longLivedResponse = await fetch('https://graph.facebook.com/v18.0/oauth/access_token', {
  method: 'GET',
  params: {
    grant_type: 'fb_exchange_token',
    client_id: process.env.FB_APP_ID,
    client_secret: process.env.FB_APP_SECRET,
    fb_exchange_token: shortLivedToken,
  },
});
```

#### 3.4 Get Instagram Business Account ID

```javascript
// First, get user's Facebook Pages
const pagesResponse = await fetch(`https://graph.facebook.com/v18.0/me/accounts?access_token=${accessToken}`);
const pages = await pagesResponse.json();

// Then get Instagram Business Account ID from Page
const pageId = pages.data[0].id;
const igAccountResponse = await fetch(
  `https://graph.facebook.com/v18.0/${pageId}?fields=instagram_business_account&access_token=${accessToken}`
);
const igAccount = await igAccountResponse.json();
const instagramAccountId = igAccount.instagram_business_account.id;
```

#### 3.5 Post to Instagram

```javascript
// Step 1: Create media container
const containerResponse = await fetch(
  `https://graph.facebook.com/v18.0/${instagramAccountId}/media`,
  {
    method: 'POST',
    body: JSON.stringify({
      image_url: 'https://example.com/image.jpg',
      caption: 'Hello from PostProber!',
      access_token: accessToken,
    }),
  }
);
const container = await containerResponse.json();

// Step 2: Publish the container
const publishResponse = await fetch(
  `https://graph.facebook.com/v18.0/${instagramAccountId}/media_publish`,
  {
    method: 'POST',
    body: JSON.stringify({
      creation_id: container.id,
      access_token: accessToken,
    }),
  }
);
```

### Key Points

- Instagram requires a **Facebook Page** connected to an **Instagram Business Account**
- Instagram Personal accounts use **Basic Display API** (limited features)
- Short-lived tokens: 1-2 hours
- Long-lived tokens: 60 days
- Must refresh tokens before expiration

---

## LinkedIn Integration

### Authentication Method

LinkedIn uses **OAuth 2.0 Authorization Code Flow** (3-legged OAuth).

### Step 1: Register Your Application

1. Go to https://developer.linkedin.com
2. Create a new app
3. Add products: "Share on LinkedIn" and "Sign In with LinkedIn using OpenID Connect"
4. Add OAuth 2.0 redirect URLs
5. Note your **Client ID** and **Client Secret**

### Step 2: Required Scopes

Common scopes:
- `openid` - OpenID Connect authentication
- `profile` - Read basic profile
- `email` - Read email address
- `w_member_social` - Post, comment, and like on behalf of user

### Step 3: Implementation Flow

#### 3.1 Authorization URL

```javascript
const authorizationUrl = new URL('https://www.linkedin.com/oauth/v2/authorization');
authorizationUrl.searchParams.append('response_type', 'code');
authorizationUrl.searchParams.append('client_id', process.env.LINKEDIN_CLIENT_ID);
authorizationUrl.searchParams.append('redirect_uri', process.env.LINKEDIN_CALLBACK_URL);
authorizationUrl.searchParams.append('scope', 'openid profile email w_member_social');
authorizationUrl.searchParams.append('state', generateRandomState());

// Redirect user to authorizationUrl
```

#### 3.2 Exchange Code for Access Token

```javascript
const tokenResponse = await fetch('https://www.linkedin.com/oauth/v2/accessToken', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authorizationCode,
    client_id: process.env.LINKEDIN_CLIENT_ID,
    client_secret: process.env.LINKEDIN_CLIENT_SECRET,
    redirect_uri: process.env.LINKEDIN_CALLBACK_URL,
  }),
});

const tokens = await tokenResponse.json();
// tokens.access_token - Use for API calls
// tokens.expires_in - Token lifetime (60 days)
```

#### 3.3 Get User Profile

```javascript
const profileResponse = await fetch('https://api.linkedin.com/v2/userinfo', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
  },
});
const profile = await profileResponse.json();
```

#### 3.4 Post to LinkedIn

```javascript
// Get user's LinkedIn ID (sub field from userinfo)
const userId = profile.sub;

// Create a post
const postResponse = await fetch('https://api.linkedin.com/v2/ugcPosts', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0',
  },
  body: JSON.stringify({
    author: `urn:li:person:${userId}`,
    lifecycleState: 'PUBLISHED',
    specificContent: {
      'com.linkedin.ugc.ShareContent': {
        shareCommentary: {
          text: 'Hello from PostProber!',
        },
        shareMediaCategory: 'NONE',
      },
    },
    visibility: {
      'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC',
    },
  }),
});
```

### Key Points

- Authorization code expires in **30 minutes** (use immediately)
- Access tokens valid for **60 days**
- Most permissions require **LinkedIn approval**
- Must request specific products in developer portal

---

## Facebook Integration

### Authentication Method

Facebook uses **OAuth 2.0 Authorization Code Flow** (similar to Instagram).

### Step 1: Register Your Application

1. Go to https://developers.facebook.com
2. Create a new app
3. Add **Facebook Login** product
4. Configure OAuth Redirect URIs
5. Note your **App ID** and **App Secret**

### Step 2: Required Permissions

Common permissions:
- `public_profile` - Read basic profile
- `email` - Read email address
- `pages_manage_posts` - Create, edit, and delete posts on Pages
- `pages_read_engagement` - Read engagement data

### Step 3: Implementation Flow

#### 3.1 Authorization URL

```javascript
const authorizationUrl = new URL('https://www.facebook.com/v18.0/dialog/oauth');
authorizationUrl.searchParams.append('client_id', process.env.FB_APP_ID);
authorizationUrl.searchParams.append('redirect_uri', process.env.FB_CALLBACK_URL);
authorizationUrl.searchParams.append('scope', 'public_profile,email,pages_manage_posts');
authorizationUrl.searchParams.append('state', generateRandomState());

// Redirect user to authorizationUrl
```

#### 3.2 Exchange Code for Access Token

Same as Instagram (see Instagram section 3.2 and 3.3).

#### 3.3 Post to Facebook Page

```javascript
// Get user's pages
const pagesResponse = await fetch(
  `https://graph.facebook.com/v18.0/me/accounts?access_token=${accessToken}`
);
const pages = await pagesResponse.json();
const pageAccessToken = pages.data[0].access_token;
const pageId = pages.data[0].id;

// Post to page
const postResponse = await fetch(`https://graph.facebook.com/v18.0/${pageId}/feed`, {
  method: 'POST',
  body: JSON.stringify({
    message: 'Hello from PostProber!',
    access_token: pageAccessToken, // Use page token, not user token
  }),
});
```

### Key Points

- Page access tokens are different from user access tokens
- Page tokens can be long-lived or permanent
- User must have page management permissions

---

## Implementation Architecture

### Backend Structure

```
src/backend/
├── auth/
│   ├── __init__.py
│   ├── oauth_handlers.py      # OAuth flow handlers
│   ├── twitter_oauth.py       # X/Twitter specific
│   ├── instagram_oauth.py     # Instagram specific
│   ├── linkedin_oauth.py      # LinkedIn specific
│   └── facebook_oauth.py      # Facebook specific
├── api/
│   └── endpoints/
│       └── auth.py            # Auth endpoints
└── database/
    └── models/
        └── user_tokens.py     # Token storage model
```

### Database Schema

```sql
CREATE TABLE user_platform_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    platform VARCHAR(50) NOT NULL,  -- 'twitter', 'instagram', 'linkedin', 'facebook'
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    token_type VARCHAR(50),
    expires_at TIMESTAMP,
    scope TEXT,
    platform_user_id VARCHAR(255),
    platform_username VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, platform)
);
```

### API Endpoints

```python
# Backend routes
@app.get("/api/auth/{platform}/login")
async def initiate_oauth(platform: str):
    """Redirect user to platform's OAuth page"""

@app.get("/api/auth/{platform}/callback")
async def oauth_callback(platform: str, code: str, state: str):
    """Handle OAuth callback and exchange code for tokens"""

@app.post("/api/auth/{platform}/refresh")
async def refresh_token(platform: str):
    """Refresh expired access token"""

@app.delete("/api/auth/{platform}/disconnect")
async def disconnect_platform(platform: str):
    """Revoke tokens and disconnect platform"""
```

### Frontend Flow

```javascript
// 1. User clicks "Connect Twitter"
const connectPlatform = async (platformId) => {
  // Backend returns authorization URL
  const response = await fetch(`/api/auth/${platformId}/login`);
  const { authUrl } = await response.json();

  // Open popup or redirect
  window.location.href = authUrl;
};

// 2. After OAuth, user redirects back to callback
// Backend handles token exchange and stores tokens

// 3. Frontend updates UI to show connected status
const checkConnectionStatus = async () => {
  const response = await fetch('/api/auth/status');
  const platforms = await response.json();
  setConnectedPlatforms(platforms);
};
```

---

## Security Best Practices

### 1. Token Storage

**Backend (Secure):**
- Store tokens in database with encryption
- Never send tokens to frontend
- Use server-side sessions

**Frontend (Avoid):**
- ❌ Don't store tokens in localStorage
- ❌ Don't store tokens in cookies without HttpOnly flag
- ✅ Use session cookies with HttpOnly and Secure flags

### 2. CSRF Protection

```javascript
// Generate random state for each OAuth flow
function generateState() {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64URLEncode(array);
}

// Verify state in callback
if (callbackState !== storedState) {
  throw new Error('CSRF attack detected');
}
```

### 3. Secure Callback URLs

- Always use **HTTPS** (except localhost development)
- Whitelist exact callback URLs (no wildcards)
- Validate redirect URIs on backend

### 4. Token Encryption

```python
from cryptography.fernet import Fernet

# Encrypt tokens before storing
def encrypt_token(token: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(token.encode()).decode()

# Decrypt when needed
def decrypt_token(encrypted_token: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted_token.encode()).decode()
```

### 5. Environment Variables

```python
# Never commit these!
# Use .env file and add to .gitignore
import os
from dotenv import load_dotenv

load_dotenv()

TWITTER_CLIENT_ID = os.getenv('X_CLIENT_ID')
TWITTER_CLIENT_SECRET = os.getenv('X_CLIENT_SECRET')
```

---

## Token Management

### Token Refresh Strategy

```python
import asyncio
from datetime import datetime, timedelta

class TokenManager:
    async def get_valid_token(self, user_id: int, platform: str) -> str:
        """Get valid access token, refreshing if necessary"""
        token_data = await self.db.get_token(user_id, platform)

        # Check if token is expired or expiring soon (5 min buffer)
        if token_data.expires_at < datetime.now() + timedelta(minutes=5):
            # Refresh token
            new_tokens = await self.refresh_platform_token(
                platform,
                token_data.refresh_token
            )

            # Update database
            await self.db.update_token(user_id, platform, new_tokens)
            return new_tokens.access_token

        return token_data.access_token

    async def refresh_platform_token(self, platform: str, refresh_token: str):
        """Platform-specific token refresh logic"""
        if platform == 'twitter':
            return await self.refresh_twitter_token(refresh_token)
        elif platform == 'instagram':
            return await self.refresh_instagram_token(refresh_token)
        # ... other platforms
```

### Background Token Refresh Job

```python
# Cron job to refresh tokens before expiration
async def refresh_expiring_tokens():
    """Run daily to refresh tokens expiring in next 7 days"""
    expiring_tokens = await db.get_tokens_expiring_soon(days=7)

    for token_data in expiring_tokens:
        try:
            new_tokens = await token_manager.refresh_platform_token(
                token_data.platform,
                token_data.refresh_token
            )
            await db.update_token(
                token_data.user_id,
                token_data.platform,
                new_tokens
            )
        except Exception as e:
            # Notify user to re-authenticate
            await notify_user_reauth_needed(token_data.user_id, token_data.platform)
```

---

## Next Steps

### Implementation Checklist

- [ ] Set up developer accounts on all platforms
- [ ] Register applications and get credentials
- [ ] Implement backend OAuth routes
- [ ] Create database schema for token storage
- [ ] Implement token encryption
- [ ] Add frontend OAuth flow UI
- [ ] Implement token refresh logic
- [ ] Set up background job for token management
- [ ] Test OAuth flows on each platform
- [ ] Implement error handling and user notifications
- [ ] Add platform-specific API endpoints (post, read, etc.)
- [ ] Test rate limiting and error scenarios

### Recommended Libraries

**Python (Backend):**
- `authlib` - OAuth client library
- `python-dotenv` - Environment variable management
- `cryptography` - Token encryption
- `httpx` - Async HTTP client

**JavaScript (Frontend):**
- Built-in `fetch` API
- `crypto` Web API (for PKCE)

### Testing

Use platform-provided test accounts:
- X: Developer sandbox accounts
- Meta: Test users in Facebook App Dashboard
- LinkedIn: Developer test accounts

---

## Additional Resources

### Official Documentation

- **X API**: https://developer.x.com/en/docs/authentication/oauth-2-0
- **Instagram Graph API**: https://developers.facebook.com/docs/instagram-api
- **LinkedIn API**: https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication
- **Facebook Graph API**: https://developers.facebook.com/docs/facebook-login

### OAuth 2.0 Resources

- OAuth 2.0 Specification: https://oauth.net/2/
- PKCE Specification: https://oauth.net/2/pkce/

### Security Guides

- OWASP OAuth 2.0 Security: https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html

---

## Troubleshooting Common Issues

### Issue: "Redirect URI mismatch"
**Solution**: Ensure exact match between registered URI and the one in authorization request (including trailing slashes, http vs https).

### Issue: "Invalid client credentials"
**Solution**: Double-check client ID and secret. Make sure they're not accidentally swapped.

### Issue: "Token expired"
**Solution**: Implement token refresh logic. Check token expiration before making API calls.

### Issue: "Insufficient permissions"
**Solution**: Request required scopes during authorization. Some scopes require platform approval.

### Issue: "CORS error in browser"
**Solution**: OAuth flow should be handled server-side, not in browser. Tokens should never be exposed to client.

---

**Document Version**: 1.0
**Last Updated**: January 2025
**Maintainer**: PostProber Development Team
