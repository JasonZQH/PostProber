# PostProber AI Backend

AI-powered backend service for PostProber featuring content optimization, hashtag generation, and real-time health monitoring.

## Features

### ✅ Phase 1 Complete
- **Content Optimization** - AI-powered post optimization for maximum engagement
- **Hashtag Generation** - Strategic hashtag mix generation
- **Platform Support** - Twitter, LinkedIn, Instagram, Facebook
- **Combined API** - Optimize content AND generate hashtags in one call

### ✅ Phase 2 Complete
- **Health Monitoring** - Real-time platform health checks with AI anomaly detection
- **WebSocket Alerts** - Live notifications for platform issues
- **Background Scheduler** - Automated health checks every 5 minutes
- **Proactive Alerting** - Critical/warning/info severity classification
- **Alert Deduplication** - Smart alert management with cooldown periods

### 🚧 Coming Soon (Phase 3)
- Trending Content Analysis
- Analytics Insights
- Best Time to Post (reimagined)

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

The `.env` file is already configured in the project root. Make sure it contains:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Run the Backend

```bash
# Make sure you're in the backend directory
cd src/backend

# Run with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs (Swagger UI)
- **ReDoc:** http://localhost:8000/redoc
- **WebSocket:** ws://localhost:8000/ws/health

## API Endpoints

### Phase 1: Content Optimization

#### Content Optimization

**POST** `/api/optimize-content`

Optimize social media content for maximum engagement.

**Request:**
```json
{
  "content": "Check out our new AI tool",
  "platform": "twitter"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "optimized_content": "Just launched our AI-powered social media tool! 🚀 Transform your content strategy today.",
    "score": 92,
    "improvements": [
      "Added stronger hook",
      "Improved call-to-action",
      "Optimized for Twitter"
    ],
    "original_length": 28,
    "optimized_length": 95,
    "platform": "twitter"
  },
  "processing_time": 3.45
}
```

#### Hashtag Generation

**POST** `/api/generate-hashtags`

Generate strategic hashtag mix for content.

**Request:**
```json
{
  "content": "Just launched our AI-powered social media tool!",
  "platform": "twitter"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "hashtags": [
      {"tag": "#AI", "category": "trending", "reach": "high"},
      {"tag": "#SocialMedia", "category": "trending", "reach": "high"},
      {"tag": "#MarketingTips", "category": "community", "reach": "medium"},
      {"tag": "#ContentStrategy", "category": "community", "reach": "medium"},
      {"tag": "#PostProber", "category": "branded", "reach": "targeted"}
    ],
    "strategy": "Balanced mix of high-reach trending hashtags and engaged community tags",
    "platform": "twitter",
    "count": 5
  },
  "processing_time": 2.1
}
```

#### Combined Optimization

**POST** `/api/optimize-with-hashtags`

Optimize content AND generate hashtags in one call (more efficient).

**Request:**
```json
{
  "content": "Check out our new AI tool",
  "platform": "twitter"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "optimization": {
      "optimized_content": "...",
      "score": 92,
      "improvements": [...]
    },
    "hashtags": {
      "hashtags": [...],
      "strategy": "...",
      "count": 5
    }
  },
  "processing_time": 4.8
}
```

### Phase 2: Health Monitoring

#### Get Health Status

**GET** `/api/health/status`

Get current health status of all platforms.

**Response:**
```json
{
  "success": true,
  "platforms": [
    {
      "platform": "twitter",
      "status": "healthy",
      "response_time": 252.5,
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
    }
  ],
  "timestamp": "2025-10-13T10:30:00"
}
```

#### Get Platform Health

**GET** `/api/health/platform/{platform}`

Get health status of a specific platform (twitter, linkedin, instagram, facebook).

#### Trigger Health Check

**POST** `/api/health/check`

Manually trigger a health check for all platforms.

#### Get Alert History

**GET** `/api/health/alerts`

Get recent health alert history.

**Response:**
```json
{
  "success": true,
  "alerts": [
    {
      "platform": "twitter",
      "severity": "warning",
      "message": "Twitter API is running slow",
      "recommended_action": "Posts may be delayed",
      "timestamp": "2025-10-13T10:25:00"
    }
  ],
  "count": 1
}
```

#### Get Scheduler Status

**GET** `/api/health/scheduler/status`

Get background scheduler status.

**Response:**
```json
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
```

#### WebSocket Connection

**WebSocket** `/ws/health`

Real-time health updates and alerts.

**Message Types:**
- `connection` - Connection established
- `health_update` - Periodic health status (every 5 minutes)
- `health_alert` - Real-time alert when issues detected
- `history` - Recent alert history
- `ping` - Keep-alive ping

## Testing the Tools

### Phase 1 Tools

#### Test Content Optimizer

```bash
cd src/backend
python -m tools.content_optimizer
```

#### Test Hashtag Generator

```bash
cd src/backend
python -m tools.hashtag_generator
```

### Phase 2 Tools

#### Test Health Monitor

```bash
cd src/backend
python -m tools.health_monitor
```

**Expected Output:**
```
🧪 Testing Health Monitor Tool
============================================================

