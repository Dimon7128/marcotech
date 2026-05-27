# syntax=docker/dockerfile:1.7
#
# Backend container — FastAPI + uvicorn.
# Matches the image base advertised in README ("python:3.12-slim").
# Listens on 8000 and is wired up by docker-compose.yml.

FROM python:3.12-slim

# Keep Python lean inside the container:
#   - no .pyc files left behind on the bind-mounted volumes
#   - stdout/stderr flushed immediately so `docker logs` is live
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install deps first so this layer is cached when only source code changes.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source. We deliberately copy individual modules instead
# of `COPY . .` so a stray local file (e.g. .env) cannot end up in the image.
COPY main.py openai_client.py food_storage.py ./

# The CSV "data tier". docker-compose bind-mounts ./backend/data on top of
# this at runtime, but having the directory in the image means the app can
# also run standalone (e.g. `docker run`) without crashing on startup.
RUN mkdir -p /app/data
VOLUME ["/app/data"]

# Drop root — uvicorn does not need it.
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# `--host 0.0.0.0` is required so the port is reachable from outside the
# container. No `--reload` here: this image is for prod/staging too.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
