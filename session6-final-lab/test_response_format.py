from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_prediction_declares_json_media_type():
    response = client.post("/predict", json={"message": "Meeting at five"})
    assert response.status_code == 200
    assert "label" in response.json()
    assert response.json()["label"] in {"spam", "ham"}
    media_type = response.headers.get("content-type", "").split(";", 1)[0]
    assert media_type.strip().lower() == "application/json"
