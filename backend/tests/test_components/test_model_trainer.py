import os
import glob
import joblib
import pandas as pd
from src.components.model_trainer import train_selected_model

def test_train_model_saves_model():
    
    train_selected_model()
    
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    # Absolute path => C:\Users\..\..\..\Samsung Health Project\backend\tests\test_components
    # Models dir it's at the same level of test so I need to move backward two steps:
    MODEL_PATH = os.path.join(CURRENT_PATH, '..', '..','models')
    
    model_paths = glob.glob(f'{str(MODEL_PATH)}/xgb_model_*.pkl')
    model_paths.sort(reverse=True)

    assert os.path.exists(model_paths[0])

    loaded_model = joblib.load(model_paths[0])
    assert loaded_model is not None

def test_train_model_returns_model():
    model = train_selected_model()

    from xgboost import XGBRegressor
    assert isinstance(model, XGBRegressor)

def test_train_model_logs_rmse():
    log_path = 'logs/metrics_log.csv'

    train_selected_model()
    
    assert os.path.exists(log_path)

    df = pd.read_csv(log_path)
    assert not df.empty
    assert 'rmse' in df.columns
