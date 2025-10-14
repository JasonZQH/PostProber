# AI Agent Integration Map

This document maps AI agent functionalities to specific frontend UI/UX components in PostProber.

## Overview

PostProber's AI agent system provides intelligent automation and insights across the application. Each AI functionality is integrated into specific frontend components to deliver seamless user experiences.

**Key Design Principle:** PostProber operates without user authentication - users simply link their social media accounts. Therefore, AI agents focus on **real-time analysis**, **platform health monitoring**, and **trending content insights** rather than historical user data analysis.

---

## AI Agent Functionalities

### 1. Content Optimization

**Purpose:** AI-powered content optimization that analyzes and improves post quality for maximum engagement using LLM best practices.

**Frontend Components:**

- **Page:** `src/frontend/pages/Compose.jsx`
- **Primary Components:**
  - **AI Optimize Button** (Lines 74-91)
    - Trigger content optimization
    - Shows loading state during AI processing
  - **Post Content Textarea** (Lines 95-101)
    - User input for post content
    - Character count per platform
  - **AI Suggestions Card** (Lines 249-309)
    - Displays optimized content
    - Shows optimization score (0-100)
    - "Use This Version" button to apply suggestions

**AI Agent Integration Points:**
- Click "AI Optimize" button → Call content optimization agent
- AI analyzes content for:
  - Hook strength (first line impact)
  - Message clarity and focus
  - Emotional appeal and tone
  - Call-to-action effectiveness
  - Platform-specific best practices (length, format, style)
- Display optimized version with quality score
- Provide specific improvement explanations

**How It Works (No Database Required):**
```python
def optimize_content(content, platform):
    prompt = f"""
    Optimize this {platform} post for maximum engagement:

    Original: "{content}"

    Improve:
    1. Hook - make first line irresistible
    2. Clarity - ensure message is focused
    3. Emotion - add appropriate emotional appeal
    4. CTA - create compelling call-to-action
    5. Platform fit - optimize for {platform} best practices

    Provide optimized version and score (0-100).
    """

    result = llm.invoke(prompt)
    return result
```

**Expected User Flow:**
1. User types content in textarea
2. User clicks "AI Optimize" button
3. AI analyzes content using LLM best practices
4. Display optimized version with quality score
5. User can accept or modify AI suggestions

---

### 2. Hashtag Strategy

**Purpose:** Smart hashtag recommendations based on content, platform, and current trending topics using real-time analysis.

**Frontend Components:**

- **Page:** `src/frontend/pages/Compose.jsx`
  - **Suggested Hashtags Section** (Lines 289-305)
    - Displays AI-recommended hashtags
    - Clickable hashtag buttons
    - One-click insertion into post content
    - Located in AI Suggestions card

**AI Agent Integration Points:**
- Analyze post content and extract key themes
- Generate strategic hashtag mix:
  - 2-3 trending/popular hashtags (high reach)
  - 3-4 niche/community hashtags (engaged audience)
  - 1-2 branded hashtags (brand building)
- Use LLM to identify relevant hashtags based on content

**How It Works (No Database Required):**
```python
def generate_hashtags(content, platform):
    prompt = f"""
    Analyze this {platform} post and suggest strategic hashtags:

    Content: "{content}"

    Generate hashtag mix:
    - 2-3 trending/popular hashtags (broad reach)
    - 3-4 niche/topic-specific hashtags (engaged community)
    - 1-2 branded/unique hashtags (brand identity)

    Explain why each hashtag is relevant and its expected reach level.
    """

    result = llm.invoke(prompt)
    return result
```

**Expected User Flow:**
1. User creates post content
2. AI analyzes content themes and topics
3. Generate hashtag recommendations with strategic mix
4. Display hashtags as clickable buttons
5. User clicks hashtag to add to content

---

### 3. Health Monitoring & Proactive Alerting ⭐ **CORE FEATURE**

**Purpose:** **Real-time platform health monitoring with AI-powered anomaly detection and proactive alerts**. Reduces time spent visiting the Health page by automatically notifying users of issues before they impact posting.

**Frontend Components:**

- **Page:** `src/frontend/pages/Health.jsx`
  - **Platform Health Indicators** (System status for each connected platform)
  - **Reliability Metrics** (Uptime, response time, error rates)
  - **Alerting System** (Real-time notifications)
  - **SLI/SLO Tracking** (Service level objectives)
  - **Incident Management** (Issue tracking and history)

