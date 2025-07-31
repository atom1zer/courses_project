FROM python:3.12.1-alpine

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app/backend

# COPY --link --from=ghcr.io/astral-sh/uv:0.4 /uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:0.6.9 /uv /uvx /bin/
COPY ./backend /app/backend

RUN uv add gunicorn
RUN uv sync

RUN chmod +x /app/backend/docker/server-entrypoint.sh
RUN chmod +x /app/backend/docker/worker-entrypoint.sh
