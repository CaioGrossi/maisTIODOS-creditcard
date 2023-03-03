from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_auth_middleware_no_credentials():
    response = client.get("/api/v1/credit-card")
    assert response.status_code == 401
    assert response.json() == "No credentials provided"


def test_auth_middleware_invalid_credentials():
    response = client.get(
        "/api/v1/credit-card", headers={"Authorization": "Basic INVALID_CREDENTIAL"}
    )
    assert response.status_code == 401
    assert response.json() == "Invalid credentials provided"
