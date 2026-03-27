import os

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.openrouter_client import OpenRouterClient


def test_chat_returns_error_when_api_key_missing() -> None:
    original_client = app.state.openrouter_client

    try:
        app.state.openrouter_client = OpenRouterClient(api_key="")
        with TestClient(app) as client:
            response = client.post("/api/chat", json={"message": "2+2"})
    finally:
        app.state.openrouter_client = original_client

    assert response.status_code == 503
    payload = response.json()
    assert payload["error"]["code"] == "openrouter_api_key_missing"


@pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY is required for live OpenRouter probe",
)
def test_chat_live_probe_returns_model_answer() -> None:
    original_client = app.state.openrouter_client

    try:
        app.state.openrouter_client = OpenRouterClient()
        with TestClient(app) as client:
            response = client.post("/api/chat", json={"message": "2+2"})
    finally:
        app.state.openrouter_client = original_client

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["model"] == "openai/gpt-oss-120b"
    assert payload["answer"].strip()
    assert "4" in payload["answer"]


@pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="Network/live OpenRouter checks are skipped without OPENROUTER_API_KEY",
)
def test_chat_with_invalid_key_returns_auth_error() -> None:
    original_client = app.state.openrouter_client

    try:
        app.state.openrouter_client = OpenRouterClient(api_key="invalid-openrouter-key")
        with TestClient(app) as client:
            response = client.post("/api/chat", json={"message": "2+2"})
    finally:
        app.state.openrouter_client = original_client

    payload = response.json()
    assert response.status_code in (401, 403, 502)
    assert payload["error"]["code"] in (
        "openrouter_auth_failed",
        "openrouter_request_failed",
        "openrouter_unreachable",
    )
