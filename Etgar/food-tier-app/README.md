# Food Tier App

A tiny educational **3-tier application**:

- **Frontend** — plain HTML / CSS / JavaScript (no framework, no build step).
- **Backend** — Python + FastAPI.
- **Data tier** — a persistent CSV file (`backend/data/food_history.csv`).
- **External API** — OpenAI Chat Completions, used as the "brain" that
  classifies a food into tier **A** / **B** / **C**.

The user types a food (e.g. `egg`) in the browser, the backend first looks
it up in the CSV; if the food has already been classified before, the
saved answer is returned (`source: "csv"`). Otherwise the backend asks
OpenAI, validates the JSON answer, saves it to the CSV, and returns it
(`source: "openai"`).

```
food-tier-app/
├── docker-compose.yml
├── frontend/    # nginx container
└── backend/     # FastAPI container, owns the CSV
```

---

## 1. Prerequisites

- An **OpenAI API key** (https://platform.openai.com/api-keys).
- Either:
  - **Docker** + **Docker Compose v2** (recommended), or
  - **Python 3.12+** if you want to run it without Docker.

---

## 2. Configure your API key

```bash
cd food-tier-app
cp backend/.env.example backend/.env
# then open backend/.env and replace the placeholder with your real key
```

`backend/.env` is git-ignored / Docker-ignored — secrets stay on your
machine.

---

## 3. Run with Docker Compose (recommended)

```bash
docker compose up --build
```

Then open **http://localhost:8080** in your browser.

What this does:

| Container             | Image base       | Host port | Container port |
| --------------------- | ---------------- | --------- | -------------- |
| `food-tier-frontend`  | `nginx:alpine`   | `8080`    | `80`           |
| `food-tier-backend`   | `python:3.12-slim` | `8000`  | `8000`         |

- The backend bind-mounts `./backend/data` into the container, so the CSV
  **persists on your host** — you can `cat backend/data/food_history.csv`
  to see what has been saved.
- The browser talks to **both** containers over `localhost`: nginx
  (port 8080) serves the static UI, and the JS makes a CORS-enabled
  request to FastAPI on port 8000.

Stop everything with:

```bash
docker compose down
```

---

## 4. Run locally without Docker

```bash
# backend
cd backend
python -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

In a second terminal, serve the frontend (any static server works):

```bash
cd frontend
python -m http.server 8080
```

Open http://localhost:8080.

---

## 5. API reference

### `POST /api/food-tier`

**Request**

```bash
curl -X POST http://localhost:8000/api/food-tier \
  -H "Content-Type: application/json" \
  -d '{"food":"egg"}'
```

**Response**

```json
{
  "food": "egg",
  "tier": "A",
  "explanation": "Eggs are rich in high-quality protein and important nutrients.",
  "source": "openai"
}
```

The second time you call it with `"egg"` you will get the same response
but with `"source": "csv"` (no OpenAI call, no cost).

### `GET /api/history/{food}`

```bash
curl http://localhost:8000/api/history/egg
```

If the food is in the CSV:

```json
{
  "exists": true,
  "food": "egg",
  "tier": "A",
  "explanation": "Eggs are rich in high-quality protein and important nutrients."
}
```

If not:

```json
{ "exists": false, "food": "egg" }
```

### `GET /health`

```json
{ "status": "ok" }
```

Used by the docker-compose healthcheck.

---

## 6. The data tier — CSV schema

File: `backend/data/food_history.csv`

| food | tier | explanation                                                       |
| ---- | ---- | ----------------------------------------------------------------- |
| egg  | A    | Eggs are rich in high-quality protein and important nutrients.     |
| soda | C    | Sugary drinks add empty calories with little nutritional benefit.  |

Notes:

- Food names are normalized to **trimmed lowercase** before lookup or
  save (`"Egg "`, `"egg"`, and `"EGG"` all map to the same row).
- The backend creates the file with just the header row if it does not
  exist yet.

---

## 7. Troubleshooting

**`OPENAI_API_KEY is not set`** — you forgot step 2 (`cp .env.example
.env` and paste a real key). Restart the backend / `docker compose up`
after editing the file.

**CORS error in the browser console** — make sure you are loading the
frontend from `http://localhost:8080` (matching the origin the backend
allows). Opening `index.html` via `file://` is also handled via the
special `"null"` origin allow-listed in `main.py`.

**Port already in use** — change the host-side port in
`docker-compose.yml`, e.g. `"8081:80"`, and update `API_BASE` in
`frontend/app.js` if you change the backend port.

