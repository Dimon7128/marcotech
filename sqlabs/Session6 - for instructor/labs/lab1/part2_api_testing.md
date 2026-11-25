# Lab 1 — Guided Learning, Stage A: Test the SMS API

**Instructor reference:** Expanded teaching material. Distribute the compact [student guide](<../../../Session6 - for students/LAB1.md>) with the student folder.

**Status:** Final teaching materials. See [the QA report](../../FINAL_QA_REPORT.md) for executed checks and hosted-run limitations.  
**Placement:** Session 6, Part 2. Continue the same exercise in Part 3.  
**Student work:** Approximately 25 minutes, after the instructor's explanation and demonstration.  
**Goal:** Test the existing SMS API, extend its request schema with one length rule, and finish with five passing tests.

## What you will learn

- Send requests with FastAPI TestClient without manually starting a server.
- Use pytest assertions to check expected responses.
- Explain how a request schema rejects invalid input.
- Add a maximum message length and test both sides of its boundary.

These are API correctness checks. They do not measure model accuracy, precision, or recall.

## Before the timed exercise

- Have Python 3.10 available. This matches the supplied model handoff and the existing Session 5 Dockerfile.
- Obtain the instructor-provided starter folder and shared, previously trained `model.joblib`. No training or dataset download is needed.
- Have a terminal, a text editor, and access to install the supplied Python dependencies.
- Use synthetic examples only. The supplied model is a fitted `TfidfVectorizer` + `MultinomialNB` Pipeline, with labels `spam` and `ham`.
- If setup takes longer than planned, tell the instructor. Extend practice rather than skipping the assertions or length-boundary checks.

## Your working folder

The starter is at `session6/Session6 - for students/sms-service/` within the MLOPS repository:

```text
Session6 - for students/
├── README.md
├── LAB1.md
├── LAB2.md
└── sms-service/
    ├── main.py                 # Session 5 API; no maximum length initially
    ├── model.joblib            # Shared existing fitted Pipeline
    ├── requirements.txt        # Existing runtime dependencies
    ├── requirements-dev.txt    # Runtime dependencies + pytest and httpx
    ├── test_api.py             # Three core test functions; one TODO
    ├── dockerfile              # Saved for Part 3
    ├── .dockerignore
    └── .gitignore
```

Open a terminal **inside `sms-service/`**. Every command below runs from that folder. The hyphenated folder name is fine: we import the local `main.py` module, not a Python package named `sms-service`.

Keep `model.joblib` beside `main.py`. The application loads it when Python imports `main`, including during testing.

## Checkpoints and time

| Activity | Minutes | Expected checkpoint |
| --- | ---: | --- |
| Set up and import the app | 3 | `SMS Classifier` is printed |
| Read and run the health test | 4 | `1 passed` |
| Complete the prediction assertion | 5 | Valid response contains an allowed label |
| Extend invalid-input cases | 6 | `3 passed` for the core test functions |
| Add and test the length rule | 7 | `5 passed` |
| Total | 25 | Files ready for Part 3 |

## 1. Prepare the test environment

**Why:** The API and tests must run with compatible libraries. A virtual environment keeps the lab's packages together.

### Windows PowerShell

```powershell
py -3.10 --version
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

### macOS/Linux

```bash
python3.10 --version
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

After activation, the remaining `python` commands are the same on both platforms. If PowerShell blocks activation, see the direct-interpreter alternative in troubleshooting.

The development requirements are:

```text
-r requirements.txt
pytest==8.4.2
httpx==0.28.1
```

`pytest` runs the tests. `httpx` is required by TestClient. The first line also installs the API's existing runtime dependencies. Keep the supplied ML versions; they match the shared model.

Confirm that the application can load:

```bash
python -c "from main import app; print(app.title)"
```

Expected output:

```text
SMS Classifier
```

If this fails, fix the environment or model-file problem first. Do not start Uvicorn or Docker for this exercise: TestClient calls the app directly.

## 2. Read and run the health test

