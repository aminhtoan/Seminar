
=======
# Finally — AI Trading Workstation
>>>>>>> 33be1fd047b659c84db06c5319f2362a14775bfa

FinAlly is an AI-assisted trading workstation built as an agentic coding project. The target product is a single-container app with a FastAPI backend, a Next.js frontend, live market data over SSE, a simulated portfolio, and an LLM-powered trading assistant.

## Status

This repository is still implementation-in-progress.

- `backend/` contains the active Python/FastAPI codebase
- `frontend/` is planned in the project spec but is not present yet
- `planning/PLAN.md` is the primary product and architecture document
- `planning/REVIEW.md` contains review feedback on the current plan

## Target Stack

- Backend: FastAPI + Python + `uv`
- Frontend: Next.js + TypeScript
- Data: SQLite
- Realtime: Server-Sent Events
- AI: LiteLLM via OpenRouter

## Repo Layout

```text
finally/
|- backend/
|- planning/
|- independent-reviewer/
|- hook/
|- .github/
|- .claude/
`- README.md
```

## Local Development

Current local backend flow:

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

Then open `http://localhost:8000`.

## Environment Variables

- `OPENROUTER_API_KEY` for live LLM chat
- `MASSIVE_API_KEY` for optional real market data
- `LLM_MOCK=true` for deterministic mock LLM behavior

## References

- Project plan: `planning/PLAN.md`
- Plan review: `planning/REVIEW.md`
- Backend notes: `backend/README.md`