**Container can't reach OpenAI** — check your network / proxy. Inside
Docker, the backend uses your host's DNS by default, so `curl
https://api.openai.com` from the host first is a good sanity check.

---

## 8. CI/CD pipeline

The three workflows live at the **marcotech repo root** (`.github/workflows/`),
not inside the project folder — GitHub Actions only reads workflows from
the repo root. Path filters are prefixed with `Etgar/food-tier-app/` so a
push that only touches another exercise won't trigger these workflows.

Deployment uses **GitHub OIDC + AWS SSM Run Command** — no SSH keys, no
inbound port 22, no long-lived AWS credentials in GitHub. The runner
exchanges a signed OIDC token for short-lived STS credentials, then
asks SSM to run docker commands on the EC2 as root.

```
              push to main
                   │
        ┌──────────┴───────────┐
        ▼                      ▼
  food-tier-ci-backend     food-tier-ci-frontend
  ─ pytest                 ─ file checks
  ─ docker build           ─ docker build
  ─ container health       ─ HTTP 200 check
  ─ push :SHA              ─ push :SHA
  ─ push :staging          ─ push :staging
        │                      │
        └──────────┬───────────┘
                   ▼
        food-tier-cd-deploy  (manual: workflow_dispatch)
                   │
                   │  OIDC token
                   ▼
            AWS IAM Role  ─── STS credentials (≈1 h) ──┐
                                                       │
                   │                                   │
                   │  aws ssm send-command             │
                   ▼                                   │
            Blue EC2 (SSM Agent)                       │
            ─ docker compose pull (:staging)           │
            ─ docker compose up -d                     │
                   │                                   │
                   ▼                                   │
            integration tests (curl from runner)       │
                   │                                   │
        ┌──────────┴────── if Blue OK ──────────┐      │
        ▼                                       ▼      │
   retag staging → prod                  aws ssm send-command
   on Docker Hub                                ▼      │
                                          Prod EC2 (SSM Agent)
                                          ─ docker compose down
                                          ─ docker compose pull (:prod)
                                          ─ docker compose up -d
                                                 │
                                                 ▼
                                          production health checks
```

### Files

| File | Purpose |
| ---- | ------- |
| [../../.github/workflows/food-tier-ci-backend.yml](../../.github/workflows/food-tier-ci-backend.yml) | Test + build + push the backend image. Triggered by `Etgar/food-tier-app/backend/**` changes. |
| [../../.github/workflows/food-tier-ci-frontend.yml](../../.github/workflows/food-tier-ci-frontend.yml) | Validate + build + push the frontend image. Triggered by `Etgar/food-tier-app/frontend/**` changes. |
| [../../.github/workflows/food-tier-cd-deploy.yml](../../.github/workflows/food-tier-cd-deploy.yml) | Manual deployment to Blue then Prod (OIDC + SSM). |
| [backend/tests/test_health.py](backend/tests/test_health.py) | Minimal pytest covering the `/health` endpoint. |
| [backend/requirements-dev.txt](backend/requirements-dev.txt) | CI-only dependencies (pytest, httpx). Never shipped in the production image. |

### Image tagging scheme

Each CI run pushes two tags for the same image bits:

| Tag | Mutability | Purpose |
| --- | --- | --- |
| `:${GITHUB_SHA}` | **immutable** | The audit trail. You can always roll back to any past build. |
| `:staging` | moving pointer | What the next CD run will deploy to Blue EC2. |
| `:prod` | moving pointer | What is currently live in production. Set by CD after Blue validates. |

### Required GitHub secrets

Configure in **Settings → Secrets and variables → Actions**:

| Secret | Used by |
| ------ | ------- |
| `DOCKERHUB_USERNAME`     | CI + CD (image namespace + Docker Hub login) |
| `DOCKERHUB_TOKEN`        | CI + CD (use a **Personal Access Token**, not your Docker Hub password) |
| `AWS_DEPLOY_ROLE_ARN`    | CD (the IAM role GitHub assumes via OIDC, e.g. `arn:aws:iam::123456789012:role/github-actions-food-tier-deploy`) |
| `AWS_REGION`             | CD (e.g. `eu-west-1`) |
| `BLUE_EC2_INSTANCE_ID`   | CD (`i-0abc...` — used by `aws ssm send-command`) |
| `PROD_EC2_INSTANCE_ID`   | CD |
| `BLUE_EC2_HOST`          | CD (public DNS / IP — used by the runner to curl the integration tests) |
| `PROD_EC2_HOST`          | CD |

