# Lab 4 — Build your own SMS app with Docker Compose

Complete [Lab 3](Part3.md) first: its single-container API must already load your
trusted model and serve predictions. This lab adds a separate frontend image and
a Compose application.

**Suggested time:** 60–75 minutes, including one intermediate extension.

**Your goal:** Turn the shared classifier into an app with your own identity,
example messages and interaction. Everyone keeps the same prediction contract,
but each student's app should look and behave differently.

## What you receive — and what you build

The [reference application](docker/README.md) contains working API and frontend
source. Use it as a starting point and for diagnosis after making an attempt.

You will:

- Create your own workspace, image tags, Compose project name and host port.
- Customize the frontend for a specific audience.
- Write your own Compose configuration.
- Connect the frontend to the model by service name.
- Demonstrate validation, an outage and recovery.
- Complete one interaction enhancement and one intermediate extension.

The worksheet provides requirements and hints, rather than a complete Compose
file or implementation to paste.

## Step 1 — Make a small design plan

Choose a short student slug, an app name, an audience and an unused host port.
Record your choices in a README inside your workspace.

| Decision | Ideas to choose from |
| --- | --- |
| Audience | Campus announcements, delivery updates, travel messages, community events, or your own |
| App identity | An original name, short introduction and color theme suited to that audience |
| Sample messages | At least three original, synthetic English SMS messages relevant to the audience |
| Interaction enhancement | See Step 3; choose something beyond the existing client's features |
| Intermediate extension | Choose one task from Step 8 |

Include your slug in your Compose project name and both image tags. Choose a
different host port from another student sharing your machine.

> **Design checkpoint:** Explain who would use your app and what you changed for
> that person. Changing only a heading or color does not complete the assignment.

The model still predicts spam or ham. A new brand or audience does not retrain it,
and an example's expected label is not guaranteed. Keep the predicted label
visible even if you customize the surrounding wording.

## Step 2 — Create your own workspace

