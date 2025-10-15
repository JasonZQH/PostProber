# Technology Stack & Rationale

PostProber intentionally mixes a Python backend (for LangChain/OpenAI support) with a modern React frontend to deliver AI-assisted social media workflows. This document outlines why specific technologies were chosen and how they interact.

## Core Stack

| Layer            | Technology                 | Why it fits PostProber                                                 | Notes |
|------------------|----------------------------|------------------------------------------------------------------------|-------|
| Frontend         | **React 18 + Vite**        | Fast DX, client-side routing, interoperable component ecosystem        | Tailwind-like utility classes + custom CSS power the UI |
| Backend API      | **FastAPI**                | Async-first, excellent Pydantic support, simple OpenAPI generation     | Entry point: `src/backend/main.py` |
| AI Orchestration | **LangChain + OpenAI GPT** | Structured prompt pipelines with consistent parsing utilities          | Tools live under `src/backend/tools/` |
| Background Jobs  | **APScheduler**            | Lightweight scheduling for recurring health checks                     | Configured via `jobs/health_scheduler.py` |
| Realtime         | **FastAPI WebSockets**     | Native WebSocket support; shares event loop with API                   | Managed in `services/websocket_manager.py` |
| Persistence      | **SQLite**                 | Zero-config for local dev; adequate for storing OAuth tokens + sessions| Database file at `src/backend/database/postprober.db` |

## Alternatives Considered

| Area      | Alternative      | Reason Not Chosen                                          |
|-----------|------------------|------------------------------------------------------------|
| Backend   | Node.js/Express  | Strong JS ecosystem but lacks built-in Pydantic-style validation and tight LangChain integration. |
| Frontend  | Next.js / Remix  | Adds server-side rendering and routing complexity unnecessary for SPA dashboard. |
| Database  | PostgreSQL       | Production-ready but overkill for OAuth/token storage in a demo environment. |
| Scheduler | Celery / RQ      | Require additional brokers (Redis/RabbitMQ) and infrastructure. |

## AI Service Details
- **Models**: `gpt-3.5-turbo` via `langchain_openai.ChatOpenAI`.
- **Prompt Design**: Each tool enforces JSON-only responses and performs fallbacks when parsing fails.
- **Error Handling**: Tools catch `json.JSONDecodeError` and return deterministic fallback payloads to keep the UI responsive.

## OAuth & Security
- OAuth flows (Twitter, LinkedIn, Instagram, Facebook) use provider-specific classes under `src/backend/auth/`.
- Sessions rely on HTTP-only cookies storing a generated `session_id`; tokens are persisted per user in SQLite.
- Rate limit and anomaly detection logs flow to the WebSocket manager, which keeps a history of the last 50 alerts in memory.

## Development & Deployment
- **Local Development**: Run FastAPI on port 8000 and Vite on 5173. CORS is already configured for local origins.
- **Containerisation**: Docker artefacts can be generated via `Dockerfile`/`docker-compose.yml` if needed (review repo root).
- **Scaling**: The architecture evolves toward background workers + persistent queues if platform health checks or analytics workloads grow.

## Testing Strategy (Roadmap)
- Backend: Introduce `pytest` suites targeting tool prompts and API responses (mock OpenAI calls for determinism).
- Frontend: Add Vitest/Jest tests for WebSocket clients and compose flows.
- Integration: Exercise OAuth callbacks via asynchronous httpx clients when secrets are available.

The current stack balances rapid prototyping with clear upgrade paths. Swapping in managed databases, hosted schedulers, or alternative LLM providers requires minimal structural change thanks to modular tools and endpoint boundaries.
