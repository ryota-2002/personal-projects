FROM ghcr.io/astral-sh/uv:0.11.13 AS uv

FROM python:3.14.5-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# uv.lock に固定された依存関係だけを先にインストールする。
COPY --from=uv /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY app/ ./app/

RUN useradd --no-create-home --uid 10001 appuser
USER appuser

CMD ["python", "app/main.py"]
