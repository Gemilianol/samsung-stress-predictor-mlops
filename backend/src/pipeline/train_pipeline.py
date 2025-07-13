import os
import glob
import argparse
from datetime import date
import pandas as pd
from src.components.model_trainer import train_selected_model

def train_execution_pipeline(force_retrain=False):
    """
    Decide if the model should be retrained based on:
    - If no model exists (initial training)
    - If the data is newer than the model (fresh data)
    - If force retrain is manually triggered

    Raises:
        RuntimeError: In case of error during retraining.
    """
    try:
        # 1️⃣ First time training:
        # Where are you?
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # Where do you need to go?
        MODEL_PATH = os.path.join(CURRENT_DIR, '..','..','models')
        
        # Where are the models?
        models_paths = glob.glob(f'{str(MODEL_PATH)}/xgb_model_*.pkl') #This returns a list
        models_paths.sort(reverse=True) # Order the model paths in descending order
        
        if len(models_paths) == 0:
            print("📦 No model found. Training from scratch...")
            train_selected_model()
        
        # 2️⃣ Check if we have fresh new data an a model updated:
        # Load transformed Dataset:
        data = pd.read_csv('data/processed/data.csv', sep=',')
        
        # Check the last date from the last registers:
        data['date'] = pd.to_datetime(data['date'])
        last_date_data = data['date'].dt.date.max()
        
        # Check the last time that the model was trained.
        model_metrics = pd.read_csv('logs/metrics_log.csv', sep=',')
        last_date_model = pd.to_datetime(model_metrics['date']).dt.date.max()
        
        if last_date_model < last_date_data and last_date_model + pd.Timedelta(days=7) < date.today():
            train_selected_model()
        
        elif force_retrain:
            print("🚨 Manual retraining triggered by CLI.")
            train_selected_model()
            
        else:
            print("✅ Model is up-to-date. No retraining needed.")
                   
    except Exception as e:
        raise RuntimeError(f'Error happened when was re-training the model => {e}') from e


if __name__ == '__main__':    
    # 3️⃣ If we need to force the re-training model for some reason we can do it through:
    parser = argparse.ArgumentParser()
    parser.add_argument('--force_retrain', action='store_true', help='Force retraining even if model exists')
    args = parser.parse_args()
    
    # If the user force the re training then force_retrain comes True:
    train_execution_pipeline(force_retrain=args.force_retrain)
    
    # On bash => from the root of the project => python backend/src/pipeline/train_pipeline.py --force_retrain

