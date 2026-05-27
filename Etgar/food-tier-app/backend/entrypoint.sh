#!/bin/sh
# Container entrypoint.
#
# Decision tree at startup:
#
#   1. OPENAI_API_KEY already set in the environment?
#        -> Skip everything. This is the local-dev path: docker-compose
#           passes the key in from your .env file.
#
#   2. OPENAI_API_KEY unset AND OPENAI_PARAM_NAME set?
#        -> Production path. Call SSM Parameter Store via the EC2's
#           instance profile, export the returned value as
#           OPENAI_API_KEY, then run the original CMD (uvicorn).
#
#   3. Both unset?
#        -> Skip. The backend will boot fine and /health will work; the
#           first POST /api/food-tier will return a clear 502 with the
#           "OPENAI_API_KEY is not set" message from openai_client.py.
#
# This script intentionally does NOT fail when the SSM lookup errors —
# we'd rather have the backend up so /health responds (and the failure
# is surfaced per-request with the existing OpenAIClassificationError
# message) than crash-loop the whole container.
set -e

if [ -z "${OPENAI_API_KEY:-}" ] && [ -n "${OPENAI_PARAM_NAME:-}" ]; then
    echo "[entrypoint] fetching OPENAI_API_KEY from SSM parameter ${OPENAI_PARAM_NAME}" >&2
    if FETCHED="$(python /app/fetch_secret.py)"; then
        export OPENAI_API_KEY="${FETCHED}"
        echo "[entrypoint] OPENAI_API_KEY loaded from SSM" >&2
    else
        echo "[entrypoint] SSM fetch failed — backend will start anyway" >&2
        echo "[entrypoint] /api/food-tier will return 502 until the key is reachable" >&2
    fi
fi

exec "$@"
