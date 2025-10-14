"""
OAuth authentication handlers for social media platforms
"""
from .oauth_handlers import OAuthHandler
from .twitter_oauth import TwitterOAuth
from .linkedin_oauth import LinkedInOAuth
from .instagram_oauth import InstagramOAuth
from .facebook_oauth import FacebookOAuth

__all__ = [
    'OAuthHandler',
    'TwitterOAuth',
    'LinkedInOAuth',
    'InstagramOAuth',
    'FacebookOAuth'
]