- **Page:** `src/frontend/pages/Dashboard.jsx`
  - **All Systems Online Card** (Lines 220-239)
    - Quick health status overview
    - Proactive alert badges
    - Click to view detailed health dashboard

- **Global Components:**
  - **Header Notification Bell**
    - Real-time health alerts
    - Alert count badge
    - Click to view alert details

**AI Agent Integration Points:**

1. **Continuous Monitoring (Background Agent)**
   - Monitor platform API health every 1-5 minutes
   - Track response times, error rates, rate limits
   - Detect anomalies: sudden slowdowns, auth failures, API downtime

2. **Pattern Analysis**
   - AI analyzes patterns: "Twitter API slow for 30+ minutes"
   - Predict potential issues before they occur
   - Compare against historical baseline

3. **Smart Alerting**
   - AI determines alert severity (Critical/Warning/Info)
   - Suppress duplicate alerts (avoid alert fatigue)
   - Provide auto-recovery suggestions

4. **Alert Types:**
   - 🔴 **Critical:** Platform completely down, auth expired
   - 🟡 **Warning:** Slow response times, approaching rate limits
   - 🔵 **Info:** Scheduled maintenance, minor delays

**How It Works (Real-time Monitoring):**
```python
# Background monitoring agent (runs every 5 minutes)
async def health_monitoring_agent():
    platforms = ["twitter", "linkedin", "instagram", "facebook"]

    for platform in platforms:
        # 1. Test platform API health
        health_status = await test_platform_api(platform)

        # 2. AI analyzes health data
        prompt = f"""
        Analyze {platform} API health:

        Current status:
        - Response time: {health_status['response_time']}ms
        - Error rate: {health_status['error_rate']}%
        - Rate limit usage: {health_status['rate_limit_used']}/
{health_status['rate_limit_total']}
        - Last success: {health_status['last_success_time']}

        Historical baseline:
        - Normal response time: 150-300ms
        - Normal error rate: < 1%

        Determine:
        1. Is there an issue? (Yes/No)
        2. Severity: Critical/Warning/Info
        3. Root cause analysis
        4. Recommended action for user
        5. Should we send alert?
        """

        analysis = await llm.ainvoke(prompt)

        # 3. Send proactive alert if needed
        if analysis['should_alert']:
            await send_alert_to_user({
                "platform": platform,
                "severity": analysis['severity'],
                "message": analysis['message'],
                "action": analysis['recommended_action'],
                "timestamp": datetime.now()
            })
```

**Alert Notification Examples:**

1. **Critical Alert:**
   ```
   🔴 Twitter API Connection Lost
   Your Twitter account authentication has expired.

   Action: Please re-authenticate your Twitter account to continue posting.
   [Reconnect Twitter] button
   ```

2. **Warning Alert:**
   ```
   🟡 LinkedIn API Slow Response
   LinkedIn is experiencing delays (850ms avg, normally 200ms).

   This may affect posting speed but posts will still succeed.
   [View Details] | [Dismiss]
   ```

3. **Info Alert:**
   ```
   🔵 Rate Limit Approaching
   You've used 85% of your Twitter API hourly limit.

   Posts may be delayed for 15 minutes if limit is reached.
   [View Health Dashboard]
   ```

**Expected User Flow:**
1. AI agent monitors platform health every 5 minutes in background
2. Detects anomaly: Twitter API response time 3x slower than normal
3. AI analyzes: "Warning level, temporary slowdown, no action needed"
4. Sends proactive notification to user
5. User sees alert in header bell icon
6. User can view details in Health page or dismiss alert
7. **Benefit:** User knows about issues BEFORE trying to post

**Key Innovation:** Users don't need to manually check the Health page - AI proactively alerts them only when there are actual issues that need attention.

---

### 4. Trending Content Analysis & Recommendations

**Purpose:** Analyze top-performing posts from platform APIs in real-time to provide data-driven content recommendations. No user authentication required - uses public platform data.

**Frontend Components:**

- **Page:** `src/frontend/pages/Analytics.jsx`
  - **Engagement Trending Up Card** (Lines 313-333)
    - AI-generated trending insights
    - "What's working NOW" recommendations
  - **Content Tips Section** (NEW - can add)
    - Real-time trending patterns
    - Successful content formats

- **Page:** `src/frontend/pages/Compose.jsx`
  - **Content Tips Card** (Lines 365-392)
    - Dynamic tips based on current trends
    - Platform-specific trending advice

