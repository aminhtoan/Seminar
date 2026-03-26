from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="PM MVP Backend")

INDEX_FILE = Path(__file__).parent / "static" / "index.html"


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    return INDEX_FILE.read_text(encoding="utf-8")


@app.get("/api/hello")
async def hello() -> dict[str, str]:
    return {
        "message": "hello world from fastapi",
        "status": "ok",
    }
