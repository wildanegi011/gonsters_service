# ===== Stage 1: Builder =====
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy project files
COPY . .

# Pre-install all dependencies into uv's global cache
RUN uv sync --frozen --no-cache


# ===== Stage 2: Runtime =====
FROM python:3.12-slim AS runtime

# Install uv (kecil sekali ±6MB)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy source code (tanpa virtualenv)
COPY --from=builder /app /app

EXPOSE 8000

# Jalankan via uv run (lebih cepat, tidak butuh .venv)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
