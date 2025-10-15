# Project Structure & Responsibility Map

This project splits the codebase between a LangChain-enabled FastAPI backend and a Vite-powered React frontend. Use this guide to locate key modules when extending AI behaviour, platform monitoring, or UI workflows.

```
PostProber/
├── docs/                      # Architecture, guides, status updates
├── src/
│   ├── backend/               # FastAPI backend (Python)
│   │   ├── api/               # HTTP + WebSocket endpoints
│   │   │   └── endpoints/     # content.py, health.py, analytics.py, auth.py
│   │   ├── tools/             # LangChain GPT tools (optimization, trending, etc.)
│   │   ├── jobs/              # APScheduler tasks (health monitoring loop)
│   │   ├── services/          # WebSocket connection manager
│   │   ├── database/          # SQLite models + helpers
│   │   ├── schemas/           # Pydantic models (domain/safety contracts)
│   │   └── main.py            # FastAPI application entrypoint
│   └── frontend/              # React SPA (Vite)
│       ├── pages/             # High-level routes (Dashboard, Compose, Health, etc.)
│       ├── components/        # Reusable UI components
│       ├── services/          # API/WebSocket clients (aiService, platformService, healthWebSocket)
│       ├── hooks/             # Custom React hooks (WebSocket state, platform data)
│       └── styles/            # Global + component styling
├── requirements.txt           # Backend Python dependencies
├── package.json               # Frontend dependencies and scripts
└── README.md                  # Overview & quick start
```

## Backend Highlights (`src/backend`)
- **`api/endpoints`** – FastAPI routers grouped by feature. Each router imports the relevant tool/service and exposes REST or WebSocket interfaces.
- **`tools`** – LangChain `ChatOpenAI` wrappers that encapsulate prompt engineering and response parsing for optimization, hashtags, analytics insights, and health anomaly analysis.
- **`jobs/health_scheduler.py`** – APScheduler-driven background job that triggers `HealthMonitorTool`, deduplicates alerts, and pushes updates through the WebSocket manager.
- **`services/websocket_manager.py`** – Manages client connections, maintains alert history, and responds to real-time requests (history/stats/ping).
- **`database/models.py`** – Lightweight SQLite layer for session users, OAuth token storage, and state tracking during PKCE flows.
- **`schemas` & `auth`** – Pydantic models and OAuth providers (Twitter, LinkedIn, Instagram, Facebook) including PKCE support and token refresh helpers.

## Frontend Highlights (`src/frontend`)
- **`pages/Compose.jsx`** – Integrates `aiService` to drive content optimization and hashtag suggestions.
- **`pages/Health.jsx`** – Renders live platform status. Subscribes to `healthWebSocket` and filters updates around connected accounts.
- **`components/common/Header.jsx`** – Notification bell that listens for WebSocket alerts and displays unread counts.
- **`services/platformService.js`** – Synchronizes connected OAuth accounts, exposing helper metadata (labels, colours, icons).
- **`services/healthWebSocket.js`** – Handles WebSocket lifecycle, reconnection, history requests, and ping/pong keepalives.
- **`pages/Analytics.jsx`** – Consumes analytics/trending endpoints to surface AI insights (Phase 3 features).

## Shared Data & Configuration
- **Environment** – `.env` in repo root supplies `OPENAI_API_KEY`, OAuth credentials, and any optional secrets. Both the backend entrypoint and individual tool modules read from this file.
- **Database** – SQLite file `src/backend/database/postprober.db` stores session users, OAuth tokens, and state verification.
- **Docs** – Phase status, architecture diagrams, quick testing steps, and integration notes live under `docs/` for onboarding and QA support.

## Extension Tips
1. **Add new AI workflows** by placing LangChain logic under `src/backend/tools/` and exposing it through a FastAPI router in `api/endpoints`.
2. **Expose background tasks** through APScheduler jobs in `jobs/` and broadcast via `services/websocket_manager.py` when real-time updates are needed.
3. **Front-end integrations** typically add a `services/*` client, update a page/container, and optionally tie into the shared notification header.
4. **Testing** – Place backend tests under `src/backend/tests` and frontend tests under `tests/` or `src/frontend` depending on tooling preferences.
