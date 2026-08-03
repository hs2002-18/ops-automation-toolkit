from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "test@example.com",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test User"