from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_unexpected_request_field_is_rejected():
    response = client.post(
        "/predict", json={"message": "Meeting at five", "unexpected": True}
    )
    assert response.status_code == 422
