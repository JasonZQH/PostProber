"""
Analytics & Trending API Endpoints

Provides trending content analysis and analytics insights.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import time

from tools.trending_analyzer import TrendingAnalyzerTool
from tools.analytics_insights import AnalyticsInsightsTool

router = APIRouter()

# Initialize tools
trending_analyzer = TrendingAnalyzerTool()
analytics_insights = AnalyticsInsightsTool()


# Request Models
class TrendingAnalysisRequest(BaseModel):
    platform: str
    category: Optional[str] = None


class ContentAnalysisRequest(BaseModel):
    content: str
    platform: str


class ContentIdeasRequest(BaseModel):
    platform: str
    category: str


class PerformanceComparisonRequest(BaseModel):
    platform: str
    user_posts: Optional[List[Dict]] = []


# Trending Endpoints

@router.post("/api/trending/analyze")
async def analyze_trending(request: TrendingAnalysisRequest) -> Dict:
    """
    Analyze trending content patterns for a platform

    Args:
        platform: Platform name (twitter, linkedin, instagram, facebook)
        category: Optional category filter

    Returns:
        {
            "success": true,
            "result": {
                "platform": str,
                "patterns": [...],
                "top_formats": [...],
                "top_topics": [...],
                "engagement_drivers": [...],
                "content_length": {...},
                "posting_advice": str
            },
            "processing_time": float
        }
    """
    valid_platforms = ["twitter", "linkedin", "instagram", "facebook"]

    if request.platform.lower() not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
        )

    try:
        start_time = time.time()

        result = await trending_analyzer.analyze_trending_patterns(
            platform=request.platform.lower(),
            category=request.category
        )

        processing_time = round(time.time() - start_time, 2)

        return {
            "success": True,
            "result": result,
            "processing_time": processing_time
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/trending/best-times/{platform}")
async def get_best_posting_times(platform: str) -> Dict:
    """
    Get optimal posting times for a platform

    Args:
        platform: Platform name

    Returns:
        {
            "success": true,
            "result": {
                "platform": str,
                "recommendations": [...],
                "timezone": str,
                "general_advice": str
            },
            "processing_time": float
        }
    """
    valid_platforms = ["twitter", "linkedin", "instagram", "facebook"]

    if platform.lower() not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
        )

    try:
        start_time = time.time()

        result = await trending_analyzer.get_best_posting_times(platform.lower())

        processing_time = round(time.time() - start_time, 2)

        return {
            "success": True,
            "result": result,
            "processing_time": processing_time
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Analytics Endpoints

@router.post("/api/analytics/analyze-content")
async def analyze_user_content(request: ContentAnalysisRequest) -> Dict:
    """
    Analyze user content against trending patterns

    Args:
        content: User's post content
        platform: Platform name

    Returns:
        {
            "success": true,
            "result": {
                "content_score": int,
                "strengths": [...],
                "weaknesses": [...],
                "gap_analysis": {...},
                "recommendations": [...],
                "benchmark_comparison": {...}
            },
            "processing_time": float
        }
    """
    valid_platforms = ["twitter", "linkedin", "instagram", "facebook"]

    if request.platform.lower() not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
        )

    try:
        start_time = time.time()

        # Get trending patterns for comparison
        trending_patterns = await trending_analyzer.analyze_trending_patterns(
            platform=request.platform.lower()
        )

        # Analyze user content
        result = await analytics_insights.analyze_user_content(
            user_content=request.content,
            platform=request.platform.lower(),
            trending_patterns=trending_patterns
        )

        processing_time = round(time.time() - start_time, 2)

        return {
            "success": True,
            "result": result,
            "processing_time": processing_time
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/analytics/content-ideas")
async def generate_content_ideas(request: ContentIdeasRequest) -> Dict:
    """
    Generate content ideas based on trending patterns

    Args:
        platform: Platform name
        category: Content category

    Returns:
        {
            "success": true,
            "result": {
                "platform": str,
                "category": str,
                "ideas": [...]
            },
            "processing_time": float
        }
    """
    valid_platforms = ["twitter", "linkedin", "instagram", "facebook"]

    if request.platform.lower() not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
        )

    try:
        start_time = time.time()

        # Get trending patterns
        trending_patterns = await trending_analyzer.analyze_trending_patterns(
            platform=request.platform.lower(),
            category=request.category.lower()
        )

        # Generate ideas
        result = await analytics_insights.generate_content_ideas(
            platform=request.platform.lower(),
            category=request.category.lower(),
            trending_patterns=trending_patterns
        )

        processing_time = round(time.time() - start_time, 2)

        return {
            "success": True,
            "result": result,
            "processing_time": processing_time
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/analytics/performance-comparison")
async def compare_performance(request: PerformanceComparisonRequest) -> Dict:
    """
    Compare user performance with trending benchmarks

    Args:
        platform: Platform name
        user_posts: Optional list of user's posts with engagement data

    Returns:
        {
            "success": true,
            "result": {
                "overall_score": int,
                "comparison": {...},
                "insights": [...],
                "action_plan": [...]
            },
            "processing_time": float
        }
    """
    valid_platforms = ["twitter", "linkedin", "instagram", "facebook"]

    if request.platform.lower() not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
        )

    try:
        start_time = time.time()

        # Get trending benchmarks
        trending_patterns = await trending_analyzer.analyze_trending_patterns(
            platform=request.platform.lower()
        )

        # Compare performance
        result = await analytics_insights.compare_performance(
            user_posts=request.user_posts,
            trending_benchmarks=trending_patterns
        )

        processing_time = round(time.time() - start_time, 2)

        return {
            "success": True,
            "result": result,
            "processing_time": processing_time
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Combined endpoint for dashboard
@router.get("/api/analytics/dashboard/{platform}")
async def get_analytics_dashboard(platform: str) -> Dict:
    """
    Get complete analytics dashboard data

    Args:
        platform: Platform name

    Returns:
        {
            "success": true,
            "result": {
                "trending": {...},
                "best_times": {...},
                "performance": {...}
            },
            "processing_time": float
        }
    """
    valid_platforms = ["twitter", "linkedin", "instagram", "facebook"]

    if platform.lower() not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
        )

    try:
        start_time = time.time()

        # Get all analytics data in parallel
        import asyncio

        trending_task = trending_analyzer.analyze_trending_patterns(platform.lower())
        times_task = trending_analyzer.get_best_posting_times(platform.lower())

        trending_result, times_result = await asyncio.gather(
            trending_task,
            times_task
        )

        # Get performance comparison (with empty user posts for now)
        performance_result = await analytics_insights.compare_performance(
            user_posts=[],
            trending_benchmarks=trending_result
        )

        processing_time = round(time.time() - start_time, 2)

        return {
            "success": True,
            "result": {
                "trending": trending_result,
                "best_times": times_result,
                "performance": performance_result
            },
            "processing_time": processing_time
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
