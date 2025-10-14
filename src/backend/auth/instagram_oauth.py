"""
Instagram OAuth handler using Facebook Graph API
Requires Instagram Business Account connected to Facebook Page
"""
import os
import aiohttp
from typing import Dict
from .oauth_handlers import OAuthHandler


class InstagramOAuth(OAuthHandler):
    """OAuth handler for Instagram via Facebook Graph API"""

    @property
    def platform_name(self) -> str:
        return 'instagram'

    @property
    def authorization_base_url(self) -> str:
        return 'https://www.facebook.com/v18.0/dialog/oauth'

    @property
    def token_url(self) -> str:
        return 'https://graph.facebook.com/v18.0/oauth/access_token'

    @property
    def scopes(self) -> list:
        return [
            'instagram_basic',
            'instagram_content_publish',
            'pages_show_list',
            'pages_read_engagement'
        ]

    def _get_env_client_id(self) -> str:
        return os.getenv('FACEBOOK_APP_ID', '')

    def _get_env_client_secret(self) -> str:
        return os.getenv('FACEBOOK_APP_SECRET', '')

    def _get_env_redirect_uri(self) -> str:
        return os.getenv('INSTAGRAM_REDIRECT_URI', 'http://localhost:5000/api/auth/instagram/callback')

    async def exchange_code_for_token(self, code: str, **kwargs) -> Dict:
        """
        Exchange authorization code for access token

        Args:
            code: Authorization code from callback

        Returns:
            Dict containing access_token, expires_in, etc.
        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.token_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to exchange code for token: {error_text}")

    async def exchange_short_lived_token(self, short_lived_token: str) -> Dict:
        """
        Exchange short-lived token for long-lived token (60 days)

        Args:
            short_lived_token: Short-lived access token

        Returns:
            Dict containing long-lived access_token
        """
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'fb_exchange_token': short_lived_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.token_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to exchange token: {error_text}")

    async def refresh_access_token(self, refresh_token: str) -> Dict:
        """
        Refresh long-lived token (extends by 60 days)

        Args:
            refresh_token: Current access token

        Returns:
            Dict containing new access_token
        """
        # For Facebook/Instagram, we "refresh" by exchanging the current token
        return await self.exchange_short_lived_token(refresh_token)

    async def get_user_info(self, access_token: str) -> Dict:
        """
        Get user information and Instagram accounts

        Args:
            access_token: Valid access token

        Returns:
            Dict containing user and Instagram account information
        """
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # First, get Facebook user info
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://graph.facebook.com/v18.0/me',
                headers=headers,
                params={'fields': 'id,name,email'}
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get user info: {error_text}")

                user_info = await response.json()

            # Get user's Facebook pages
            async with session.get(
                f"https://graph.facebook.com/v18.0/{user_info['id']}/accounts",
                headers=headers,
                params={'fields': 'id,name,access_token'}
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get pages: {error_text}")

                pages_data = await response.json()

            # Get Instagram Business Accounts for each page
            instagram_accounts = []
            for page in pages_data.get('data', []):
                async with session.get(
                    f"https://graph.facebook.com/v18.0/{page['id']}",
                    params={
                        'fields': 'instagram_business_account',
                        'access_token': page['access_token']
                    }
                ) as response:
                    if response.status == 200:
                        page_data = await response.json()
                        if 'instagram_business_account' in page_data:
                            ig_account = page_data['instagram_business_account']

                            # Get Instagram account details
                            async with session.get(
                                f"https://graph.facebook.com/v18.0/{ig_account['id']}",
                                params={
                                    'fields': 'id,username,profile_picture_url,followers_count,follows_count,media_count',
                                    'access_token': page['access_token']
                                }
                            ) as ig_response:
                                if ig_response.status == 200:
                                    ig_data = await ig_response.json()
                                    instagram_accounts.append({
                                        **ig_data,
                                        'page_id': page['id'],
                                        'page_name': page['name'],
                                        'page_access_token': page['access_token']
                                    })

            user_info['instagram_accounts'] = instagram_accounts
            return user_info

    async def revoke_token(self, token: str) -> bool:
        """
        Revoke an access token

        Args:
            token: Token to revoke

        Returns:
            True if successful, False otherwise
        """
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f'https://graph.facebook.com/v18.0/me/permissions',
                params={'access_token': token}
            ) as response:
                return response.status == 200

    async def create_media_container(self, ig_account_id: str, page_access_token: str, image_url: str, caption: str) -> Dict:
        """
        Create a media container for Instagram post

        Args:
            ig_account_id: Instagram Business Account ID
            page_access_token: Page access token
            image_url: Public URL of image to post
            caption: Post caption

        Returns:
            Dict containing container ID
        """
        params = {
            'image_url': image_url,
            'caption': caption,
            'access_token': page_access_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'https://graph.facebook.com/v18.0/{ig_account_id}/media',
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to create media container: {error_text}")

    async def publish_media(self, ig_account_id: str, page_access_token: str, creation_id: str) -> Dict:
        """
        Publish a media container to Instagram

        Args:
            ig_account_id: Instagram Business Account ID
            page_access_token: Page access token
            creation_id: Media container ID

        Returns:
            Dict containing post ID
        """
        params = {
            'creation_id': creation_id,
            'access_token': page_access_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'https://graph.facebook.com/v18.0/{ig_account_id}/media_publish',
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to publish media: {error_text}")

    async def get_user_media(self, ig_account_id: str, page_access_token: str, limit: int = 10) -> Dict:
        """
        Get user's recent Instagram posts

        Args:
            ig_account_id: Instagram Business Account ID
            page_access_token: Page access token
            limit: Number of posts to retrieve

        Returns:
            Dict containing media data
        """
        params = {
            'fields': 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,like_count,comments_count',
            'limit': limit,
            'access_token': page_access_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://graph.facebook.com/v18.0/{ig_account_id}/media',
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get media: {error_text}")

    async def get_account_insights(self, ig_account_id: str, page_access_token: str, metric: str = 'impressions,reach,profile_views') -> Dict:
        """
        Get Instagram account insights

        Args:
            ig_account_id: Instagram Business Account ID
            page_access_token: Page access token
            metric: Comma-separated metrics to retrieve

        Returns:
            Dict containing insights data
        """
        params = {
            'metric': metric,
            'period': 'day',
            'access_token': page_access_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://graph.facebook.com/v18.0/{ig_account_id}/insights',
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get insights: {error_text}")
