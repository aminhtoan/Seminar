import os
from pathlib import Path
from typing import Any

import httpx

ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT_DIR / ".env"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openai/gpt-oss-120b"


def load_openrouter_api_key_from_env_file() -> None:
    if "OPENROUTER_API_KEY" in os.environ or not ENV_FILE.exists():
        return

    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        if key.strip() != "OPENROUTER_API_KEY":
            continue

        cleaned = value.strip().strip('"').strip("'")
        os.environ["OPENROUTER_API_KEY"] = cleaned
        return


load_openrouter_api_key_from_env_file()


class OpenRouterError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


class OpenRouterClient:
    def __init__(self, api_key: str | None = None, model: str = OPENROUTER_MODEL) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("OPENROUTER_API_KEY")
        self.model = model

    async def chat(self, message: str) -> dict[str, str]:
        if not self.api_key:
            raise OpenRouterError(
                status_code=503,
                code="openrouter_api_key_missing",
                message="OPENROUTER_API_KEY is not configured",
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "PM MVP",
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ],
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        except httpx.RequestError as exc:
            raise OpenRouterError(
                status_code=502,
                code="openrouter_unreachable",
                message="Failed to reach OpenRouter",
                details=str(exc),
            ) from exc

        if response.status_code >= 400:
            details: Any
            try:
                details = response.json()
            except ValueError:
                details = response.text

            message_text = "OpenRouter request failed"
            if isinstance(details, dict):
                error_payload = details.get("error", {})
                message_text = error_payload.get("message", message_text)

            if response.status_code in (401, 403):
                raise OpenRouterError(
                    status_code=response.status_code,
                    code="openrouter_auth_failed",
                    message=message_text,
                    details=details,
                )

            raise OpenRouterError(
                status_code=502,
                code="openrouter_request_failed",
                message=message_text,
                details=details,
            )

        data = response.json()
        choices = data.get("choices", [])
        first_choice = choices[0] if choices else {}
        answer = first_choice.get("message", {}).get("content", "")

        if not answer:
            raise OpenRouterError(
                status_code=502,
                code="openrouter_invalid_response",
                message="OpenRouter response did not include assistant content",
                details=data,
            )

        return {
            "model": data.get("model", self.model),
            "answer": answer,
        }
