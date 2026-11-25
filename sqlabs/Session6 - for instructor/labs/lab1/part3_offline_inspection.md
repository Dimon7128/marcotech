# Lab 1, Stage B — Offline Workflow Inspection

**Status:** Final teaching materials. See [the QA report](../../FINAL_QA_REPORT.md) for executed checks and hosted-run limitations.  
**Purpose:** A guided fallback when GitHub access is unavailable. Use this within the Stage B lab time, not as a third lab.  
**Evidence status:** The summaries below are illustrative teaching examples. They are not captured GitHub logs and do not prove that a workflow or Docker build has been run.

## What you need

- This file and the [Stage B student guide](part3_github_actions.md), including its complete reference workflow. Keep both files available locally before class.
- The completed Part 2 service/model/tests if you will run commands locally.
- Python dependencies for local pytest, and a working Docker installation only if you will reproduce the build.

Without local software, complete the reading and inspection tasks. Record that you inspected examples; do not report a successful local or GitHub run.

## Inspect the complete workflow

Open [Complete reference workflow](part3_github_actions.md#complete-reference-workflow) in the saved student guide. It contains the full YAML, not just the slide excerpt.

Identify these values:

| Item | Your answer |
| --- | --- |
| Event that starts a run | |
| Job identifier | |
| Runner image label | |
| Selected Python version | |
| Command that runs the tests | |
| Command that builds the image | |

Explain why the runner needs both `main.py` and `model.joblib` in the checkout. Then point to the step that installs the testing dependencies.

## Example A — A failed assertion

**Illustrative normalized summary, not an actual captured run.** The instructor deliberately changed the health test's expected status from 200 to 201 without changing the API.

```text
Workflow: SMS API CI
Job: check-and-build

Check out repository    SUCCESS
Set up Python           SUCCESS
Install dependencies    SUCCESS
Run API tests           FAILURE

FAILED test_api.py::test_health
    assert response.status_code == 201
E   assert 200 == 201

1 failed, 4 passed

Build Docker image      SKIPPED
Overall result          FAILURE
```

Discuss with the instructor:

- Which step failed, and which test function failed?
- What did the API return, and what did the test expect?
- In this deliberately constructed example, which expectation should be restored?
- Why was the image not built?

Read the assertion rather than treating every failed run as a model problem.

## Example B — Tests and build succeed

**Illustrative normalized summary, not an actual captured run.** This represents the intended result after the correct health expectation is restored.

```text
Workflow: SMS API CI
Job: check-and-build

Check out repository    SUCCESS
Set up Python           SUCCESS
Install dependencies    SUCCESS
Run API tests           SUCCESS
5 passed

Build Docker image      SUCCESS
Image named             sms-api:ci
Overall result          SUCCESS
```

Explain what evidence would be needed in a real run: open the pytest log and the build log for the same pushed commit.

Which of these statements are supported by this **example**?

- The configured API tests passed.
- The Docker image could be built.
- The model was retrained.
- The image was published to a registry.
- The application was deployed.
- Good precision/recall was demonstrated.

The instructor will review the answers. A summary is not evidence of a real execution; the exercise is about interpreting what the intended steps establish.

## Reproduce the local checks where software is available

These instructions reproduce local behavior after the approved lab files are available. They do not run GitHub Actions.

Open a terminal at the completed service project root. Use the matching Python environment from Part 2, with `model.joblib` beside `main.py`.

Run:

```bash
python -m pytest -q
```

Expect `5 passed` for the completed project. To view the familiar failure, the instructor may temporarily change only `test_health` from expecting 200 to expecting 201, then rerun pytest. Expect `1 failed, 4 passed`. Restore 200 and confirm `5 passed` again. Students are not required to make the deliberate failure themselves.

**Only after pytest succeeds**, and only where Docker is available and running, build:

```bash
docker build -f dockerfile -t sms-api:ci .
```

Check that the local image exists:

```bash
docker image ls sms-api:ci
```

Build output will differ between Docker versions and cache states. Record the actual result you observed, including any setup failure. If Docker is unavailable, inspect the build command and example instead; do not mark the build as executed.

## Completion record

Write down:

- Whether you inspected example summaries, ran local pytest, built locally, or inspected a real hosted run.
- Which workflow step corresponds to each local command.
- The assertion mismatch in Example A and the reason for skipping the build.
- What a passing tests-and-build run establishes, and what remains outside it.

To complete the **hosted** lab later, push the workflow and required files to your own repository, then inspect the actual GitHub Actions run. Offline inspection and local execution are useful preparation, but they do not establish that the hosted workflow works.
