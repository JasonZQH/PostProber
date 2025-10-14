"""
Content API Endpoints

FastAPI endpoints for AI-powered content optimization and hashtag generation.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import time
import sys
import os

# Add parent directory to path to import tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from tools.content_optimizer import ContentOptimizerTool
from tools.hashtag_generator import HashtagGeneratorTool

# Create router
router = APIRouter(prefix="/api", tags=["content"])

# Initialize tools (singleton pattern)
content_optimizer = ContentOptimizerTool()
hashtag_generator = HashtagGeneratorTool()


# Request/Response Models
class OptimizeContentRequest(BaseModel):
    """Request model for content optimization"""
    content: str = Field(..., min_length=1, max_length=5000, description="Post content to optimize")
    platform: str = Field(..., description="Target platform: twitter, linkedin, instagram, or facebook")

    class Config:
        schema_extra = {
            "example": {
                "content": "Check out our new AI tool for social media management",
                "platform": "twitter"
            }
        }


class HashtagRequest(BaseModel):
    """Request model for hashtag generation"""
    content: str = Field(..., min_length=1, max_length=5000, description="Post content for hashtag generation")
    platform: str = Field(..., description="Target platform: twitter, linkedin, instagram, or facebook")

    class Config:
        schema_extra = {
            "example": {
                "content": "Just launched our AI-powered social media management tool!",
                "platform": "twitter"
            }
        }


class HashtagItem(BaseModel):
    """Individual hashtag with metadata"""
    tag: str
    category: str
    reach: str


class OptimizeContentResponse(BaseModel):
    """Response model for content optimization"""
    success: bool
    result: Dict
    processing_time: float


class HashtagResponse(BaseModel):
    """Response model for hashtag generation"""
    success: bool
    result: Dict
    processing_time: float


# Endpoints

@router.post(
    "/optimize-content",
    response_model=OptimizeContentResponse,
    summary="Optimize social media content",
    description="AI-powered content optimization that improves post quality for maximum engagement"
)
async def optimize_content(request: OptimizeContentRequest):
    """
    Optimize post content for specific platform

    - **content**: Original post content (1-5000 characters)
    - **platform**: Target platform (twitter, linkedin, instagram, facebook)

    Returns optimized content with quality score and improvements.
    """
    start_time = time.time()

    try:
        # Validate platform
        valid_platforms = ["twitter", "linkedin", "instagram", "facebook"]
        if request.platform.lower() not in valid_platforms:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
            )

        # Optimize content
        result = content_optimizer.optimize(
            content=request.content,
            platform=request.platform
        )

        # Check if optimization failed
        if "error" in result and result.get("score", 0) < 60:
            raise HTTPException(
                status_code=500,
                detail=f"Content optimization failed: {result['error']}"
            )

        processing_time = round(time.time() - start_time, 2)

        return {
            "success": True,
            "result": result,
            "processing_time": processing_time
        }

    except HTTPException:
        raise

    except Exception as e:
        processing_time = round(time.time() - start_time, 2)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/generate-hashtags",
    response_model=HashtagResponse,
    summary="Generate strategic hashtags",
    description="AI-powered hashtag generation that creates optimal mix for reach and engagement"
)
async def generate_hashtags(request: HashtagRequest):
    """
    Generate strategic hashtag mix for content

    - **content**: Post content to analyze (1-5000 characters)
    - **platform**: Target platform (twitter, linkedin, instagram, facebook)

    Returns hashtags with categories and reach estimates.
    """
    start_time = time.time()

    try:
        # Validate platform
        valid_platforms = ["twitter", "linkedin", "instagram", "facebook"]
        if request.platform.lower() not in valid_platforms:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
            )

        # Generate hashtags
        result = hashtag_generator.generate(
            content=request.content,
            platform=request.platform
        )

        processing_time = round(time.time() - start_time, 2)

        return {
            "success": True,
            "result": result,
            "processing_time": processing_time
        }

    except HTTPException:
        raise

    except Exception as e:
        processing_time = round(time.time() - start_time, 2)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/optimize-with-hashtags",
    summary="Optimize content AND generate hashtags",
    description="Combined endpoint that optimizes content and generates hashtags in parallel"
)
async def optimize_with_hashtags(request: OptimizeContentRequest):
    """
    Optimize content AND generate hashtags (combined for efficiency)

    This endpoint runs both optimization and hashtag generation,
    returning both results together.

    Useful when user wants to optimize content and get hashtags at once.
    """
    start_time = time.time()

    try:
        # Validate platform
        valid_platforms = ["twitter", "linkedin", "instagram", "facebook"]
        if request.platform.lower() not in valid_platforms:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
            )

        # Run both operations (could be parallelized with asyncio for better performance)
        optimization_result = content_optimizer.optimize(
            content=request.content,
            platform=request.platform
        )

        hashtag_result = hashtag_generator.generate(
            content=request.content,
            platform=request.platform
        )

        processing_time = round(time.time() - start_time, 2)

        return {
            "success": True,
            "result": {
                "optimization": optimization_result,
                "hashtags": hashtag_result
            },
            "processing_time": processing_time
        }

    except HTTPException:
        raise

    except Exception as e:
        processing_time = round(time.time() - start_time, 2)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# Health check endpoint
@router.get("/health", summary="API Health Check")
async def health_check():
    """
    Check if the AI API is healthy and ready to process requests
    """
    return {
        "status": "healthy",
        "service": "PostProber AI API",
        "features": [
            "content-optimization",
            "hashtag-generation"
        ]
    }
