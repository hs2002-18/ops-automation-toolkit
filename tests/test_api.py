import logging
from pathlib import Path

from fastapi.testclient import TestClient

from app.logger import logger

# Redirect logs for tests
logger.handlers.clear()

log_dir = Path("tests/logs")
log_dir.mkdir(parents=True, exist_ok=True)

file_handler = logging.FileHandler(log_dir / "test.log")
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s"
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

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