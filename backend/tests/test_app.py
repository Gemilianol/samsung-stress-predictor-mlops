import json
from app import app

def test_predict_route_success():
    
    client = app.test_client()
    
    response = client.post("/predict", json={
     'heart_max_rate': 102, 
     'heart_min_rate': 102,
     'heart_rate': 102, 
     'stress_max': 102,
     'stress_min': 102,
     'heart_min_rate_lag1': 102, 
     'heart_min_rate_lag2': 102, 
     'heart_min_rate_lag3': 102,
     })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Prediction" in data
    assert isinstance(data["Prediction"], (int, float))
    
    
