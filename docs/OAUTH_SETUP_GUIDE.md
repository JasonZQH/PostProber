# OAuth Setup Guide for PostProber

This guide will help you set up OAuth authentication for all supported platforms (Twitter/X, LinkedIn, Instagram, and Facebook).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Platform-Specific Setup](#platform-specific-setup)
   - [Twitter/X](#1-twitterx-oauth-setup)
   - [LinkedIn](#2-linkedin-oauth-setup)
   - [Instagram](#3-instagram-oauth-setup-via-facebook)
   - [Facebook](#4-facebook-oauth-setup)
4. [Installation](#installation)
5. [Running the Application](#running-the-application)
6. [Testing OAuth Flow](#testing-oauth-flow)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn
- A PostProber account (session-based, no registration required)

## Environment Setup

1. **Copy the environment template:**

```bash
cp .env.template .env
```

2. **Edit `.env` file with your credentials** (see Platform-Specific Setup below)

---

## Platform-Specific Setup

### 1. Twitter/X OAuth Setup

**Time Required:** ~10 minutes

#### Step 1: Create a Twitter Developer Account

1. Go to [https://developer.twitter.com/en/portal/dashboard](https://developer.twitter.com/en/portal/dashboard)
2. Sign in with your Twitter account
3. Click "Create App" or "Create Project"

#### Step 2: Configure OAuth 2.0

1. In your app dashboard, navigate to **"User authentication settings"**
2. Click **"Set up"**
3. Configure the following:
   - **App permissions:** Read and write
   - **Type of App:** Web App
   - **Callback URI:** `http://localhost:8000/api/auth/twitter/callback`
   - **Website URL:** `http://localhost:5173`
4. Save your settings

#### Step 3: Get Credentials

1. Navigate to **"Keys and tokens"** tab
2. Copy your **Client ID** and **Client Secret**
3. Add to `.env`:

```env
TWITTER_CLIENT_ID=your_client_id_here
TWITTER_CLIENT_SECRET=your_client_secret_here
TWITTER_REDIRECT_URI=http://localhost:8000/api/auth/twitter/callback
```

**Important Notes:**
- Twitter uses OAuth 2.0 with PKCE (Proof Key for Code Exchange)
- Access tokens expire after 2 hours
- Refresh tokens are valid until revoked

---

### 2. LinkedIn OAuth Setup

**Time Required:** ~10 minutes

#### Step 1: Create a LinkedIn App

1. Go to [https://www.linkedin.com/developers/apps](https://www.linkedin.com/developers/apps)
2. Click **"Create app"**
3. Fill in required information:
   - App name: "PostProber"
   - LinkedIn Page: (select or create one)
   - App logo: (optional)
4. Accept terms and create

#### Step 2: Configure OAuth Settings

1. In your app dashboard, go to **"Auth"** tab
2. Add **Redirect URLs:**
   - `http://localhost:8000/api/auth/linkedin/callback`
3. Under **"OAuth 2.0 scopes"**, request:
   - `openid`
   - `profile`
   - `email`
   - `w_member_social` (for posting)

#### Step 3: Verify and Get Credentials

1. Go to **"Settings"** tab
2. Copy your **Client ID** and **Client Secret**
3. Add to `.env`:

```env
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8000/api/auth/linkedin/callback
```

**Important Notes:**
- LinkedIn access tokens are valid for 60 days
- No refresh tokens (users must re-authenticate after 60 days)
- Requires a verified LinkedIn Page for posting

---

### 3. Instagram OAuth Setup (via Facebook)

**Time Required:** ~20 minutes (includes Facebook verification)

#### Step 1: Create Facebook App

1. Go to [https://developers.facebook.com/apps](https://developers.facebook.com/apps)
2. Click **"Create App"**
3. Select **"Business"** as app type
4. Fill in app details

#### Step 2: Add Instagram Product

1. In app dashboard, click **"Add Product"**
2. Find **"Instagram"** and click **"Set Up"**

#### Step 3: Configure OAuth Settings

1. Go to **Settings → Basic**
2. Add **Privacy Policy URL** and **Terms of Service URL** (required)
3. Go to **Instagram → Basic Display**
4. Add **Valid OAuth Redirect URIs:**
   - `http://localhost:8000/api/auth/instagram/callback`
5. Add **Deauthorize Callback URL:**
   - `http://localhost:8000/api/auth/instagram/deauthorize`
6. Add **Data Deletion Request URL:**
   - `http://localhost:8000/api/auth/instagram/deletion`

#### Step 4: Connect Instagram Business Account

1. Go to **Instagram → Basic Display**
2. Scroll to **"Instagram Testers"**
3. Click **"Add Instagram Testers"**
4. Add your Instagram Business Account
5. Open Instagram app → Settings → Account → Business → Instagram partners
6. Accept the tester invite

#### Step 5: Get Credentials

1. Go to **Settings → Basic**
2. Copy **App ID** and **App Secret**
3. Add to `.env`:

```env
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
INSTAGRAM_REDIRECT_URI=http://localhost:8000/api/auth/instagram/callback
```

**Important Notes:**
- Requires Instagram Business Account (not Personal Account)
- Instagram Business Account must be connected to a Facebook Page
- Access tokens are short-lived (1 hour) but can be exchanged for long-lived tokens (60 days)
- App must be in "Development Mode" for testing

---

### 4. Facebook OAuth Setup

**Time Required:** ~15 minutes

#### Step 1: Create/Use Existing Facebook App

If you created an app for Instagram, you can use the same app. Otherwise:

1. Go to [https://developers.facebook.com/apps](https://developers.facebook.com/apps)
2. Click **"Create App"**
3. Select **"Business"** as app type

#### Step 2: Add Facebook Login Product

1. In app dashboard, click **"Add Product"**
2. Find **"Facebook Login"** and click **"Set Up"**

#### Step 3: Configure OAuth Settings

1. Go to **Facebook Login → Settings**
2. Add **Valid OAuth Redirect URIs:**
   - `http://localhost:8000/api/auth/facebook/callback`
3. Enable **"Client OAuth Login"**
4. Enable **"Web OAuth Login"**

#### Step 4: Request Permissions

1. Go to **App Review → Permissions and Features**
2. Request the following permissions:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
   - `pages_read_user_content`

#### Step 5: Get Credentials

1. Go to **Settings → Basic**
2. Copy **App ID** and **App Secret**
3. Add to `.env` (if not already added for Instagram):

```env
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/auth/facebook/callback
```

**Important Notes:**
- Requires Facebook Page for posting
- Access tokens are short-lived but can be exchanged for long-lived tokens (60 days)
- Some permissions require App Review for production use

---

## Installation

### 1. Install Backend Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
# Navigate to frontend directory
cd src/frontend

# Install npm dependencies
npm install
```

### 3. Initialize Database

The database will be automatically initialized on first run. It will create:
- `src/backend/database/postprober.db`
- Tables: users, platform_tokens, oauth_states

---

## Running the Application

### 1. Start Backend Server

```bash
# From project root
cd src/backend
python main.py
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### 2. Start Frontend Development Server

```bash
# In a new terminal, from project root
cd src/frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## Testing OAuth Flow

### 1. Access the Application

1. Open your browser to `http://localhost:5173`
2. You'll see the PostProber dashboard

### 2. Connect a Platform

1. Navigate to **"Accounts"** page
2. Click **"Add Platform"** tab
3. Choose a platform (e.g., Twitter)
4. Click **"Connect"**

### 3. OAuth Flow

1. You'll be redirected to the platform's authorization page
2. Review the permissions requested
3. Click **"Authorize"** or **"Allow"**
4. You'll be redirected back to PostProber
5. See a success notification: "Successfully connected {platform}!"

### 4. Verify Connection

1. Go to **"Accounts"** page
2. See your connected account in the **"Connected Accounts"** tab
3. View your username and connection timestamp

### 5. Test Platform Features

**Twitter:**
- Go to **"Compose"** page
- Write a tweet (max 280 characters)
- Click **"Post Now"**

**LinkedIn:**
- Go to **"Compose"** page
- Write a professional post
- Click **"Post Now"**

**Instagram:**
- Go to **"Compose"** page
- Add image URL and caption
- Click **"Post Now"**

**Facebook:**
- Go to **"Compose"** page
- Write a post for your page
- Click **"Post Now"**

---

## Troubleshooting

### Issue: "Invalid redirect URI" Error

**Solution:**
- Ensure redirect URIs in platform developer consoles exactly match:
  - Twitter: `http://localhost:8000/api/auth/twitter/callback`
  - LinkedIn: `http://localhost:8000/api/auth/linkedin/callback`
  - Instagram: `http://localhost:8000/api/auth/instagram/callback`
  - Facebook: `http://localhost:8000/api/auth/facebook/callback`
- No trailing slashes
- Must use `http://` for localhost (not `https://`)

### Issue: "Invalid client credentials" Error

**Solution:**
- Double-check Client ID and Client Secret in `.env`
- Ensure no extra spaces or quotes
- Regenerate credentials if needed

### Issue: Instagram "No Business Account Found"

**Solution:**
- Convert Instagram account to Business Account:
  1. Go to Instagram Settings
  2. Account → Switch to Professional Account
  3. Choose "Business"
- Link Instagram Business Account to Facebook Page
- Add account as tester in Facebook App

### Issue: Token Expired

**Solution:**
- Most platforms support automatic token refresh
- LinkedIn requires re-authentication after 60 days
- Check **"Accounts"** page for token expiration warnings

### Issue: CORS Errors

**Solution:**
- Ensure backend is running on `http://localhost:8000`
- Ensure frontend is running on `http://localhost:5173`
- Check CORS configuration in `src/backend/main.py`

### Issue: Database Errors

**Solution:**
- Delete database and restart:
  ```bash
  rm src/backend/database/postprober.db
  python src/backend/main.py
  ```

### Issue: "Cannot POST" Error

**Solution:**
- Check if you have required permissions for the platform
- Instagram: Requires Business Account and proper scope
- Facebook: Requires Page Admin role
- LinkedIn: Requires `w_member_social` scope

---

## Security Notes

### Production Deployment

When deploying to production:

1. **Update Redirect URIs:**
   - Change from `http://localhost:8000` to your production domain
   - Update in both `.env` and platform developer consoles

2. **Use HTTPS:**
   - All OAuth providers require HTTPS in production
   - Obtain SSL certificate (Let's Encrypt is free)

3. **Secure Environment Variables:**
   - Never commit `.env` to version control
   - Use environment variable management (e.g., AWS Secrets Manager)

4. **Database Security:**
   - Consider encrypting tokens at rest
   - Implement proper database backups
   - Use PostgreSQL instead of SQLite for production

5. **Session Management:**
   - Set secure cookie flags
   - Implement session expiration
   - Consider Redis for session storage

---

## API Endpoints Reference

### OAuth Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/{platform}/login` | GET | Initiate OAuth flow |
| `/api/auth/{platform}/callback` | GET | OAuth callback handler |
| `/api/auth/{platform}/disconnect` | POST | Disconnect platform |
| `/api/auth/status` | GET | Get all platform statuses |
| `/api/auth/{platform}/token` | GET | Get token (internal use) |

### Supported Platforms

- `twitter` - Twitter/X
- `linkedin` - LinkedIn
- `instagram` - Instagram
- `facebook` - Facebook

---

## Need Help?

If you encounter issues not covered in this guide:

1. Check the browser console for errors
2. Check backend logs for detailed error messages
3. Review platform-specific developer documentation
4. Ensure all credentials are correct in `.env`

---

## Next Steps

After successfully connecting platforms:

1. Explore the **Analytics** page for engagement insights
2. Use the **Health** monitoring dashboard
3. Schedule posts using the **Schedule** feature
4. Use AI-powered content optimization

Happy posting! 🚀
