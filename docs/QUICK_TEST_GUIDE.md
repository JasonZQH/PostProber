# 🚀 Quick Test Guide - PostProber AI System

**Get up and running in 5 minutes!**

---

## Prerequisites

✅ Python 3.9+ installed
✅ Node.js 16+ installed
✅ OpenAI API key in `.env` file
✅ Virtual environment created (from Phase 1)

---

## Step 1: Start Backend (2 minutes)

```bash
# Navigate to backend
cd src/backend

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Success Indicators:**
```
🚀 PostProber AI API Starting...
✅ Content Optimization: Ready
✅ Hashtag Generation: Ready
✅ Health Monitoring: Initializing...
🔍 Running scheduled health check...
✅ Health Monitoring: Ready
📝 API Docs: http://localhost:8000/docs
🔌 WebSocket: ws://localhost:8000/ws/health
```

**🔴 If you see errors:**
- Make sure port 8000 is not already in use
- Check that `.env` file exists with `OPENAI_API_KEY`
- Verify all dependencies: `pip install -r requirements.txt`

---

## Step 2: Start Frontend (1 minute)

**Open a new terminal window:**

```bash
# Navigate to frontend
cd src/frontend

# Start React dev server
npm run dev
```

**✅ Success Indicators:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

---

## Step 3: Test Phase 1 - Content Optimization (1 minute)

### Via Browser:

1. Open http://localhost:5173
2. Navigate to **Compose** page
3. Type: `"Check out our new AI tool"`
4. Select platform: **Twitter**
5. Click **🤖 AI Optimize** button
6. Wait 3-5 seconds

**✅ Expected Result:**
- Optimized content appears
- Quality score shows (e.g., 85/100)
- List of improvements
- Suggested hashtags
- Processing time

### Via API:

Open http://localhost:8000/docs and try:

```
POST /api/optimize-with-hashtags
{
  "content": "Check out our new AI tool",
  "platform": "twitter"
}
```

---

## Step 4: Test Phase 2 - Health Monitoring (1 minute)

### Test WebSocket Connection:

1. Look at the **header notification bell** 🔔
2. Check for green dot + "Live" indicator
3. **If you see green dot** = WebSocket connected ✅
4. **If bell is grayed out** = Connection issue 🔴

### Test Health Dashboard:

1. Navigate to **Health** page
2. Verify you see:
   - 4 platform health cards (Twitter, LinkedIn, Instagram, Facebook)
   - Connection status: "Live Updates" with green dot
   - Last update timestamp
   - Platform status badges
   - Response times
   - Rate limit bars

### Test Health API:

Open http://localhost:8000/docs and try:

```
GET /api/health/status
```

**✅ Expected Response:**
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
      "rate_limit_total": 1000
    },
    ...
  ]
}
```

### Test Background Scheduler:

```
GET /api/health/scheduler/status
```

**✅ Expected Response:**
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

---

## Step 5: Test Real-time Alerts (Optional)

### Simulate an Alert:

While backend is running, open Python console:

```bash
cd src/backend
python
```

Then run:

```python
import asyncio
from services.websocket_manager import manager
from datetime import datetime

# Create a test critical alert
alert = {
    "platform": "twitter",
    "severity": "critical",
    "message": "Twitter API is experiencing issues",
    "recommended_action": "Posts may be delayed",
    "status": "degraded",
    "response_time": 1500,
    "error_rate": 15,
    "rate_limit_used": 450,
    "rate_limit_total": 1000,
    "timestamp": datetime.now().isoformat()
}

# Broadcast to all clients
asyncio.run(manager.broadcast_health_alert(alert))
```

**✅ Expected Result:**
- Notification bell badge shows **1** (new alert)
- Click bell to see alert dropdown
- Alert shows in Health page (no refresh needed)
- Alert has red background (critical severity)

---

## Common Issues & Fixes

### Issue 1: Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Fix:**
```bash
cd src/backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 2: Frontend shows "Failed to optimize"

**Error:** Network error when clicking AI Optimize

**Fix:**
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify API endpoint: `curl http://localhost:8000/api/ping`

### Issue 3: WebSocket won't connect

**Error:** Notification bell shows "Disconnected"

**Fix:**
- Check backend logs for WebSocket errors
- Verify WebSocket endpoint: `ws://localhost:8000/ws/health`
- Try refreshing the page
- Check browser console for connection errors