- **Page:** `src/frontend/pages/Dashboard.jsx`
  - **Insights Widget** (Can add to sidebar)
    - "Trending on Twitter: Posts with video get 3x engagement"
    - "LinkedIn tip: Carousel posts performing 40% better this week"

**AI Agent Integration Points:**

1. **Trending Data Collection**
   - Fetch top posts from platform APIs (Twitter trending, LinkedIn top posts, etc.)
   - No user authentication needed - uses public APIs
   - Refreshes every 4-6 hours

2. **Pattern Analysis**
   - AI analyzes successful posts:
     - Content formats (video, images, carousels, text-only)
     - Post length and structure
     - Hook patterns
     - Topic themes
     - Engagement metrics

3. **Recommendation Generation**
   - Compare user's linked accounts against trending benchmarks
   - Provide actionable advice: "Your posts average 2% engagement, trending posts get 8%"
   - Suggest improvements based on current trends

**How It Works (No User Database Required):**
```python
async def trending_analysis_agent(platform):
    # 1. Fetch trending public posts
    trending_posts = await fetch_platform_trending(platform)
    # Returns: Top 50 posts from platform's public API

    # 2. AI analyzes patterns
    prompt = f"""
    Analyze these top-performing {platform} posts from today:

    {format_posts_for_analysis(trending_posts)}

    Identify patterns:
    1. Common content formats (video/image/text ratio)
    2. Average post length of top performers
    3. Hook patterns in first line
    4. Most engaging topics
    5. Hashtag usage patterns
    6. Posting time patterns

    Generate 3-5 actionable recommendations for users posting on {platform} today.
    """

    insights = await llm.ainvoke(prompt)

    # 3. Compare user's account performance (if linked)
    if user_has_linked_account(platform):
        user_stats = await get_account_stats(platform)

        comparison_prompt = f"""
        User's {platform} performance:
        - Avg engagement rate: {user_stats['engagement_rate']}%
        - Avg likes: {user_stats['avg_likes']}
        - Avg comments: {user_stats['avg_comments']}

        Trending benchmark:
        - Avg engagement rate: {insights['trending_avg_engagement']}%

        Provide specific advice to close the gap.
        """

        personalized_advice = await llm.ainvoke(comparison_prompt)

    return {
        "trending_insights": insights,
        "personalized_advice": personalized_advice,
        "last_updated": datetime.now()
    }
```

**Example Insights:**

1. **Format Trends:**
   ```
   📊 Trending This Week on LinkedIn:
   - Carousel posts get 40% more engagement
   - Posts with 3-5 images outperform single images
   - Video posts under 60 seconds perform best

   💡 Recommendation: Try creating a carousel post about your expertise
   ```

2. **Content Patterns:**
   ```
   🔥 What's Working on Twitter Right Now:
   - Threads with 5-7 tweets get highest engagement
   - Posts starting with questions get 2x replies
   - Adding relevant GIFs increases engagement by 35%

   💡 Your Opportunity: Your tweets average 50 characters - top posts use 150-200
   ```

3. **Benchmark Comparison:**
   ```
   📈 Your Performance vs. Trending:
   - Your engagement rate: 2.1%
   - Trending average: 6.8%

   Gap Analysis:
   - Top posts use 4-6 hashtags, you use 1-2
   - Top posts include visual content 80% of time
   - Top posts post during 2-4 PM, you post mornings

   💡 Quick Wins: Add 2-3 more hashtags, post between 2-4 PM
   ```

**Expected User Flow:**
1. User opens Dashboard or Analytics page
2. AI agent has already analyzed trending content (background job)
3. Display current trending insights and recommendations
4. User sees actionable advice: "Posts with video trending 3x higher"
5. User applies insights to their next post
6. **No user login required** - trends based on public platform data

**Key Innovation:** Provides data-driven recommendations without needing user historical data - analyzes what's working RIGHT NOW on each platform.

---

### 5. Smart Analytics Insights (Combined with Trending Analysis)

**Purpose:** Combine linked account analytics with trending benchmarks to provide personalized, actionable recommendations.

**Frontend Components:**

- **Page:** `src/frontend/pages/Analytics.jsx`
  - **Overview Stats** (Lines 238-266)
    - Display user's performance metrics
  - **Engagement Trending Up Card** (Lines 313-333)
    - Show comparison against trending benchmarks
    - AI-generated improvement suggestions
  - **Performance Badges** (Lines 147-175)
    - Color-coded performance indicators
  - **Export Report** (Lines 177-231)
    - Generate AI-powered analytics reports

