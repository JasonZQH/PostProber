from dotenv import load_dotenv
from pathlib import Path

# Load environment variables FIRST before any other imports
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import content  # AI content endpoints
from api.endpoints import health as health_monitoring  # AI health monitoring
from api.endpoints import analytics  # AI analytics & trending
from jobs.health_scheduler import start_health_monitoring, stop_health_monitoring
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="PostProber API",
    description="AI Agent powered Social Media Management & Analytics Platform",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - Only AI features (no auth/database)
app.include_router(content.router, tags=["AI content"])  # AI content optimization & hashtags
app.include_router(health_monitoring.router, tags=["AI health monitoring"])  # AI health monitoring & alerts
app.include_router(analytics.router, tags=["AI analytics & trending"])  # AI analytics & trending analysis


# Startup event - Start health monitoring
@app.on_event("startup")
async def startup_event():
    """
    Application startup event
    - Initialize health monitoring scheduler
    - Start background jobs
    """
    print("🚀 PostProber AI API Starting...")
    print("✅ Phase 1: Content Optimization & Hashtags: Ready")
    print("✅ Phase 2: Health Monitoring: Initializing...")

    # Start health monitoring
    await start_health_monitoring()

    print("✅ Phase 2: Health Monitoring: Ready")
    print("✅ Phase 3: Analytics & Trending: Ready")
    print("")
    print("📝 API Docs: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws/health")
    print("")
    print("🎉 All systems operational!")


# Shutdown event - Stop health monitoring
@app.on_event("shutdown")
def shutdown_event():
    """
    Application shutdown event
    - Stop health monitoring scheduler
    - Cleanup resources
    """
    print("⏹️ PostProber AI API Shutting down...")
    stop_health_monitoring()
    print("✅ Shutdown complete")


@app.get("/")
async def root():
    return {
        "name": "PostProber API",
        "version": "3.0.0",
        "description": "AI Agent powered Social Media Management & Analytics Platform",
        "status": "All Phases Complete",
        "features": {
            "phase1": [
                "AI Content Optimization",
                "Strategic Hashtag Generation",
                "Platform-specific Recommendations"
            ],
            "phase2": [
                "Real-time Health Monitoring",
                "Proactive Alerting System",
                "WebSocket Live Notifications",
                "Background Job Scheduling"
            ],
            "phase3": [
                "Trending Content Analysis",
                "Analytics Insights & Benchmarking",
                "Content Ideas Generation",
                "Best Time to Post Recommendations"
            ]
        },
        "endpoints": {
            "docs": "/docs",
            "websocket": "/ws/health",
            "content": "/api/optimize-with-hashtags",
            "health": "/api/health/status",
            "analytics": "/api/analytics/dashboard/{platform}",
            "trending": "/api/trending/analyze"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)