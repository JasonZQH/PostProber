"""
Facebook OAuth handler using Graph API
"""
import os
import aiohttp
from typing import Dict
from .oauth_handlers import OAuthHandler


class FacebookOAuth(OAuthHandler):
    """OAuth handler for Facebook via Graph API"""

    @property
    def platform_name(self) -> str:
        return 'facebook'

    @property
    def authorization_base_url(self) -> str:
        return 'https://www.facebook.com/v18.0/dialog/oauth'

    @property
    def token_url(self) -> str:
        return 'https://graph.facebook.com/v18.0/oauth/access_token'

    @property
    def scopes(self) -> list:
        return [
            'public_profile',
            'email',
            'pages_show_list',
            'pages_read_engagement',
            'pages_manage_posts',
            'pages_read_user_content'
        ]

    def _get_env_client_id(self) -> str:
        return os.getenv('FACEBOOK_APP_ID', '')

    def _get_env_client_secret(self) -> str:
        return os.getenv('FACEBOOK_APP_SECRET', '')

    def _get_env_redirect_uri(self) -> str:
        return os.getenv('FACEBOOK_REDIRECT_URI', 'http://localhost:5000/api/auth/facebook/callback')

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
        return await self.exchange_short_lived_token(refresh_token)

    async def get_user_info(self, access_token: str) -> Dict:
        """
        Get user information and Facebook pages

        Args:
            access_token: Valid access token

        Returns:
            Dict containing user and pages information
        """
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        async with aiohttp.ClientSession() as session:
            # Get Facebook user info
            async with session.get(
                'https://graph.facebook.com/v18.0/me',
                headers=headers,
                params={'fields': 'id,name,email,picture'}
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get user info: {error_text}")

                user_info = await response.json()

            # Get user's Facebook pages
            async with session.get(
                f"https://graph.facebook.com/v18.0/{user_info['id']}/accounts",
                headers=headers,
                params={'fields': 'id,name,access_token,picture,fan_count,followers_count'}
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get pages: {error_text}")

                pages_data = await response.json()
                user_info['pages'] = pages_data.get('data', [])

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

    async def create_page_post(self, page_id: str, page_access_token: str, message: str, link: str = None) -> Dict:
        """
        Create a post on a Facebook page

        Args:
            page_id: Facebook Page ID
            page_access_token: Page access token
            message: Post message
            link: Optional link to share

        Returns:
            Dict containing post ID
        """
        params = {
            'message': message,
            'access_token': page_access_token
        }

        if link:
            params['link'] = link

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'https://graph.facebook.com/v18.0/{page_id}/feed',
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to create post: {error_text}")

    async def create_page_photo(self, page_id: str, page_access_token: str, photo_url: str, caption: str = None) -> Dict:
        """
        Post a photo to a Facebook page

        Args:
            page_id: Facebook Page ID
            page_access_token: Page access token
            photo_url: Public URL of photo
            caption: Optional photo caption

        Returns:
            Dict containing post ID
        """
        params = {
            'url': photo_url,
            'access_token': page_access_token
        }

        if caption:
            params['caption'] = caption

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'https://graph.facebook.com/v18.0/{page_id}/photos',
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to post photo: {error_text}")

    async def get_page_posts(self, page_id: str, page_access_token: str, limit: int = 10) -> Dict:
        """
        Get page's recent posts

        Args:
            page_id: Facebook Page ID
            page_access_token: Page access token
            limit: Number of posts to retrieve

        Returns:
            Dict containing posts data
        """
        params = {
            'fields': 'id,message,created_time,permalink_url,likes.summary(true),comments.summary(true),shares',
            'limit': limit,
            'access_token': page_access_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://graph.facebook.com/v18.0/{page_id}/posts',
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get posts: {error_text}")

    async def get_page_insights(self, page_id: str, page_access_token: str, metric: str = 'page_impressions,page_engaged_users,page_views_total') -> Dict:
        """
        Get page insights

        Args:
            page_id: Facebook Page ID
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
                f'https://graph.facebook.com/v18.0/{page_id}/insights',
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get insights: {error_text}")

    async def get_post_insights(self, post_id: str, page_access_token: str) -> Dict:
        """
        Get insights for a specific post

        Args:
            post_id: Facebook post ID
            page_access_token: Page access token

        Returns:
            Dict containing post insights
        """
        params = {
            'metric': 'post_impressions,post_engaged_users,post_clicks',
            'access_token': page_access_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://graph.facebook.com/v18.0/{post_id}/insights',
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get post insights: {error_text}")

    async def delete_post(self, post_id: str, access_token: str) -> bool:
        """
        Delete a post

        Args:
            post_id: Post ID to delete
            access_token: Access token

        Returns:
            True if successful, False otherwise
        """
        params = {
            'access_token': access_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f'https://graph.facebook.com/v18.0/{post_id}',
                params=params
            ) as response:
                return response.status == 200
