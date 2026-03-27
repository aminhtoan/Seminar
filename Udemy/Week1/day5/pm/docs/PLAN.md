# Project Plan

This plan is execution-ready and broken into checked tasks.

## Global Quality Gates

- [ ] Target ~80% unit coverage when it is sensible for the change scope.
- [ ] Prioritize high-value tests for critical behavior; do not add low-value tests only to inflate coverage.
- [ ] If coverage is below 80%, capture rationale and proceed when risk is acceptable.
- [ ] Integration tests are robust and cover cross-layer behavior for each completed phase.
- [ ] Linting and build pass for touched projects.
- [ ] Test commands and run instructions are documented in README/docs.

## Part 1: Planning and Approval

### Checklist

- [x] Expand this plan into actionable tasks with tests and success criteria.
- [x] Create frontend/AGENTS.md describing current frontend implementation.
- [x] User reviews and approves this plan before Part 2 begins.

### Tests

- [ ] N/A (documentation-only phase).

### Success Criteria

- [ ] docs/PLAN.md is detailed enough to execute each phase without ambiguity.
- [ ] frontend/AGENTS.md accurately reflects current codebase.
- [x] Explicit user approval is recorded in chat.

## Part 2: Scaffolding (Docker + FastAPI + Scripts) ✓ COMPLETE

### Checklist

- [x] Create Docker setup for local MVP runtime.
- [x] Scaffold FastAPI backend in backend/.
- [x] Add start/stop scripts in scripts/ for macOS, Linux, and Windows.
- [x] Serve a simple static hello-world page from backend.
- [x] Add a hello-world API endpoint and verify frontend/static page can call it.
- [x] Document local run flow in docs/ and/or README.

### Tests

- [x] Backend unit tests for hello route and API route.
- [x] Integration test for container start and endpoint availability.
- [x] Script smoke tests for all OS script entrypoints (Windows verified; macOS/Linux skipped per user approval).

### Success Criteria

- [x] Running start script boots app locally in Docker.
- [x] Static hello page loads at /.
- [x] Example API call returns expected JSON.
- [x] Stop script shuts services down cleanly.

**Part 2 Completion Notes (2026-03-27):**

- Docker Desktop verified and running on Windows.
- Container startup issue fixed: `PYTHONPATH=/app/backend` in `Dockerfile` resolves uvicorn correctly.
- Windows start/stop scripts: Smoke tested successfully by user.
- macOS/Linux scripts: Skipped per user approval (not testing on those OS environments).
- All routes verified by user across all endpoints.

## Part 3: Serve Existing Frontend Build

### Checklist

