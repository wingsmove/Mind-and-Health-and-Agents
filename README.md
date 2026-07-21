# Mind-and-Health-and-Agents

A mental-health & wellness assistant powered by a two-agent pipeline built on the
OpenAI Agents SDK. The user describes their situation, and the backend runs two
agents in sequence:

1. **Message Agent** — replies to the user with helpful, non-diagnostic guidance
   (may use screening forms such as PHQ-9, GAD-7, PHQ-2).
2. **Report Agent** — using the user input and the Message Agent's reply,
   generates a Markdown research report intended for researchers/professionals
   (should not be shown to the user but shown on the frontend for now for debug usage).

> Disclaimer: this project does not provide medical diagnosis or treatment.

## Tech Stack

- **Frontend**: React 19 + TypeScript + Vite (`frontend/`)
- **Backend**: Python + FastAPI + OpenAI Agents SDK (`backend/`)

## Project Structure

```
.
├── frontend/            # React frontend
│   ├── src/
│   │   ├── api.ts       # Backend base URL + response types
│   │   ├── App.tsx      # Chat UI: input, agent reply, and report
│   │   └── App.css
│   └── vite.config.ts
└── backend/             # FastAPI backend
    ├── app/
    │   ├── main.py               # App entry point (CORS, routes, /analyze)
    │   ├── schemas.py            # AnalyzeRequest / AnalyzeResponse models
    │   ├── core/config.py        # Environment variable configuration
    │   ├── api/routes.py         # Routes (/api/health, /api/info)
    │   └── services/agent.py     # Agent framework + message/report agents
    ├── requirements.txt
    └── .env.example
```

## API

- `POST /analyze` — body `{ "message": "..." }`, returns `{ "content": "...", "report": "..." }`
- `GET /api/health` — health check
- `GET /api/info` — basic runtime info (app name, model, whether the key is configured)

## Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env   # then fill in OPENAI_API_KEY (and optionally OPENAI_MODEL)

# Start the dev server (defaults to http://127.0.0.1:8000)
uvicorn app.main:app --reload
```

API docs: after starting, visit http://127.0.0.1:8000/docs

### Environment variables (`backend/.env`)

- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL` (default `gpt-4o-mini`)
- `OPENAI_BASE_URL` (optional, for proxies / OpenAI-compatible providers)
- `CORS_ORIGINS` (comma-separated allowed frontend origins)

## Frontend Setup

```powershell
cd frontend
npm install
npm run dev   # defaults to http://localhost:5173 (falls back to 5174 if in use)
```

The frontend calls the backend directly at `http://localhost:8000` (see `src/api.ts`),
so the backend must allow the frontend's origin via `CORS_ORIGINS`. If Vite starts on
a different port (e.g. 5174), add that origin to `CORS_ORIGINS`.

## Notes

- `/analyze` runs two agents sequentially, so a single request can take a while
  depending on the model.
- Never commit `backend/.env`; it contains your real API key (it is already
  covered by `.gitignore`).

## Develop notes
This is my second time trying Full-Stack programming.
This time I only used a generated framework and done most of the work by myself.
AI models only helped with debugging in this project.
I want to make this project a more useful one and hopefully start doing an actual research based on this topic.
