#!/usr/bin/env bash
#
# Smoke-test the broken compose stack.
#
# Brings the broken-stack/ up, waits a few seconds, and asserts that the
# exercise is still broken-in-the-intended-way: at least one service is not
# healthy OR the proxy does not return HTTP 200 on /.
#
# If this script reports SUCCESS, the broken stack is still broken (good).
# If it reports FAILURE, the exercise has accidentally been fixed and a
# bug needs to be re-introduced.
#
# Usage:
#   ./build.sh            # smoke-test the broken-stack/
#   ./build.sh solution   # smoke-test the solution/ instead (expects it WORKS)
#

set -euo pipefail

MODE="${1:-broken}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "${MODE}" in
    broken)
        STACK_DIR="${SCRIPT_DIR}/broken-stack"
        EXPECT_HEALTHY=0
        ;;
    solution|fixed)
        STACK_DIR="${SCRIPT_DIR}/solution"
        EXPECT_HEALTHY=1
        ;;
    *)
        echo "Unknown mode: ${MODE} (expected 'broken' or 'solution')" >&2
        exit 2
        ;;
esac

PROJECT_NAME="broken_compose_ex_${MODE}"

cd "${STACK_DIR}"

cleanup() {
    echo ">> Tearing down ${PROJECT_NAME}"
    docker compose -p "${PROJECT_NAME}" down -v --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo ">> Bringing up the ${MODE} stack in ${STACK_DIR}"
docker compose -p "${PROJECT_NAME}" up -d --build

echo ">> Waiting 15s for the stack to settle"
sleep 15

echo ">> Service status:"
docker compose -p "${PROJECT_NAME}" ps

HTTP_CODE="$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/ || echo 000)"
echo ">> GET http://localhost:8080/ returned HTTP ${HTTP_CODE}"

if [[ "${HTTP_CODE}" == "200" ]]; then
    STACK_HEALTHY=1
else
    STACK_HEALTHY=0
fi

if [[ "${EXPECT_HEALTHY}" == "1" ]]; then
    if [[ "${STACK_HEALTHY}" == "1" ]]; then
        echo ">> OK: solution stack is healthy (HTTP 200) as expected."
        exit 0
    fi
    echo ">> FAIL: solution stack did NOT return 200. The fix is incomplete." >&2
    docker compose -p "${PROJECT_NAME}" logs --tail=80 >&2 || true
    exit 1
fi

if [[ "${STACK_HEALTHY}" == "0" ]]; then
    echo ">> OK: broken stack is still broken (HTTP ${HTTP_CODE} != 200) as expected."
    exit 0
fi

echo ">> FAIL: broken stack is returning HTTP 200 -- the exercise has accidentally been fixed." >&2
exit 1
