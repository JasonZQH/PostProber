"""
OAuth authentication endpoints for social media platforms
"""
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Dict, Optional
import logging
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from auth.twitter_oauth import TwitterOAuth
from auth.linkedin_oauth import LinkedInOAuth
from auth.instagram_oauth import InstagramOAuth
from auth.facebook_oauth import FacebookOAuth
from database.models import db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth")

# Initialize OAuth handlers
oauth_handlers = {
    'twitter': TwitterOAuth(),
    'linkedin': LinkedInOAuth(),
    'instagram': InstagramOAuth(),
    'facebook': FacebookOAuth()
}


def get_or_create_user(request: Request) -> int:
    """
    Get or create user based on session

    Args:
        request: FastAPI request object

    Returns:
        User ID
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        # Generate new session ID
        import secrets
        session_id = secrets.token_urlsafe(32)

    # Get or create user
    user = db.get_user_by_session(session_id)
    if not user:
        user_id = db.create_user(session_id)
    else:
        user_id = user['id']
        db.update_user_activity(user_id)

    return user_id, session_id


@router.get("/{platform}/login")
async def platform_login(platform: str, request: Request):
    """
    Initiate OAuth flow for a platform

    Args:
        platform: Platform name (twitter, linkedin, instagram, facebook)

    Returns:
        Redirect to platform authorization URL
    """
    if platform not in oauth_handlers:
        raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")

    try:
        handler = oauth_handlers[platform]

        # Get or create user
        user_id, session_id = get_or_create_user(request)

        # Generate state for CSRF protection
        state = handler.generate_state()

        # Build authorization URL
        if platform == 'twitter':
            # Twitter requires PKCE
            code_verifier, code_challenge = handler.generate_pkce_pair()

            # Store state and code verifier in database
            db.create_oauth_state(
                state=state,
                user_id=user_id,
                platform=platform,
                code_verifier=code_verifier
            )

            auth_url = handler.get_authorization_url(state, code_challenge=code_challenge)
        else:
            # Other platforms use standard OAuth
            db.create_oauth_state(
                state=state,
                user_id=user_id,
                platform=platform
            )

            auth_url = handler.get_authorization_url(state)

        # Create response with session cookie
        response = RedirectResponse(url=auth_url)
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            samesite='lax',
            max_age=30 * 24 * 60 * 60  # 30 days
        )

        return response

    except Exception as e:
        logger.error(f"Error initiating {platform} OAuth: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate OAuth: {str(e)}")


@router.get("/{platform}/callback")
async def platform_callback(
    platform: str,
    request: Request,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    error_description: Optional[str] = None
):
    """
    Handle OAuth callback from platform

    Args:
        platform: Platform name
        code: Authorization code (if successful)
        state: CSRF state parameter
        error: Error code (if authorization failed)
        error_description: Human-readable error description

    Returns:
        Redirect to frontend with success/error
    """
    if platform not in oauth_handlers:
        raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")

    # Check if platform returned an error
    if error:
        error_msg = error_description or error
        logger.error(f"OAuth error from {platform}: {error_msg}")
        return RedirectResponse(url=f"http://localhost:5173/accounts?error={error_msg}")

    # Check for required parameters
    if not code or not state:
        return RedirectResponse(url=f"http://localhost:5173/accounts?error=Missing authorization code or state")

    try:
        # Verify state
        oauth_state = db.get_oauth_state(state)
        if not oauth_state:
            raise HTTPException(status_code=400, detail="Invalid or expired state")

        if oauth_state['platform'] != platform:
            raise HTTPException(status_code=400, detail="Platform mismatch")

        user_id = oauth_state['user_id']
        handler = oauth_handlers[platform]

        # Exchange code for token
        if platform == 'twitter':
            code_verifier = oauth_state['code_verifier']
            token_data = await handler.exchange_code_for_token(code, code_verifier=code_verifier)
        else:
            token_data = await handler.exchange_code_for_token(code)

        # Get user info from platform
        access_token = token_data.get('access_token')
        user_info = await handler.get_user_info(access_token)

        # For Instagram and Facebook, we need to handle multiple accounts
        if platform == 'instagram':
            # Instagram can have multiple business accounts
            instagram_accounts = user_info.get('instagram_accounts', [])
            if instagram_accounts:
                # Use the first Instagram account
                ig_account = instagram_accounts[0]
                platform_user_id = ig_account.get('id')
                platform_username = ig_account.get('username')
                # Store page access token for posting
                user_info['selected_account'] = ig_account
            else:
                raise HTTPException(status_code=400, detail="No Instagram Business Account found")
        elif platform == 'facebook':
            # Facebook uses pages for posting
            pages = user_info.get('pages', [])
            if pages:
                # Use the first page
                page = pages[0]
                platform_user_id = page.get('id')
                platform_username = page.get('name')
                user_info['selected_page'] = page
            else:
                raise HTTPException(status_code=400, detail="No Facebook Page found")
        elif platform == 'twitter':
            platform_user_id = user_info.get('id')
            platform_username = user_info.get('username')
        elif platform == 'linkedin':
            # LinkedIn /v2/me returns 'id', 'localizedFirstName', 'localizedLastName'
            platform_user_id = user_info.get('id')
            # Combine first and last name
            first_name = user_info.get('localizedFirstName', '')
            last_name = user_info.get('localizedLastName', '')
            platform_username = f"{first_name} {last_name}".strip() or platform_user_id

        # Save token to database
        db.save_platform_token(
            user_id=user_id,
            platform=platform,
            access_token=access_token,
            refresh_token=token_data.get('refresh_token'),
            expires_in=token_data.get('expires_in'),
            scope=token_data.get('scope'),
            platform_user_id=platform_user_id,
            platform_username=platform_username,
            platform_user_data=user_info
        )

        # Delete used state
        db.delete_oauth_state(state)

        # Redirect to frontend success page
        return RedirectResponse(url=f"http://localhost:5173/accounts?connected={platform}")

    except Exception as e:
        logger.error(f"Error in {platform} OAuth callback: {str(e)}")
        # Redirect to frontend error page
        return RedirectResponse(url=f"http://localhost:5173/accounts?error={str(e)}")


@router.get("/status")
async def auth_status(request: Request):
    """
    Get authentication status for all platforms

    Returns:
        Dict with connection status for each platform
    """
    try:
        # Get user from session
        session_id = request.cookies.get('session_id')
        if not session_id:
            return JSONResponse(content={
                "connected_platforms": [],
                "platforms": {
                    'twitter': {'connected': False},
                    'linkedin': {'connected': False},
                    'instagram': {'connected': False},
                    'facebook': {'connected': False}
                }
            })

        user = db.get_user_by_session(session_id)
        if not user:
            return JSONResponse(content={
                "connected_platforms": [],
                "platforms": {
                    'twitter': {'connected': False},
                    'linkedin': {'connected': False},
                    'instagram': {'connected': False},
                    'facebook': {'connected': False}
                }
            })

        # Get all platform tokens for user
        platforms = db.get_user_platforms(user['id'])

        # Build response
        connected_platforms = []
        platform_status = {}

        for platform_name in ['twitter', 'linkedin', 'instagram', 'facebook']:
            # Find token for this platform
            platform_token = next((p for p in platforms if p['platform'] == platform_name), None)

            if platform_token:
                connected_platforms.append({
                    'id': platform_name,
                    'name': platform_name.capitalize(),
                    'username': platform_token.get('platform_username'),
                    'user_id': platform_token.get('platform_user_id'),
                    'connected_at': platform_token.get('created_at')
                })

                platform_status[platform_name] = {
                    'connected': True,
                    'username': platform_token.get('platform_username'),
                    'expires_at': platform_token.get('expires_at')
                }
            else:
                platform_status[platform_name] = {
                    'connected': False
                }

        return JSONResponse(content={
            "connected_platforms": connected_platforms,
            "platforms": platform_status
        })

    except Exception as e:
        logger.error(f"Error getting auth status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{platform}/disconnect")
async def platform_disconnect(platform: str, request: Request):
    """
    Disconnect a platform

    Args:
        platform: Platform name

    Returns:
        Success message
    """
    if platform not in oauth_handlers:
        raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")

    try:
        # Get user from session
        session_id = request.cookies.get('session_id')
        if not session_id:
            raise HTTPException(status_code=401, detail="Not authenticated")

        user = db.get_user_by_session(session_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Get platform token
        platform_token = db.get_platform_token(user['id'], platform)
        if not platform_token:
            raise HTTPException(status_code=404, detail=f"{platform} not connected")

        # Revoke token on platform
        handler = oauth_handlers[platform]
        try:
            await handler.revoke_token(platform_token['access_token'])
        except Exception as e:
            logger.warning(f"Failed to revoke {platform} token: {str(e)}")
            # Continue anyway to delete from database

        # Delete token from database
        db.delete_platform_token(user['id'], platform)

        return JSONResponse(content={
            "success": True,
            "message": f"Successfully disconnected {platform}"
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disconnecting {platform}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{platform}/token")
async def get_platform_token(platform: str, request: Request):
    """
    Get platform token for authenticated user (for internal use)

    Args:
        platform: Platform name

    Returns:
        Token data
    """
    if platform not in oauth_handlers:
        raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")

    try:
        # Get user from session
        session_id = request.cookies.get('session_id')
        if not session_id:
            raise HTTPException(status_code=401, detail="Not authenticated")

        user = db.get_user_by_session(session_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Get platform token
        platform_token = db.get_platform_token(user['id'], platform)
        if not platform_token:
            raise HTTPException(status_code=404, detail=f"{platform} not connected")

        # Check if token is expired and refresh if needed
        from datetime import datetime
        if platform_token.get('expires_at'):
            expires_at = datetime.fromisoformat(platform_token['expires_at'])
            if datetime.now() >= expires_at:
                # Token expired, try to refresh
                handler = oauth_handlers[platform]
                if platform_token.get('refresh_token'):
                    try:
                        new_token_data = await handler.refresh_access_token(platform_token['refresh_token'])

                        # Update token in database
                        db.save_platform_token(
                            user_id=user['id'],
                            platform=platform,
                            access_token=new_token_data['access_token'],
                            refresh_token=new_token_data.get('refresh_token') or platform_token['refresh_token'],
                            expires_in=new_token_data.get('expires_in'),
                            platform_user_id=platform_token['platform_user_id'],
                            platform_username=platform_token['platform_username']
                        )

                        # Get updated token
                        platform_token = db.get_platform_token(user['id'], platform)
                    except Exception as e:
                        logger.error(f"Failed to refresh {platform} token: {str(e)}")
                        raise HTTPException(status_code=401, detail="Token expired and refresh failed")
                else:
                    raise HTTPException(status_code=401, detail="Token expired, please reconnect")

        return JSONResponse(content={
            "platform": platform,
            "access_token": platform_token['access_token'],
            "platform_user_id": platform_token['platform_user_id'],
            "platform_username": platform_token['platform_username'],
            "platform_user_data": platform_token.get('platform_user_data')
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting {platform} token: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
