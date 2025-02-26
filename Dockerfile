FROM python:3.12.5-slim AS build

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    ca-certificates \
    libgmp-dev \
    libssl-dev \
    python3-dev \
    libpq-dev && \
    apt-get clean

ENV PYTHONUNBUFFERED=True
ENV UV_PROJECT_ENVIRONMENT=/app
ENV UV_PREVIEW=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

COPY . /tmp
WORKDIR /tmp

RUN --mount=type=cache,target=/root/.cache \
    uv sync --locked --no-dev --no-editable


FROM python:3.12.5-slim

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends && \
    apt-get clean

COPY --from=build /app /app

WORKDIR /app
