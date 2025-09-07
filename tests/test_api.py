import os
from fastapi.testclient import TestClient
from src.api import app

API_KEY = os.environ.get("ENDPOINT_API_KEY", "seu_token_aqui")


def test_get_all_predictions():
    """Test the /predictions endpoint"""
    with TestClient(app) as client:
        response = client.get("/predictions", headers={"Authorization": f"Bearer {API_KEY}"})
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        if response.json():
            match = response.json()[0]
            assert "match_id" in match
            assert "predictions" in match


def test_get_stats():
    """Test the /stats endpoint"""
    with TestClient(app) as client:
        response = client.get("/stats", headers={"Authorization": f"Bearer {API_KEY}"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json() == {} or "accuracy" in response.json() or "error" in response.json()


def test_get_last_update():
    """Test the /meta/last-update endpoint"""
    with TestClient(app) as client:
        response = client.get("/meta/last-update", headers={"Authorization": f"Bearer {API_KEY}"})
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert "last_update" in response.json()
        else:
            assert "not found" in response.json()["detail"].lower()
