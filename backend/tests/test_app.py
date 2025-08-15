import json
import pytest
from unittest.mock import patch
from app import app

# Mock data for model_features.json
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
    # Patch the open() call where model_features.json is read
    # patch("builtins.open") intercepts any open() calls in the tested code.
    with patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_features)

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

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Prediction" in data
    assert isinstance(data["Prediction"], (int, float))

    
    
