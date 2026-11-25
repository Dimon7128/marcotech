# Session 6 — Final lab solutions

Runnable SMS API combining the independent challenge solutions from
`sqlabs/Session6 - for instructor/labs/final-lab/solutions/`:

- `main.py` uses option A's policy to reject unexpected request fields.
- `test_extra_fields.py` and `test_response_format.py` contain options A and B's checks.
- The model, dependencies, Docker files and five baseline tests come from the completed Lab 1 solution.
- The repository workflow adapts option C to run on pushes affecting this folder.

## Set up and test

Use Python 3.10. From the repository root on macOS/Linux:

```bash
cd session6-final-lab
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Expected: **7 passed**. Keep `model.joblib` beside `main.py`.

## Run the API

From this folder with the environment activated:

```bash
python -m uvicorn main:app --reload
```

Open <http://127.0.0.1:8000/docs>. TestClient runs the tests directly, so a running Uvicorn server is optional for testing.

## CI

Commit both `session6-final-lab/` and
`.github/workflows/session6-final-lab-ci.yml` from the repository root so GitHub
receives the project and its workflow together.

[Session 6 Final Lab CI](../.github/workflows/session6-final-lab-ci.yml) runs on
branch pushes that change `session6-final-lab/**`. It installs the dependencies,
runs `python -m pytest -q`, then builds `sms-api:ci` using this folder as the Docker
build context. A failing test prevents the build step from running.

To build the same image locally, run from this folder:

```bash
docker build -f dockerfile -t sms-api:ci .
```