Start in **sqlabs/lab4/**. Replace your-slug in the commands with your own slug:

```bash
mkdir -p submissions/your-slug
cp -R docker/sms-service docker/chat-client submissions/your-slug/
cp docker/smoke_test.py submissions/your-slug/
cd submissions/your-slug
```

Do not copy the reference compose.yaml. Create that file yourself in this
directory. Keep your edits in your own workspace so another student can still
run the reference application.

Check that your copied sms-service/model.joblib is the accepted fitted Pipeline
from Lab 3. Preserve its compatible Python and ML dependency versions.

> **CHECK:** Your workspace contains sms-service/, chat-client/ and smoke_test.py.
> Your README records your app name, slug, chosen port and model artifact version.

## Step 3 — Make the client yours

Inspect index.html, styles.css and app.js before editing.

**Required customization:**

1. Give the app your chosen name, introduction and color theme.
2. Replace the examples with at least three original synthetic messages for
   your audience. Keep their labels as real model results.
3. Add one interaction enhancement beyond the supplied client.

The reference already includes sample buttons, character counting, a loading
state, clearing the conversation, keyboard submission and round-trip timing.
Choose an additional feature, for example:

- Session counters for the number of spam and ham predictions.
- A filter that shows all results, only spam, or only ham.
- A switch between a readable result and the raw response JSON.
- A way to save a message as a reusable example for the current page session.

You may propose a different feature if you can define how to verify it.

**Hints:** Find how example buttons are discovered. Check how user text is
inserted into the conversation. Decide where state for your new feature belongs.

> **CHECK:** Your examples and new interaction work. User text displays as text,
> the layout remains usable on a narrow screen, and the model's actual label is
> distinguishable from your presentation.

## Step 4 — Build the two images

Create a frontend image separately from the API image. Choose tags containing
your slug and select the correct build context for each.

Before building, answer in your README:

1. Which files must be in the API's build context?
2. Which files execute in the browser, and which configuration runs in Nginx?
3. Which image needs rebuilding after a CSS change? After an API code change?

**Hints:** Read both Dockerfiles. The API Dockerfile uses a lowercase filename.
Use docker build --help if you need to specify a Dockerfile explicitly.

> **CHECK:** docker image ls shows your two distinct image tags. Neither build
> retrains the model.

## Step 5 — Write your Compose application

Create compose.yaml with two services: your model API and your frontend.
Choose their names and make the proxy configuration agree with your choices.

Your configuration must satisfy these requirements:

- Both services build from their own contexts and use your image tags.
- Your project name includes your student slug.
- The browser reaches the frontend on your chosen local host port.
- The API has no published host port in the normal configuration.
- The frontend reaches the API over the Compose network.
- Startup uses a meaningful API health check before the frontend is ready.
- Rebuilding and starting the application takes one Compose command.

Preserve these HTTP paths so the shared checks remain useful:

| Browser-facing operation | Required behavior |
| --- | --- |
| GET / | Your chat page |
| GET /health | Frontend health: status=ok |
| GET /api/health | Model health through the proxy: status=ok |
| POST /api/predict | Accept message and return label=spam or label=ham |

**Hints:** Look up build, ports, healthcheck and depends_on in the
[Compose service reference](https://docs.docker.com/reference/compose-file/services/).
Inspect the Nginx upstream name and how the /api prefix is handled. Use
[Compose networking](https://docs.docker.com/compose/how-tos/networking/) to
check your assumptions about service names.

Validate before starting:

```bash
docker compose config
docker compose up --build --wait
docker compose ps
```

> **CHECK:** Both services become healthy, only the frontend is published
> normally, and a chat message produces a real prediction.

> **Explain in your README:** Why might an address work inside Nginx's container
> but fail in the browser? What does localhost refer to in each place?

## Step 6 — Prove each hop works

Use the browser's Network panel to identify one prediction request, its JSON
body, response and status. Then make a request to the API by service name from
inside the frontend container.

Run the shared HTTP checks against your chosen port and app name. This example
uses port 8091 and the name QuietInbox; replace both with your choices:

```bash
python3 smoke_test.py --base-url http://localhost:8091 --app-name "QuietInbox"
```

The checks verify the HTTP contract, not model accuracy or your custom feature.
Also demonstrate your interaction enhancement yourself.

Try valid text, an empty message, whitespace-only text and a request missing
message. Record the observed statuses rather than changing the checks to hide a
failure.

> **CHECK:** The page and assets load, proxied health succeeds, prediction returns
> a valid label, and the API rejects invalid input even when the browser is
> bypassed. Extra response fields are allowed; keep label compatible.

## Step 7 — Break one service and recover

Keep the chat page open. Stop only your API service using Compose, then submit
another message.

Investigate before restarting anything:

1. Does the page still load?
2. What do frontend health and proxied model health report?
3. Does the user see an understandable error and have a way to retry?
4. What evidence do the logs provide?

Check the expected outage behavior. Again, replace the example name and port:

```bash
python3 smoke_test.py --base-url http://localhost:8091 --app-name "QuietInbox" --expect-model-down
```

Restart the API, wait for health, and demonstrate another successful prediction.
Run the normal checks again.

> **CHECK:** The frontend remains available while the failed prediction returns
> a readable JSON error with HTTP 503. The stack recovers without retraining or
> restarting the frontend.

> **Explain:** What did the startup dependency guarantee, and what did it not
> guarantee after the API stopped?

## Step 8 — Choose one intermediate extension

Implement one task and write its acceptance evidence in your README.

### A. Identify the model in every response

Add model_version to successful predictions, configure it through Compose, and
display it in your client. Use a value identifying the artifact actually copied
into the image.

**Acceptance:** The browser and API show the same configured version, label
checks still pass, and you can explain why changing an environment variable
does not replace the fitted model.

### B. Define your own input policy

Choose and document a maximum message length appropriate to your app. Implement
it on both the client and API. Decide how the UI explains the limit.

**Acceptance:** A request sent outside the browser is rejected with 422 when it
exceeds the limit; normal predictions and the original checks still pass.

### C. Add optional API documentation access

Make FastAPI's /docs available directly from the host for development, while
keeping the API unpublished in the normal Compose setup. Choose a separate
unused local host port and make the diagnostic configuration opt-in.

**Acceptance:** You can open /docs, load its schema and execute a prediction.
You can then return to the normal configuration and show that only the
frontend is published.

**Questions:** Is the browser running inside the container? Is publishing a
port the same as changing the API's container port? Why might proxying /docs
also require thinking about the OpenAPI schema URL?

### D. Add a bounded batch prediction feature

Create a separate endpoint and client control for a small collection of
messages. Choose a maximum batch size and a policy for an invalid item.

**Acceptance:** Three synthetic messages produce three results in the original
order. An empty or oversized batch is rejected. Explain whether one invalid
item rejects the whole batch or gives a per-item error.

Rebuild affected images after source changes, recreate the affected services
and rerun the checks. Verify your extension separately.

## Submit and compare

Submit your workspace with a README containing:

- Your slug, app name, audience, port and image tags.
- Your startup and shutdown instructions.
- A screenshot showing your original examples and a real prediction.
- A screenshot or output showing both services healthy.
- Normal and outage check results, followed by evidence of recovery.
- A short explanation of the request path and your Step 4–7 decisions.
- Evidence for your interaction enhancement and intermediate extension.

Explain where your trusted model artifact comes from so another person can
reproduce the run. Follow the class's model-file handoff convention.

Compare with another student's app: identify one visible design difference,
one interaction difference and one operational decision. Check that both still
respect the same spam/ham contract.

Stop your own project when finished:

```bash
docker compose down
```

**Finished when:** A reviewer can start your two-container app, recognize your
customization, send a message, reproduce one controlled failure and recovery,
and verify the extension you chose.
