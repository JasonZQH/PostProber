# Quick Reference: AI Agent Architecture

**One-page visual overview of PostProber's AI Agent System**

---

## 🎯 5 AI Tools Overview

| # | Tool Name | Type | Trigger | Response Time | Communication |
|---|-----------|------|---------|---------------|---------------|
| 1 | **Content Optimizer** | Sync | Button click | 2-5s | REST API |
| 2 | **Hashtag Generator** | Sync | Button click | 1-3s | REST API |
| 3 | **Health Monitor** ⭐ | Async | Background (5min) | Instant | WebSocket |
| 4 | **Trending Analyzer** | Batch | Background (4hr) | Cached | REST API |
| 5 | **Analytics Insights** | Sync | Page load | 3-8s | REST API |

---

## 📊 Data Flow Diagrams

### Flow 1: Content Optimization (Real-time)
```
┌─────────────┐     POST     ┌──────────────┐     LangChain    ┌────────────┐
│   Compose   │─────────────>│  FastAPI     │────────────────>│  OpenAI    │
│   Page      │   /optimize  │  Endpoint    │   GPT-3.5-turbo │  API       │
│             │              │              │                  │            │
│  [Button]   │<─────────────│  {result}    │<────────────────│  {response}│
└─────────────┘   2-5 seconds└──────────────┘                  └────────────┘
```

### Flow 2: Health Monitoring (Background + WebSocket)
```
BACKGROUND JOB (Every 5 minutes)
┌─────────────────┐
│ APScheduler     │
│ Health Check    │
└────────┬────────┘
         │
         ├──> Check Twitter API ──┐
         ├──> Check LinkedIn API ─┤
         ├──> Check Instagram API ┤─> AI Analysis ─> Severity?
         └──> Check Facebook API ─┘                       │
                                                           │
                                      ┌────────────────────┴─────────────────┐
                                      │                                       │
                                   Yes│                                    No │
                                      ▼                                       ▼
                            ┌──────────────────┐                    ┌──────────────┐
                            │  WebSocket       │                    │  Store in    │
                            │  Broadcast Alert │                    │  Redis Cache │
                            └────────┬─────────┘                    └──────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
              ┌─────────┐      ┌─────────┐    ┌─────────┐
              │ Client 1│      │ Client 2│    │ Client N│
              │ Header  │      │ Header  │    │ Header  │
              │   🔔(1) │      │   🔔(1) │    │   🔔(1) │
              └─────────┘      └─────────┘    └─────────┘
```

### Flow 3: Trending Analysis (Background + Cache)
```
BACKGROUND JOB (Every 4 hours)
┌─────────────────┐
│ APScheduler     │
│ Trending Sync   │
└────────┬────────┘
         │
         ├──> Fetch Twitter Trending ──┐
         ├──> Fetch LinkedIn Popular ──┤
         └──> Fetch Instagram Explore ─┘
                         │
                         ▼
                  ┌─────────────┐
                  │ AI Analysis │
                  │ (Patterns)  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Redis Cache │
                  │ TTL: 4 hours│
                  └──────┬──────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
   ┌──────────┐    ┌──────────┐   ┌──────────┐
   │Analytics │    │ Compose  │   │Dashboard │
   │  Page    │    │  Tips    │   │ Widget   │
   └──────────┘    └──────────┘   └──────────┘
   GET /api/trending-insights (cached, <100ms)
```

---

## 🏗️ Backend Structure

```
src/backend/
├── main.py                          # FastAPI app entry point
├── api/
│   └── endpoints/
│       ├── content.py               # /api/optimize-content
│       │                            # /api/generate-hashtags
│       ├── health.py                # /api/health-status
│       │                            # /ws/health-alerts (WebSocket)
│       └── trending.py              # /api/trending-insights
├── tools/
│   ├── content_optimizer.py         # ContentOptimizerTool
│   ├── hashtag_generator.py         # HashtagGeneratorTool
│   ├── health_monitor.py            # HealthMonitorTool
│   ├── trending_analyzer.py         # TrendingAnalyzerTool
│   └── analytics_insights.py        # AnalyticsInsightsTool
├── jobs/
│   ├── health_monitor_job.py        # Background job (5min interval)
│   └── trending_sync_job.py         # Background job (4hr interval)
└── services/
    └── websocket_manager.py         # WebSocket connection manager
```

---

## 🎨 Frontend Structure

```
src/frontend/
├── services/
│   ├── aiService.js                 # Content optimization, hashtags
│   ├── healthWebSocket.js           # WebSocket for health alerts
│   └── trendingService.js           # Trending insights fetching
├── components/
│   └── common/
│       └── Header.jsx               # ✨ Add notification bell 🔔
└── pages/
    ├── Compose.jsx                  # ✨ Add AI assistant panel
    ├── Analytics.jsx                # ✨ Add trending comparison
    ├── Dashboard.jsx                # ✨ Add health status widget
    └── Health.jsx                   # ✨ Add real-time monitoring
```

