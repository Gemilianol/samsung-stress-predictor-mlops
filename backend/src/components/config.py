
"""
Placeholder config file for CI/CD tests.
Replace with real configuration in development/production environments.
"""

# Example dummy vars to avoid attribute errors in imports
DATA_PATH = ""
MODEL_PATH = ""
DATA_SOURCES = {
    'stress': {
        'file_path': '',
          'cols_to_keep': [],
          'col_date': 'date',
          'prefix': 'stress_'
    },
    'heart_rate': {
        'file_path': '',
              'cols_to_keep':[],
              'col_date': {'oem':'date',
                           'mod': 'date'},
              'prefix': 'heart_',
              'data_type': 'heart',
              'new_name_columns': ['date', 'heart_max_rate', 'heart_min_rate','heart_rate'],
              
    },
    'data_transformation': {
        'features_to_lag': ['heart_min_rate']
    }
}