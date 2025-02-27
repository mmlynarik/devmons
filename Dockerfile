FROM python:3.12.5-slim AS base

WORKDIR /app

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    ca-certificates \
    libgmp-dev \
    libssl-dev \
    libpq-dev && \
    apt-get clean

ENV PYTHONUNBUFFERED=True

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

COPY . /app

RUN --mount=type=cache,target=/root/.cache \
    uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"


FROM base AS dev
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --dev
CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "src/devmons/app.py"]


FROM base AS prod
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "src/devmons/app.py"]
