# Development Environment Setup Guide

This guide covers the steps required to spin up the FastAPI backend and the Vite-powered React frontend locally.

## 1. Prerequisites
- **Python 3.10+** (virtual environment recommended)
- **Node.js 18+ / npm 9+**
- **SQLite** (bundled with Python; no separate install required)
- Git, package managers, and your editor of choice (VS Code + Python/ESLint extensions suggested)

Verify versions:
```bash
python --version
node --version
npm --version
```

## 2. Clone the Repository
```bash
git clone <repository-url>
cd PostProber
```

## 3. Configure Environment Variables
The backend and tooling expect an `.env` file in the repository root. Duplicate the template (if present) or create a new file with the required keys:

```bash
cp .env.template .env  # or create manually if the template is missing
```

Required values:
```
OPENAI_API_KEY=sk-...

# OAuth credentials (update with real values before running actual flows)
TWITTER_CLIENT_ID=...
TWITTER_CLIENT_SECRET=...
TWITTER_REDIRECT_URI=http://localhost:8000/api/auth/twitter/callback

LINKEDIN_CLIENT_ID=...
LINKEDIN_CLIENT_SECRET=...
LINKEDIN_REDIRECT_URI=http://localhost:8000/api/auth/linkedin/callback

INSTAGRAM_CLIENT_ID=...
INSTAGRAM_CLIENT_SECRET=...
INSTAGRAM_REDIRECT_URI=http://localhost:8000/api/auth/instagram/callback

FACEBOOK_CLIENT_ID=...
FACEBOOK_CLIENT_SECRET=...
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/auth/facebook/callback
```

> The default SQLite path (`src/backend/database/postprober.db`) is relative to the backend package. No additional configuration is needed unless you move the database.

## 4. Backend Setup (FastAPI)
```bash
cd src/backend
python -m venv ../../venv
source ../../venv/bin/activate        # Windows PowerShell: ..\..\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# Launch the API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Key URLs:
- REST Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health WebSocket: `ws://localhost:8000/ws/health`

The first startup triggers the health scheduler and initializes the SQLite database if it does not exist.

## 5. Frontend Setup (React + Vite)
Open a new terminal (keep the backend running):
```bash
cd PostProber
npm install
npm run dev
```

Vite serves the app at `http://localhost:5173` with hot module replacement. API requests target `http://localhost:8000` by default; update `VITE_API_URL` in `.env` if your backend runs elsewhere.

## 6. Optional Utilities
- **Testing**: 
  - Backend tests can be added under `src/backend/tests`. Use `pytest` or `httpx.AsyncClient` for FastAPI testing.
  - Frontend tests (Jest/Vitest) can be run via `npm test` once suites are added.
- **Database Inspection**: Use `sqlite3 src/backend/database/postprober.db` or GUI tools (DB Browser for SQLite) to inspect saved tokens and session records.
- **Formatting/Linting**: Integrate `black`/`ruff` for Python and ESLint/Prettier for React as desired (not preconfigured).

## 7. Common Troubleshooting
- **`ModuleNotFoundError` importing backend packages** – ensure you run commands from `src/backend` (or set `PYTHONPATH`) so FastAPI resolves relative packages.
- **LLM calls failing** – verify `OPENAI_API_KEY` is present and not rate-limited. Tools log raw responses when parsing fails for easier debugging.
- **WebSocket disconnects** – clients only connect when platforms are linked; ensure OAuth flows complete successfully or call `healthWebSocket.connect()` manually during development.

With both servers running you can:
1. Visit `/accounts` to connect social profiles via OAuth.
2. Compose and optimize posts with AI assistance.
3. Monitor platform health in real time through the header bell and dedicated health dashboard.
