# AI Agent System Architecture

**PostProber AI Agent System - Complete Technical Design**

This document provides the complete system architecture for PostProber's AI agent features, including tools design, backend services, communication flows, and frontend integration.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Backend Tools Architecture](#backend-tools-architecture)
3. [Communication Flows](#communication-flows)
4. [Real-time vs Batch Processing](#real-time-vs-batch-processing)
5. [Frontend Component Enhancements](#frontend-component-enhancements)
6. [Implementation Guide](#implementation-guide)

---

## System Overview

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
├─────────────────────────────────────────────────────────────────┤
│  Compose.jsx  │  Analytics.jsx  │  Health.jsx  │  Dashboard.jsx │
│  [AI Optimize]│  [Insights]     │  [Monitor]   │  [Alerts]      │
└────────┬──────────────┬─────────────────┬──────────────┬─────────┘
         │              │                 │              │
         │ REST API     │ REST API        │ WebSocket    │ REST API
         │              │                 │ (Real-time)  │
┌────────▼──────────────▼─────────────────▼──────────────▼─────────┐
│                      BACKEND (FastAPI)                            │
├───────────────────────────────────────────────────────────────────┤
│  API Endpoints  │  WebSocket Server  │  Background Jobs          │
│  /api/optimize  │  /ws/health-alerts │  Health Monitor (5min)    │
│  /api/hashtags  │                    │  Trending Sync (4hr)      │
│  /api/insights  │                    │                           │
└────────┬────────────────────┬─────────────────┬──────────────────┘
         │                    │                 │
         │                    │                 │
┌────────▼────────────────────▼─────────────────▼──────────────────┐
│                    AI AGENT TOOLS LAYER                           │
├───────────────────────────────────────────────────────────────────┤
│  ContentOptimizer │ HashtagGenerator │ HealthMonitor │ TrendAnalyzer │
│  (LangChain)      │ (LangChain)      │ (Multi-Agent) │ (Background)   │
└────────┬──────────────────┬──────────────────┬───────────┬────────┘
         │                  │                  │           │
         │                  │                  │           │
┌────────▼──────────────────▼──────────────────▼───────────▼────────┐
│                    EXTERNAL SERVICES                               │
├───────────────────────────────────────────────────────────────────┤
│  OpenAI API       │  Platform APIs (Twitter, LinkedIn, etc.)      │
│  (GPT-3.5/4)      │  (Health checks, Trending data, User stats)   │
└───────────────────────────────────────────────────────────────────┘
```

---

## Backend Tools Architecture

### Tool 1: Content Optimization Tool

**Purpose:** Optimize post content for maximum engagement

**Type:** Synchronous (Real-time)

**Implementation:**
```python
# File: src/backend/tools/content_optimizer.py

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import Dict
import json

class ContentOptimizerTool:
    """Tool for optimizing social media content"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=800
        )

    def optimize(self, content: str, platform: str) -> Dict:
        """
        Optimize content for specific platform

        Args:
            content: Original post content
            platform: Target platform (twitter, linkedin, etc.)

        Returns:
            {
                "optimized_content": str,
                "score": int (0-100),
                "improvements": List[str],
                "original_length": int,
                "optimized_length": int
            }
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a social media optimization expert.
            Analyze and improve content for maximum engagement.

            Return ONLY a valid JSON object with this exact structure:
            {{
                "optimized_content": "the improved content here",
                "score": 85,
                "improvements": [
                    "Added stronger hook",
                    "Improved call-to-action",
                    "Optimized for platform"
                ]
            }}
            """),
            ("human", """
            Platform: {platform}
            Original content: "{content}"

            Optimize this content by:
            1. Creating an irresistible hook (first line)
            2. Ensuring message clarity and focus
            3. Adding appropriate emotional appeal
            4. Including a compelling call-to-action
            5. Following {platform} best practices

            Character limits:
            - Twitter: 280 characters
            - LinkedIn: 3000 characters (but 150-200 is optimal)
            - Instagram: 2200 characters
            """)
        ])

        chain = prompt | self.llm | StrOutputParser()

        try:
            response = chain.invoke({
                "content": content,
                "platform": platform
            })

            # Parse JSON response
            result = json.loads(response)

            # Add metadata
            result["original_length"] = len(content)
            result["optimized_length"] = len(result["optimized_content"])
            result["platform"] = platform

            return result

        except Exception as e:
            return {
                "error": str(e),
                "optimized_content": content,
                "score": 50,
                "improvements": ["Unable to optimize at this time"]
            }
```

**API Endpoint:**
```python
# File: src/backend/api/endpoints/content.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tools.content_optimizer import ContentOptimizerTool

router = APIRouter()
optimizer = ContentOptimizerTool()

class OptimizeRequest(BaseModel):
    content: str
    platform: str

@router.post("/api/optimize-content")
async def optimize_content(request: OptimizeRequest):
    """
    Optimize post content for maximum engagement

    Request body:
    {
        "content": "Your post content here",
        "platform": "twitter"
    }

    Response:
    {
        "success": true,
        "result": {
            "optimized_content": "...",
            "score": 92,
            "improvements": [...],
            "original_length": 50,
            "optimized_length": 180
        },
        "processing_time": 2.3
    }
    """
    import time
    start_time = time.time()

    try:
        result = optimizer.optimize(
            content=request.content,
            platform=request.platform
        )

        processing_time = time.time() - start_time

        return {
            "success": True,
            "result": result,
            "processing_time": round(processing_time, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Frontend Integration:**
```javascript
// File: src/frontend/services/aiService.js

class AIService {
    async optimizeContent(content, platform) {
        try {
            const response = await fetch('/api/optimize-content', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content, platform })
            });

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Content optimization failed:', error);
            throw error;
        }
    }
}

export default new AIService();
```

**Compose.jsx Update:**
- Button click → Show loading spinner
- Call `aiService.optimizeContent()`
- Display result in AI Suggestions card
- Show score with progress bar
- List improvements as bullet points
- "Use This Version" button to replace content

---

### Tool 2: Hashtag Generator Tool

**Purpose:** Generate strategic hashtag mix for posts

**Type:** Synchronous (Real-time)

**Implementation:**
```python
# File: src/backend/tools/hashtag_generator.py

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict, List
import json

class HashtagGeneratorTool:
    """Tool for generating strategic hashtags"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.8,  # Higher for creativity
            max_tokens=500
        )

    def generate(self, content: str, platform: str) -> Dict:
        """
        Generate strategic hashtag mix

        Returns:
        {
            "hashtags": [
                {"tag": "#AI", "category": "trending", "reach": "high"},
                {"tag": "#TechTips", "category": "niche", "reach": "medium"},
                ...
            ],
            "strategy": "explanation of hashtag choices"
        }
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a social media hashtag strategist.
            Generate optimal hashtag mixes that balance reach and engagement.

            Return ONLY valid JSON:
            {{
                "hashtags": [
                    {{"tag": "#Example", "category": "trending", "reach": "high"}},
                    {{"tag": "#Niche", "category": "community", "reach": "medium"}}
                ],
                "strategy": "Brief explanation of why these hashtags work"
            }}
            """),
            ("human", """
            Platform: {platform}
            Content: "{content}"

            Generate a strategic hashtag mix:

            1. 2-3 trending/popular hashtags (broad reach)
            2. 3-4 niche/topic-specific hashtags (engaged community)
            3. 1-2 branded/unique hashtags (brand identity)

            Total: 6-9 hashtags

            For each hashtag:
            - Ensure it's relevant to the content
            - Categorize: "trending", "niche", or "branded"
            - Estimate reach: "high", "medium", or "targeted"
            """)
        ])

        chain = prompt | self.llm

        try:
            response = chain.invoke({
                "content": content,
                "platform": platform
            })

            result = json.loads(response.content)
            return result

        except Exception as e:
            # Fallback hashtags
            return {
                "hashtags": [
                    {"tag": "#SocialMedia", "category": "trending", "reach": "high"},
                    {"tag": "#ContentCreation", "category": "niche", "reach": "medium"}
                ],
                "strategy": "Generated fallback hashtags"
            }
