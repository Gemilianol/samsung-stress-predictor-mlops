# Here the focus is testing the orchestration logic of the pipeline.
# Since this is an orchestration function, we test the control flow, not the ML model itself.
# You're not testing the actual training, but whether the orchestration decides to call it under the right conditions.

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import date
from src.pipeline.train_pipeline import train_execution_pipeline

# The order of @patch decorators must match the reverse order of arguments passed into your function.
# You can also mock internal functions that never will be call inside the test in order
# to prevent real execution (e.g., avoid real read_csv calls during test).

# 1️⃣ Check if first time training works properly:
@patch('src.pipeline.train_pipeline.train_selected_model')
@patch('src.pipeline.train_pipeline.glob.glob')
@patch('src.pipeline.train_pipeline.pd.read_csv')
def test_train_from_scratch(mock_read_csv, mock_glob, mock_train):
    '''
    If you mock something and then the mock will be never call then it's
    preventing real execution of it when run the test.
     
    '''
    # Simulate no models existing
    mock_glob.return_value = []
    
    # ✅ Return real DataFrames — not mocks
    mock_read_csv.side_effect = [
        pd.DataFrame({'date': [pd.to_datetime(date.today())]}),  # This simulates data.csv
        pd.DataFrame({'date': [pd.to_datetime(date.today())]})   # This simulates metrics_log.csv
    ]

    # Run
    train_execution_pipeline()

    # Expect training to be triggered
    mock_train.assert_called_once()
    
# 2️⃣ Check if we have fresh new data an a model updated:
@patch('src.pipeline.train_pipeline.train_selected_model')
@patch('src.pipeline.train_pipeline.glob.glob')
@patch('src.pipeline.train_pipeline.pd.read_csv')
def test_train_due_new_data(mock_read_csv, mock_glob, mock_train):
    
    # Simulate models existing
    mock_glob.return_value = ['models/xgb_model_20250725.pkl']
    
    # ✅ Return real DataFrames — not mocks
    mock_read_csv.side_effect = [
        pd.DataFrame({'date': [pd.to_datetime(date.today())]}),  # This simulates data.csv
        pd.DataFrame({'date': [pd.to_datetime('2025-07-25')]})   # This simulates metrics_log.csv
    ]

    # Run
    train_execution_pipeline()

    # Expect training to be triggered
    mock_train.assert_called_once()

# 3️⃣ Check if we need to force the re-training model for some reason works properly:
@patch('src.pipeline.train_pipeline.train_selected_model')
@patch('src.pipeline.train_pipeline.glob.glob')
@patch('src.pipeline.train_pipeline.pd.read_csv')
def test_force_retrain(mock_read_csv, mock_glob, mock_train):
    # Simulate model exists
    mock_glob.return_value = ['models/xgb_model_20250720.pkl']

    # ✅ Return real DataFrames — not mocks
    mock_read_csv.side_effect = [
        pd.DataFrame({'date': [pd.to_datetime(date.today())]}),  # This simulates data.csv
        pd.DataFrame({'date': [pd.to_datetime(date.today())]})   # This simulates metrics_log.csv
    ]

    # Run with force
    train_execution_pipeline(force_retrain=True)

    # Expect training
    mock_train.assert_called_once()

# 4️⃣ Check if the dates condition is not meet and the function is not trigger it. 
@patch('src.pipeline.train_pipeline.train_selected_model')
@patch('src.pipeline.train_pipeline.glob.glob')
@patch('src.pipeline.train_pipeline.pd.read_csv')
def test_no_retrain_needed(mock_read_csv, mock_glob, mock_train):
    mock_glob.return_value = ['models/xgb_model_20250720.pkl']

    # ✅ Return real DataFrames — not mocks
    mock_read_csv.side_effect = [
        pd.DataFrame({'date': [pd.to_datetime(date.today())]}),  # This simulates data.csv
        pd.DataFrame({'date': [pd.to_datetime(date.today())]})   # This simulates metrics_log.csv
    ]

    # No force
    train_execution_pipeline(force_retrain=False)

    mock_train.assert_not_called()
