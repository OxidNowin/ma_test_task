from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_upload_file():
    with open("test_image.png", "rb") as file:
        response = client.post("/file_management/upload/", files={"file": file})
        assert response.status_code == 200
        assert "uid" in response.json()

def test_get_file():
    uid = "some-existing-uid"
    response = client.get(f"/file_management/file/{uid}")
    assert response.status_code == 200
