#!/usr/bin/env bash
#
# Build (and optionally push) the intentionally-broken NGINX image used by
# the "Fix the Broken NGINX Container" exercise.
#
# Usage:
#   ./build.sh                                          # dimabu/broken_image:latest
#   ./build.sh dimabu/broken_image                      # dimabu/broken_image:latest
#   ./build.sh dimabu/broken_image v1                   # dimabu/broken_image:v1
#   PUSH=1 ./build.sh dimabu/broken_image latest        # build + push
#
# You can also override the default repo via env var:
#   REPO=someoneelse/nginx-broken ./build.sh
#

set -euo pipefail

REPO="${1:-${REPO:-dimabu/broken_image}}"
TAG="${2:-latest}"
IMAGE="${REPO}:${TAG}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXT="${SCRIPT_DIR}/nginx-broken"

echo ">> Building ${IMAGE} from ${CONTEXT}"
docker build -t "${IMAGE}" "${CONTEXT}"

echo ">> Quick smoke test (expecting the container to crash)"
CID="$(docker run -d --rm "${IMAGE}" || true)"
sleep 1
docker logs "${CID}" 2>&1 | sed 's/^/   | /' || true
docker rm -f "${CID}" >/dev/null 2>&1 || true

if [[ "${PUSH:-0}" == "1" ]]; then
    echo ">> Pushing ${IMAGE}"
    docker push "${IMAGE}"
fi

echo ">> Done. Students can now run:"
echo "   docker run -d --name broken-nginx -p 8080:80 ${IMAGE}"
