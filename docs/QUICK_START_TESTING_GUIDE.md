# Quick Start Testing Guide - Connect Real Platforms

This guide shows you how to connect real social media platforms to PostProber for immediate testing.

## 🚀 Fastest Way: Twitter/X with API Keys (5 minutes)

Twitter/X is the **easiest platform to test** because it supports direct API key entry - no OAuth flow needed!

### Prerequisites

- Twitter/X account
- Twitter Developer account (free)

---

## Step-by-Step: Connect Twitter/X for Testing

### 1. Get Twitter API Credentials

#### 1.1 Create Developer Account
1. Go to https://developer.x.com
2. Sign in with your Twitter account
3. Click "Sign up" for developer account (if you don't have one)
4. Complete the application (basic info, use case)
5. Verify your email

#### 1.2 Create a Project and App
1. In the Developer Portal, click **"Create Project"**
2. Name your project (e.g., "PostProber Testing")
3. Select use case: "Making a bot" or "Exploring the API"
4. Provide project description
5. Click **"Create App"**
6. Name your app (e.g., "PostProber")

#### 1.3 Get Your API Keys
1. After creating the app, you'll see **"API Key and Secret"**
2. **SAVE THESE IMMEDIATELY** (you can't see them again):
   ```
   API Key: xxxxxxxxxxxxxxxxxxxxx
   API Key Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

#### 1.4 Get Bearer Token (Easiest method)
1. In your app settings, go to the **"Keys and tokens"** tab
2. Under **"Authentication Tokens"**, click **"Generate"** next to **"Bearer Token"**
3. Copy your Bearer Token:
   ```
   Bearer Token: AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxxxxxxxxx
   ```
4. **SAVE THIS TOKEN** - you'll need it for read-only operations

#### 1.5 Get Access Token & Secret (For posting)
1. In the same **"Keys and tokens"** tab
2. Under **"Authentication Tokens"**, find **"Access Token and Secret"**
3. Click **"Generate"**
4. Copy both values:
   ```
   Access Token: 1234567890-xxxxxxxxxxxxxxxxxxxxx
   Access Token Secret: xxxxxxxxxxxxxxxxxxxxx
   ```
5. **SAVE THESE** - you need them to post tweets

#### 1.6 Set App Permissions
1. Go to **"Settings"** tab in your app
2. Under **"User authentication settings"**, click **"Set up"**
3. Enable **"OAuth 1.0a"**
4. Set App permissions to **"Read and write"** (to post tweets)
5. Save changes
6. **Regenerate your Access Token & Secret** (required after permission change)

---

## Step 2: Configure PostProber Backend

### 2.1 Add API Keys to Environment Variables

Edit your `.env` file:

```bash
# Twitter/X API Credentials
TWITTER_API_KEY=your_api_key_here
TWITTER_API_KEY_SECRET=your_api_key_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

# For posting (user context)
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

### 2.2 Install Twitter API Library

```bash
# Install Tweepy (Python Twitter library)
pip install tweepy
```

---

## Step 3: Update Backend to Support Direct API Key Entry

### 3.1 Create Twitter API Client

Create `src/backend/platforms/twitter_client.py`:

```python
import os
import tweepy
from typing import Dict, Optional

class TwitterClient:
    def __init__(self,
                 api_key: Optional[str] = None,
                 api_key_secret: Optional[str] = None,
                 access_token: Optional[str] = None,
                 access_token_secret: Optional[str] = None,
                 bearer_token: Optional[str] = None):
        """
        Initialize Twitter client with API credentials.

        For posting: Requires API Key, API Secret, Access Token, Access Secret
        For reading: Can use Bearer Token only
        """

        # Use provided credentials or fall back to environment variables
        self.api_key = api_key or os.getenv('TWITTER_API_KEY')
        self.api_key_secret = api_key_secret or os.getenv('TWITTER_API_KEY_SECRET')
        self.access_token = access_token or os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = access_token_secret or os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.bearer_token = bearer_token or os.getenv('TWITTER_BEARER_TOKEN')

        # Initialize Tweepy client for API v2 (posting)
        if all([self.api_key, self.api_key_secret, self.access_token, self.access_token_secret]):
            self.client = tweepy.Client(
                consumer_key=self.api_key,
                consumer_secret=self.api_key_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
        elif self.bearer_token:
            # Read-only client with Bearer Token
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                wait_on_rate_limit=True
            )
        else:
            raise ValueError("Missing Twitter API credentials")

    async def post_tweet(self, text: str) -> Dict:
        """Post a tweet"""
        try:
            response = self.client.create_tweet(text=text)
            return {
                "success": True,
                "tweet_id": response.data['id'],
                "text": text
            }
        except tweepy.TweepyException as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def get_user_info(self) -> Dict:
        """Get authenticated user's information"""
        try:
            # Get authenticated user
            me = self.client.get_me(
                user_fields=['username', 'name', 'profile_image_url', 'public_metrics']
            )

            return {
                "success": True,
                "user": {
                    "id": me.data.id,
                    "username": me.data.username,
                    "name": me.data.name,
                    "profile_image": me.data.profile_image_url,
                    "followers": me.data.public_metrics['followers_count'],
                    "following": me.data.public_metrics['following_count'],
                    "tweets": me.data.public_metrics['tweet_count']
                }
            }
        except tweepy.TweepyException as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def get_recent_tweets(self, max_results: int = 5) -> Dict:
        """Get user's recent tweets"""
        try:
            me = self.client.get_me()
            tweets = self.client.get_users_tweets(
                id=me.data.id,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics']
            )

            return {
                "success": True,
                "tweets": [
                    {
                        "id": tweet.id,
                        "text": tweet.text,
                        "created_at": tweet.created_at.isoformat(),
                        "likes": tweet.public_metrics['like_count'],
                        "retweets": tweet.public_metrics['retweet_count'],
                        "replies": tweet.public_metrics['reply_count']
                    }
                    for tweet in tweets.data
                ] if tweets.data else []
            }
        except tweepy.TweepyException as e:
            return {
                "success": False,
                "error": str(e)
            }
```

### 3.2 Create API Endpoint for Direct Connection

Update `src/backend/api/endpoints/auth.py`:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from platforms.twitter_client import TwitterClient

router = APIRouter()

class TwitterDirectConnect(BaseModel):
    api_key: str
    api_key_secret: str
    access_token: str
    access_token_secret: str

@router.post("/api/auth/twitter/connect-direct")
async def connect_twitter_direct(credentials: TwitterDirectConnect):
    """
    Connect Twitter using direct API key entry (for testing)
    """
    try:
        # Initialize Twitter client with provided credentials
        client = TwitterClient(
            api_key=credentials.api_key,
            api_key_secret=credentials.api_key_secret,
            access_token=credentials.access_token,
            access_token_secret=credentials.access_token_secret
        )

        # Verify credentials by getting user info
        user_info = await client.get_user_info()

        if not user_info['success']:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Store credentials in session/database (encrypted)
        # For now, return success with user info
        return {
            "success": True,
            "platform": "twitter",
            "user": user_info['user'],
            "message": "Successfully connected to Twitter!"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/twitter/post")
async def post_to_twitter(content: dict):
    """
    Post a tweet

    Request body: {"text": "Your tweet content here"}
    """
    try:
        # Get stored credentials from session/database
        # For now, use environment variables
        client = TwitterClient()

        result = await client.post_tweet(content['text'])

        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Step 4: Update Frontend for Direct API Key Entry

### 4.1 Create API Key Input Modal

Create `src/frontend/components/platforms/TwitterKeyEntryModal.jsx`:

```jsx
import React, { useState } from 'react'

function TwitterKeyEntryModal({ isOpen, onClose, onConnect }) {
  const [credentials, setCredentials] = useState({
    apiKey: '',
    apiKeySecret: '',
    accessToken: '',
    accessTokenSecret: ''
  })
  const [isConnecting, setIsConnecting] = useState(false)
  const [error, setError] = useState(null)

  const handleConnect = async () => {
    setIsConnecting(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/api/auth/twitter/connect-direct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_key: credentials.apiKey,
          api_key_secret: credentials.apiKeySecret,
          access_token: credentials.accessToken,
          access_token_secret: credentials.accessTokenSecret
        })
      })

      const data = await response.json()

      if (data.success) {
        onConnect(data)
        onClose()
      } else {
        setError('Failed to connect. Please check your credentials.')
      }
    } catch (err) {
      setError('Connection error. Make sure the backend is running.')
    } finally {
      setIsConnecting(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <div className="p-8">
          <h2 className="text-3xl font-bold mb-2" style={{ color: 'var(--gray-900)' }}>
            Connect Twitter with API Keys 🔑
          </h2>
          <p className="mb-6" style={{ color: 'var(--gray-600)' }}>
            Enter your Twitter API credentials from the Developer Portal
          </p>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: 'var(--gray-700)' }}>
                API Key
              </label>
              <input
                type="text"
                value={credentials.apiKey}
                onChange={(e) => setCredentials({ ...credentials, apiKey: e.target.value })}
                placeholder="Your API Key"
                className="w-full px-4 py-3 border rounded-lg"
                style={{ borderColor: 'var(--gray-300)' }}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: 'var(--gray-700)' }}>
                API Key Secret
              </label>
              <input
                type="password"
                value={credentials.apiKeySecret}
                onChange={(e) => setCredentials({ ...credentials, apiKeySecret: e.target.value })}
                placeholder="Your API Key Secret"
                className="w-full px-4 py-3 border rounded-lg"
                style={{ borderColor: 'var(--gray-300)' }}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: 'var(--gray-700)' }}>
                Access Token
              </label>
              <input
                type="text"
                value={credentials.accessToken}
                onChange={(e) => setCredentials({ ...credentials, accessToken: e.target.value })}
                placeholder="Your Access Token"
                className="w-full px-4 py-3 border rounded-lg"
                style={{ borderColor: 'var(--gray-300)' }}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: 'var(--gray-700)' }}>
                Access Token Secret
              </label>
              <input
                type="password"
                value={credentials.accessTokenSecret}
                onChange={(e) => setCredentials({ ...credentials, accessTokenSecret: e.target.value })}
                placeholder="Your Access Token Secret"
                className="w-full px-4 py-3 border rounded-lg"
                style={{ borderColor: 'var(--gray-300)' }}
              />
            </div>
          </div>

          <div className="mt-6 flex gap-3">
            <button
              onClick={handleConnect}
              disabled={isConnecting || !credentials.apiKey || !credentials.accessToken}
              className="btn btn-primary flex-1"
            >
              {isConnecting ? (
                <>
                  <div className="spinner"></div>
                  <span>Connecting...</span>
                </>
              ) : (
                <>
                  <span>Connect Twitter</span>
                </>
              )}
            </button>
            <button
              onClick={onClose}
              className="btn btn-outline"
              disabled={isConnecting}
            >
              Cancel
            </button>
          </div>

          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm" style={{ color: 'var(--gray-700)' }}>
              <strong>💡 Where to find these:</strong>
              <br />
              1. Go to <a href="https://developer.x.com" target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">developer.x.com</a>
              <br />
              2. Select your app → "Keys and tokens" tab
              <br />
              3. Copy all 4 credentials
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TwitterKeyEntryModal
```

### 4.2 Update PlatformConnectionModal

Update `src/frontend/components/platforms/PlatformConnectionModal.jsx` to show the API key entry option:

```jsx
import TwitterKeyEntryModal from './TwitterKeyEntryModal'

// Add state
const [showTwitterKeyEntry, setShowTwitterKeyEntry] = useState(false)

// Update Twitter connect button
<button
  className="btn btn-primary w-full"
  onClick={() => {
    if (platform.id === 'twitter') {
      setShowTwitterKeyEntry(true)
    } else {
      handleConnectPlatform(platform)
    }
  }}
>
  Connect {platform.name}
</button>

// Add modal at the end
<TwitterKeyEntryModal
  isOpen={showTwitterKeyEntry}
  onClose={() => setShowTwitterKeyEntry(false)}
  onConnect={(data) => {
    // Handle successful connection
    console.log('Connected:', data)
    // Update platformService with real connection
  }}
/>
```

---

## Step 5: Test the Connection

### 5.1 Start Backend
```bash
cd src/backend
python -m uvicorn main:app --reload --port 8000
```

### 5.2 Start Frontend
```bash
npm run dev:frontend
```

### 5.3 Connect Twitter
1. Open http://localhost:5173
2. Click "Connect Twitter"
3. Enter your 4 API credentials from Step 1
4. Click "Connect"
5. ✅ You should see "Successfully connected!"

### 5.4 Test Posting
1. Go to "Compose" page
2. Write a tweet: "Testing PostProber! 🚀"
3. Select Twitter
4. Click "Publish Now"
5. Check your Twitter account - the tweet should appear!

---

## Comparison: API Keys vs OAuth

### ✅ API Keys (What we just did)
**Pros:**
- ⚡ **Fastest setup** (5 minutes)
- 🧪 **Perfect for testing**
- 🔧 **No callback URLs needed**
- 💻 **Works on localhost**

**Cons:**
- 👤 **Only works for YOUR account** (the developer)
- 🔐 **Users must have developer accounts**
- ⚠️ **Users handle sensitive tokens**
- 🚫 **Not suitable for production**

### 🔐 OAuth Flow (Production-ready)
**Pros:**
- 👥 **Works for any user** (not just developers)
- 🛡️ **More secure** (users don't see tokens)
- ✅ **Professional user experience**
- 📱 **Industry standard**

**Cons:**
- ⏱️ **Takes longer to set up** (1-2 hours)
- 🌐 **Requires HTTPS/ngrok** for callbacks
- 📋 **More complex implementation**
- 🔄 **Requires app approval** on some platforms

---

## Next: Other Platforms

### LinkedIn & Instagram
**⚠️ OAuth Required** - These platforms don't support direct API key entry. You must implement OAuth flow:

1. **LinkedIn:**
   - Requires OAuth 2.0
   - See `docs/OAUTH_INTEGRATION_GUIDE.md` Section: LinkedIn Integration
   - Estimated time: 30-60 minutes

2. **Instagram:**
   - Requires Facebook OAuth + Instagram Business Account
   - See `docs/OAUTH_INTEGRATION_GUIDE.md` Section: Instagram Integration
   - Estimated time: 45-90 minutes

---

## Troubleshooting

### Error: "Invalid or expired token"
**Solution:** Regenerate your Access Token & Secret in the Twitter Developer Portal

### Error: "Read-only application cannot POST"
**Solution:**
1. Go to your app settings
2. Change permissions to "Read and Write"
3. Regenerate Access Token & Secret

### Error: "Could not authenticate you"
**Solution:** Double-check all 4 credentials are correct (no extra spaces)

### Error: "Backend not responding"
**Solution:** Make sure backend is running on port 8000

---

## Production Recommendation

For **production deployment**, implement OAuth instead of API keys:
- Users can connect without developer accounts
- More secure (no token exposure)
- Better user experience

See `docs/OAUTH_INTEGRATION_GUIDE.md` for full OAuth implementation.

---

## Summary: Testing Right Now

**Fastest path (5 minutes):**
1. ✅ Get Twitter API keys from developer.x.com
2. ✅ Add API key input to frontend
3. ✅ Test posting a tweet
4. ✅ Verify it works!

**Production path (later):**
1. 📋 Implement OAuth for all platforms
2. 🔐 Store tokens securely
3. 🔄 Add token refresh logic
4. 🚀 Deploy with HTTPS

---

**Document Version:** 1.0
**Last Updated:** January 2025
**Recommended for:** Testing & Development Only
