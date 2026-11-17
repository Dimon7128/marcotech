# Session 5  |  Expanded Mini-Labs

*Part 3: FastAPI  •  Part 4: Docker  •  Beginner-friendly, guided practice*

**Learning outcome:** Run the saved SMS spam/ham pipeline through an HTTP API, then package and test the same application inside Docker.

## Before you begin

- Python matching Session 4, a terminal or VS Code; Docker Desktop / Docker Engine for Part 4.
- A trusted fitted whole Pipeline (TF-IDF + MultinomialNB) from Session 4, saved as model.joblib. No retraining.
- The exact compatible requirements.txt from the model-training environment. Add fastapi==0.128.2 and uvicorn==0.48.0 if absent; do not duplicate or upgrade the ML package pins.
- Use only synthetic SMS examples; do not log or publish real messages.
> Keep these files together in sms-service/: main.py, model.joblib, requirements.txt. Create Dockerfile during Lab 3.

### LAB 1  |  Run your first API

**10 minutes  |  After teaching Slide 15**

**Goal:** Start FastAPI and see an HTTP response in your browser.

1.  Open the sms-service folder in a terminal. Create a virtual environment and install dependencies.

```bash
python -m venv .venv
# macOS / Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2.  Create main.py with a health endpoint. (We will add prediction logic in Lab 2.)

```python
from fastapi import FastAPI

app = FastAPI(title="SMS Classifier")

@app.get("/health")
def health():
    return {"status": "ok"}
```

3.  Start the local web server, and leave the terminal open.

```bash
python -m uvicorn main:app --reload
```

4.  Open http://127.0.0.1:8000/health and then http://127.0.0.1:8000/docs.

> **CHECK:** GET /health returns HTTP 200 and {"status":"ok"}. You can also find /health in /docs.

> **Think about it:** Which program is the client (the browser), and which is the server (FastAPI)?
