# PostProber - AI Agent Powered Social Media Co-Pilot

PostProber pairs a FastAPI backend with a React (Vite) frontend to deliver AI-assisted social media workflows. The system combines OpenAI-powered content tooling with real-time platform health monitoring, OAuth account linking, and rich documentation aimed at phased delivery.

## Core Capabilities
- **Content Intelligence (Phase 1)** – GPT-backed optimization and hashtag generation exposed through `/api/optimize-content`, `/api/generate-hashtags`, and the combined `/api/optimize-with-hashtags` endpoint.
- **Health Monitoring (Phase 2)** – Concurrent platform checks, APScheduler driven polling, and WebSocket push alerts keep connected clients up to date.
- **Analytics & Trending (Phase 3)** – LLM agents surface trending patterns, posting guidance, and performance gap analysis for connected platforms.
- **OAuth Account Linking** – Twitter, LinkedIn, Instagram, and Facebook handlers manage PKCE + token storage inside the bundled SQLite database.

## Project Layout
```
PostProber/
├── docs/                        # Architecture, status, and integration guides
├── src/
│   ├── backend/                 # FastAPI application (Python)
│   │   ├── api/endpoints/       # FastAPI routers (content, health, analytics, auth)
│   │   ├── tools/               # LangChain/OpenAI powered agents
│   │   ├── jobs/                # APScheduler health monitoring loop
│   │   ├── services/            # WebSocket connection manager
│   │   └── database/            # SQLite models + helpers
│   └── frontend/                # React (Vite) single-page app
│       ├── pages/               # Compose, Health, Analytics, etc.
│       ├── services/            # API + WebSocket clients
│       └── components/          # UI building blocks
├── package.json                 # Frontend dependencies and scripts
├── requirements.txt             # Backend Python dependencies
└── README.md                    # You are here
```

## Quick Start

### 1. Backend (FastAPI)
```bash
cd src/backend
python -m venv ../../venv
source ../../venv/bin/activate        # Windows: ..\..\venv\Scripts\activate
pip install -r requirements.txt
# ensure .env in repo root defines OPENAI_API_KEY and OAuth secrets
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Key endpoints:
- Swagger UI: `http://localhost:8000/docs`
- Health WebSocket: `ws://localhost:8000/ws/health`

### 2. Frontend (React + Vite)
```bash
cd <repo-root>
npm install
npm run dev
```

The Vite dev server defaults to `http://localhost:5173` and proxies API traffic against the FastAPI server.

## Notable Modules
- `src/backend/tool/*.py` – LangChain agents encapsulating GPT prompts for optimization, hashtags, analytics, and health analysis.
- `src/backend/jobs/health_scheduler.py` – APScheduler job orchestrating periodic health checks and deduplicated alerts.
- `src/backend/services/websocket_manager.py` – Connection manager that broadcasts health updates and alert history to clients.
- `src/frontend/services/aiService.js` – Thin wrapper around the AI endpoints used across the compose experience.
- `src/frontend/services/healthWebSocket.js` – Reconnect-capable WebSocket client that powers the header notifications and health dashboard.

## Development Notes
- Environment variables are loaded from the repository root `.env`. Both backend entrypoint and individual tools expect `OPENAI_API_KEY` plus OAuth credentials (Twitter, LinkedIn, Instagram, Facebook).
- The SQLite database stored at `src/backend/database/postprober.db` manages ephemeral session users and per-platform tokens.
- WebSocket traffic is only initiated when the frontend detects connected platforms, minimizing idle connections.

## Testing & Validation
- **Backend** – Add FastAPI unit or integration tests under `src/backend/tests` (currently placeholder). Use `pytest` or `httpx.AsyncClient` to validate endpoints when extending functionality.
- **Frontend** – React components can be tested with the Vite/Jest configuration (`npm test`). Ensure WebSocket flows are mocked when adding new health-monitoring features.
- **Manual** – Use the Compose page to exercise AI workflows and the Health page/Header bell to confirm alert streaming once OAuth connections are established.

## Additional Documentation
The `docs/` directory contains phase summaries, architecture diagrams, integration checklists, and status updates to help orient new contributors. Start with:
- `docs/PROJECT_STATUS_OVERVIEW.md` – Phase completion highlights.
- `docs/AI_AGENT_SYSTEM_ARCHITECTURE.md` – Deep dive into tool orchestration and data flows.
- `docs/QUICK_TEST_GUIDE.md` – Manual validation steps per feature area.
