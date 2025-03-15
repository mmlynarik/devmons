FROM python:3.13.2-slim AS base

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    ca-certificates && \
    apt-get clean

ENV PYTHONUNBUFFERED=True
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

COPY . /tmp
WORKDIR /tmp

RUN --mount=type=cache,target=/root/.cache \
    uv sync --locked --no-dev --no-editable


FROM python:3.13.2-slim AS ci
WORKDIR /app
COPY --from=base /app /app
ENV PATH="/app/bin:$PATH"
CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "src/devmons/app.py"]


FROM python:3.13.2-slim AS prod
COPY --from=base /app /app
WORKDIR /app
ENV PATH="/app/bin:$PATH"
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "lib/python3.13/site-packages/devmons/app.py"]
