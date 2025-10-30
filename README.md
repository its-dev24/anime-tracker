# Anime Tracker

A small FastAPI service for tracking anime (starter project).

This repository contains a minimal FastAPI application with a healthcheck route. It's intended as a starting point for building an anime-tracking backend or learning FastAPI.

## What’s included

- `app/server.py` — FastAPI application instance (`app`) and router registration.
- `app/routes/healthcheck.py` — Health check router mounted at `/healthcheck/`.
- `anime-env/` — A Python virtual environment (already present in the repo). Use it or create your own.

## Prerequisites

- Python 3.11 (recommended; venv in this repo was created with Python 3.11)
- pip
- Optional: use the included virtual environment at `anime-env/`.

If you don't want to use the included venv, create one:

```powershell
# Windows PowerShell (recommended)
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install --upgrade pip
pip install fastapi uvicorn
```

If you prefer to use the provided environment, activate it:

```powershell
# Activate the provided venv (PowerShell)
.\\anime-env\\Scripts\\Activate.ps1
```

> Note: The repo doesn't include a `requirements.txt`. If you modify dependencies, consider adding one via `pip freeze > requirements.txt`.

## Running the app (development)

The FastAPI application instance is named `app` in `app/server.py`.
Start the development server with Uvicorn from the repository root:

```powershell
# From repo root (PowerShell)
uvicorn app.server:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs` to view the interactive Swagger UI or `http://127.0.0.1:8000/redoc` for ReDoc.

## Healthcheck endpoint

A simple health endpoint is provided in `app/routes/healthcheck.py`.

- Path: `GET /healthcheck/`
- Example response:

```json
{
  "detail": "Server Health Good"
}
```

## Project Structure

```
README.md
anime-env/                 # Included virtualenv (optional)
app/
	server.py                # FastAPI app instance and router registration
	routes/
		healthcheck.py         # /healthcheck/ endpoint
```

## Development notes & next steps

- Add a `requirements.txt` or `pyproject.toml` if you plan to share this project or deploy it.
- Add more routes (auth, users, anime models) and tests.
- Add CI to run linting and tests.

## License & contact

Add license info here if you want to open-source the project.

---

Generated README — tailored to the current repository layout and `app/server.py` implementation.