🔍 Checking all platforms...

📊 Health Check Results:
============================================================

✅ TWITTER
  Status: healthy
  Response Time: 252ms
  Rate Limit: 450/1000

✅ LINKEDIN
  Status: healthy
  Response Time: 305ms
  Rate Limit: 80/100
...
```

#### Test WebSocket Connection

Use a WebSocket client or browser console:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/health')
ws.onmessage = (event) => {
  console.log('Received:', JSON.parse(event.data))
}
```

## Project Structure

```
src/backend/
├── main.py                          # FastAPI application
├── requirements.txt                 # Python dependencies
├── api/
│   └── endpoints/
│       ├── content.py               # Content & hashtag endpoints (Phase 1)
│       └── health.py                # Health monitoring endpoints (Phase 2)
├── tools/
│   ├── content_optimizer.py         # Content optimization tool (Phase 1)
│   ├── hashtag_generator.py         # Hashtag generation tool (Phase 1)
│   └── health_monitor.py            # Health monitoring tool (Phase 2)
├── jobs/
│   └── health_scheduler.py          # Background health checks (Phase 2)
└── services/
    └── websocket_manager.py         # WebSocket connection manager (Phase 2)
```

## Development

### Run with Auto-reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### View API Documentation

Open http://localhost:8000/docs in your browser to see the interactive API documentation.

### Debug Mode

Add `--log-level debug` for detailed logging:

```bash
uvicorn main:app --reload --log-level debug
```

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running from the `src/backend` directory:

```bash
cd src/backend
python -m tools.content_optimizer  # Not: python tools/content_optimizer.py
```

### OpenAI API Errors

- Verify your `OPENAI_API_KEY` is set correctly in `.env`
- Check you have API credits available
- Ensure the key has the necessary permissions

### CORS Issues

The backend is configured to allow requests from:
- http://localhost:5173 (React dev server)
- http://localhost:3000
- http://localhost:3001

If you're running the frontend on a different port, update the CORS settings in `main.py`.

## Performance

### Expected Response Times

**Phase 1 (Content Optimization):**
- Content Optimization: 2-5 seconds
- Hashtag Generation: 1-3 seconds
- Combined API: 3-8 seconds

**Phase 2 (Health Monitoring):**
- Health Check (single platform): 250-400ms
- Health Check (all platforms): 400-500ms (parallel execution)
- WebSocket connection: <100ms
- Alert broadcast: <50ms

### Token Usage

**Phase 1:**
- Content Optimization: ~700 tokens ($0.0011)
- Hashtag Generation: ~400 tokens ($0.0006)
- Combined: ~1100 tokens ($0.0017)

**Phase 2:**
- Health Monitor AI Analysis: ~400 tokens per platform ($0.0006)
- Full health check (4 platforms): ~1600 tokens ($0.0024)
- Background job runs every 5 minutes: ~$5/month

### Cost Estimates

**Monthly costs (assuming 1000 users):**
- Content Optimization: ~$17/month (10 optimizations per user)
- Health Monitoring: ~$5/month (automated background checks)
- **Total: ~$22/month** or **$0.022/user/month**

## Documentation

### Complete Guides:
- 📘 **Quick Test Guide**: `/docs/QUICK_TEST_GUIDE.md` - Get started in 5 minutes
- 📙 **Phase 1 Summary**: `/docs/PHASE1_COMPLETED_SUMMARY.md` - Content optimization
- 📕 **Phase 2 Summary**: `/docs/PHASE2_HEALTH_MONITORING_COMPLETE.md` - Health monitoring
- 📗 **Architecture**: `/docs/AI_AGENT_SYSTEM_ARCHITECTURE.md` - Complete design
- 📓 **Implementation**: `/docs/IMPLEMENTATION_CHECKLIST.md` - Step-by-step guide
- 📖 **Quick Reference**: `/docs/QUICK_REFERENCE_ARCHITECTURE.md` - Visual overview

## Next Steps

**Phase 3 features coming soon:**
- 📊 Trending Content Analysis - What's working NOW
- 📈 Analytics Insights - Performance benchmarking
- 🔮 Best Time to Post - Reimagined with public data

See `/docs/AI_AGENT_SYSTEM_ARCHITECTURE.md` for complete roadmap.

## Support

For issues or questions:
1. **Quick Start**: `/docs/QUICK_TEST_GUIDE.md`
2. **API Docs**: http://localhost:8000/docs
3. **Architecture**: `/docs/AI_AGENT_SYSTEM_ARCHITECTURE.md`
4. **Troubleshooting**: Check Phase 1/2 summary docs

---

**Status:** ✅ Phase 1 & 2 Complete!
**Features:** Content Optimization, Hashtag Generation, Health Monitoring, Real-time Alerting
**Next:** Phase 3 - Trending Analysis & Analytics Insights
**Version:** 2.0.0
