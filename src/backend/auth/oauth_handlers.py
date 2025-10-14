"""
Base OAuth handler class for social media platform authentication
"""
import secrets
import hashlib
import base64
from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple
from urllib.parse import urlencode
import os


class OAuthHandler(ABC):
    """Base class for OAuth 2.0 handlers"""

    def __init__(self, client_id: str = None, client_secret: str = None, redirect_uri: str = None):
        """
        Initialize OAuth handler

        Args:
            client_id: OAuth client ID (from env if not provided)
            client_secret: OAuth client secret (from env if not provided)
            redirect_uri: OAuth redirect URI (from env if not provided)
        """
        self.client_id = client_id or self._get_env_client_id()
        self.client_secret = client_secret or self._get_env_client_secret()
        self.redirect_uri = redirect_uri or self._get_env_redirect_uri()

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Platform identifier (e.g., 'twitter', 'linkedin')"""
        pass

    @property
    @abstractmethod
    def authorization_base_url(self) -> str:
        """OAuth authorization endpoint URL"""
        pass

    @property
    @abstractmethod
    def token_url(self) -> str:
        """OAuth token exchange endpoint URL"""
        pass

    @property
    @abstractmethod
    def scopes(self) -> list:
        """Required OAuth scopes for the platform"""
        pass

    @abstractmethod
    def _get_env_client_id(self) -> str:
        """Get client ID from environment variables"""
        pass

    @abstractmethod
    def _get_env_client_secret(self) -> str:
        """Get client secret from environment variables"""
        pass

    @abstractmethod
    def _get_env_redirect_uri(self) -> str:
        """Get redirect URI from environment variables"""
        pass

    def generate_state(self) -> str:
        """
        Generate secure random state for CSRF protection

        Returns:
            Random state string
        """
        return secrets.token_urlsafe(32)

    def generate_pkce_pair(self) -> Tuple[str, str]:
        """
        Generate PKCE code verifier and challenge

        Returns:
            Tuple of (code_verifier, code_challenge)
        """
        # Generate code verifier (43-128 characters)
        code_verifier = secrets.token_urlsafe(96)

        # Generate code challenge (SHA256 hash of verifier, base64url encoded)
        challenge_bytes = hashlib.sha256(code_verifier.encode()).digest()
        code_challenge = base64.urlsafe_b64encode(challenge_bytes).decode().rstrip('=')

        return code_verifier, code_challenge

    def get_authorization_url(self, state: str, **kwargs) -> str:
        """
        Build authorization URL for OAuth flow

        Args:
            state: CSRF state parameter
            **kwargs: Additional platform-specific parameters

        Returns:
            Authorization URL
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'state': state,
            'scope': ' '.join(self.scopes)
        }

        # Add any additional parameters
        params.update(kwargs)

        return f"{self.authorization_base_url}?{urlencode(params)}"

    @abstractmethod
    async def exchange_code_for_token(self, code: str, **kwargs) -> Dict:
        """
        Exchange authorization code for access token

        Args:
            code: Authorization code from callback
            **kwargs: Additional platform-specific parameters

        Returns:
            Dict containing access_token, refresh_token, expires_in, etc.
        """
        pass

    @abstractmethod
    async def refresh_access_token(self, refresh_token: str) -> Dict:
        """
        Refresh an expired access token

        Args:
            refresh_token: The refresh token

        Returns:
            Dict containing new access_token and potentially new refresh_token
        """
        pass

    @abstractmethod
    async def get_user_info(self, access_token: str) -> Dict:
        """
        Get user information from the platform

        Args:
            access_token: Valid access token

        Returns:
            Dict containing user information (id, username, etc.)
        """
        pass

    @abstractmethod
    async def revoke_token(self, token: str) -> bool:
        """
        Revoke an access token

        Args:
            token: Token to revoke

        Returns:
            True if successful, False otherwise
        """
        pass