**Why:** Start with one request and two clear expectations.

The supplied `test_api.py` begins with:

```python
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

The request gives us `response`. The assertions check that the response is successful and that its JSON content matches the health contract.

Run only this function:

```bash
python -m pytest -q test_api.py::test_health
```

Expected result: **`1 passed`**. Execution time and terminal formatting may vary.

An `assert` defines an expectation. A `print` statement can display a result but does not tell pytest whether that result is acceptable.

## 3. Complete the prediction assertion

**Why:** A successful HTTP status alone does not prove that the client can read the prediction.

The starter includes this deliberately incomplete test:

```python
def test_valid_prediction():
    response = client.post("/predict", json={"message": "Meeting at five"})
    assert response.status_code == 200
    assert "label" in response.json()
    assert response.json()["label"] in {"TODO"}, "Complete the allowed-label assertion"
```

**Your task:** Replace the placeholder set `{"TODO"}` with the two label values allowed by our API. Keep a membership check: this synthetic SMS is not required to receive one particular label.

The assertions have different jobs:

- HTTP 200 checks that the valid request succeeded.
- The `label` check confirms that the response contains the field the client expects.
- The membership check confirms that its value is one of the allowed labels.

Run only this test:

```bash
python -m pytest -q test_api.py::test_valid_prediction
```

Before completing the placeholder, this test intentionally fails. After completing it, expect **`1 passed`**. Do not change the API to return `TODO`.

Use `json=...`, not `data=...`, to send the JSON request body. No external URL or running server is needed.

## 4. Test the existing request schema

**Why:** Invalid input should be rejected before a prediction is attempted.

Our starting request schema requires `message` to be text. It trims spaces from both ends and requires at least one remaining character. It has no maximum length yet.

The starter's third function checks missing, empty, and whitespace-only input:

```python
def test_invalid_input():
    invalid_payloads = [
        {},
        {"message": ""},
        {"message": "   "},
    ]
    for payload in invalid_payloads:
        response = client.post("/predict", json=payload)
        assert response.status_code == 422, payload
```

The loop repeats the same request and expectation for each payload. The extra `payload` after the assertion is a diagnostic message if the assertion fails. This is one pytest test function, even though it sends several requests.

Add two payloads to `invalid_payloads`:

```python
{"message": None},
{"message": 123},
```

Keep the existing three payloads. Python's `None` is sent as JSON `null`; the number remains a number, rather than quoted text.

| Input | Schema rule | Expected status |
| --- | --- | --- |
| Missing `message` | Required field | 422 |
| `message: null` | Must be text | 422 |
| Numeric `message` | Must be text | 422 |
| Empty text | At least one character | 422 |
| Whitespace-only text | Trimming leaves no characters | 422 |

These payloads are valid JSON but invalid API input. An HTTP 422 response is the desired behavior, so an assertion expecting 422 should pass.

Run the three core functions:

```bash
python -m pytest -q
```

Expected result at this point: **`3 passed`**. If the prediction test still mentions `TODO`, finish the previous step. The invalid-input loop does not make the collected test count larger.

## 5. Add one validation rule and test its boundary

**Why:** A new input policy needs tests that show both what remains allowed and what becomes invalid.

For this exercise, our proposed API policy is **1–500 characters after trimming**. The maximum is a teaching choice for our application; it is not a universal SMS-length rule.

### Write the boundary tests first

Append these functions to `test_api.py`:

```python
def test_maximum_length_is_accepted():
    response = client.post("/predict", json={"message": "x" * 500})
    assert response.status_code == 200
    assert response.json()["label"] in {"spam", "ham"}


def test_overlong_message_is_rejected():
    response = client.post("/predict", json={"message": "x" * 501})
    assert response.status_code == 422
