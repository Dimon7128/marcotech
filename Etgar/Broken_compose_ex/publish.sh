#!/usr/bin/env bash
#
# Build (and optionally push) the web-app image used by the
# "Fix the Broken Compose Stack" exercise.
#
# The other three services in the stack (nginx, postgres, redis) are
# already published on Docker Hub. Only the custom Flask app needs to
# be built and shared. Students who pull this image can then run the
# whole exercise without ever having the ./broken-stack/web source.
#
# Usage:
#   ./publish.sh                                # dimabu/motd-web:latest, build only
#   ./publish.sh dimabu/motd-web                # dimabu/motd-web:latest, build only
#   ./publish.sh dimabu/motd-web v1             # dimabu/motd-web:v1,     build only
#   PUSH=1 ./publish.sh dimabu/motd-web latest  # build AND push to Docker Hub
#
# You can also override the default repo via env var:
#   REPO=someoneelse/motd-web ./publish.sh
#
# Before pushing, make sure you have authenticated:
#   docker login
#

set -euo pipefail

REPO="${1:-${REPO:-dimabu/motd-web}}"
TAG="${2:-latest}"
IMAGE="${REPO}:${TAG}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXT="${SCRIPT_DIR}/broken-stack/web"

if [[ ! -d "${CONTEXT}" ]]; then
    echo "ERROR: build context ${CONTEXT} not found." >&2
    exit 2
fi

echo ">> Building ${IMAGE} from ${CONTEXT}"
docker build -t "${IMAGE}" "${CONTEXT}"

echo ">> Quick smoke test: import the app inside the freshly built image"
docker run --rm \
    -e DB_HOST=unused -e DB_PASSWORD=unused \
    --entrypoint python "${IMAGE}" -c "import app; print('OK: web image is importable')" \
    | sed 's/^/   | /'

if [[ "${PUSH:-0}" == "1" ]]; then
    echo ">> Pushing ${IMAGE} to Docker Hub"
    docker push "${IMAGE}"
    echo ">> Done. Students can now run:"
    echo "      WEB_IMAGE=${IMAGE} docker compose -f broken-stack/docker-compose.yml pull"
    echo "      WEB_IMAGE=${IMAGE} docker compose -f broken-stack/docker-compose.yml up -d"
    echo "   Or, if they keep the default image name, just:"
    echo "      cd broken-stack && docker compose pull && docker compose up -d"
else
    echo ">> Built locally as ${IMAGE} (not pushed). Set PUSH=1 to push to Docker Hub."
fi