### Issue 4: No health data showing

**Error:** Health page shows "Loading..." forever

**Fix:**
- Check backend is running: `curl http://localhost:8000/api/health/status`
- Check browser console for fetch errors
- Try clicking "Refresh" button
- Verify backend logs for errors

---

## Quick API Reference

### Content Optimization
- **POST** `/api/optimize-content` - Optimize content only
- **POST** `/api/generate-hashtags` - Generate hashtags only
- **POST** `/api/optimize-with-hashtags` - Both (recommended)

### Health Monitoring
- **GET** `/api/health/status` - Current health status
- **GET** `/api/health/platform/{platform}` - Specific platform
- **POST** `/api/health/check` - Trigger manual check
- **GET** `/api/health/alerts` - Alert history
- **GET** `/api/health/scheduler/status` - Scheduler status
- **WebSocket** `/ws/health` - Real-time updates

### General
- **GET** `/` - API info
- **GET** `/api/ping` - Health check
- **GET** `/docs` - Interactive API docs

---

## Performance Benchmarks

### Expected Response Times:
- Content Optimization: **2-5 seconds**
- Hashtag Generation: **1-3 seconds**
- Combined API: **3-8 seconds**
- Health Check (single): **250-400ms**
- Health Check (all): **400-500ms**
- WebSocket connection: **<100ms**
- Alert broadcast: **<50ms**

### If slower than expected:
- Check OpenAI API status
- Verify internet connection
- Check backend logs for errors
- Consider using caching (future enhancement)

---

## Success Checklist

**Phase 1 - Content Optimization:**
- [ ] Backend starts without errors
- [ ] Frontend loads at http://localhost:5173
- [ ] Can compose a post
- [ ] AI Optimize button works
- [ ] Gets optimized content back
- [ ] Gets hashtag suggestions
- [ ] Shows quality score
- [ ] Shows processing time

**Phase 2 - Health Monitoring:**
- [ ] Health dashboard loads
- [ ] Shows 4 platform cards
- [ ] WebSocket connects (green dot)
- [ ] Platform status shows
- [ ] Response times display
- [ ] Rate limits display
- [ ] Can refresh manually
- [ ] Notification bell works
- [ ] Alert dropdown opens
- [ ] Scheduler is running

---

## Next Steps

### If Everything Works:
🎉 **Congratulations!** Both phases are working!

**Explore:**
1. Try different content types
2. Test different platforms
3. Wait 5 minutes for auto-refresh
4. Simulate alerts (see Step 5)
5. Check the interactive API docs at http://localhost:8000/docs

**Learn More:**
- Read `/docs/PHASE1_COMPLETED_SUMMARY.md`
- Read `/docs/PHASE2_HEALTH_MONITORING_COMPLETE.md`
- Read `/docs/AI_AGENT_SYSTEM_ARCHITECTURE.md`

### If Something Doesn't Work:
1. Check the **Common Issues & Fixes** section above
2. Look at backend logs for errors
3. Check browser console for frontend errors
4. Review the detailed docs in `/docs/`
5. Verify all prerequisites are met

---

## Getting Help

### Documentation:
- 📘 Full Phase 1 guide: `/docs/PHASE1_COMPLETED_SUMMARY.md`
- 📙 Full Phase 2 guide: `/docs/PHASE2_HEALTH_MONITORING_COMPLETE.md`
- 📗 Architecture: `/docs/AI_AGENT_SYSTEM_ARCHITECTURE.md`
- 📕 Implementation guide: `/docs/IMPLEMENTATION_CHECKLIST.md`

### Backend Setup:
- `/src/backend/README.md`

### Testing:
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:5173
- Health API: http://localhost:8000/api/health/status

---

## Development Tips

### Hot Reload:
- Backend: `--reload` flag automatically reloads on code changes
- Frontend: Vite automatically reloads on code changes

### Debugging:
- Backend logs: Check terminal where `uvicorn` is running
- Frontend logs: Check browser console (F12)
- WebSocket: Check browser console Network tab

### Stopping Servers:
- Backend: `Ctrl+C` in terminal
- Frontend: `Ctrl+C` in terminal

---

**Happy Testing! 🚀**

*Need more details? Check the comprehensive guides in `/docs/`*
