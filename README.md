# Mind-and-Health-and-Agents

The basic frontend/backend framework is set up. Specific features are yet to be developed.

## Tech Stack

- **Frontend**: React 19 + TypeScript + Vite (`frontend/`)
- **Backend**: Python + FastAPI + OpenAI Agents SDK (`backend/`)

## Project Structure

```
.
├── frontend/            # React frontend
│   ├── src/
│   │   ├── lib/api.ts   # Wrapper for backend communication
│   │   └── App.tsx      # Skeleton page (with backend connectivity check)
│   └── vite.config.ts   # /api proxy to the backend is configured
└── backend/             # FastAPI backend
    ├── app/
    │   ├── main.py               # App entry point (CORS, route mounting)
    │   ├── core/config.py        # Environment variable configuration
    │   ├── api/routes.py         # Routes (/api/health, /api/info)
    │   └── services/agent.py     # Agent framework (OpenAI Agents SDK)
    └── requirements.txt
```

## Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env   # then fill in OPENAI_API_KEY

# Start the dev server (defaults to http://127.0.0.1:8000)
uvicorn app.main:app --reload
```

API docs: after starting, visit http://127.0.0.1:8000/docs

## Frontend Setup

```powershell
cd frontend
npm install
npm run dev   # defaults to http://localhost:5173
```

Frontend `/api` requests are proxied by Vite to the backend at `http://127.0.0.1:8000`.

## Notes

This is currently only a framework skeleton:
- The Agent wrapper (`services/agent.py`) is built on the OpenAI Agents SDK and provides only a generic `run()` entry point; no business logic is implemented.
- The frontend has only a backend connectivity check page.
