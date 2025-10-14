"""
LinkedIn OAuth 2.0 handler (3-legged OAuth)
"""
import os
import aiohttp
from typing import Dict
from .oauth_handlers import OAuthHandler


class LinkedInOAuth(OAuthHandler):
    """OAuth 2.0 handler for LinkedIn (3-legged OAuth)"""

    @property
    def platform_name(self) -> str:
        return 'linkedin'

    @property
    def authorization_base_url(self) -> str:
        return 'https://www.linkedin.com/oauth/v2/authorization'

    @property
    def token_url(self) -> str:
        return 'https://www.linkedin.com/oauth/v2/accessToken'

    @property
    def user_info_url(self) -> str:
        return 'https://api.linkedin.com/v2/me'

    @property
    def scopes(self) -> list:
        return [
            'profile',
            'w_member_social'  # Required for posting
            # Note: 'openid' and 'email' are only available for certain API products
            # If using "Share on LinkedIn", only profile + w_member_social are needed
        ]

    def _get_env_client_id(self) -> str:
        return os.getenv('LINKEDIN_CLIENT_ID', '')

    def _get_env_client_secret(self) -> str:
        return os.getenv('LINKEDIN_CLIENT_SECRET', '')

    def _get_env_redirect_uri(self) -> str:
        return os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:5000/api/auth/linkedin/callback')

    async def exchange_code_for_token(self, code: str, **kwargs) -> Dict:
        """
        Exchange authorization code for access token

        Args:
            code: Authorization code from callback

        Returns:
            Dict containing access_token, expires_in, etc.
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri
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
        LinkedIn access tokens are valid for 60 days and don't support refresh tokens.
        Users need to re-authenticate when the token expires.

        Args:
            refresh_token: Not used for LinkedIn

        Returns:
            Dict with error message
        """
        raise Exception(
            "LinkedIn access tokens cannot be refreshed. "
            "Tokens are valid for 60 days. User must re-authenticate."
        )

    async def get_user_info(self, access_token: str) -> Dict:
        """
        Get user information from LinkedIn

        Args:
            access_token: Valid access token

        Returns:
            Dict containing user information
        """
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.user_info_url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get user info: {error_text}")

    async def revoke_token(self, token: str) -> bool:
        """
        LinkedIn doesn't provide a token revocation endpoint.
        Tokens expire automatically after 60 days.

        Args:
            token: Token to revoke

        Returns:
            True (no-op)
        """
        # LinkedIn doesn't support token revocation
        # Tokens automatically expire after 60 days
        return True

    async def create_post(self, access_token: str, person_urn: str, text: str, visibility: str = 'PUBLIC') -> Dict:
        """
        Create a LinkedIn post

        Args:
            access_token: Valid access token
            person_urn: LinkedIn person URN (from user info)
            text: Post text
            visibility: Post visibility ('PUBLIC', 'CONNECTIONS')

        Returns:
            Dict containing post data
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        data = {
            'author': person_urn,
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {
                        'text': text
                    },
                    'shareMediaCategory': 'NONE'
                }
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': visibility
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.linkedin.com/v2/ugcPosts',
                headers=headers,
                json=data
            ) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to create post: {error_text}")

    async def get_user_posts(self, access_token: str, person_urn: str, count: int = 10) -> Dict:
        """
        Get user's recent posts

        Args:
            access_token: Valid access token
            person_urn: LinkedIn person URN
            count: Number of posts to retrieve

        Returns:
            Dict containing posts data
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        params = {
            'q': 'author',
            'author': person_urn,
            'count': count
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://api.linkedin.com/v2/ugcPosts',
                headers=headers,
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get posts: {error_text}")

    async def get_profile_statistics(self, access_token: str, person_urn: str) -> Dict:
        """
        Get profile statistics (followers, connections)

        Args:
            access_token: Valid access token
            person_urn: LinkedIn person URN

        Returns:
            Dict containing statistics
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://api.linkedin.com/v2/networkSizes/{person_urn}',
                headers=headers,
                params={'edgeType': 'CompanyFollowedByMember'}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get profile statistics: {error_text}")
