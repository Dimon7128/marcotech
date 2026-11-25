# Instructor reference — SMS chat stack

Student worksheets:

- [Lab 3 — Single model container](../Part3.md)
- [Lab 4 — Your own chat application with Compose](../Part4.md)

This directory is the completed reference implementation. Lab 4 students build
a separate project, write their own Compose configuration, and customize the app.
Use the reference for comparison after attempting the assignment.

## Reference architecture

```text
Browser :8080 → frontend (Nginx :80) → model-api (FastAPI :8000)
                       /api/predict → /predict
```

Each message gets a spam/ham prediction. The model does not generate
conversational answers.

## Run the reference

Open a terminal in this directory. Confirm that sms-service/model.joblib contains
your trusted fitted Pipeline. If it is missing, copy an accepted model from the
Session 4 training exercise, for example:

```bash
cp ../../lab3/models/sms_model_v3.joblib sms-service/model.joblib
```

Keep the API's Python and ML versions compatible with the environment that saved
the artifact. The supplied Dockerfile uses Python 3.10 and the requirements pin
scikit-learn 1.7.2.

```bash
docker compose config
docker compose up --build --wait
```

Open **http://localhost:8080**. If 8080 is occupied:

```bash
export FRONTEND_PORT=8081
docker compose up -d
```

Then open http://localhost:8081. The export also keeps your chosen port when
running the documentation overlay commands below in the same terminal.

Only the frontend is published by the normal configuration. The API is available
to the frontend through the Compose network. Browser requests use relative
/api/... URLs; Nginx forwards them to model-api:8000 and strips /api.

## Optional: open the model container's /docs with Compose

Lab 3 already exposes the model's /docs at http://localhost:8001/docs through its
single-container docker run command. Stop that run before using the same port
for Compose.

To access the API directly while the reference Compose stack is running, add the
provided development overlay:

```bash
docker compose -f compose.yaml -f compose.docs.yaml up --build --wait
```

Open:

- **http://localhost:8001/docs** — FastAPI Swagger UI from the model container.
- http://localhost:8001/openapi.json — the API schema.
- http://localhost:8080 — the chat frontend, or the port you selected above.

The overlay publishes the API only on the local host. If port 8001 is occupied:

```bash
export API_DOCS_PORT=8002
docker compose -f compose.yaml -f compose.docs.yaml up -d
```

Then open http://localhost:8002/docs. Keep using the same overlay and custom port
values when updating that development configuration. Exports apply to this
terminal; record your choices if you open a new terminal. The chat proxy's
/api/docs URL is not the direct
documentation entry point; the published model port keeps Swagger's schema and
request URLs consistent.

## Check and stop

```bash
python3 smoke_test.py --base-url "http://localhost:${FRONTEND_PORT:-8080}"
docker compose ps
docker compose logs --tail=30 frontend model-api
```

After rebranding a student copy, supply its expected app name and host port:

```bash
python3 smoke_test.py --base-url http://localhost:8091 --app-name "QuietInbox"
```

Stop the reference project:

```bash
docker compose down
```

If you used the documentation overlay, use:

```bash
docker compose -f compose.yaml -f compose.docs.yaml down
```

Read the separate student worksheets for the challenges, customization choices,
acceptance criteria and submission requirements.
