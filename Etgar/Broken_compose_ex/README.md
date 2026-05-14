# Exercise -- Fix the Broken Compose Stack

You are given a multi-service `docker-compose` stack that **does not work**. Your job is to figure out **why** it's broken, fix the configuration, and end up with a healthy stack that serves traffic on `http://localhost:8080`.

The stack has more moving parts than the single-container exercise: a reverse proxy, a web app, a database, and a cache. There are **three independent bugs**, each in a different file and each surfaces in the logs of a different service. Treat it like a real on-call ticket.

---

## Stack Overview

```
        ┌────────────────────┐
client ─►       proxy        │  nginx:1.27-alpine, host port 8080 -> 80
        │  (reverse proxy)   │
        └─────────┬──────────┘
                  │  HTTP
                  ▼
        ┌────────────────────┐
        │        web         │  Python Flask app, port 5000
        │   (MOTD service)   │
        └─────┬──────────┬───┘
              │          │
              ▼          ▼
       ┌───────────┐ ┌───────────┐
       │    db     │ │   cache   │
       │ postgres  │ │   redis   │
       └───────────┘ └───────────┘
```

| Service | Image                | Port (host) | Purpose                              |
|---------|----------------------|-------------|--------------------------------------|
| proxy   | `nginx:1.27-alpine`  | `8080`      | Reverse proxy in front of the app    |
| web     | built from `./web`   | (internal)  | Flask MOTD service, listens on 5000  |
| db      | `postgres:16-alpine` | (internal)  | Stores the MOTD message              |
| cache   | `redis:7-alpine`     | (internal)  | Counts visits                        |

A successful response from `http://localhost:8080/` looks like:

```json
{ "message": "Compose stack is alive. You fixed it!", "visits": 1 }
```

> The custom `web` service is published as **`dimabu/motd-web:latest`** on Docker Hub. The other three services use stock public images (`nginx`, `postgres`, `redis`). Students do **not** need to build anything locally -- a single `docker compose pull` fetches everything.

---

## Quick Start (students)

You only need Docker. You do **not** need to build the app image yourself.

```bash
# 1. Get the exercise files
git clone <this-repo>
cd Broken_compose_ex/broken-stack

# 2. Pull all four images (web from Docker Hub, plus nginx/postgres/redis)
docker compose pull

# 3. Bring the stack up -- it WILL be broken on purpose
docker compose up -d
docker compose ps

# 4. Diagnose with per-service logs
docker compose logs web   --tail=50
docker compose logs db    --tail=50
docker compose logs proxy --tail=50

# 5. Fix the bugs in .env and proxy/nginx.conf (see "Steps" below)

# 6. When done
docker compose down -v
```

If your instructor published the image under a different name, point at it with the `WEB_IMAGE` env var:

```bash
WEB_IMAGE=youruser/motd-web:latest docker compose pull
WEB_IMAGE=youruser/motd-web:latest docker compose up -d
```

---

## Objective

1. Bring the stack up and watch it fail.
2. Read the logs of each service and identify all three bugs.
3. Apply minimal, targeted fixes -- do **not** rewrite the stack from scratch.
4. End with a running stack that returns the JSON above through the proxy.

---

## Steps

1. **Start the stack.**
   ```bash
   cd broken-stack
   docker compose up -d --build
   docker compose ps
   ```
   You will see one or more services in `unhealthy`, `restarting`, or `Exit` state.

2. **Look at the logs, per service.** This is the key skill the exercise drills.
   ```bash
   docker compose logs web    --tail=50
   docker compose logs db     --tail=50
   docker compose logs proxy  --tail=50
   docker compose logs cache  --tail=50
   ```
   Each log will point you at a different bug.

3. **Fix the bugs.** There are three of them and they live in:
   - `broken-stack/.env`
   - `broken-stack/proxy/nginx.conf`

   You should not need to edit `docker-compose.yml` itself, the Flask app, or the SQL file.

4. **Re-apply each fix without rebuilding the whole world.**
   - After editing `.env`:
     ```bash
     docker compose up -d
     ```
     (Compose re-creates only the services whose env changed.)
   - After editing `proxy/nginx.conf`:
     ```bash
     docker compose restart proxy
     ```