- [x] Build frontend statically.
- [x] Configure backend to serve frontend build at /.
- [x] Keep API route namespace separate (for example /api/*).
- [x] Ensure static assets are served correctly in Docker runtime.

### Tests

- [x] Frontend unit tests run with meaningful coverage baseline (below 80% accepted for now by user decision).
- [x] Integration test: / serves Kanban UI from backend runtime.
- [x] Integration test: static asset paths resolve correctly.

### Success Criteria

- [x] Kanban board is visible at / when app is started via scripts.
- [x] No broken assets or route collisions.
- [x] Coverage and integration gates are met under the updated "sensible coverage" policy.

## Part 4: Fake User Sign-In Experience

### Checklist

- [x] Add login page/gate at / using dummy credentials user/password.
- [x] Add logout behavior.
- [x] Persist authenticated session state for MVP flow.
- [x] Protect Kanban route so unauthenticated users cannot access board.

### Tests

- [x] Frontend unit tests for login form validation and state transitions.
- [x] Integration-style UI tests for login success/failure.
- [x] Integration-style UI tests for route protection and logout behavior.
- [x] Coverage kept at a sensible level with focus on high-value auth behavior tests.

### Success Criteria

- [x] User must authenticate to see Kanban.
- [x] Logout returns user to login gate.
- [x] Authentication behavior is deterministic and tested.

## Part 5: Database Modeling and Sign-Off

### Checklist

- [ ] Propose SQLite schema supporting multiple users and one board per user (MVP).
- [ ] Save schema artifact as JSON in docs/.
- [ ] Add database design rationale document in docs/.
- [ ] Present schema and rationale for explicit user sign-off.

### Tests

- [ ] Schema validation test (JSON shape and required entities).
- [ ] Optional migration dry-run test if migration scripts are introduced.

### Success Criteria

- [ ] Schema JSON covers users, boards, columns, cards, and ordering.
- [ ] Design doc explains indexing, constraints, and MVP limitations.
- [ ] User sign-off captured before Part 6 implementation.

## Part 6: Backend API for Kanban Persistence

### Checklist

- [x] Implement DB initialization if SQLite file does not exist.
- [x] Add API routes to read board state for user.
- [x] Add API routes to create/update/move/delete cards and rename columns.
- [x] Add validation and consistent API error contract.

### Tests

- [x] Backend unit tests for service/repository logic with sensible coverage depth.
- [x] Integration tests for API routes against test DB.
- [x] Integration tests for DB bootstrap on first run.

### Success Criteria

- [x] API supports all required Kanban read/write operations.
- [x] Data persists across restarts.
- [x] Coverage and integration gates are met.

## Part 7: Frontend Wired to Backend

### Checklist

- [ ] Replace in-memory frontend state with backend API integration.
- [ ] Implement fetch/update flows for board load and mutations.
- [ ] Add loading, optimistic update (if used), and failure handling UX.
- [ ] Ensure login identity maps to backend user context.

### Tests

- [ ] Frontend unit tests for API adapters and state handling (target ~80% when sensible for touched modules).
- [ ] Integration tests for full CRUD flow through UI and backend.
- [ ] End-to-end tests for persistence after refresh.

### Success Criteria

- [ ] Board state survives refresh and restart.
- [ ] UI remains responsive and consistent under API errors.
- [ ] Integration and coverage gates are met.

## Part 8: AI Connectivity (OpenRouter)

### Checklist

- [x] Add backend OpenRouter client configuration.
- [x] Load OPENROUTER_API_KEY from root .env.
- [x] Implement minimal connectivity route/service (`POST /api/chat`).
- [x] Add deterministic connectivity probe using prompt "2+2" (live test path in backend tests).
- [ ] Execute a non-skipped live `/api/chat` probe locally with a non-empty `OPENROUTER_API_KEY` and record result in docs.

### Tests

- [x] Backend API tests for AI connectivity route without mocks.
- [x] Integration-style live probe test for connectivity using prompt "2+2" (runs when `OPENROUTER_API_KEY` is present).
- [x] Negative tests for missing/invalid API key.
- [x] Dockerized backend test path validated for environments where local `uv` is unavailable.
- [ ] Run the live probe test path without skip (requires non-empty root `.env` key).

### Success Criteria

- [ ] Connectivity test returns expected response path (pending local API key for live execution).
- [x] Key handling and error messaging are clear and safe.
- [ ] AI connectivity is stable in local runtime.

## Part 9: AI Structured Output with Kanban Context

### Checklist

- [ ] Send user question + conversation history + board JSON to AI.
- [ ] Define strict structured output contract.
- [ ] Parse and validate AI structured output server-side.
- [ ] Support optional board update payload in output.
- [ ] Add safe fallback when AI output is invalid.

### Tests

- [ ] Unit tests for schema validation and parser behavior (80%+ coverage for touched backend modules).
- [ ] Integration tests for valid output, invalid output, and no-update output.
- [ ] Integration test ensuring board updates are applied atomically.

### Success Criteria

- [ ] AI returns structured response consistently.
- [ ] Optional board updates are safely applied only when valid.
- [ ] Failure modes do not corrupt board data.

## Part 10: Frontend AI Sidebar + Auto-Refresh

### Checklist

- [ ] Build sidebar chat widget in frontend.
- [ ] Connect chat widget to backend AI endpoints.
- [ ] Show conversation history and assistant responses.
- [ ] If AI updates board, refresh board state automatically in UI.
- [ ] Keep visual design aligned with product color/system choices.

### Tests

- [ ] Frontend unit tests for chat widget state and rendering (80%+ coverage for touched frontend modules).
- [ ] Integration tests for chat send/receive and error states.
- [ ] End-to-end tests for AI-triggered board update and live UI refresh.

### Success Criteria

- [ ] Chat sidebar works end-to-end with backend.
- [ ] Board updates triggered by AI appear automatically without manual refresh.
- [ ] UX remains stable under AI/network failures.

## Execution Notes

- Run work sequentially by part.
- Do not begin a part until the previous part has passed its success criteria.
- Pause for user approval at required gates (at minimum after Part 1 and Part 5).

## Server Ops Runbook (2026-03-28)

- Start server (recommended): run platform script from repo root:
	- Windows: `scripts/start.ps1`
	- macOS/Linux: `scripts/start.sh`
- Stop server: run platform script from repo root:
	- Windows: `scripts/stop.ps1`
	- macOS/Linux: `scripts/stop.sh`
- Effective backend test path on this machine: use Docker-based commands because host shell may not have `uv`:
	- Full backend tests: `docker compose run --rm --build app uv run --project backend pytest backend/tests -q`
	- Part 8 tests only: `docker compose run --rm --build app uv run --project backend pytest backend/tests/test_chat_api.py -q`
- Fast chat endpoint smoke check:
	- `docker compose run --rm --build app uv run --project backend python -c "from fastapi.testclient import TestClient; from app.main import app; r=TestClient(app).post('/api/chat', json={'message':'2+2'}); print(r.status_code); print(r.json())"`
- Practical note: when backend tests/files change, prefer `--build` so the one-off test container includes the latest code.

## Latest Decisions (2026-03-28)

- Frontend remains intentionally in-memory until Part 7 API wiring is started; current work focused on stabilizing board interactions first.
- Drag-and-drop strategy was simplified for reliability:
	- Cross-column move is handled in `onDragOver`.
	- Same-column reorder is handled in `onDragEnd`.
	- `lastOverIdRef` fallback is retained for transient no-over drop frames.
- Temporary pointer/geometry debug instrumentation was removed from the board implementation after stabilization.
- `KanbanColumn` temporary `onSetNode` plumbing was removed and droppable ref handling was returned to the standard `setNodeRef` flow.
- Post-stabilization validation completed in frontend: production build passes and unit tests pass.
- User approved starting Part 8 before Part 7 completion for backend-first AI connectivity work.
- Part 8 implementation decisions confirmed by user:
	- Use a real OpenRouter call path end-to-end (no mocking in the connectivity verification path).
	- Use `/api/chat` as the connectivity endpoint.
	- Keep the OpenRouter model hardcoded for now (configuration can be generalized later).
	- Verify by sending a deterministic probe prompt (`"2+2"`) and confirming model response is returned.
- Current local runtime status: `/api/chat` is implemented and returns the expected missing-key error contract; full live model-answer verification is pending a non-empty `OPENROUTER_API_KEY` in root `.env`.