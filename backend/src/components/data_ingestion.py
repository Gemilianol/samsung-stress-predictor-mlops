import pandas as pd
from src.components.config import DATA_SOURCES

def process_heart_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Args:
        data (pd.DataFrame): Prehandled Heart Dataset.
    
    Returns:
        data (pd.DataFrame): Handled Heart Dataset.
    """
    try:
        df1 = data.groupby(DATA_SOURCES['heart_rate']['col_date']['mod'])[DATA_SOURCES['heart_rate']['cols_to_keep'][3]].max().reset_index()
        df2 = data.groupby(DATA_SOURCES['heart_rate']['col_date']['mod'])[DATA_SOURCES['heart_rate']['cols_to_keep'][1]].min().reset_index()
        df3 = data.groupby(DATA_SOURCES['heart_rate']['col_date']['mod'])[DATA_SOURCES['heart_rate']['cols_to_keep'][2]].median().reset_index()

        data = pd.merge(df1, df2, on= DATA_SOURCES['heart_rate']['col_date']['mod'], how='outer')
        data = pd.merge(data, df3, on= DATA_SOURCES['heart_rate']['col_date']['mod'], how='outer')

        data.columns = DATA_SOURCES['heart_rate']['new_name_columns']
        return data
    
    except Exception as e:
        raise RuntimeError(f'Error happened handling heart dataset => {e}') from e
        

def load_data(file_path: str, cols_to_keep: list,
              col_date: str, prefix: str, data_type: str = '') -> pd.DataFrame:
    """
    Loads a single Samsung Health CSV, cleans and aggregates it by date.

    Args:
        file_path (str): Path to the CSV file.
        cols_to_keep (list): List of columns to retain from the CSV.
        col_date (str): Name of the column containing date or datetime info.
        prefix (str): Prefix to apply to all columns (except date).
        data_type: Data type of the dataset (for example, heart).

    Returns:
        pd.DataFrame: Cleaned and aggregated dataframe with daily granularity.
    """
    try:
        data =  pd.read_csv(file_path,
                            sep=",",
                            usecols=cols_to_keep,
                            header=1,
                            index_col=False,
                            encoding="latin-1",
                            na_values=["", " ", "NaN", "nan"],
                            keep_default_na=True)
        
        data[col_date] = pd.to_datetime(data[col_date]).dt.date
        
        # Here I'll take the median because it's the most suitable for this case and also more robust to outliers:
        data = data.groupby(col_date).median().reset_index()
        
        data = data.rename(columns={col_date: 'date'})
        
        # data.isna() => Boolean pd.Dataframe .sum() => pd.Series (per feture) .sum() Total NaN of pd.Dataframe
        if data.isna().sum().sum() > 0:
            data = data.sort_values('date')
            data = data.bfill().ffill()
            
        if data_type == 'heart':
            data = process_heart_data(data)
            return data
        else:
            data.columns = ['date' if col == 'date' else f'{prefix}{col}' for col in data.columns]
            return data
        
    except Exception as e:
        raise RuntimeError(f'Error loading the CSV file => {e}') from e

# Uncomment this snippet only for testing or debugging purposes

# if __name__ == '__main__':
#     example = load_data(file_path= DATA_SOURCES['heart_rate']['file_path'],
#               cols_to_keep= DATA_SOURCES['heart_rate']['cols_to_keep'],
#               col_date= DATA_SOURCES['heart_rate']['col_date']['oem'],
#               prefix= DATA_SOURCES['heart_rate']['prefix'],
#               data_type= DATA_SOURCES['heart_rate']['data_type'])
    
#     print(example.head(5))