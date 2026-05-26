"""Smoke test for the /health endpoint.

This is intentionally the *simplest* possible test:
    - we import the FastAPI app
    - we send a GET /health using FastAPI's built-in TestClient
    - we assert HTTP 200 and the exact JSON body

If this test passes, we know the app boots cleanly and the framework
wiring (FastAPI + routes + JSON serialization) is healthy. It does NOT
touch OpenAI or the CSV, so it works offline without any API key.

Run it locally from the backend folder:
    pytest -q
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_returns_200_and_status_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
