# Project Plan

This plan is execution-ready and broken into checked tasks.

## Global Quality Gates

- [ ] Unit test coverage is at least 80% for each relevant package before completion.
- [ ] Integration tests are robust and cover cross-layer behavior for each completed phase.
- [ ] Linting and build pass for touched projects.
- [ ] Test commands and run instructions are documented in README/docs.

## Part 1: Planning and Approval

### Checklist

- [x] Expand this plan into actionable tasks with tests and success criteria.
- [x] Create frontend/AGENTS.md describing current frontend implementation.
- [ ] User reviews and approves this plan before Part 2 begins.

### Tests

- [ ] N/A (documentation-only phase).

### Success Criteria

- [ ] docs/PLAN.md is detailed enough to execute each phase without ambiguity.
- [ ] frontend/AGENTS.md accurately reflects current codebase.
- [ ] Explicit user approval is recorded in chat.

## Part 2: Scaffolding (Docker + FastAPI + Scripts)

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
- [ ] Script smoke tests for each OS script entrypoint.

### Success Criteria

- [x] Running start script boots app locally in Docker.
- [x] Static hello page loads at /.
- [x] Example API call returns expected JSON.
- [x] Stop script shuts services down cleanly.

Part 2 validation notes:

- Docker Desktop is now available on this machine and container runtime checks were executed on 2026-03-27.
- Container startup issue was fixed by setting `PYTHONPATH=/app/backend` in `Dockerfile` so `uvicorn app.main:app` resolves correctly in Docker.
- Windows start/stop scripts were smoke tested successfully. macOS/Linux script smoke tests remain pending on their respective OS environments.

## Part 3: Serve Existing Frontend Build

### Checklist

- [ ] Build frontend statically.
- [ ] Configure backend to serve frontend build at /.
- [ ] Keep API route namespace separate (for example /api/*).
- [ ] Ensure static assets are served correctly in Docker runtime.

### Tests

- [ ] Frontend unit tests pass with at least 80% coverage.
- [ ] Integration test: / serves Kanban UI from backend runtime.
- [ ] Integration test: static asset paths resolve correctly.

### Success Criteria

- [ ] Kanban board is visible at / when app is started via scripts.
- [ ] No broken assets or route collisions.
- [ ] Coverage and integration gates are met.

## Part 4: Fake User Sign-In Experience

### Checklist

- [ ] Add login page/gate at / using dummy credentials user/password.
- [ ] Add logout behavior.
- [ ] Persist authenticated session state for MVP flow.
- [ ] Protect Kanban route so unauthenticated users cannot access board.

### Tests

- [ ] Frontend unit tests for login form validation and state transitions.
- [ ] Integration tests for login success/failure.
- [ ] Integration tests for route protection and logout behavior.
- [ ] Preserve at least 80% frontend unit coverage.

### Success Criteria

- [ ] User must authenticate to see Kanban.
- [ ] Logout returns user to login gate.
- [ ] Authentication behavior is deterministic and tested.

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

- [ ] Implement DB initialization if SQLite file does not exist.
- [ ] Add API routes to read board state for user.
- [ ] Add API routes to create/update/move/delete cards and rename columns.
- [ ] Add validation and consistent API error contract.

### Tests

- [ ] Backend unit tests for service/repository logic (target 80%+ coverage).
- [ ] Integration tests for API routes against test DB.
- [ ] Integration tests for DB bootstrap on first run.

### Success Criteria

- [ ] API supports all required Kanban read/write operations.
- [ ] Data persists across restarts.
- [ ] Coverage and integration gates are met.

## Part 7: Frontend Wired to Backend

### Checklist

- [ ] Replace in-memory frontend state with backend API integration.
- [ ] Implement fetch/update flows for board load and mutations.
- [ ] Add loading, optimistic update (if used), and failure handling UX.
- [ ] Ensure login identity maps to backend user context.

### Tests

- [ ] Frontend unit tests for API adapters and state handling (80%+ coverage).
- [ ] Integration tests for full CRUD flow through UI and backend.
- [ ] End-to-end tests for persistence after refresh.

### Success Criteria

- [ ] Board state survives refresh and restart.
- [ ] UI remains responsive and consistent under API errors.
- [ ] Integration and coverage gates are met.

## Part 8: AI Connectivity (OpenRouter)

### Checklist

- [ ] Add backend OpenRouter client configuration.
- [ ] Load OPENROUTER_API_KEY from root .env.
- [ ] Implement minimal connectivity route/service.
- [ ] Add deterministic connectivity probe using prompt "2+2".

### Tests

- [ ] Backend unit tests for AI client wrapper (mocked).
- [ ] Integration test for live/mocked connectivity pathway.
- [ ] Negative tests for missing/invalid API key.

### Success Criteria

- [ ] Connectivity test returns expected response path.
- [ ] Key handling and error messaging are clear and safe.
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