---

## 🔄 Real-time vs Batch Processing

### Real-time (Immediate Response)
```
User Action → API Call → AI Processing → Response → UI Update
            └─ 1-8 seconds total ─────────────────────────┘

Examples:
✓ Content Optimization (2-5s)
✓ Hashtag Generation (1-3s)
✓ Analytics Insights (3-8s)
✓ Health Alerts (instant via WebSocket)
```

### Batch (Pre-computed)
```
Background Job → Fetch Data → AI Analysis → Cache in Redis
     │                                            │
     └─ Runs every X hours                       │
                                                  │
User Request → Fetch from Cache (< 100ms) <──────┘

Examples:
✓ Health Monitoring (every 5 minutes)
✓ Trending Analysis (every 4 hours)
```

---

## 🎯 Frontend Component Updates

### 1. Header.jsx - Notification Bell

**Add:**
```jsx
<div className="notification-bell">
    🔔 {unreadCount > 0 && <span className="badge">{unreadCount}</span>}
</div>

{showAlerts && (
    <div className="alerts-dropdown">
        {alerts.map(alert => (
            <AlertItem key={alert.id} alert={alert} />
        ))}
    </div>
)}
```

**Connect to WebSocket:**
```javascript
useEffect(() => {
    healthWebSocket.connect();
    healthWebSocket.subscribe(handleNewAlert);
    return () => healthWebSocket.disconnect();
}, []);
```

---

### 2. Compose.jsx - AI Assistant Panel

**Layout:**
```
┌────────────────────────────────────┐
│ Content Textarea                   │
└────────────────────────────────────┘

┌────────────────────────────────────┐  ┌────────────────────┐
│ Platform Selection                 │  │ AI ASSISTANT       │
│ [Twitter] [LinkedIn] [Instagram]   │  │                    │
└────────────────────────────────────┘  │ [🚀 Optimize]      │
                                        │ [#️⃣ Hashtags]      │
┌────────────────────────────────────┐  │                    │
│ [Post Now] [Schedule]              │  │ Quality: 92/100    │
└────────────────────────────────────┘  │ ██████████░        │
                                        │                    │
                                        │ Improvements:      │
                                        │ ✅ Strong hook     │
                                        │ ✅ Clear CTA       │
                                        │                    │
                                        │ Suggested Hashtags:│
                                        │ [#AI] [#Social]    │
                                        │                    │
                                        │ 💡 Trending Tips   │
                                        │ Videos get 3x...   │
                                        └────────────────────┘
```

**API Calls:**
```javascript
const handleOptimize = async () => {
    setLoading(true);
    const result = await aiService.optimizeContent(content, platform);
    setOptimized(result);
    setLoading(false);
};

const handleGenerateHashtags = async () => {
    const hashtags = await aiService.generateHashtags(content, platform);
    setHashtags(hashtags);
};
```

---

### 3. Dashboard.jsx - Health Status Widget

**Enhanced "All Systems Online" Card:**
```jsx
<div className="health-status-card">
    <h3>System Health</h3>
    <div className="status-badge">
        {overallStatus === 'healthy' ? '✅' : '⚠️'} {overallStatus}
    </div>

    <div className="platform-grid">
        {platforms.map(p => (
            <div className="platform-item">
                {p.icon} {p.name}
                <span className={`status-${p.status}`}>●</span>
                <span className="metric">{p.response_time}ms</span>
            </div>
        ))}
    </div>

    {recentAlerts.length > 0 && (
        <div className="recent-alerts">
            {recentAlerts.map(alert => (
                <div className="alert-preview">{alert.message}</div>
            ))}
        </div>
    )}

    <button onClick={() => navigate('/health')}>
        View Full Dashboard →
    </button>
</div>
```

---

### 4. Analytics.jsx - Trending Comparison

**New Section:**
```jsx
<div className="trending-comparison-card">
    <h3>📊 Your Performance vs. Trending</h3>

    <div className="comparison-bars">
        <div className="metric">
            <label>Engagement Rate</label>
            <div className="bar-user">You: 2.1%</div>
            <div className="bar-trending">Trending: 6.8%</div>
            <span className="gap">68% gap</span>
        </div>
    </div>

    <div className="recommendations">
        <h4>💡 AI Recommendations</h4>
        {recommendations.map(rec => (
            <div className={`rec priority-${rec.priority}`}>
                <span className="action">{rec.action}</span>
                <span className="reason">{rec.reason}</span>
            </div>
        ))}
    </div>

    <div className="expected-impact">
        Expected Impact: {impact}
    </div>
</div>
```

---

### 5. Health.jsx - Real-time Dashboard

