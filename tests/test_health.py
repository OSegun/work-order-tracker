from fastapi import status

from app.main import app
from app.routers.health import get_db
from tests.utils import client, override_get_db

app.dependency_overrides[get_db] = override_get_db


def test_live_answers_without_the_database():
    response = client.get("/health/live")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "alive"}


def test_ready_answers_when_the_database_responds():
    response = client.get("/health/ready")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ready"}


def test_ready_reports_503_when_the_database_fails():
    def broken_db():
        class Broken:
            def execute(self, *args, **kwargs):
                raise RuntimeError("no database")

        yield Broken()

    app.dependency_overrides[get_db] = broken_db
    try:
        response = client.get("/health/ready")
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert response.json() == {"detail": "Database unavailable"}
    finally:
        app.dependency_overrides[get_db] = override_get_db
