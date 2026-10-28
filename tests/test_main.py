from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# def test_check_health():
#     response = client.get("/health")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == {"status": "Healthy"}
