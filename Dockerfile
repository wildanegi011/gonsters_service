# ===============================
# Stage 1 — Builder
# ===============================
FROM python:3.12-slim AS builder

# Install security essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files only → better caching
COPY pyproject.toml uv.lock ./

# Pre-install dependencies into global uv cache
RUN uv sync --frozen --no-cache

# Copy the rest of the app (source code)
COPY . .

# ===============================
# Stage 2 — Runtime
# ===============================
FROM python:3.12-slim AS runtime

# Create non-root user (best practice)
RUN adduser --disabled-password --gecos "" appuser

# Install uv (only 6 MB)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy app INCLUDING uv’s global cache
COPY --from=builder /app /app

RUN RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs

USER appuser

# Optimize Python runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=2 \
    UV_SYSTEM_PYTHON=1

EXPOSE 8000

# Use production-ready Uvicorn settings
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers"]
