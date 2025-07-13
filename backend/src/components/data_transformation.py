from src.components.data_ingestion import load_data
from src.components.config import DATA_SOURCES
import pandas as pd

def lag_features(data: pd.DataFrame, features: list) -> pd.DataFrame:
    """ For each feature that it's present on the list, add a shifted version of it from 1 to 3 lags

    Args:
        data (pd.DataFrame): Loaded and merged Datasets
        features (list): Features to shift
        
    Returns:
        data (pd.DataFrame): Same Dataset with the Lagged features. 
    """
    try:
        data = data.sort_values(by=DATA_SOURCES['heart_rate']['col_date']['mod'])
        
        for feature in features:
            for i in range(1,4):
                data[f'{feature}_lag{i}'] = data[feature].shift(i)

        data.dropna(inplace=True)
        
        return data
    except Exception as e:
        raise RuntimeError(f'Error during lag feature generation => {e}') from e

def data_transformation():
    """ Consolidates all actions required before the dataset can be ingested by the model.
    This script:
    - Loads the latest CSV files for heart rate and stress data.
    - Merges them on the appropriate date column.
    - Applies lag features based on a predefined configuration.
    - Saves the resulting dataset to `data/processed/data.csv` for use in model training and evaluation.

    This script is intended to be run manually or as part of a preprocessing pipeline before training.
    """
    try:
        stress_data = load_data(file_path= DATA_SOURCES['stress']['file_path'],
                cols_to_keep= DATA_SOURCES['stress']['cols_to_keep'],
                col_date= DATA_SOURCES['stress']['col_date'],
                prefix= DATA_SOURCES['stress']['prefix'])
            
        heart_data = load_data(file_path= DATA_SOURCES['heart_rate']['file_path'],
                cols_to_keep= DATA_SOURCES['heart_rate']['cols_to_keep'],
                col_date= DATA_SOURCES['heart_rate']['col_date']['oem'],
                prefix= DATA_SOURCES['heart_rate']['prefix'],
                data_type= DATA_SOURCES['heart_rate']['data_type'])
        
        data=pd.merge(heart_data, stress_data, on=DATA_SOURCES['heart_rate']['col_date']['mod'], how='outer')
        
        if data.duplicated().sum() > 0:
            data = data.groupby(DATA_SOURCES['heart_rate']['col_date']['mod']).median().reset_index()
            data = data.sort_values[DATA_SOURCES['heart_rate']['col_date']['mod']]
            
        data = lag_features(data, DATA_SOURCES['data_transformation']['features_to_lag'])
        
        data.to_csv('data/processed/data.csv', index=False)
        
        print("✅ Lagged dataset saved to data/processed/data.csv")
    except Exception as e:
        raise RuntimeError(f'Error happened handling heart dataset => {e}') from e
    

# if __name__ == '__main__':
#     data_transformation()