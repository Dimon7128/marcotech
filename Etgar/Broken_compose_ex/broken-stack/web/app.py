"""
Tiny MOTD service used by the "Fix the Broken Compose Stack" exercise.

Behaviour:
  GET /            -> JSON {"message": "<from postgres>", "visits": <from redis>}
  GET /healthz     -> "ok"

It depends on:
  - PostgreSQL (DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
  - Redis      (REDIS_HOST, REDIS_PORT)

Every misconfiguration in the broken docker-compose.yml surfaces as a
specific, easy-to-grep error in this app's stdout.
"""

import logging
import os
import sys
import time

from flask import Flask, jsonify

import psycopg2
import redis


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("motd")

DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_USER = os.environ.get("DB_USER", "appuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "appdb")

REDIS_HOST = os.environ.get("REDIS_HOST", "cache")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

APP_PORT = int(os.environ.get("APP_PORT", "5000"))

log.info(
    "config db=%s:%s user=%s name=%s redis=%s:%s app_port=%s",
    DB_HOST, DB_PORT, DB_USER, DB_NAME, REDIS_HOST, REDIS_PORT, APP_PORT,
)

app = Flask(__name__)

_redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def db_connect():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        connect_timeout=3,
    )


def wait_for_db(max_seconds: int = 30) -> None:
    """Retry the DB connection so we don't crash on a slow Postgres boot."""
    deadline = time.time() + max_seconds
    last_err: Exception | None = None
    while time.time() < deadline:
        try:
            conn = db_connect()
            conn.close()
            log.info("db is reachable")
            return
        except Exception as exc:
            last_err = exc
            log.warning("db not ready yet: %s", exc)
            time.sleep(2)
    log.error("db never became reachable: %s", last_err)


@app.route("/")
def index():
    try:
        visits = _redis.incr("visits")
    except Exception as exc:
        log.exception("redis failure")
        return jsonify(error="redis unavailable", detail=str(exc)), 500

    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT message FROM motd ORDER BY id LIMIT 1;")
        row = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as exc:
        log.exception("postgres failure")
        return jsonify(error="db unavailable", detail=str(exc)), 500

    return jsonify(message=row[0] if row else "(no message)", visits=visits)


@app.route("/healthz")
def healthz():
    return "ok", 200


if __name__ == "__main__":
    wait_for_db()
    app.run(host="0.0.0.0", port=APP_PORT)
