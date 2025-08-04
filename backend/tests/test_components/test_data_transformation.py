import os
import pandas as pd
from src.components.data_transformation import data_transformation

def test_data_transformation_returns_dataframe():
    df = data_transformation()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_data_transformation_saves_csv():
    # Expected route of the csv file:
    output_path = 'data/processed/data.csv'

    data_transformation()
    
    assert os.path.exists(output_path)
    
    df = pd.read_csv(output_path)
    assert not df.empty
