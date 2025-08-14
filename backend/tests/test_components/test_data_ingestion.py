from unittest.mock import patch, MagicMock
import pandas as pd
from src.components.data_ingestion import load_data

@patch('src.components.data_ingestion.pd.read_csv')
def test_load_data_returns_dataframe(mock_read_csv):
    # Create synthetic mock data
    mock_df = pd.DataFrame({
        'end_time': pd.date_range("2024-01-01", periods=10, freq='D'),
        'max': [70 + i for i in range(10)],
        'min': [60 + i for i in range(10)],
        'score': [50 + i for i in range(10)]
        })
    
    mock_read_csv.return_value = mock_df

    df = load_data(
        file_path="dummy/path.csv",  
        cols_to_keep=['end_time', 'max', 'min', 'score'],
        col_date='end_time',
        prefix='stress_'
    )

    assert isinstance(df, pd.DataFrame)
    assert not df.empty

# To run this from root (Bash): 
# choco install make (CMD as admin) or 
# sudo apt update sudo apt install make (Ubuntu) and then 
# run the Markfile directly through the command => make test from the root