**Add Live Monitoring:**
```jsx
<div className="health-header">
    <h1>System Health Dashboard</h1>
    <div className="live-indicator">
        <span className="live-dot">●</span> Live Monitoring
    </div>
    <div className="last-updated">
        Last updated: {formatTime(lastUpdate)}
    </div>
</div>

<div className="platform-details">
    {platforms.map(platform => (
        <div className="platform-card">
            <div className="platform-header">
                {platform.icon} {platform.name}
                <span className={`status-${platform.status}`}>
                    {platform.status}
                </span>
            </div>

            <div className="metrics">
                <Metric label="Response Time" value={`${platform.response_time}ms`} />
                <Metric label="Error Rate" value={`${platform.error_rate}%`} />
                <Metric label="Rate Limit" value={`${platform.rate_used}/${platform.rate_total}`} />
                <Metric label="Uptime" value={`${platform.uptime}%`} />
            </div>

            {platform.alerts.length > 0 && (
                <div className="platform-alerts">
                    {platform.alerts.map(alert => (
                        <AlertItem alert={alert} />
                    ))}
                </div>
            )}
        </div>
    ))}
</div>

<div className="health-history">
    <h3>Health History (Last 24 Hours)</h3>
    <LineChart data={healthHistory} />
</div>

<div className="incident-log">
    <h3>Recent Incidents</h3>
    {incidents.map(incident => (
        <IncidentItem incident={incident} />
    ))}
</div>
```

---

## 🚀 Quick Start Commands

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn langchain langchain-openai \
            apscheduler aiohttp redis websockets python-dotenv

# Set environment variables
echo "OPENAI_API_KEY=your-key-here" > .env
echo "REDIS_URL=redis://localhost:6379" >> .env

# Run backend
cd src/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Install dependencies
cd src/frontend
npm install

# Start development server
npm run dev
```

### Redis Setup
```bash
# Using Docker
docker run -d -p 6379:6379 redis:alpine

# Or install locally
brew install redis  # macOS
sudo apt-get install redis-server  # Ubuntu
```

---

## 📈 Monitoring & Metrics

### Key Metrics to Track

**Performance:**
- API response times (p50, p95, p99)
- WebSocket connection count
- Background job execution time
- Redis cache hit rate

**AI Usage:**
- Total API calls per day
- Token usage per request
- Average cost per user
- Success rate of AI operations

**Health:**
- Platform API uptime
- Alert frequency by severity
- Mean time to detect issues
- False positive rate

**User Engagement:**
- % of posts using AI optimization
- % of users who click hashtag suggestions
- Alert click-through rate
- Trending insights views

---

## 💰 Cost Breakdown

### OpenAI API (GPT-3.5-turbo)

**Per Request Estimates:**
- Content Optimization: 700 tokens → $0.0011
- Hashtag Generation: 400 tokens → $0.0006
- Health Analysis: 300 tokens → $0.0005
- Trending Analysis: 2000 tokens → $0.0030
- Analytics Insights: 800 tokens → $0.0013

**Monthly Cost (1000 users):**
- Content: 10,000 req × $0.0011 = $11
- Hashtags: 10,000 req × $0.0006 = $6
- Health: 34,560 req × $0.0005 = $17
- Trending: 540 req × $0.0030 = $2
- Analytics: 4,000 req × $0.0013 = $5

**Total AI Cost: ~$41/month**

### Infrastructure
- FastAPI Server: $50/month
- Redis: $15/month
- **Total: $65/month**

### Grand Total: ~$106/month for 1000 users
**Cost per user: $0.106/month** ✅ Very affordable!

---

## ⚠️ Critical Success Factors

### Must-Have Features
1. ✅ Content optimization works <5s
2. ✅ Health alerts delivered within 5 minutes
3. ✅ WebSocket stays connected reliably
4. ✅ No false-positive health alerts
5. ✅ Trending data refreshes every 4 hours

### Performance Targets
- API Response Time: <5s (95th percentile)
- WebSocket Uptime: >99.9%
- Background Jobs: 100% success rate
- Cache Hit Rate: >90%
- AI Accuracy: >85% helpful responses

### User Experience Goals
- AI features used in >60% of posts
- Health alerts acknowledged within 5 minutes
- User satisfaction: >4.5/5 stars
- Support tickets for AI: <5% of total

---

## 🎓 Learning Resources

### LangChain + LangGraph
- Official Docs: https://python.langchain.com/
- LangGraph Guide: https://langchain-ai.github.io/langgraph/
- Example Implementations: `src/shared/ai-examples/` (01-06)

### FastAPI
- Official Docs: https://fastapi.tiangolo.com/
- WebSocket Guide: https://fastapi.tiangolo.com/advanced/websockets/
- Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/

### Redis
- Commands Reference: https://redis.io/commands/
- Caching Patterns: https://redis.io/docs/manual/patterns/

---

## 📞 Next Steps

1. ✅ Review this architecture
2. 🔧 Set up development environment
3. 👨‍💻 Start Phase 1 implementation (Week 1)
4. 🧪 Test each feature thoroughly
5. 🚀 Deploy to production incrementally
6. 📊 Monitor metrics and iterate

---

**Ready to build? Let's ship it! 🚀**

**Last Updated:** 2025-10-13
**Version:** 1.0
**Status:** Ready for Implementation

