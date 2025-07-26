import os
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.metrics import root_mean_squared_error
from xgboost import XGBRegressor
import joblib  # For saving model

from src.components.data_transformation import data_transformation

#Ignore warnings in order to have a cleaner output
import warnings
warnings.filterwarnings('ignore')
#Suppress scientific notation
np.set_printoptions(suppress=True)


def train_selected_model():
    """
    Trains and evaluates an XGBoost Regressor on the prepared dataset.

    This function is responsible for:

    - Loading and transforming the raw data.
    - Splitting the data into training and test sets using a time-aware strategy.
    - Training an XGBRegressor using TimeSeriesSplit cross-validation.
    - Evaluating model performance on the test set.
    - Saving the trained model for future use.
    - Logging the RMSE every time the script is executed.

    Raises:
        RuntimeError: If any step in the pipeline fails.
    """

    try:
        #Load transform raw data and return the data as csv file:
        data_transformation()
        
        #Load transformed Dataset:
        data = pd.read_csv('data/processed/data.csv', sep=',')
        
        #Train-Test Split:
        data['date'] = pd.to_datetime(data['date'])
        
        #Always keep the last 90 days as Test Set:
        cutoff_date = data['date'].max() - pd.Timedelta(days=90)

        X_train = data[data['date'] < cutoff_date]
        y_train = X_train['stress_score']
        X_train = X_train.drop(columns=['stress_score'])

        X_test = data[data['date'] >= cutoff_date]
        y_test = X_test['stress_score']
        X_test = X_test.drop(columns=['stress_score'])
        
        # Drop the date becuase it's not necessary:
        #So we can safety drop it:
        X_train = X_train.drop(columns='date')
        X_test = X_test.drop(columns='date')
        
        # Use a rolling windows strategy as cross-validation
        tscv = TimeSeriesSplit()
        
        # Since cv it's not a param of XGBRegressor I need to wrapped into RandomSearch first
        xgb = XGBRegressor(objective='reg:squarederror', random_state=42)
        
        # At the beginning, we use an empty dict in order to use the default params from XGBRegressor
        # In nearly future, we can use this dict to tuning model.
        # HINT: You can play with the param_grid of models_trained.ipynb here.
        param_grid = {}
        
        xgbs = RandomizedSearchCV(
            xgb,
            param_distributions=param_grid,
            n_iter=1, # 1 because it's only the default XGBRegressor. If you modify param_grid then modify n_iter too. 
            scoring='neg_root_mean_squared_error',
            cv=tscv,
            n_jobs=-1,
            random_state=42
        )
        
        # Train different XGBRegressors (Only one (the default) in this case)
        xgbs.fit(X_train, y_train)
        
        # Keep the best of them
        bestXGB = xgbs.best_estimator_
        
        # Use it to predict on Test-set data:
        preds = bestXGB.predict(X_test)
        
        rmse = np.round(root_mean_squared_error(y_test,preds), 2)
        
        # Check the RMSE of the model:
        print(f'🗒️ RMSE of XGB Regressor (Default): {rmse}')
        
        # Save model
        os.makedirs("models", exist_ok=True)
        model_filename = f"models/xgb_model_{datetime.today().strftime('%Y%m%d')}.pkl"
        joblib.dump(bestXGB, model_filename)
        print(f"✅ Model saved to {model_filename}")

        # Log metrics
        os.makedirs("logs", exist_ok=True)
        log_path = "logs/metrics_log.csv"
        
        # If the file doesn't exist yet, then create it, open and write the header:
        if not os.path.exists(log_path):
            with open(log_path, "w") as f:
                f.write("date,model,rmse,path\n")
        
        # Else, if exist, then write the new metric from the new run ('a' means append line):
        with open(log_path, "a") as f:
            f.write(f"{datetime.today().strftime('%Y-%m-%d')},XGBRegressor,{rmse},{model_filename}\n")
        print(f"📝 Metrics logged to {log_path}")
        
        return bestXGB
        
    except Exception as e:
        raise RuntimeError(f'Error happened when was training the model => {e}') from e

# if __name__ == '__main__':
#     train_selected_model()