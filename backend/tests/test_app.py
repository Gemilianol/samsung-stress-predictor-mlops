import json
import pytest
import numpy as np
from unittest.mock import patch
from app import app

# list of feature names expected by your route (match model_features order)
mock_features = [
    "heart_max_rate",
    "heart_min_rate",
    "heart_rate",
    "stress_max",
    "stress_min",
    "heart_min_rate_lag1",
    "heart_min_rate_lag2",
    "heart_min_rate_lag3",
]

@pytest.fixture
def client():
    return app.test_client()

def test_predict_route_success(client):
    # patch json.load so the route believes models/model_features.json contains mock_features
    # and patch the predict_input function imported into 'app' to return a fake numeric prediction.
    fake_prediction = np.array([123.45])

    with patch("json.load", return_value=mock_features), \
         patch("app.predict_input", return_value=fake_prediction):

        response = client.post("/predict", json={
            "heart_max_rate": 102,
            "heart_min_rate": 102,
            "heart_rate": 102,
            "stress_max": 102,
            "stress_min": 102,
            "heart_min_rate_lag1": 102,
            "heart_min_rate_lag2": 102,
            "heart_min_rate_lag3": 102,
        })

    assert response.status_code == 200, f"body: {response.data.decode('utf-8')}"
    data = response.get_json()
    assert "Prediction" in data
    # numeric check (float or int)
    assert isinstance(data["Prediction"], (float, int))

    
    