5. **Verify the stack end-to-end.**
   ```bash
   docker compose ps                                       # all services Up / healthy
   curl -s http://localhost:8080/healthz                   # -> ok
   curl -s http://localhost:8080/        | python -m json.tool
   # {
   #     "message": "Compose stack is alive. You fixed it!",
   #     "visits": 1
   # }
   curl -s http://localhost:8080/                          # hit it again, visits should grow
   ```

6. **Tear down when done.**
   ```bash
   docker compose down -v
   ```

---

## Deliverables

Submit a short write-up containing:

1. **Per-bug diagnosis** -- for each of the three bugs:
   - the service whose logs revealed it,
   - the relevant log line,
   - the file and line you changed.
2. **Proof of success** -- the output of `docker compose ps` and `curl -s http://localhost:8080/` after the fixes.

The full reference solution lives in [`solution/SOLUTION.md`](solution/SOLUTION.md). Try to solve it yourself first.

---

## Useful Hints (no spoilers)

* `docker compose ps` shows you which services are healthy, which restarted, and which exited.
* `docker compose logs <service>` is your single most important tool. Read each service's logs **separately**.
* Inside a Compose network, services reach each other by **service name** -- the name in `docker-compose.yml`, not `localhost`. `localhost` inside a container is the container itself.
* When the app says it cannot connect to a DB, ask two questions in order:
    1. Is it talking to the *right host*?
    2. Is it using the *right credentials*?
* When a reverse proxy returns `502 Bad Gateway`, check the **proxy's** logs -- they will usually tell you exactly which upstream address failed.
* Postgres seeds anything in `/docker-entrypoint-initdb.d/` **only on first boot of an empty data volume**. If you change init scripts, run `docker compose down -v` to clear the volume.

---

## Repository Layout

```
Broken_compose_ex/
├── README.md                     # this file
├── guide.txt                     # short, no-frills version of this README
├── publish.sh                    # instructor: build + push the web image
├── build.sh                      # instructor: smoke-test the broken/solution stacks
├── broken-stack/                 # the exercise the student edits
│   ├── docker-compose.yml        # references dimabu/motd-web:latest on Docker Hub
│   ├── .env                      # contains bugs #1 and #2
│   ├── web/                      # source for the published image (instructors)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app.py
│   ├── proxy/
│   │   └── nginx.conf            # contains bug #3
│   └── db/
│       └── init.sql
└── solution/
    ├── SOLUTION.md               # full walkthrough -- spoiler!
    ├── docker-compose.yml        # identical to broken (bugs were not here)
    ├── .env                      # fixed
    └── proxy/
        └── nginx.conf            # fixed
```

---

## For Instructors -- Publish the Image

The custom Flask app under `broken-stack/web/` needs to be on Docker Hub so students can pull it. The three other services already are.

The repo ships a `publish.sh` that builds and (optionally) pushes the image:

```bash
# Build locally only (no push), as dimabu/motd-web:latest
./publish.sh

# Build under a different repo / tag
./publish.sh youruser/motd-web v2

# Build AND push to Docker Hub (requires `docker login` first)
PUSH=1 ./publish.sh youruser/motd-web latest
```

After pushing, the students' command stays the same -- they just run `docker compose pull && docker compose up -d` and Compose grabs the image from Docker Hub.

If you publish under a name other than `dimabu/motd-web`, tell students to set `WEB_IMAGE`:

```bash
WEB_IMAGE=youruser/motd-web:latest docker compose pull
```

Or change the default in `broken-stack/docker-compose.yml` from `dimabu/motd-web:latest` to whatever you pushed.

## For Instructors -- Smoke Test

`build.sh` brings the broken stack up, waits a few seconds, asserts that **at least one** service is failing or that the proxy returns a 5xx, then tears it down again. Run it after any change to confirm the exercise is still broken-in-the-intended-way:

```bash
./build.sh           # tests broken-stack/  (expects FAILURE)
./build.sh solution  # tests solution/      (expects SUCCESS)
```

If `./build.sh` reports the broken stack is healthy, the exercise has accidentally been fixed and you need to re-introduce a bug.

> The smoke test still relies on the `build:` directive in `docker-compose.yml`, so it builds the image locally rather than pulling. After you `./publish.sh PUSH=1`, you can confirm the published image works from a student's perspective by removing the locally built copy and re-running the test:
>
> ```bash
> docker image rm dimabu/motd-web:latest
> cd broken-stack && docker compose pull && docker compose up -d
> ```