```

**API Endpoint:**
```python
# File: src/backend/api/endpoints/content.py

@router.post("/api/generate-hashtags")
async def generate_hashtags(request: OptimizeRequest):
    """Generate strategic hashtags for content"""

    generator = HashtagGeneratorTool()

    try:
        result = generator.generate(
            content=request.content,
            platform=request.platform
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Frontend Integration:**
- Can be called together with content optimization (parallel)
- Display hashtags as clickable pills/buttons
- Click to insert into content
- Show category badge (trending/niche/branded)
- Show reach indicator (high/medium/targeted)

---

### Tool 3: Health Monitoring Tool ⭐ CORE FEATURE

**Purpose:** Monitor platform API health and send proactive alerts

**Type:** Asynchronous (Background job + WebSocket)

**Implementation:**
```python
# File: src/backend/tools/health_monitor.py

import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List
from langchain_openai import ChatOpenAI
import json

class HealthMonitorTool:
    """Background tool for monitoring platform health"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3  # Lower for analytical tasks
        )

        # Baseline health metrics (normal ranges)
        self.baselines = {
            "twitter": {"response_time": 250, "error_rate": 0.5},
            "linkedin": {"response_time": 300, "error_rate": 0.8},
            "instagram": {"response_time": 400, "error_rate": 1.0},
            "facebook": {"response_time": 350, "error_rate": 1.0}
        }

    async def check_platform_health(self, platform: str) -> Dict:
        """
        Check single platform health

        Returns:
        {
            "platform": "twitter",
            "status": "healthy" | "degraded" | "down",
            "response_time": 245,
            "error_rate": 0.3,
            "rate_limit_used": 450,
            "rate_limit_total": 1000,
            "last_check": "2025-01-15T10:30:00Z"
        }
        """

        start_time = datetime.now()

        try:
            # Test platform API endpoint
            async with aiohttp.ClientSession() as session:
                # Mock health check - replace with actual platform API
                async with session.get(
                    f"https://api.{platform}.com/health",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:

                    response_time = (datetime.now() - start_time).total_seconds() * 1000

                    health_data = {
                        "platform": platform,
                        "status": "healthy" if response.status == 200 else "degraded",
                        "response_time": round(response_time, 2),
                        "error_rate": 0 if response.status == 200 else 1.0,
                        "rate_limit_used": response.headers.get("X-Rate-Limit-Used", 0),
                        "rate_limit_total": response.headers.get("X-Rate-Limit-Total", 1000),
                        "last_check": datetime.now().isoformat()
                    }

                    return health_data

        except asyncio.TimeoutError:
            return {
                "platform": platform,
                "status": "down",
                "response_time": 5000,  # Timeout
                "error_rate": 100,
                "last_check": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "platform": platform,
                "status": "down",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }

    async def analyze_health(self, health_data: Dict) -> Dict:
        """
        AI analyzes health data and determines alert level

        Returns:
        {
            "should_alert": true,
            "severity": "critical" | "warning" | "info",
            "message": "Twitter API response time 3x slower than normal",
            "recommended_action": "Posts may be delayed. Please wait...",
            "issue_detected": true
        }
        """

        platform = health_data["platform"]
        baseline = self.baselines.get(platform, {})

        prompt = f"""
        Analyze {platform} API health and determine if users need to be alerted:

        Current Status:
        - Response time: {health_data.get('response_time', 0)}ms
        - Error rate: {health_data.get('error_rate', 0)}%
        - Status: {health_data.get('status', 'unknown')}
        - Rate limit: {health_data.get('rate_limit_used', 0)}/{health_data.get('rate_limit_total', 1000)}

        Normal Baseline:
        - Expected response time: {baseline.get('response_time', 300)}ms
        - Expected error rate: <{baseline.get('error_rate', 1)}%

        Determine:
        1. Is there an issue? (yes/no)
        2. Severity level:
           - "critical": Platform down, auth expired, complete failure
           - "warning": Slow responses (2-3x slower), elevated errors
           - "info": Minor delays, approaching rate limits
        3. User-friendly message (max 100 characters)
        4. Recommended action for the user
        5. Should we send an alert? (yes/no)

        Return ONLY valid JSON:
        {{
            "should_alert": true,
            "severity": "warning",
            "message": "LinkedIn API experiencing delays",
            "recommended_action": "Posts will succeed but may take longer",
            "issue_detected": true
        }}
        """

        try:
            response = await self.llm.ainvoke(prompt)
            analysis = json.loads(response.content)
            return analysis

        except Exception as e:
            # Fallback logic
            rt = health_data.get('response_time', 0)
            baseline_rt = baseline.get('response_time', 300)

            if rt > baseline_rt * 3:  # 3x slower
                return {
                    "should_alert": True,
                    "severity": "warning",
                    "message": f"{platform.title()} API is slow ({rt}ms)",
                    "recommended_action": "Posts may be delayed",
                    "issue_detected": True
                }

            return {"should_alert": False, "issue_detected": False}
```

**Background Job:**
```python
# File: src/backend/jobs/health_monitor_job.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tools.health_monitor import HealthMonitorTool
from services.websocket_manager import WebSocketManager
import asyncio

class HealthMonitorJob:
    """Background job that runs every 5 minutes"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.monitor = HealthMonitorTool()
        self.ws_manager = WebSocketManager()

    async def check_all_platforms(self):
        """Check all platforms simultaneously"""

        platforms = ["twitter", "linkedin", "instagram", "facebook"]

        # Check all platforms in parallel
        tasks = [
            self.monitor.check_platform_health(platform)
            for platform in platforms
        ]

        health_results = await asyncio.gather(*tasks)

        # Analyze each result and send alerts
        for health_data in health_results:
            analysis = await self.monitor.analyze_health(health_data)

            if analysis.get("should_alert"):
                # Send WebSocket alert to connected clients
                await self.ws_manager.broadcast_alert({
                    "platform": health_data["platform"],
                    "severity": analysis["severity"],
                    "message": analysis["message"],
                    "action": analysis["recommended_action"],
                    "timestamp": health_data["last_check"]
                })

        # Store health status for REST API queries
        await self.store_health_status(health_results)

    def start(self):
        """Start the background job"""

        # Run every 5 minutes
        self.scheduler.add_job(
            self.check_all_platforms,
            'interval',
            minutes=5,
            id='health_monitor'
        )

        # Run immediately on startup
        self.scheduler.add_job(
            self.check_all_platforms,
            'date',
            run_date=datetime.now()
        )

        self.scheduler.start()
        print("✅ Health monitoring job started (runs every 5 minutes)")
```

**WebSocket Server:**
```python
# File: src/backend/services/websocket_manager.py

from fastapi import WebSocket
from typing import List
import json

class WebSocketManager:
    """Manages WebSocket connections for real-time alerts"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ WebSocket connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"❌ WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast_alert(self, alert: dict):
        """Send alert to all connected clients"""

        message = json.dumps({
            "type": "health_alert",
            "data": alert
        })

        # Send to all connected clients
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending to client: {e}")

# WebSocket endpoint
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
ws_manager = WebSocketManager()

@app.websocket("/ws/health-alerts")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back for heartbeat
            await websocket.send_text(f"pong: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
```

**REST API for Health Status:**
```python
# File: src/backend/api/endpoints/health.py

@router.get("/api/health-status")
async def get_health_status():
    """
    Get current health status of all platforms

    Response:
    {
        "platforms": [
            {
                "platform": "twitter",
                "status": "healthy",
                "response_time": 245,
                "last_check": "2025-01-15T10:30:00Z"
            },
            ...
        ],
        "overall_status": "healthy",
        "last_updated": "2025-01-15T10:30:00Z"
    }
    """

    # Fetch from cache/database
    health_data = await get_cached_health_status()

    return {
        "platforms": health_data,
        "overall_status": determine_overall_status(health_data),
        "last_updated": datetime.now().isoformat()
    }
```

**Frontend Integration:**

1. **WebSocket Connection (Header.jsx):**
```javascript
// src/frontend/services/healthWebSocket.js

class HealthWebSocket {
    constructor() {
        this.ws = null;
        this.listeners = [];
    }

    connect() {
        this.ws = new WebSocket('ws://localhost:8000/ws/health-alerts');

        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);

            if (message.type === 'health_alert') {
                // Notify all listeners
                this.listeners.forEach(callback => callback(message.data));
            }
        };

        this.ws.onclose = () => {
            // Reconnect after 5 seconds
            setTimeout(() => this.connect(), 5000);
        };
    }

    subscribe(callback) {
        this.listeners.push(callback);
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

export default new HealthWebSocket();
```

2. **Header Notification Bell:**
```javascript
// Add to Header.jsx

import { useState, useEffect } from 'react';
import healthWebSocket from '../services/healthWebSocket';

function Header() {
    const [alerts, setAlerts] = useState([]);
    const [unreadCount, setUnreadCount] = useState(0);

    useEffect(() => {
        // Connect to WebSocket
        healthWebSocket.connect();

        // Subscribe to alerts
        healthWebSocket.subscribe((alert) => {
            setAlerts(prev => [alert, ...prev]);
            setUnreadCount(prev => prev + 1);

            // Show browser notification if permission granted
            if (Notification.permission === 'granted') {
                new Notification(`${alert.platform} Alert`, {
                    body: alert.message,
                    icon: '/favicon.ico'
                });
            }
        });

        return () => healthWebSocket.disconnect();
    }, []);

    return (
        <header>
            {/* ... existing header content ... */}

            {/* Notification Bell */}
            <div className="notification-bell" onClick={openAlerts}>
                <span className="icon">🔔</span>
                {unreadCount > 0 && (
                    <span className="badge">{unreadCount}</span>
                )}
            </div>
        </header>
    );
}
```

---

### Tool 4: Trending Content Analysis Tool

**Purpose:** Analyze trending content to provide benchmarks

**Type:** Asynchronous (Background job, cached results)

**Implementation:**
```python
# File: src/backend/tools/trending_analyzer.py

from langchain_openai import ChatOpenAI
from typing import Dict, List
import json
import asyncio

class TrendingAnalyzerTool:
    """Analyzes trending content from platforms"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.5
        )

    async def fetch_trending_posts(self, platform: str) -> List[Dict]:
        """
        Fetch trending posts from platform public API

        Returns: List of top 50 posts with metrics
        """

        # Mock implementation - replace with actual platform APIs
        # Twitter: Use Twitter API v2 - GET /2/tweets/search/recent?query=trending
        # LinkedIn: Use LinkedIn API - GET /ugcPosts with sort=popular

        mock_posts = [
            {
                "content": "Check out this amazing AI tool!",
                "engagement": 1250,
                "likes": 850,
                "comments": 200,
                "shares": 200,
                "format": "text+image",
                "length": 35
            },
            # ... more posts
        ]

        return mock_posts

    async def analyze_patterns(self, posts: List[Dict], platform: str) -> Dict:
        """
        AI analyzes trending posts to identify patterns

        Returns:
        {
            "insights": [
                "Posts with video get 3x more engagement",
                "Optimal length: 150-200 characters",
                "Questions in hooks get 2x replies"
            ],
            "format_distribution": {
                "video": 45,
                "image": 30,
                "text": 15,
                "carousel": 10
            },
            "avg_engagement_rate": 6.8,
            "optimal_post_length": 180,
            "top_topics": ["AI", "Productivity", "Marketing"]
        }
        """

        # Prepare data for AI
        posts_summary = "\n".join([
            f"- Format: {p['format']}, Length: {p['length']}, Engagement: {p['engagement']}"
            for p in posts[:20]  # Sample top 20
        ])

        prompt = f"""
        Analyze these top-performing {platform} posts:

        {posts_summary}

        Identify patterns:
        1. Which content formats perform best? (video/image/text/carousel)
        2. What's the optimal post length?
        3. What hook patterns work? (questions, statements, numbers)
        4. What topics are trending?
        5. Common engagement drivers

        Return ONLY valid JSON:
        {{
            "insights": [
                "Key finding 1",
                "Key finding 2",
                "Key finding 3"
            ],
            "format_distribution": {{"video": 45, "image": 30}},
            "avg_engagement_rate": 6.8,
            "optimal_post_length": 180,
            "top_topics": ["topic1", "topic2"]
        }}
        """

        response = await self.llm.ainvoke(prompt)
        analysis = json.loads(response.content)

        return analysis
```

**Background Job:**
```python
# File: src/backend/jobs/trending_sync_job.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tools.trending_analyzer import TrendingAnalyzerTool
import asyncio

class TrendingSyncJob:
    """Syncs trending data every 4 hours"""

    def __init__(self, redis_client):
        self.scheduler = AsyncIOScheduler()
        self.analyzer = TrendingAnalyzerTool()
        self.redis = redis_client  # Redis for caching

    async def sync_trending_data(self):
        """Fetch and analyze trending data for all platforms"""

        platforms = ["twitter", "linkedin", "instagram"]

        for platform in platforms:
            try:
                # Fetch trending posts
                posts = await self.analyzer.fetch_trending_posts(platform)

                # Analyze patterns
                analysis = await self.analyzer.analyze_patterns(posts, platform)

                # Cache results (4-hour TTL)
                await self.redis.setex(
                    f"trending:{platform}",
                    14400,  # 4 hours in seconds
                    json.dumps(analysis)
                )

                print(f"✅ Trending data synced for {platform}")

            except Exception as e:
                print(f"❌ Error syncing {platform}: {e}")

    def start(self):
        """Start background job"""

        # Run every 4 hours
        self.scheduler.add_job(
            self.sync_trending_data,
            'interval',
            hours=4,
            id='trending_sync'
        )

        # Run immediately on startup
        self.scheduler.add_job(
            self.sync_trending_data,
            'date'
        )

        self.scheduler.start()
        print("✅ Trending sync job started (runs every 4 hours)")
```

**API Endpoint:**
```python
# File: src/backend/api/endpoints/trending.py

@router.get("/api/trending-insights")
async def get_trending_insights(platform: str):
    """
    Get cached trending insights for platform

    Response:
    {
        "platform": "twitter",
        "insights": [...],
        "format_distribution": {...},
        "avg_engagement_rate": 6.8,
        "last_updated": "2025-01-15T08:00:00Z"
    }
    """

    # Fetch from Redis cache
    cached_data = await redis.get(f"trending:{platform}")

    if not cached_data:
        return {"error": "No trending data available"}

    data = json.loads(cached_data)
    data["platform"] = platform
    data["last_updated"] = "..."  # From cache metadata

    return data
```

**Frontend Integration:**

```javascript
// src/frontend/services/trendingService.js

class TrendingService {
    async getTrendingInsights(platform) {
        const response = await fetch(`/api/trending-insights?platform=${platform}`);
        const data = await response.json();
        return data;
    }
}

// Analytics.jsx - Add trending insights card
useEffect(() => {
    const loadTrending = async () => {
        const insights = await trendingService.getTrendingInsights('twitter');
        setTrendingInsights(insights);
    };

    loadTrending();
}, []);
```

---

### Tool 5: Analytics Insights Generator Tool

**Purpose:** Compare user performance vs trending benchmarks

**Type:** Synchronous (On-demand)

**Implementation:**
```python
# File: src/backend/tools/analytics_insights.py

from langchain_openai import ChatOpenAI
from typing import Dict
import json

class AnalyticsInsightsToolTool:
    """Generates personalized analytics insights"""

    def __init__(self, redis_client):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.4)
        self.redis = redis_client

    async def generate_insights(
        self,
        user_stats: Dict,
        platform: str
    ) -> Dict:
        """
        Generate insights by comparing user vs trending

        Args:
            user_stats: {
                "post_count": 15,
                "avg_engagement_rate": 2.1,
                "avg_reach": 450,
                "top_format": "text"
            }

        Returns:
        {
            "assessment": "below_benchmark",
            "gap_analysis": {...},
            "recommendations": [...],
            "expected_impact": "25-35% improvement possible"
        }
        """

        # Get trending benchmarks from cache
        trending_data = await self.redis.get(f"trending:{platform}")
        trending = json.loads(trending_data) if trending_data else {}

        prompt = f"""
        Compare user's {platform} performance against trending benchmarks:

        User's Performance (last 30 days):
        - Posts: {user_stats.get('post_count', 0)}
        - Avg engagement rate: {user_stats.get('avg_engagement_rate', 0)}%
        - Avg reach: {user_stats.get('avg_reach', 0)}
        - Top format: {user_stats.get('top_format', 'unknown')}

        Trending Benchmarks:
        - Avg engagement rate: {trending.get('avg_engagement_rate', 6.8)}%
        - Top format: video (45% of top posts)
        - Optimal length: {trending.get('optimal_post_length', 180)} characters

        Provide:
        1. Assessment: "above_benchmark" | "at_benchmark" | "below_benchmark"
        2. Gap analysis: What's the difference?
        3. Top 3 specific, actionable recommendations
        4. Expected impact if recommendations followed

        Return ONLY valid JSON:
        {{
            "assessment": "below_benchmark",
            "gap_percentage": 68,
            "recommendations": [
                {{
                    "action": "Add more video content",
                    "reason": "Videos get 3x engagement",
                    "priority": "high"
                }},
                {{
                    "action": "Increase post frequency to 5/week",
                    "reason": "Consistency builds audience",
                    "priority": "medium"
                }},
                {{
                    "action": "Use 4-6 hashtags per post",
                    "reason": "Top posts average 5 hashtags",
                    "priority": "high"
                }}
            ],
            "expected_impact": "30-40% engagement improvement"
        }}
        """

        response = await self.llm.ainvoke(prompt)
        insights = json.loads(response.content)

        return insights
```

**API Endpoint:**
```python
@router.post("/api/analytics-insights")
async def generate_analytics_insights(request: AnalyticsRequest):
    """
    Generate personalized analytics insights

    Request:
    {
        "platform": "twitter",
        "account_id": "linked_account_123",
        "stats": {
            "post_count": 15,
            "avg_engagement_rate": 2.1
        }
    }
    """

    tool = AnalyticsInsightsToolTool(redis)

    insights = await tool.generate_insights(
        user_stats=request.stats,
        platform=request.platform
    )

    return {
        "success": True,
        "insights": insights
    }
```

---

## Communication Flows

### Flow 1: Content Optimization (Real-time)

```
User clicks "AI Optimize" button
    ↓
Frontend: Show loading spinner
    ↓
POST /api/optimize-content
    ↓
Backend: ContentOptimizerTool.optimize()
    ↓
LangChain → OpenAI API (2-5 seconds)
    ↓
Backend: Parse response, add metadata
    ↓
Return JSON response
    ↓
Frontend: Display optimized content + score
    ↓
User clicks "Use This Version"
    ↓
Replace textarea content
```

**Timing:** 2-5 seconds
**Type:** Synchronous REST API
**User Experience:** Button → Loading → Result

---

### Flow 2: Hashtag Generation (Real-time, can be parallel)

```
Option A: User clicks "Generate Hashtags" button
Option B: Auto-triggered after content optimization

    ↓
POST /api/generate-hashtags
    ↓
Backend: HashtagGeneratorTool.generate()
    ↓
LangChain → OpenAI API (1-3 seconds)
    ↓
Return hashtags array
    ↓
Frontend: Display as clickable pills
    ↓
User clicks hashtag → Insert into content
```

**Timing:** 1-3 seconds
**Type:** Synchronous REST API
**Can run in parallel with content optimization**

---

### Flow 3: Health Monitoring & Alerts (Real-time + Background)

```
BACKGROUND JOB (Every 5 minutes):
    ↓
Check all platforms simultaneously (asyncio.gather)
    ↓
For each platform:
    - Test API health
    - Measure response time
    - Check rate limits
    ↓
AI analyzes each result
    ↓
If issue detected:
    - Determine severity
    - Generate user message
    ↓
Broadcast via WebSocket to all connected clients
    ↓
Frontend: Receive alert
    ↓
Show notification bell badge
    ↓
Display browser notification (if permitted)
    ↓
User clicks bell → View all alerts


USER QUERY (On-demand):
    ↓
GET /api/health-status
    ↓
Return cached health data
    ↓
Display in Health.jsx page
```

**Timing:**
- Background check: Every 5 minutes
- Alert delivery: Instant via WebSocket
- REST query: <100ms (cached)

**Type:** WebSocket (alerts) + REST API (status page)

---

### Flow 4: Trending Insights (Batch + Cached)

```
BACKGROUND JOB (Every 4 hours):
    ↓
For each platform:
    - Fetch top 50 trending posts (public API)
    - AI analyzes patterns
    - Cache results in Redis (4-hour TTL)


USER QUERY (On-demand):
    ↓
GET /api/trending-insights?platform=twitter
    ↓
Return cached data from Redis
    ↓
Display in Analytics.jsx or Compose.jsx
```

**Timing:**
- Background sync: Every 4 hours
- User query: <100ms (cached)
- Cache TTL: 4 hours

**Type:** Background job + REST API (cached)

---

### Flow 5: Analytics Insights (On-demand)

```
User opens Analytics page
    ↓
Frontend: Fetch user's account stats via platform API
    ↓
POST /api/analytics-insights
    ↓
Backend:
    - Get user stats from platform API
    - Get trending benchmarks from cache
    - AI generates comparison insights
    ↓
LangChain → OpenAI API (3-8 seconds)
    ↓
Return personalized recommendations
    ↓
Display in Analytics.jsx
```

**Timing:** 3-8 seconds
**Type:** Synchronous REST API

---

## Real-time vs Batch Processing

### Real-time Features (Immediate Response Required)

| Feature | Trigger | Processing Time | Communication |
|---------|---------|-----------------|---------------|
| Content Optimization | Button click | 2-5 seconds | REST API |
| Hashtag Generation | Button click | 1-3 seconds | REST API |
| Health Alerts | Background detect | Instant | WebSocket |
| Analytics Insights | Page load | 3-8 seconds | REST API |

### Batch/Background Features (Can be pre-computed)

| Feature | Frequency | Processing Time | Communication |
|---------|-----------|-----------------|---------------|
| Health Monitoring | Every 5 minutes | 10-30 seconds | Background job → WebSocket |
| Trending Analysis | Every 4 hours | 5-15 minutes | Background job → Redis cache |

### Parallel Processing Opportunities

1. **Content Optimization + Hashtags:**
   - Can run simultaneously
   - Use Promise.all() in frontend
   - Reduces total wait time

2. **Health Monitoring:**
   - Check all platforms simultaneously
   - Use asyncio.gather() in backend
   - 4 platforms checked in parallel

3. **Initial Page Load:**
   - Fetch health status
   - Fetch trending insights
   - Fetch analytics data
   - All in parallel with Promise.all()

---

## Frontend Component Enhancements

### Enhancement 1: Header - Add Notification Bell

**Location:** `src/frontend/components/common/Header.jsx`

**New Component:**
```javascript
// Add notification bell to the right side of header
<div className="header-actions">
    {/* Existing search bar */}
    <div className="search-bar">...</div>

    {/* NEW: Notification Bell */}
    <div className="notification-container">
        <button
            className="notification-bell"
            onClick={() => setShowAlerts(!showAlerts)}
        >
            <span className="bell-icon">🔔</span>
            {unreadAlerts > 0 && (
                <span className="notification-badge">{unreadAlerts}</span>
            )}
        </button>

        {/* Alerts Dropdown */}
        {showAlerts && (
            <div className="alerts-dropdown">
                <div className="alerts-header">
                    <h3>System Alerts</h3>
                    <button onClick={markAllRead}>Mark all read</button>
                </div>

                <div className="alerts-list">
                    {alerts.map(alert => (
                        <div
                            key={alert.id}
                            className={`alert-item severity-${alert.severity}`}
                        >
                            <span className="alert-icon">
                                {getSeverityIcon(alert.severity)}
                            </span>
                            <div className="alert-content">
                                <div className="alert-platform">
                                    {alert.platform}
                                </div>
                                <div className="alert-message">
                                    {alert.message}
                                </div>
                                <div className="alert-action">
                                    {alert.action}
                                </div>
                                <div className="alert-time">
                                    {formatTime(alert.timestamp)}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="alerts-footer">
                    <button onClick={viewHealthPage}>
                        View Health Dashboard →
                    </button>
                </div>
            </div>
        )}
    </div>
</div>
```

**Styling:**
```css
/* Add to Header.css */
.notification-bell {
    position: relative;
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 24px;
    padding: 8px;
}

.notification-badge {
    position: absolute;
    top: 4px;
    right: 4px;
    background: var(--error-red);
    color: white;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

.alerts-dropdown {
    position: absolute;
    top: 60px;
    right: 20px;
    width: 400px;
    max-height: 600px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    z-index: 1000;
    overflow: hidden;
}

.alert-item {
    padding: 16px;
    border-bottom: 1px solid var(--gray-200);
    display: flex;
    gap: 12px;
}

.alert-item.severity-critical {
    background: #fee;
    border-left: 4px solid var(--error-red);
}

.alert-item.severity-warning {
    background: #ffeaa7;
    border-left: 4px solid var(--warning-orange);
}

.alert-item.severity-info {
    background: #e8f4f8;
    border-left: 4px solid var(--primary-blue);
}
```

---

### Enhancement 2: Compose Page - AI Panel Redesign

**Location:** `src/frontend/pages/Compose.jsx`

**Enhanced Layout:**

```
┌────────────────────────────────────────────────────────────┐
│  Main Content Area (2/3 width)                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Post Content Textarea                                │  │
│  │                                                        │  │
│  │  [Your content here...]                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  [Select Platforms: Twitter LinkedIn Instagram]            │
│                                                             │
│  [Post Now]  [Schedule]                                    │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  AI Assistant Panel (1/3 width - Right Sidebar)            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🤖 AI Assistant                                      │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  [🚀 Optimize Content] [#️⃣ Generate Hashtags]  │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  📊 Quality Score: 92/100                            │  │
│  │  [████████████████████░░] Excellent                 │  │
│  │                                                       │  │
│  │  ✅ Strong hook                                       │  │
│  │  ✅ Clear call-to-action                             │  │
│  │  ⚠️  Consider adding emoji                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ✨ Optimized Content                                │  │
│  │                                                       │  │
│  │  [Your optimized content will appear here...]        │  │
│  │                                                       │  │
│  │  [Use This Version]                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  #️⃣ Suggested Hashtags                               │  │
│  │                                                       │  │
│  │  [#AI] [#SocialMedia] [#MarketingTips]              │  │
│  │  [#ContentCreation] [#BusinessGrowth]               │  │
│  │                                                       │  │
│  │  Click to add to post                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  💡 Trending Insights                                │  │
│  │                                                       │  │
│  │  🔥 What's working on Twitter today:                 │  │
│  │  • Posts with video get 3x engagement                │  │
│  │  • Optimal length: 150-200 characters                │  │
│  │  • Questions in hooks get 2x replies                 │  │
│  │                                                       │  │
│  │  Last updated: 2 hours ago                           │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

**Key Changes:**
1. AI buttons at top of sidebar (always visible)
2. Quality score with visual progress bar
3. Optimized content in expandable card
4. Hashtags as clickable pills
5. NEW: Trending insights card at bottom

---

### Enhancement 3: Dashboard - Health Status Widget

**Location:** `src/frontend/pages/Dashboard.jsx`

**Enhanced "All Systems Online" Card:**

```javascript
<div className="card health-status-card">
    <div className="card-header">
        <h3>System Health</h3>
        <span className={`status-badge status-${overallStatus}`}>
            {getStatusIcon(overallStatus)} {overallStatus.toUpperCase()}
        </span>
    </div>

    <div className="card-content">
        {/* Platform Health Grid */}
        <div className="platform-health-grid">
            {['twitter', 'linkedin', 'instagram', 'facebook'].map(platform => (
                <div key={platform} className="platform-health-item">
                    <div className="platform-icon">
                        {getPlatformIcon(platform)}
                    </div>
                    <div className="platform-info">
                        <div className="platform-name">{platform}</div>
                        <div className={`platform-status status-${health[platform].status}`}>
                            {health[platform].status}
                        </div>
                        <div className="platform-metric">
                            {health[platform].response_time}ms
                        </div>
                    </div>
                    <div className={`status-indicator status-${health[platform].status}`}>
                        ●
                    </div>
                </div>
            ))}
        </div>

        {/* Recent Alerts */}
        {recentAlerts.length > 0 && (
            <div className="recent-alerts">
                <h4>Recent Alerts</h4>
                {recentAlerts.slice(0, 2).map(alert => (
                    <div className="alert-preview" key={alert.id}>
                        <span className="alert-severity">{alert.severity}</span>
                        <span className="alert-message">{alert.message}</span>
                    </div>
                ))}
            </div>
        )}

        <button
            className="btn-secondary"
            onClick={() => navigate('/health')}
        >
            View Full Health Dashboard →
        </button>
    </div>
</div>
```

---

### Enhancement 4: Analytics Page - Trending Comparison Section

**Location:** `src/frontend/pages/Analytics.jsx`

**New Section: "Your Performance vs. Trending"**

```javascript
<div className="card trending-comparison-card">
    <div className="card-header">
        <h3>📊 Your Performance vs. Trending</h3>
        <select
            value={selectedPlatform}
            onChange={(e) => setSelectedPlatform(e.target.value)}
        >
            <option value="twitter">Twitter</option>
            <option value="linkedin">LinkedIn</option>
            <option value="instagram">Instagram</option>
        </select>
    </div>

    <div className="card-content">
        {/* Comparison Bars */}
        <div className="comparison-metrics">
            <div className="metric-comparison">
                <div className="metric-label">Engagement Rate</div>
                <div className="comparison-bars">
                    <div className="bar-container">
                        <div className="bar bar-user" style={{width: `${userEngagement}%`}}>
                            {userEngagement}%
                        </div>
                        <span className="bar-label">You</span>
                    </div>
                    <div className="bar-container">
                        <div className="bar bar-trending" style={{width: `${trendingEngagement}%`}}>
                            {trendingEngagement}%
                        </div>
                        <span className="bar-label">Trending Average</span>
                    </div>
                </div>
                <div className="gap-indicator">
                    {gapPercentage}% gap
                </div>
            </div>

            {/* Similar for Reach, Frequency, etc. */}
        </div>

        {/* AI Recommendations */}
        <div className="ai-recommendations">
            <h4>💡 AI Recommendations</h4>
            {recommendations.map((rec, i) => (
                <div key={i} className={`recommendation priority-${rec.priority}`}>
                    <div className="rec-icon">
                        {getPriorityIcon(rec.priority)}
                    </div>
                    <div className="rec-content">
                        <div className="rec-action">{rec.action}</div>
                        <div className="rec-reason">{rec.reason}</div>
                    </div>
                </div>
            ))}
        </div>

        <div className="expected-impact">
            <span className="impact-label">Expected Impact:</span>
            <span className="impact-value">{expectedImpact}</span>
        </div>
    </div>
</div>
```

---

### Enhancement 5: Health Page - Real-time Dashboard

**Location:** `src/frontend/pages/Health.jsx`

**Enhanced with Real-time Updates:**

```javascript
// Add WebSocket connection
useEffect(() => {
    // Initial load
    loadHealthStatus();

    // WebSocket for real-time updates
    healthWebSocket.connect();
    healthWebSocket.subscribe(handleHealthAlert);

    // Refresh every 30 seconds as backup
    const interval = setInterval(loadHealthStatus, 30000);

    return () => {
        clearInterval(interval);
        healthWebSocket.disconnect();
    };
}, []);

// Add live status indicator
<div className="health-header">
    <h1>System Health Dashboard</h1>
    <div className="live-indicator">
        <span className="live-dot"></span>
        <span>Live Monitoring</span>
    </div>
    <div className="last-updated">
        Last updated: {formatTime(lastUpdate)}
    </div>
</div>
```

**Add Platform Timeline:**
```javascript
<div className="platform-timeline">
    <h3>Health History (Last 24 Hours)</h3>

    {/* Mini chart showing response time over time */}
    <div className="timeline-chart">
        {/* Use a simple line chart library or custom SVG */}
        <LineChart data={healthHistory} />
    </div>

    {/* Incident Log */}
    <div className="incident-log">
        <h4>Recent Incidents</h4>
        {incidents.map(incident => (
            <div className="incident-item" key={incident.id}>
                <span className="incident-time">
                    {formatTime(incident.timestamp)}
                </span>
                <span className="incident-platform">
                    {incident.platform}
                </span>
                <span className="incident-description">
                    {incident.description}
                </span>
                <span className={`incident-status ${incident.resolved ? 'resolved' : 'ongoing'}`}>
                    {incident.resolved ? '✅ Resolved' : '⚠️ Ongoing'}
                </span>
            </div>
        ))}
    </div>
</div>
```

---

## Implementation Guide

### Step 1: Backend Setup (Week 1)

```bash
# Install dependencies
pip install fastapi uvicorn langchain langchain-openai apscheduler aiohttp redis websockets

# Project structure
mkdir -p src/backend/{api/endpoints,tools,jobs,services}

# Create files
touch src/backend/tools/content_optimizer.py
touch src/backend/tools/hashtag_generator.py
touch src/backend/tools/health_monitor.py
touch src/backend/tools/trending_analyzer.py
touch src/backend/tools/analytics_insights.py

touch src/backend/api/endpoints/content.py
touch src/backend/api/endpoints/health.py
touch src/backend/api/endpoints/trending.py

touch src/backend/jobs/health_monitor_job.py
touch src/backend/jobs/trending_sync_job.py

touch src/backend/services/websocket_manager.py

touch src/backend/main.py
```

### Step 2: Implement Tools (Week 1-2)

1. **Content Optimizer** (Day 1-2)
   - Implement ContentOptimizerTool
   - Create API endpoint
   - Test with sample content

2. **Hashtag Generator** (Day 2-3)
   - Implement HashtagGeneratorTool
   - Create API endpoint
   - Test hashtag generation

3. **Health Monitor** (Day 4-7)
   - Implement HealthMonitorTool
   - Set up background job
   - Configure WebSocket server
   - Test alert flow

### Step 3: Frontend Integration (Week 2)

1. **Create Services** (Day 1)
   ```bash
   mkdir -p src/frontend/services
   touch src/frontend/services/aiService.js
   touch src/frontend/services/healthWebSocket.js
   touch src/frontend/services/trendingService.js
   ```

2. **Update Components** (Day 2-5)
   - Header.jsx - Add notification bell
   - Compose.jsx - Integrate AI features
   - Dashboard.jsx - Add health widget
   - Analytics.jsx - Add trending comparison
   - Health.jsx - Add real-time updates

### Step 4: Background Jobs (Week 3)

1. **Health Monitoring**
   - Start background job on server startup
   - Test concurrent platform checks
   - Verify WebSocket alerts

2. **Trending Sync**
   - Implement platform API integrations
   - Set up Redis caching
   - Test data freshness

### Step 5: Testing & Optimization (Week 3-4)

1. **Performance Testing**
   - Measure API response times
   - Test WebSocket reliability
   - Optimize LLM token usage

2. **Error Handling**
   - Add retry logic
   - Implement fallbacks
   - Test edge cases

3. **User Testing**
   - Beta test with real users
   - Gather feedback
   - Iterate on UX

---

## Summary

### Tools Designed: 5

1. ✅ **ContentOptimizerTool** - Real-time, REST API
2. ✅ **HashtagGeneratorTool** - Real-time, REST API
3. ✅ **HealthMonitorTool** - Background + WebSocket
4. ✅ **TrendingAnalyzerTool** - Background + Cached
5. ✅ **AnalyticsInsightsTool** - On-demand, REST API

### Communication Methods:

- **REST API**: Content Optimization, Hashtags, Analytics Insights
- **WebSocket**: Health Alerts (real-time push)
- **Background Jobs**: Health Monitoring (5min), Trending Sync (4hr)
- **Redis Cache**: Trending data, Health status

### Frontend Enhancements: 5

1. ✅ Header - Notification bell with WebSocket
2. ✅ Compose - AI assistant panel
3. ✅ Dashboard - Health status widget
4. ✅ Analytics - Trending comparison section
5. ✅ Health - Real-time monitoring dashboard

### Real-time Features:

- ✅ Content optimization (2-5s)
- ✅ Hashtag generation (1-3s)
- ✅ Health alerts (instant via WebSocket)
- ✅ Analytics insights (3-8s)

### Background Features:

- ✅ Health monitoring (every 5 minutes)
- ✅ Trending analysis (every 4 hours)

---

**Status:** ✅ Complete Architecture Design
**Next Step:** Begin Phase 1 Implementation
**Estimated Timeline:** 5 weeks total

