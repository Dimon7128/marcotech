from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_prediction():
    response = client.post("/predict", json={"message": "Meeting at five"})
    assert response.status_code == 200
    assert "label" in response.json()
    assert response.json()["label"] in {"spam", "ham"}


def test_invalid_input():
    invalid_payloads = [
        {},
        {"message": ""},
        {"message": "   "},
        {"message": None},
        {"message": 123},
    ]
    for payload in invalid_payloads:
        response = client.post("/predict", json=payload)
        assert response.status_code == 422, payload


def test_maximum_length_is_accepted():
    response = client.post("/predict", json={"message": "x" * 500})
    assert response.status_code == 200
    assert response.json()["label"] in {"spam", "ham"}


def test_overlong_message_is_rejected():
    response = client.post("/predict", json={"message": "x" * 501})
    assert response.status_code == 422
