import pytest
import os
from fastapi.testclient import TestClient
from src.api import app

API_KEY = os.environ.get("ENDPOINT_API_KEY")


def test_get_all_predictions():
    with TestClient(app) as client:
        response = client.get("/predictions", headers={"x-api-key": API_KEY})
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        if response.json():
            match = response.json()[0]
            assert "match_id" in match
            assert "predictions" in match


def test_get_prediction_by_id_found():
    with TestClient(app) as client:
        response = client.get("/predictions", headers={"x-api-key": API_KEY})
        predictions = response.json()
        if predictions:
            match_id = predictions[0]["match_id"]
            response2 = client.get(f"/predictions/{match_id}", headers={"x-api-key": API_KEY})
            assert response2.status_code == 200
            assert response2.json()["match_id"] == match_id
        else:
            pytest.skip("No predictions available to test by id.")


def test_get_prediction_by_id_not_found():
    with TestClient(app) as client:
        response = client.get("/predictions/999999999", headers={"x-api-key": API_KEY})
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