```

`"x" * 500` creates a synthetic string of exactly 500 characters. Its specific predicted label is not important here.

Run the tests:

```bash
python -m pytest -q
```

With the original starter schema, expect **`1 failed, 4 passed`**. The failing function should be `test_overlong_message_is_rejected`: the API currently accepts 501 characters and returns 200. The new test expects 422.

Read the failure before editing. This test expresses a new requirement that the starting API does not yet implement.

### Add the rule to the lab copy

In the lab's `main.py`, add `max_length=500` to the existing `StringConstraints`:

```python
class SMSRequest(BaseModel):
    message: Annotated[str, StringConstraints(
        strip_whitespace=True, min_length=1, max_length=500
    )]
```

Keep the existing imports, routes, response fields, model loading, and minimum length. Edit only this new lab copy of the service.

Run the tests again:

```bash
python -m pytest -q
```

Expected result: **`5 passed`**.

This checks the exact maximum as well as the first rejected length. Spaces trimmed from the ends are not part of the checked length. The test strings avoid spaces so the boundary is easy to understand.

## Finish Stage A

Your final file contains these five test functions:

```text
test_health
test_valid_prediction
test_invalid_input
test_maximum_length_is_accepted
test_overlong_message_is_rejected
```

You are finished when:

- All five functions pass in one local pytest run.
- The allowed-label placeholder has been completed, and no deliberate 201 expectation remains from the instructor demo.
- Missing, null, numeric, empty, and whitespace-only input are rejected.
- A 500-character synthetic message is accepted; a 501-character message receives HTTP 422.
- You can explain what at least one assertion checks and why HTTP 422 can be a passing result.
- You can explain why these tests do not prove good precision or recall.

Keep the same `main.py`, `model.joblib`, `test_api.py`, and requirements files for **Lab 1, Stage B in Part 3**. That stage will automate these tests and build the Docker image. Do not change the dataset, retrain, or implement a GitHub Actions workflow during this stage.

## Troubleshooting

| Symptom | What to check and why |
| --- | --- |
| `No module named pytest` or `httpx` | Use the lab's Python environment and install `requirements-dev.txt`. The runtime requirements alone do not include the testing tools. |
| `No module named main` | Open the terminal in `sms-service/`, beside `main.py` and `test_api.py`, and use `python -m pytest`. |
| `model.joblib` is missing | Put the instructor-provided artifact beside `main.py`. Importing the application loads it before tests run. |
| Model cannot load or a version mismatch appears | Use the supplied model and matching Python/ML versions. Reinstalling unrelated latest packages is not the intended fix. |
| `no tests ran` | Check the filename `test_api.py`, function names starting with `test_`, and the current working folder. |
| The prediction test reports `TODO` | Complete the allowed-label assertion. This placeholder is intentionally incomplete. |
| The predicted label differs from your guess | Check membership in `spam`/`ham`; this test does not require a particular prediction for the example sentence. |
| Empty or whitespace-only input returns 200 | Check that trimming and `min_length=1` remain in `SMSRequest`, and that the tests import the intended lab copy. |
| The overlong-input test returns 200 | Add `max_length=500` in the lab copy, save `main.py`, and rerun pytest. Each new run imports the saved code again. |
| A 500-character input is rejected | Check the exact maximum and the input construction. The boundary itself must remain allowed. |
| A failure says 200 was expected to equal 201 | Restore the health assertion to 200 after the deliberate instructor demo. |
| PowerShell blocks activation | Use the virtual environment's Python directly, as shown below; changing machine-wide policy is unnecessary for the lab. |

PowerShell direct-interpreter alternative, after creating `.venv`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -c "from main import app; print(app.title)"
.\.venv\Scripts\python.exe -m pytest -q
```

On macOS/Linux, the equivalent direct interpreter is `./.venv/bin/python`.

## Sources

The API starting point comes from the [existing Session 5 worksheet](../../../../lab4/part2.md). TestClient usage follows [FastAPI — Testing](https://fastapi.tiangolo.com/tutorial/testing/); assertion discovery/reporting follows [pytest — Get started](https://docs.pytest.org/en/stable/getting-started.html). The new limit uses [Pydantic — StringConstraints](https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints).