Notice what is **no longer** required compared to the SSH variant:
`BLUE_EC2_USER`, `BLUE_EC2_SSH_KEY`, `PROD_EC2_USER`, `PROD_EC2_SSH_KEY`.

### AWS one-time setup

#### A. Create the OIDC identity provider (once per AWS account)

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

The thumbprint is GitHub's well-known root CA fingerprint; AWS no longer
validates it strictly (it accepts any value) but the field is still
required by the API.

#### B. Create the IAM role GitHub assumes

**Trust policy** — restricts who can assume the role to *this repo on main*:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
      },
      "StringLike": {
        "token.actions.githubusercontent.com:sub": "repo:<GH_ORG>/<GH_REPO>:ref:refs/heads/main"
      }
    }
  }]
}
```

**Permissions policy** — only what SSM Run Command actually needs:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["ssm:SendCommand"],
      "Resource": [
        "arn:aws:ssm:<REGION>::document/AWS-RunShellScript",
        "arn:aws:ec2:<REGION>:<ACCOUNT_ID>:instance/<BLUE_INSTANCE_ID>",
        "arn:aws:ec2:<REGION>:<ACCOUNT_ID>:instance/<PROD_INSTANCE_ID>"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetCommandInvocation",
        "ssm:ListCommandInvocations",
        "ssm:ListCommands"
      ],
      "Resource": "*"
    }
  ]
}
```

Note the per-instance scoping — even if the runner is compromised, it
cannot SSM-execute on any EC2 outside Blue and Prod.

#### C. Attach an instance profile to each EC2 (Blue and Prod)

The SSM Agent on the EC2 needs to call back to AWS. Attach the AWS-managed
policy **`AmazonSSMManagedInstanceCore`** to a role and attach that role
as the instance profile of both EC2s. The SSM Agent comes pre-installed
on Amazon Linux 2023 and recent Ubuntu AMIs — verify with:

```bash
sudo systemctl status amazon-ssm-agent
```

If it's not running:

```bash
sudo systemctl enable --now amazon-ssm-agent
```

### One-time EC2 setup (Blue and Prod)

If you provisioned the EC2s with the Terraform in
[infra/](infra/), Docker + Compose plugin + git + AWS CLI v2 are already
installed and the `/home/ubuntu/food-tier-app/` directory is ready. You
only need to drop the compose file and `.env` on each box:

```bash
# SSH alternative (not strictly needed — you can do this via SSM too):
# `aws ssm start-session --target <instance-id>`

# 1. lay down the compose file (images come from Docker Hub — no source
#    code lives on the EC2)
cd ~/food-tier-app
curl -O https://raw.githubusercontent.com/<your-org>/marcotech/main/Etgar/food-tier-app/docker-compose.yml

# 2. .env  (Blue server — on Prod use IMAGE_TAG=prod)
cat > .env <<'EOF'
DOCKERHUB_USERNAME=<your-dockerhub-user>
IMAGE_TAG=staging
OPENAI_API_KEY=<your-openai-key>
EOF
```

SSM Run Command runs as **root**, so the `APP_DIR` in the workflow
(`/home/ubuntu/food-tier-app`) is the absolute path on the box. If
your AMI uses a different user, update `APP_DIR` in
[../../.github/workflows/food-tier-cd-deploy.yml](../../.github/workflows/food-tier-cd-deploy.yml).

### Triggering a deployment

1. Push a change to `main`. CI runs and pushes new `:staging` images.
2. Go to **Actions → food-tier-app — deploy → Run workflow**.
3. Type `deploy` in the confirm input and click **Run**.
4. Watch the two jobs (`deploy-blue`, then `promote-and-deploy-prod`).
   If Blue's integration tests fail, the prod job is skipped — your
   production stays on whatever `:prod` pointed to before.

The full audit trail lives in two places:
- **GitHub Actions logs** — every SSM command's stdout/stderr is printed.
- **AWS CloudTrail** — the `AssumeRoleWithWebIdentity` and every
  `SendCommand` are logged with the `gh-actions-food-tier-deploy-*`
  session name.

### Rolling back

The immutable `:${GITHUB_SHA}` tags make rollback a one-liner. From your
laptop (or via SSM):

```bash
# locally — push a new :prod pointer to an old build
docker pull <user>/food-tier-backend:<old-sha>
docker tag  <user>/food-tier-backend:<old-sha> <user>/food-tier-backend:prod
docker push <user>/food-tier-backend:prod

# then on the Prod EC2 (via SSM or directly):
docker compose pull && docker compose up -d
```
