import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from src.pipeline.predict_pipeline import predict_input

@patch('src.pipeline.predict_pipeline.joblib.load')
@patch('src.pipeline.predict_pipeline.glob.glob')
@patch('src.pipeline.predict_pipeline.pd.read_csv')
def test_if_na_data_provided(mock_read_csv,mock_glob,mock_joblib):
    
    # The mock for model.pkl
    mock_glob.return_value = ['models/xgb_model_20240720.pkl']
    
    # The mock of the model itself
    # MagicMock() in order to call then .assert_not_called() and predict
    mock_joblib.return_value = {"key": "value", "model": MagicMock()}
    
    # ✅ Return real DataFrames — not mocks
    # lambda path: Every time that pd.read_csv(path) is called then return a new DF.
    # Without lambda path every call will return the same DF. 
    mock_read_csv.side_effect = lambda path: pd.DataFrame({
    'heart_max_rate': [np.nan],
    'heart_min_rate': [65],
    'heart_rate': [np.nan],
    'stress_max': [np.nan],
    'stress_min':[1],
    'heart_min_rate_lag1': [75],
    'heart_min_rate_lag2':[62],
    'heart_min_rate_lag3': [69]})
    
    # ⚠️ Check if ValueError is raised:
    with pytest.raises(ValueError, match='You have to provide all the values to predict your Stress Score'):
        predict_input(mock_read_csv)
        
@patch('src.pipeline.predict_pipeline.joblib.load')
@patch('src.pipeline.predict_pipeline.glob.glob')
@patch('src.pipeline.predict_pipeline.pd.read_csv')    
def test_if_not_model_path(mock_read_csv,mock_glob,mock_joblib):
    
    # 1️⃣ I need to mock a full form in order to pass the first if statement.
    mock_read_csv.side_effect = None # Restart the side effect from the preview test.
    mock_read_csv.return_value = pd.DataFrame({
        'heart_max_rate': 102,
        'heart_min_rate': 65,
        'heart_rate': 86,
        'stress_max': 99,
        'stress_min':10,
        'heart_min_rate_lag1': 57,
        'heart_min_rate_lag2':62,
        'heart_min_rate_lag3': 69
    }, index=[0]) 
    
    mock_glob.return_value =[]
    
    # 2️⃣ The I can try directly if runs the exception
    with pytest.raises(RuntimeError, match='📄 Model file not found'):
        predict_input(mock_read_csv.return_value)
        
@patch('src.pipeline.predict_pipeline.joblib.load')
@patch('src.pipeline.predict_pipeline.glob.glob')
@patch('src.pipeline.predict_pipeline.pd.read_csv')    
def test_if_model_path(mock_read_csv,mock_glob,mock_joblib):
    
    # 1️⃣ I need to mock a full form in order to pass the first if statement.
    mock_read_csv.side_effect = None # Restart the side effect from the preview test.
    mock_read_csv.return_value = pd.DataFrame({
        'heart_max_rate': 102,
        'heart_min_rate': 65,
        'heart_rate': 86,
        'stress_max': 99,
        'stress_min':10,
        'heart_min_rate_lag1': 57,
        'heart_min_rate_lag2':62,
        'heart_min_rate_lag3': 69
    }, index=[0]) 
    
    mock_glob.return_value =['models/xgb_model_20240720.pkl']
    
    # Act
    predict_input(mock_read_csv.return_value)
    
    # Assert
    mock_joblib.assert_called_once_with('models/xgb_model_20240720.pkl')


@patch('src.pipeline.predict_pipeline.joblib.load')
@patch('src.pipeline.predict_pipeline.glob.glob')
@patch('src.pipeline.predict_pipeline.pd.read_csv')
def test_model_predict(mock_read_csv,mock_glob,mock_joblib):
    
    # 1️⃣ I need to mock a full form in order to pass the first if statement.
    mock_read_csv.side_effect = None # Restart the side effect from the preview test.
    mock_read_csv.return_value = pd.DataFrame({
        'heart_max_rate': 102,
        'heart_min_rate': 65,
        'heart_rate': 86,
        'stress_max': 99,
        'stress_min':10,
        'heart_min_rate_lag1': 57,
        'heart_min_rate_lag2':62,
        'heart_min_rate_lag3': 69
    }, index=[0]) 
    
    mock_glob.return_value =['models/xgb_model_20240720.pkl']
    
    # Simulated model with .predict
    mock_model = MagicMock()
    mock_model.predict.return_value = [742]
    mock_joblib.return_value = mock_model

    # Act
    result = predict_input(mock_read_csv.return_value)

    # Assert
    mock_model.predict.assert_called_once()
    assert result == 742 or result == [742]