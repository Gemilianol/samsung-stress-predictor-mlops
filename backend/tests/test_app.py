# tests/test_app.py
import json
import numpy as np
from unittest.mock import patch, mock_open
from app import app

mock_features = [
    "heart_max_rate","heart_min_rate","heart_rate",
    "stress_max","stress_min",
    "heart_min_rate_lag1","heart_min_rate_lag2","heart_min_rate_lag3"
]

def test_predict_route_success():
    client = app.test_client()
    fake_prediction = np.array([123.45])

    # mock_open provides a fake file with JSON content
    m = mock_open(read_data=json.dumps(mock_features))

    with patch("builtins.open", m), \
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

    assert response.status_code == 200, response.data.decode()
    data = response.get_json()
    assert "Prediction" in data and isinstance(data["Prediction"], (float, int))


    
    
