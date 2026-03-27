# Stage 1: Build frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

# Stage 2: Run backend with frontend
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY backend/pyproject.toml backend/pyproject.toml
RUN uv sync --project backend --no-dev

COPY backend backend

# Copy frontend static output
COPY --from=frontend-builder /app/frontend/out backend/app/static

EXPOSE 8000

CMD ["uv", "run", "--project", "backend", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
