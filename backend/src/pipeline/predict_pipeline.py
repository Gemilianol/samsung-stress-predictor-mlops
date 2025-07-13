import pandas as pd
import numpy as np
import glob
import joblib
import os

def predict_input(X: pd.DataFrame) -> np.array:
    """ Take rows as input and return its predictions.

    Args:
        X (pd.DataFrame): input values for each feature

    Returns:
        np.array : with the corresponded predictions
    """
    try:
        if X.isna().any().any():
            raise ValueError('You have to provide all the values to predict your Stress Score')
        
        CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
        # Absolute path => C:\Users\..\..\..\Samsung Health Project\backend\src\pipeline
        # Models dir it's at the same level of backend so I need to move backward two times:
        MODEL_PATH = os.path.join(CURRENT_PATH, '..','..','models')
        
        model_paths = glob.glob(f'{str(MODEL_PATH)}/xgb_model_*.pkl')
        model_paths.sort(reverse=True)
        
        print(model_paths)
    
        if not model_paths:
            raise FileNotFoundError('👎 No model have been found to predict the request.')
            
        model = joblib.load(model_paths[0]) # Get the most updated model
        
        pred = model.predict(X)
        
        return pred
    
    except Exception as e:
        raise RuntimeError(f'Error happened when tried to predict => {e}') from e

# if __name__ == '__main__':
    
#     data = pd.DataFrame({
#         'heart_max_rate': 102,
#         'heart_min_rate': 65,
#         'heart_rate': 86,
#         'stress_max': 99,
#         'stress_min':1,
#         'heart_min_rate_lag1': 57,
#         'heart_min_rate_lag2':62,
#         'heart_min_rate_lag3': 69
#     }, index=[0]) 
#     # If you use scalar values like these then pass an index value too. 
    
#     pred = predict_input(data)
    
#     print(f'The predicted Stress Score is: {np.round(pred,2)}')
