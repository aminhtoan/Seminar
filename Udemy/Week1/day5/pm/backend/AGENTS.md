# Backend Code Description

## Purpose

The backend hosts the initial FastAPI scaffold for the PM MVP. In Part 2 it provides:

- Static hello page at /
- Example API endpoint at /api/hello
- Backend tests for both routes

## Structure

- backend/pyproject.toml
	- Python project config and dependencies
	- Runtime: fastapi, uvicorn
	- Dev/test: pytest, pytest-cov, httpx
- backend/app/main.py
	- FastAPI app entrypoint
	- Route: GET /
	- Route: GET /api/hello
- backend/app/static/index.html
	- Simple static HTML that fetches /api/hello from the same origin
- backend/tests/test_main.py
	- Unit/API tests for route behavior

## Runtime

- App is containerized through root Dockerfile and docker-compose.yml
- Uvicorn serves app.main:app on port 8000

## Testing

- Run backend tests in container:
	- docker compose run --rm app uv run --project backend pytest backend/tests
