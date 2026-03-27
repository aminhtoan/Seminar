from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, model_validator

from app.kanban_repository import KanbanRepository, RepositoryError
from app.openrouter_client import OpenRouterClient, OpenRouterError


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.repo.initialize()
    yield

app = FastAPI(title="PM MVP Backend", lifespan=lifespan)
app.state.repo = KanbanRepository()
app.state.openrouter_client = OpenRouterClient()

STATIC_DIR = Path(__file__).parent / "static"
INDEX_FILE = STATIC_DIR / "index.html"


class RenameColumnRequest(BaseModel):
    user: str = "user"
    title: str = Field(min_length=1)


class CreateCardRequest(BaseModel):
    user: str = "user"
    columnId: str = Field(min_length=1)
    title: str = Field(min_length=1)
    details: str = "No details yet."


class UpdateCardRequest(BaseModel):
    user: str = "user"
    title: str | None = None
    details: str | None = None

    @model_validator(mode="after")
    def validate_payload(self) -> "UpdateCardRequest":
        if self.title is None and self.details is None:
            raise ValueError("Provide at least one field to update")
        return self


class MoveCardRequest(BaseModel):
    user: str = "user"
    toColumnId: str = Field(min_length=1)
    toIndex: int = Field(ge=0)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "invalid_request",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict):
        error = exc.detail
    else:
        error = {"code": "http_error", "message": str(exc.detail)}
    return JSONResponse(status_code=exc.status_code, content={"error": error})


def handle_repository_error(exc: RepositoryError) -> None:
    raise HTTPException(
        status_code=exc.status_code,
        detail={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
    )


def handle_openrouter_error(exc: OpenRouterError) -> None:
    raise HTTPException(
        status_code=exc.status_code,
        detail={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
    )


@app.get("/api/hello")
async def hello() -> dict[str, str]:
    return {
        "message": "hello world from fastapi",
        "status": "ok",
    }


@app.get("/api/board")
async def read_board(user: str = Query(default="user")) -> dict:
    try:
        return app.state.repo.get_board(user)
    except RepositoryError as exc:
        handle_repository_error(exc)


@app.post("/api/chat")
async def chat(payload: ChatRequest) -> dict[str, str]:
    try:
        response = await app.state.openrouter_client.chat(payload.message)
        return {
            "status": "ok",
            "model": response["model"],
            "answer": response["answer"],
        }
    except OpenRouterError as exc:
        handle_openrouter_error(exc)


@app.patch("/api/columns/{column_id}")
async def rename_column(column_id: str, payload: RenameColumnRequest) -> dict:
    try:
        return app.state.repo.rename_column(payload.user, column_id, payload.title)
    except RepositoryError as exc:
        handle_repository_error(exc)


@app.post("/api/cards")
async def create_card(payload: CreateCardRequest) -> dict:
    card_id = f"card-{uuid4().hex[:12]}"
    try:
        return app.state.repo.create_card(
            payload.user,
            payload.columnId,
            card_id,
            payload.title,
            payload.details,
        )
    except RepositoryError as exc:
        handle_repository_error(exc)


@app.patch("/api/cards/{card_id}")
async def update_card(card_id: str, payload: UpdateCardRequest) -> dict:
    try:
        return app.state.repo.update_card(payload.user, card_id, payload.title, payload.details)
    except RepositoryError as exc:
        handle_repository_error(exc)


@app.post("/api/cards/{card_id}/move")
async def move_card(card_id: str, payload: MoveCardRequest) -> dict:
    try:
        return app.state.repo.move_card(payload.user, card_id, payload.toColumnId, payload.toIndex)
    except RepositoryError as exc:
        handle_repository_error(exc)


@app.delete("/api/cards/{card_id}")
async def delete_card(card_id: str, user: str = Query(default="user")) -> dict:
    try:
        return app.state.repo.delete_card(user, card_id)
    except RepositoryError as exc:
        handle_repository_error(exc)


# Mount static files (Next.js build output)
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
else:
    # Fallback for development without frontend build
    @app.get("/", response_class=HTMLResponse)
    async def root() -> str:
        if INDEX_FILE.exists():
            return INDEX_FILE.read_text(encoding="utf-8")
        return "<h1>PM MVP Backend - Frontend not built</h1>"
