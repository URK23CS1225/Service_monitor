"""
Basic pytest tests for the /check API endpoint.
"""

import json
import pytest
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_check_missing_url(client):
    """Should return 400 when url is missing."""
    response = client.post("/check", data=json.dumps({}), content_type="application/json")
    assert response.status_code == 400
    assert b"url is required" in response.data


def test_check_down_service(client):
    """Should return DOWN for an unreachable URL."""
    payload = {"url": "http://localhost:19999"}
    response = client.post("/check", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "DOWN"
    assert "response_time" in data


def test_check_valid_url(client):
    """Should return UP or DOWN with a response_time for a real URL."""
    payload = {"url": "https://httpbin.org/status/200"}
    response = client.post("/check", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] in ("UP", "DOWN")
    assert "response_time" in data
