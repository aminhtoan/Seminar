# Part 2 Scaffolding Guide

## What was scaffolded

- Dockerized FastAPI backend
- Static hello page at /
- API hello endpoint at /api/hello
- Start/stop scripts for Windows, macOS, Linux
- Backend tests for both routes

## Run

From project root:

- Windows PowerShell:
  - ./scripts/start.ps1
- macOS/Linux:
  - ./scripts/start.sh

App URL:

- http://localhost:8000

## Verify

- Open http://localhost:8000 and confirm the page says PM MVP Hello World.
- Confirm page shows API result from GET /api/hello.
- Optional direct API check:
  - http://localhost:8000/api/hello

## Test

Run backend tests in container:

- docker compose run --rm app uv run --project backend pytest backend/tests

## Stop

From project root:

- Windows PowerShell:
  - ./scripts/stop.ps1
- macOS/Linux:
  - ./scripts/stop.sh
