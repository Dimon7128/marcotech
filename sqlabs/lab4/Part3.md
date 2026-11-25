# Lab 3 — Package and run the model in one container

Continue after [Part 2](part2.md). This lab keeps the single-container workflow:
read the Dockerfile, build the image, run the model API, and test it using FastAPI's
interactive documentation.

**Suggested time:** 25–30 minutes.

**Outcome:** One running model container with working /health, /predict and /docs.
The separate [Lab 4](Part4.md) adds a customized frontend and Docker Compose.

## Before starting

Open a terminal in **sqlabs/lab4/docker/**. All commands below run from that
directory. For this lab, use only the sms-service/ folder:

```text
docker/
└── sms-service/
    ├── dockerfile
    ├── requirements.txt
    ├── main.py
    └── model.joblib
```

Check Docker:

```bash
docker --version
```

Confirm that sms-service/model.joblib is your trusted fitted Pipeline from the
Session 4 training exercise. If it is missing, copy an accepted saved model,
for example:

```bash
cp ../../lab3/models/sms_model_v3.joblib sms-service/model.joblib
```

Choose the version you actually trained; use v1 if that is your accepted artifact.
Keep the Python and ML package versions compatible with the environment that
saved that model. The provided example uses Python 3.10, pandas 2.2.3,
scikit-learn 1.7.2 and joblib 1.5.3, with FastAPI and Uvicorn added for serving.

Use synthetic SMS messages. Reuse the saved Pipeline throughout this lab.

## Step 1 — Read the Dockerfile

**8 minutes**

1. Open sms-service/dockerfile. Its lowercase filename is intentional; the build
   command selects it explicitly.

```dockerfile
# Match the Python environment used for the supplied trained model.
FROM python:3.10-slim

# Use /app as the working directory inside the image.
WORKDIR /app

# Keep dependency installation in a layer before the app and model copies.
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Package the API and fitted Pipeline.
COPY main.py model.joblib ./

# Listen on all container interfaces so published ports can reach the API.
CMD ["python3","-m","uvicorn","main:app","--host","0.0.0.0","--port","8000"]
```

2. Find the instruction that installs dependencies and the instruction that
   copies the trained model.
3. Explain why the server listens on 0.0.0.0 rather than only 127.0.0.1.
4. Predict which layers can be reused if only main.py changes.

> **CHECK:** Explain FROM, WORKDIR, COPY, RUN and CMD. Distinguish pip's download
> cache from Docker's image-layer cache.

## Step 2 — Build the image

**8 minutes**

1. Build from the docker/ directory:

```bash
docker build -f sms-service/dockerfile -t sms-api:lab4 sms-service
```

2. Explain the difference between the Dockerfile path and the final sms-service
   argument. COPY reads files from the build context.
3. Check the result:

```bash
docker image ls sms-api
```

> **CHECK:** sms-api:lab4 exists. Building it has not started an API process.

> **Challenge:** Would putting model.joblib next to the sms-service directory be
> enough for this build? Use the COPY instruction and build context to justify
> your answer.

## Step 3 — Run the model container

**9 minutes, including the next step**

Publish the API's container port 8000 on host port 8001:

```bash
docker run --rm -p 127.0.0.1:8001:8000 sms-api:lab4
```

Leave this terminal open. In the browser, open:

- Health: http://localhost:8001/health
- Interactive API documentation: **http://localhost:8001/docs**
- OpenAPI schema: http://localhost:8001/openapi.json

FastAPI serves /docs from the model container. Your browser runs on the host and
reaches it through the published port; you do not need a browser inside the
container. Port publishing is described in the [Docker documentation](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/).

If host port 8001 is occupied, choose another host port in the run command and
use that same port in your browser.

> **Think:** Which side of 8001:8000 would you change? Why would changing only
> the browser URL be insufficient?

## Step 4 — Test the container through /docs

1. In /docs, open POST /predict and click **Try it out**.
2. Send:

```json
{"message": "Meeting at five"}
```

3. Record the HTTP status and predicted label.
4. Send an empty message, then a whitespace-only message. Inspect the status and
   validation details.
5. Check GET /health separately.

> **CHECK:** Valid input returns HTTP 200 and label=spam or label=ham; empty and
> whitespace-only input return HTTP 422. The exact label depends on your model.

> **Think:** Does a successful /health response prove that the predicted labels
> are correct? What would you need to check that separately?

## Finish Lab 3

Stop the container with Ctrl+C. Because the run command used --rm, Docker removes
that stopped container; the image remains available.

Before moving on, demonstrate:

- The built image and its tag.
- A running container with a successful prediction.
- A rejected input in /docs.
- The difference between the host port and the container port.

Continue to **[Lab 4 — Build your own chat application with Compose](Part4.md)**.
Your next task is a separate student project with its own branding, examples,
interaction feature, image tags and Compose configuration.

## Fast fixes

| Symptom | Check |
| --- | --- |
| model.joblib is missing during build | Put it inside sms-service/, the build context. |
| Model cannot load | Match the Python and ML versions used to save the artifact. |
| /docs does not open | Check container startup logs and the published host port. |
| /docs opens but prediction fails | Read the HTTP response and the model container's logs. |
| Port 8001 is occupied | Stop the previous run or choose another unused host port. |
| Changes do not appear | Rebuild the image and start a new container from that image. |
