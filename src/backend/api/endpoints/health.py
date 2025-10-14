"""
Health Monitoring API Endpoints

Provides real-time platform health monitoring and alerting.
"""

from fastapi import APIRouter, WebSocket, HTTPException
from typing import Dict, List
from datetime import datetime

from jobs.health_scheduler import health_scheduler
from services.websocket_manager import manager as ws_manager, handle_websocket_connection
from tools.health_monitor import HealthMonitorTool

router = APIRouter()
health_monitor = HealthMonitorTool()


@router.get("/api/health/status")
async def get_health_status() -> Dict:
    """
    Get current health status of all platforms

    Returns:
        {
            "success": true,
            "platforms": [
                {
                    "platform": "twitter",
                    "status": "healthy" | "degraded" | "down",
                    "response_time": 250.5,
                    "error_rate": 0.0,
                    "rate_limit_used": 450,
                    "rate_limit_total": 1000,
                    "last_check": "2025-10-13T10:30:00",
                    "analysis": {
                        "should_alert": false,
                        "severity": "info",
                        "message": "Twitter is healthy",
                        "recommended_action": "No action needed"
                    }
                },
                ...
            ],
            "timestamp": "2025-10-13T10:30:00"
        }
    """
    try:
        # Get last scheduled check results if available
        results = health_scheduler.get_last_results()

        # If no scheduled results yet, perform a fresh check
        if not results:
            results = await health_monitor.check_all_platforms()

        return {
            "success": True,
            "platforms": results,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/health/platform/{platform}")
async def get_platform_health(platform: str) -> Dict:
    """
    Get health status of a specific platform

    Args:
        platform: Platform name (twitter, linkedin, instagram, facebook)

    Returns:
        {
            "success": true,
            "platform": "twitter",
            "status": "healthy",
            "response_time": 250.5,
            "error_rate": 0.0,
            "rate_limit_used": 450,
            "rate_limit_total": 1000,
            "last_check": "2025-10-13T10:30:00",
            "analysis": { ... }
        }
    """
    valid_platforms = ["twitter", "linkedin", "instagram", "facebook"]

    if platform.lower() not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
        )

    try:
        # Check specific platform
        health_data = await health_monitor.check_platform_health(platform.lower())
        analysis = await health_monitor.analyze_health(health_data)

        return {
            "success": True,
            **health_data,
            "analysis": analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/health/check")
async def trigger_health_check() -> Dict:
    """
    Manually trigger a health check for all platforms

    Returns:
        {
            "success": true,
            "message": "Health check completed",
            "platforms": [ ... ],
            "processing_time": 2.5
        }
    """
    try:
        import time
        start_time = time.time()

        # Run health check
        results = await health_monitor.check_all_platforms()

        # Broadcast to WebSocket clients
        await ws_manager.broadcast_health_update(results)

        processing_time = round(time.time() - start_time, 2)

        return {
            "success": True,
            "message": "Health check completed",
            "platforms": results,
            "processing_time": processing_time
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/health/alerts")
async def get_alert_history() -> Dict:
    """
    Get recent health alert history

    Returns:
        {
            "success": true,
            "alerts": [
                {
                    "platform": "twitter",
                    "severity": "warning",
                    "message": "Twitter API is running slow",
                    "recommended_action": "Posts may be delayed",
                    "timestamp": "2025-10-13T10:25:00"
                },
                ...
            ],
            "count": 5
        }
    """
    try:
        alerts = ws_manager.alert_history

        return {
            "success": True,
            "alerts": alerts,
            "count": len(alerts)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/health/scheduler/status")
async def get_scheduler_status() -> Dict:
    """
    Get background scheduler status

    Returns:
        {
            "success": true,
            "scheduler": {
                "running": true,
                "jobs": [
                    {
                        "id": "health_check",
                        "name": "Platform Health Check",
                        "next_run": "2025-10-13T10:35:00",
                        "trigger": "interval[0:05:00]"
                    }
                ]
            }
        }
    """
    try:
        status = health_scheduler.get_job_status()

        return {
            "success": True,
            "scheduler": status
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/health/websocket/stats")
async def get_websocket_stats() -> Dict:
    """
    Get WebSocket connection statistics

    Returns:
        {
            "success": true,
            "stats": {
                "active_connections": 3,
                "total_alerts": 12,
                "clients": [
                    {
                        "client_id": "client_1",
                        "connected_at": "2025-10-13T10:20:00",
                        "alerts_sent": 5
                    },
                    ...
                ]
            }
        }
    """
    try:
        stats = ws_manager.get_stats()

        return {
            "success": True,
            "stats": stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws/health")
async def websocket_health_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time health alerts

    Client receives:
    1. Connection confirmation
    2. Recent alert history
    3. Real-time health updates every 5 minutes
    4. Real-time alerts when issues detected
    5. Periodic pings to keep connection alive

    Message Types:
    - connection: Connection established
    - history: Recent alert history
    - health_update: Periodic health status
    - health_alert: Real-time alert
    - ping: Keep-alive ping
    """
    await handle_websocket_connection(websocket)


# Health check endpoint (simple ping)
@router.get("/api/ping")
async def ping() -> Dict:
    """
    Simple health check endpoint

    Returns:
        {"status": "ok", "timestamp": "2025-10-13T10:30:00"}
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }
