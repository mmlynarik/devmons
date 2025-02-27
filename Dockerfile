FROM python:3.12.5-slim AS build

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


FROM python:3.12.5-slim

WORKDIR /app

COPY --from=build /app /app

ENV PATH=/app/bin:$PATH

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "lib/python3.12/site-packages/devmons/app.py"]
