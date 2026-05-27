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
#   entrypoint.sh + fetch_secret.py implement the "fetch OPENAI_API_KEY
#   from SSM Parameter Store on EC2" path. They no-op when OPENAI_API_KEY
#   is already in the environment (local dev via .env).
COPY main.py openai_client.py food_storage.py fetch_secret.py entrypoint.sh ./
RUN chmod +x /app/entrypoint.sh

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

# Entrypoint wraps the CMD: it loads OPENAI_API_KEY from SSM if needed
# and then exec's whatever is in CMD. Keeping CMD as the uvicorn line
# means `docker run <image> python -c '...'` still works for debugging.
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
