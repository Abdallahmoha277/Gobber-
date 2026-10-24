from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "testpassword123"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_login_user():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