**AI Agent Integration Points:**
- Fetch user's linked account performance (via platform APIs)
- Compare against trending benchmarks (from Feature #4)
- Generate gap analysis and recommendations
- Identify specific improvement opportunities
- No historical database needed - uses current platform API data

**How It Works:**
```python
async def analytics_insights_agent(platform, user_account_id):
    # 1. Get user's recent performance from platform API
    user_data = await platform_api.get_account_stats(user_account_id)

    # 2. Get trending benchmarks (from trending analysis)
    trending_data = await get_trending_benchmarks(platform)

    # 3. AI generates personalized insights
    prompt = f"""
    Compare user's performance against trending benchmarks:

    User's {platform} metrics (last 30 days):
    - Posts: {user_data['post_count']}
    - Avg engagement rate: {user_data['engagement_rate']}%
    - Avg reach: {user_data['avg_reach']}
    - Top content type: {user_data['top_format']}

    Trending benchmarks:
    - Avg engagement rate: {trending_data['avg_engagement']}%
    - Top-performing format: {trending_data['top_format']}
    - Optimal posting frequency: {trending_data['post_frequency']}

    Provide:
    1. Performance assessment (above/below/at benchmark)
    2. Top 3 improvement opportunities
    3. Specific actionable recommendations
    4. Expected impact of each recommendation
    """

    insights = await llm.ainvoke(prompt)
    return insights
```

**Expected User Flow:**
1. User opens Analytics page
2. AI fetches recent performance from linked accounts
3. Compares against real-time trending benchmarks
4. Displays personalized insights and recommendations
5. User can export full AI-generated report

---

## Summary Mapping Table

| AI Functionality | Primary Page | Component Location | Key Features | Database Required? |
|-----------------|--------------|-------------------|--------------|-------------------|
| **Content Optimization** | Compose | Lines 74-91, 249-309 | Optimize content, show quality score | ❌ No |
| **Hashtag Strategy** | Compose | Lines 289-305 | Generate strategic hashtags | ❌ No |
| **⭐ Health Monitoring** | Health / Dashboard | Health page + Header alerts | Proactive platform health alerts | ❌ No (monitors in real-time) |
| **Trending Analysis** | Analytics / Compose | Lines 313-333, 365-392 | What's working NOW on each platform | ❌ No (public API data) |
| **Analytics Insights** | Analytics | Lines 177-396 | Compare performance vs. benchmarks | ❌ No (platform API data) |

---

## Integration Architecture

### Frontend → Backend Communication

```
Frontend Component
    ↓
API Request to Backend
    ↓
LangGraph Workflow Router
    ↓
Specialized AI Agent (LangChain + LangGraph)
    ↓
OpenAI API (GPT-3.5-turbo / GPT-4)
    ↓
Process Response
    ↓
Return to Frontend
    ↓
Update UI Component
```

### State Management

Each AI request includes:
- **Session ID:** Temporary session identifier (no login required)
- **Request Type:** content_optimization, hashtag_generation, health_monitoring, trending_analysis, analytics_insights
- **User Input:** content, platform, linked_account_ids
- **Real-time Data:** Platform API responses, trending data, health metrics

### Response Format

All AI agents return structured responses:
```javascript
{
  success: true,
  request_type: "content_optimization",
  result: {
    optimized_content: "...",
    score: 92,
    improvements: ["..."],
    predictions: {...}
  },
  suggestions: [...],
  processing_time: 1.23,
  session_id: "uuid"
}
```

---

## Implementation Priority

### Phase 1: Core Features (MVP) - **START HERE**
1. 🎯 **Content Optimization** (Compose page)
   - Simple, no database required
   - Immediate value to users
   - **Priority: HIGH**

2. 🎯 **Hashtag Strategy** (Compose page)
   - Works with content optimization
   - No external APIs needed
   - **Priority: HIGH**

3. ⭐ **Health Monitoring & Alerting** (Health + Dashboard)
   - **CORE DIFFERENTIATOR**
   - Reduces manual health checking
   - Proactive user experience
   - Requires background job setup
   - **Priority: CRITICAL**

### Phase 2: Intelligence & Insights
4. 📊 **Trending Content Analysis** (Analytics + Compose)
   - Requires platform public APIs
   - Background job (refresh every 4-6 hours)
   - Provides competitive edge
   - **Priority: MEDIUM**

5. 📈 **Smart Analytics Insights** (Analytics page)
   - Combines with trending analysis
   - Uses platform API data (no database)
   - **Priority: MEDIUM**

### Phase 3: Future Enhancements
6. ⏳ Real-time streaming AI responses
7. ⏳ Multi-language support
8. ⏳ Advanced sentiment analysis

---

## Technical Requirements

### Frontend
- React hooks for state management
- Async/await for API calls
- Loading states during AI processing
- Error handling for failed requests
- Real-time updates with WebSocket (optional for streaming)

### Backend
- FastAPI endpoints for each AI feature
- LangChain for LLM interactions
- LangGraph for workflow orchestration
- OpenAI API integration
- ~~Database for storing user preferences~~ **NOT REQUIRED** - uses platform APIs
- Background job scheduler (for health monitoring + trending analysis)
- Caching for trending data (Redis recommended)
- WebSocket for real-time health alerts

### AI Models
- **Primary:** GPT-3.5-turbo (fast, cost-effective)
- **Advanced:** GPT-4 (complex analysis, higher quality)
- **Temperature:** 0.7 for creative content, 0.3 for analytics
- **Max Tokens:** 800-1000 for responses

---

## Next Steps

### Immediate Actions:
1. ✅ **Review this refined mapping** - Ensure alignment with PostProber's no-login architecture
2. 🔧 **Set up development environment:**
   - Install LangChain + LangGraph dependencies
   - Configure OpenAI API key
   - Set up FastAPI backend structure

### Phase 1 Implementation (MVP):
3. 🎯 **Content Optimization** (Week 1)
   - Create `/api/optimize-content` endpoint
   - Implement LangChain agent (see `src/shared/ai-examples/02_langchain_with_prompts.py`)
   - Connect to Compose page frontend

4. 🎯 **Hashtag Strategy** (Week 1)
   - Create `/api/generate-hashtags` endpoint
   - Implement hashtag generation agent
   - Integrate with Compose page

5. ⭐ **Health Monitoring** (Week 2-3)
   - Set up background job scheduler (Celery/APScheduler)
   - Create platform API health check functions
   - Implement AI health analysis agent
   - Create WebSocket endpoint for real-time alerts
   - Add notification bell to header
   - Connect to Health page dashboard

### Phase 2 Implementation:
6. 📊 **Trending Analysis** (Week 4)
   - Integrate platform public APIs (Twitter, LinkedIn, etc.)
   - Create background job for trending data collection
   - Implement AI pattern analysis agent
   - Update Analytics and Compose pages

7. 📈 **Analytics Insights** (Week 5)
   - Create `/api/analytics-insights` endpoint
   - Fetch user account data via platform APIs
   - Compare against trending benchmarks
   - Generate personalized recommendations

### Testing & Deployment:
8. 🧪 **Test all features** thoroughly
9. 📊 **Monitor AI costs** and optimize token usage
10. 🚀 **Deploy to production** incrementally

---

## Related Documentation

- **AI Learning Examples:** `src/shared/ai-examples/` (01-06)
- **Frontend Components:** `src/frontend/pages/`
- **API Documentation:** (To be created)
- **LangChain Docs:** https://python.langchain.com/
- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/

---

**Last Updated:** 2025-10-13
**Version:** 2.0 (Refined for no-login architecture)
**Status:** Ready for Implementation
**Next Review:** After Phase 1 MVP completion

---

## Key Refinements from Original Plan

### ❌ Removed (Requires User Database):
- ~~Best Time to Post~~ - Needs historical user posting data
- ~~Engagement Prediction based on user history~~ - Needs user's past performance
- ~~Real-time writing suggestions~~ - Too expensive, called on every keystroke

### ✅ Added (Works Without Database):
- **Health Monitoring & Proactive Alerting** ⭐ - CORE FEATURE
- **Trending Content Analysis** - Uses public platform APIs
- **Benchmark Comparisons** - Compares linked accounts vs. trending data

### 🎯 Core Value Proposition:
PostProber provides **intelligent, real-time insights** without requiring user login or historical databases. AI agents analyze:
1. Content quality (LLM best practices)
2. Platform health (real-time monitoring)
3. Current trends (public platform data)
4. Linked account performance (platform APIs)

This approach delivers immediate value while maintaining simplicity and privacy.
