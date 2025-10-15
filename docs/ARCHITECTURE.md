# System Architecture & Data Flow

PostProber couples a FastAPI backend with a React/Vite frontend to orchestrate AI-powered content tooling and platform health monitoring. This document summarises the current architecture (Phases 1–3) and how the moving pieces interact.

## High-Level Diagram
```
┌──────────────────────────────────────────────────────────────────────┐
│                              Frontend (Vite)                         │
│  Pages: Dashboard, Compose, Health, Analytics, Accounts              │
│  Services: aiService, analyticsService, platformService,             │
│            healthWebSocket                                           │
└───────────────▲───────────────────────────────┬──────────────────────┘
                │ REST (JSON)                   │ WebSocket (JSON)
┌───────────────┴───────────────────────────────▼──────────────────────┐
│                        Backend (FastAPI + APScheduler)               │
│  api.endpoints.content    → GPT optimization + hashtags              │
│  api.endpoints.analytics  → Trending + performance insights          │
│  api.endpoints.health     → Health checks + WebSocket gateway        │
│  api.endpoints.auth       → OAuth login/callback/token management    │
│  jobs.health_scheduler    → Periodic platform health polling         │
│  services.websocket_mgr   → Connection registry + broadcast helpers  │
└───────────────┬──────────────────────────────────────────────────────┘
                │
┌───────────────▼──────────────────────────────────────────────────────┐
│                     AI Agents & Data Providers                       │
│  tools.content_optimizer / hashtag_generator                         │
│  tools.trending_analyzer / analytics_insights                        │
│  tools.health_monitor                                                │
│  SQLite (`database/models.py`) storing sessions + OAuth tokens       │
│  External APIs: OpenAI, Twitter, LinkedIn, Instagram, Facebook       │
└──────────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Backend (FastAPI)
- **Routers** (`api/endpoints/*.py`)
  - `content.py` – Exposes optimization + hashtag endpoints invoked by the compose flow.
  - `analytics.py` – Provides trending analysis, best posting times, content insights, and dashboard aggregates.
  - `health.py` – Returns current status, triggers manual checks, and upgrades clients to the health WebSocket.
  - `auth.py` – Handles OAuth flows for Twitter, LinkedIn, Instagram, and Facebook using provider-specific helpers.
- **Tools (`tools/*.py`)**
  - Wrap LangChain `ChatOpenAI` calls, enforce JSON outputs, and append metadata used by the UI.
  - Include fallbacks for JSON parsing errors to avoid blocking user flows.
- **Scheduler (`jobs/health_scheduler.py`)**
  - Runs `HealthMonitorTool.check_all_platforms()` every five minutes.
  - Deduplicates alerts (cooldown logic), maintains last results, and broadcasts over WebSocket.
- **WebSocket Manager (`services/websocket_manager.py`)**
  - Tracks active connections, relays alerts/updates, responds to history/stat requests, and issues periodic pings.
- **Database (`database/models.py`)**
  - SQLite-based persistence for session IDs, OAuth tokens, and state records used during PKCE exchanges.

### Frontend (React + Vite)
- **Pages**
  - `Compose.jsx` – Authoring surface that calls `aiService.optimizeWithHashtags()` and renders AI suggestions.
  - `Health.jsx` – Real-time status dashboard driven by REST fetches and WebSocket updates.
  - `Analytics.jsx` – Surfaces trending analysis, best posting times, and AI insights (Phase 3).
  - `Accounts.jsx` – Manages OAuth connections via `platformService`.
  - `Dashboard.jsx` – Entry overview with health summaries and quick metrics.
- **Services**
  - `aiService.js` & `analyticsService.js` – REST clients targeting FastAPI endpoints (uses `VITE_API_URL` if defined).
  - `platformService.js` – Keeps connected platform metadata in sync with `/api/auth/status`.
  - `healthWebSocket.js` – Handles connection lifecycle, reconnection, ping/pong, and listener management.
- **Shared UI**
  - `components/common/Header.jsx` – Notification bell that subscribes to `healthWebSocket` events and shows unread alerts.

## Data Flows

### Content Optimization & Hashtags
1. User composes text on `/compose`.
2. `aiService.optimizeWithHashtags` posts `{content, platform}` to `/api/optimize-with-hashtags`.
3. FastAPI invokes `ContentOptimizerTool.optimize` and `HashtagGeneratorTool.generate`.
4. Response includes optimized copy, improvement list, score, and hashtag collection for UI rendering.

### Health Monitoring
1. APScheduler job runs `HealthMonitorTool.check_all_platforms()` on startup and at five-minute intervals.
2. Results are stored in `HealthScheduler.last_health_check` and broadcast via `websocket_manager`.
3. Web clients subscribe to `/ws/health`; header + health page update UI, maintain history, and reflect unread alerts.
4. Manual checks (`POST /api/health/check`) reuse the same tool and broadcast path.

### OAuth Linking
1. User clicks “Connect” in `/accounts`.
2. `platformService.connectPlatform()` redirects to `/api/auth/{platform}/login`.
3. `auth.py` creates/updates a session, persists state, and redirects to external provider with PKCE if needed.
4. Callback exchanges code for tokens, stores them via `Database.save_platform_token`, and redirects back to the app.
5. Frontend refreshes platform list via `/api/auth/status`.

### Analytics & Trending
1. Frontend requests `/api/trending/analyze`, `/api/trending/best-times/{platform}`, or `/api/analytics/analyze-content`.
2. Backend orchestrates `TrendingAnalyzerTool` and `AnalyticsInsightsTool`, returning insights used in dashboards and reports.

## Deployment Considerations
- **Configuration** – All secrets live in the root `.env`. Tools also load this file directly, so keep paths stable.
- **Scaling** – For higher throughput, move periodic jobs to dedicated workers and promote the SQLite database to PostgreSQL.
- **Monitoring** – WebSocket manager currently keeps alert history in memory; persist alerts to SQLite if long-term auditability is required.

## Future Enhancements
- Persist health alerts and analytics summaries for historical dashboards.
- Add retry/backoff strategies for OpenAI calls and OAuth token refresh flows.
- Introduce background queues (e.g., Redis + RQ) if platform polling or analytics workloads expand.

This architecture emphasises modular AI tooling, clean API boundaries, and real-time feedback loops, making it straightforward to evolve PostProber’s agent capabilities over time.
