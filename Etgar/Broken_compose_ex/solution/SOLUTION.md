# Solution -- Fix the Broken Compose Stack

> **Spoiler.** Do not read this file before attempting the exercise.

There are **three independent bugs** in this stack. Each one surfaces in a different service's logs, in roughly the order the request flows through the system.

```
client ──► proxy ──► web ──► db / cache
              (3)     (1,2)    (1,2)
```

| #  | File                              | Bug                                                      | Symptom            |
|----|-----------------------------------|----------------------------------------------------------|--------------------|
| 1  | `broken-stack/.env`               | `DB_HOST=localhost` (should be `db`)                     | web: connection refused |
| 2  | `broken-stack/.env`               | `DB_PASSWORD` doesn't match `POSTGRES_PASSWORD`          | db:  password authentication failed |
| 3  | `broken-stack/proxy/nginx.conf`   | upstream points to `web:8000`, app listens on `5000`     | proxy: 502 Bad Gateway / connection refused to upstream |

---

## 1. Bring it up and look at it

```bash
cd broken-stack
docker compose up -d --build
docker compose ps
```

You should see at least the `web` service stuck restarting and the `proxy` returning 502 on `http://localhost:8080/`.

---

## 2. Bug #1 -- `DB_HOST=localhost`

### Diagnose

```bash
docker compose logs web --tail=30
```

You'll see something like:

```
psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1),
port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
```

The web container is trying to reach Postgres on **its own** loopback. There is no Postgres inside the `web` container -- Postgres is in the `db` service. In a Compose network, the DNS name **is the service name**.

### Fix

Edit `broken-stack/.env`:

```diff
-DB_HOST=localhost
+DB_HOST=db
```

Then re-create the services that depend on it:

```bash
docker compose up -d
```

---

## 3. Bug #2 -- password mismatch

### Diagnose

Once `web` can reach `db`, the error in `docker compose logs web` changes to:

```
psycopg2.OperationalError: connection to server at "db" (172.x.x.x), port 5432
failed: FATAL:  password authentication failed for user "appuser"
```

You'll also see this same authentication failure surface in `docker compose logs db`:

```
FATAL: password authentication failed for user "appuser"
DETAIL: Password does not match for user "appuser".
```

The web app and the database disagree on the password. Compose itself doesn't enforce that two env vars must agree -- you have to keep them in sync.

### Fix

In `broken-stack/.env`:

```diff
-DB_PASSWORD=wrong_app_pw
+DB_PASSWORD=super_secret_db_pw
```

Re-apply:

```bash
docker compose up -d
```

> If you had been changing the *server-side* password instead of the client-side one, you would also need `docker compose down -v` -- Postgres only initializes credentials on first boot of an empty data volume. As long as you only change `DB_PASSWORD` to match `POSTGRES_PASSWORD`, you don't have to wipe the volume.

---

## 4. Bug #3 -- proxy points to the wrong port

### Diagnose

Now `web` is happy and you can confirm that with:

```bash
docker compose exec web curl -s http://localhost:5000/healthz   # -> ok
```

But from the host, `curl -s http://localhost:8080/` still returns nothing useful and:

```bash
docker compose logs proxy --tail=20
```

shows:

```
[error] ... connect() failed (111: Connection refused) while connecting to
upstream, ..., upstream: "http://172.x.x.x:8000/", ...
```

The proxy is asking for port **8000**, but the Flask app listens on **5000** (see `web/app.py` and the `EXPOSE 5000` in `web/Dockerfile`).

### Fix

In `broken-stack/proxy/nginx.conf`:

```diff
 upstream motd_app {
-    server web:8000;
+    server web:5000;
 }
```

Reload just the proxy:

```bash
docker compose restart proxy
```

---

## 5. Verify

```bash
docker compose ps
#  motd-db     running (healthy)
#  motd-cache  running
#  motd-web    running
#  motd-proxy  running

curl -s http://localhost:8080/healthz
# ok

curl -s http://localhost:8080/ | python -m json.tool
# {
#     "message": "Compose stack is alive. You fixed it!",
#     "visits": 1
# }

curl -s http://localhost:8080/ | python -m json.tool
# visits goes up -> Redis is wired in correctly too.
```

Tear down when you're done:

```bash
docker compose down -v
```

---

## 6. Reference: the fixed files

The corrected versions of the files you needed to edit are checked in next to this walkthrough:

- [`solution/.env`](./.env)
- [`solution/proxy/nginx.conf`](./proxy/nginx.conf)
- [`solution/docker-compose.yml`](./docker-compose.yml)

You can run the fixed stack end-to-end with:

```bash
cd solution
docker compose up -d --build
curl -s http://localhost:8080/
docker compose down -v
```

Or use the convenience smoke test from the exercise root:

```bash
./build.sh solution
```

---

## 7. Take-aways

- **Per-service logs are the entry point.** `docker compose logs <service>` (not just `docker compose logs`) is how you isolate which moving part is unhappy.
- **`localhost` inside a container is the container.** To reach another service, use its Compose **service name** as the hostname.
- **Env vars are not magically synchronized.** If the server says password X and the client says password Y, Compose has no opinion. You have to keep them in sync (or, better, define each one once and reference it from both places).
- **A 502 from a reverse proxy is the proxy's confession that it couldn't reach the backend.** Always read the proxy's own logs before blaming the backend.
- **Bugs in a multi-service stack reveal themselves in layers.** Each fix can unblock the *next* error message. That is exactly how real outages cascade.
