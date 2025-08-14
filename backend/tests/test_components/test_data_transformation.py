import pandas as pd
import numpy as np
from unittest.mock import patch
from pathlib import Path

from src.components.data_transformation import data_transformation

# Here a helper function which returns the same dfs which returns load_data
def make_mock_dfs(n=10):
    dates = pd.date_range("2024-01-01", periods=n, freq="D")
    heart_df = pd.DataFrame({
        "date": dates,
        "heart_rate": np.random.randint(60, 100, size=n),
        "heart_min_rate": np.random.randint(50, 70, size=n),
        "heart_max_rate": np.random.randint(90, 110, size=n),
    })
    stress_df = pd.DataFrame({
        "date": dates,
        "stress_min": np.random.randint(1, 5, size=n),
        "stress_max": np.random.randint(30, 100, size=n),
        "stress_score": np.random.randint(300, 1200, size=n),
    })
    return heart_df, stress_df

@patch("src.components.data_transformation.load_data")
def test_data_transformation_returns_dataframe(mock_load_data, tmp_path, monkeypatch):
    # Arrange: mock load_data to return our mock DataFrames
    heart_df, stress_df = make_mock_dfs(n=20)
    # The code calls load_data twice (stress then heart) — ensure ordering matches your function
    mock_load_data.side_effect = [stress_df, heart_df]

    # Also patch DATA_SOURCES inside the module to use 'date' as the merge key
    test_data_sources = {
        "heart_rate": {
            "col_date": {"oem": "date", "mod": "date"},
            "cols_to_keep": [],
            "prefix": "heart_",
            "data_type": "heart",
        },
        "stress": {
            "col_date": "date",
            "cols_to_keep": [],
            "prefix": "stress_",
        },
        "data_transformation": {
        'features_to_lag': ['heart_min_rate']
    }
    }
    
    # Replace attribute inside a module (handy for patching config objects).
    monkeypatch.setattr("src.components.config.DATA_SOURCES", test_data_sources, raising=False)

    # set working dir to the temp folder
    monkeypatch.chdir(tmp_path)

    # create target dir so the function can save there
    (tmp_path / "data" / "processed").mkdir(parents=True, exist_ok=True)

    df_out = data_transformation()
    
    assert (tmp_path / "data" / "processed" / "data.csv").exists()

    # Assert
    assert isinstance(df_out, pd.DataFrame)
    assert not df_out.empty
    # check that merged column exists (merge on 'date')
    assert "date" in df_out.columns
    
#------------------------------------------------------------------------------------------------------------
@patch("src.components.data_transformation.load_data")
def test_data_transformation_saves_csv(mock_load_data, tmp_path, monkeypatch):
    heart_df, stress_df = make_mock_dfs(n=30)
    mock_load_data.side_effect = [stress_df, heart_df]

    # Also patch DATA_SOURCES inside the module to use 'date' as the merge key
    test_data_sources = {
        "heart_rate": {
            "col_date": {"oem": "date", "mod": "date"},
            "cols_to_keep": [],
            "prefix": "heart_",
            "data_type": "heart",
        },
        "stress": {
            "col_date": "date",
            "cols_to_keep": [],
            "prefix": "stress_",
        },
        "data_transformation": {
        'features_to_lag': ['heart_min_rate']
    }
    }
    
    monkeypatch.setattr("src.components.config.DATA_SOURCES", test_data_sources, raising=False)
    
    # set working dir to the temp folder
    monkeypatch.chdir(tmp_path)

    # create target dir so the function can save there
    (tmp_path / "data" / "processed").mkdir(parents=True, exist_ok=True)

    # Act
    data_transformation()

    # Assert file exists at data/processed/data.csv under tmp_path
    out_path = tmp_path / "data" / "processed" / "data.csv"
    
    # read and assert content
    df_read = pd.read_csv(out_path)
    assert not df_read.empty
    assert "date" in df_read.columns
