FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY backend/pyproject.toml backend/pyproject.toml
RUN uv sync --project backend --no-dev

COPY backend backend

EXPOSE 8000

CMD ["uv", "run", "--project", "backend", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
