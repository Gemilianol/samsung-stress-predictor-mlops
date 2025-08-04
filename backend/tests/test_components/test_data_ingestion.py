import pandas as pd
from src.components.data_ingestion import load_data
from src.components.config import DATA_SOURCES

def test_load_data_returns_dataframe():
    """ 
    Test for load_data function.
    """
    df = load_data(
        file_path=DATA_SOURCES['heart_rate']['file_path'],
        cols_to_keep=DATA_SOURCES['heart_rate']['cols_to_keep'],
        col_date=DATA_SOURCES['heart_rate']['col_date']['oem'],
        prefix=DATA_SOURCES['heart_rate']['prefix'],
        data_type=DATA_SOURCES['heart_rate']['data_type']
    )
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

# To run this from root (Bash): 
# choco install make (CMD as admin) or 
# sudo apt update sudo apt install make (Ubuntu) and then 
# run the Markfile directly through the command => make test from the root