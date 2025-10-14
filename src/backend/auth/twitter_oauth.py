"""
Twitter/X OAuth 2.0 handler with PKCE
"""
import os
import aiohttp
import base64
from typing import Dict
from .oauth_handlers import OAuthHandler


class TwitterOAuth(OAuthHandler):
    """OAuth 2.0 handler for Twitter/X with PKCE"""

    @property
    def platform_name(self) -> str:
        return 'twitter'

    @property
    def authorization_base_url(self) -> str:
        return 'https://twitter.com/i/oauth2/authorize'

    @property
    def token_url(self) -> str:
        return 'https://api.twitter.com/2/oauth2/token'

    @property
    def revoke_url(self) -> str:
        return 'https://api.twitter.com/2/oauth2/revoke'

    @property
    def user_info_url(self) -> str:
        return 'https://api.twitter.com/2/users/me'

    @property
    def scopes(self) -> list:
        return [
            'tweet.read',
            'tweet.write',
            'users.read',
            'offline.access'  # Required for refresh token
        ]

    def _get_env_client_id(self) -> str:
        return os.getenv('TWITTER_CLIENT_ID', '')

    def _get_env_client_secret(self) -> str:
        return os.getenv('TWITTER_CLIENT_SECRET', '')

    def _get_env_redirect_uri(self) -> str:
        return os.getenv('TWITTER_REDIRECT_URI', 'http://localhost:5000/api/auth/twitter/callback')

    def get_authorization_url(self, state: str, code_challenge: str = None) -> str:
        """
        Build Twitter authorization URL with PKCE

        Args:
            state: CSRF state parameter
            code_challenge: PKCE code challenge

        Returns:
            Authorization URL
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'state': state,
            'scope': ' '.join(self.scopes),
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }

        from urllib.parse import urlencode
        return f"{self.authorization_base_url}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str, code_verifier: str = None, **kwargs) -> Dict:
        """
        Exchange authorization code for access token

        Args:
            code: Authorization code from callback
            code_verifier: PKCE code verifier

        Returns:
            Dict containing access_token, refresh_token, expires_in, etc.
        """
        # Prepare basic auth header
        credentials = f"{self.client_id}:{self.client_secret}"
        b64_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            'Authorization': f'Basic {b64_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'code_verifier': code_verifier
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, headers=headers, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to exchange code for token: {error_text}")

    async def refresh_access_token(self, refresh_token: str) -> Dict:
        """
        Refresh an expired access token

        Args:
            refresh_token: The refresh token

        Returns:
            Dict containing new access_token and potentially new refresh_token
        """
        # Prepare basic auth header
        credentials = f"{self.client_id}:{self.client_secret}"
        b64_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            'Authorization': f'Basic {b64_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, headers=headers, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to refresh token: {error_text}")

    async def get_user_info(self, access_token: str) -> Dict:
        """
        Get user information from Twitter

        Args:
            access_token: Valid access token

        Returns:
            Dict containing user information
        """
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        params = {
            'user.fields': 'id,name,username,profile_image_url,description'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.user_info_url, headers=headers, params=params) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('data', {})
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get user info: {error_text}")

    async def revoke_token(self, token: str) -> bool:
        """
        Revoke an access token

        Args:
            token: Token to revoke

        Returns:
            True if successful, False otherwise
        """
        # Prepare basic auth header
        credentials = f"{self.client_id}:{self.client_secret}"
        b64_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            'Authorization': f'Basic {b64_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'token': token,
            'token_type_hint': 'access_token'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.revoke_url, headers=headers, data=data) as response:
                return response.status == 200

    async def post_tweet(self, access_token: str, text: str) -> Dict:
        """
        Post a tweet

        Args:
            access_token: Valid access token
            text: Tweet text (max 280 characters)

        Returns:
            Dict containing tweet data
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'text': text
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.twitter.com/2/tweets',
                headers=headers,
                json=data
            ) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to post tweet: {error_text}")

    async def get_user_tweets(self, access_token: str, user_id: str, max_results: int = 10) -> Dict:
        """
        Get user's recent tweets

        Args:
            access_token: Valid access token
            user_id: Twitter user ID
            max_results: Number of tweets to retrieve (5-100)

        Returns:
            Dict containing tweet data
        """
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        params = {
            'max_results': min(max_results, 100),
            'tweet.fields': 'created_at,public_metrics,text'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://api.twitter.com/2/users/{user_id}/tweets',
                headers=headers,
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get tweets: {error_text}")
