import os
import json
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
import joblib

from src.components.model_trainer import train_selected_model

# Create a minimal fake estimator (must have predict)
class FakeEstimator:
    def predict(self, X):
        # return zeros of the right shape
        import numpy as np
        return np.zeros(len(X))

@patch("src.components.model_trainer.RandomizedSearchCV")
def test_train_selected_model_mocked_random_search(mock_random_search, tmp_path, monkeypatch):
    # 1) isolate FS
    monkeypatch.chdir(tmp_path)

    # 2) write the processed CSV that trainer reads
    n = 120
    dates = pd.date_range("2020-01-01", periods=n)
    df = pd.DataFrame({
        "date": dates,
        "feat_a": np.linspace(0, 1, n),
        "feat_b": np.linspace(1, 0, n),
        "stress_score": np.random.randint(300, 1200, size=n)
    })
    (tmp_path / "data" / "processed").mkdir(parents=True, exist_ok=True)
    df.to_csv(tmp_path / "data" / "processed" / "data.csv", index=False)

    # 3) monkeypatch data_transformation to be noop
    monkeypatch.setattr("src.components.model_trainer.data_transformation", lambda: None)

    # 4) configure the RandomizedSearchCV mock to expose a .best_estimator_
    fake_search = MagicMock()
    fake_search.fit.return_value = None
    fake_search.best_estimator_ = FakeEstimator()
    mock_random_search.return_value = fake_search

    # 5) run; should use the patched RandomizedSearchCV
    train_selected_model()

    # 6) assertions: files created
    assert (tmp_path / "models").exists()
    models = list((tmp_path / "models").glob("xgb_model_*.pkl"))
    assert len(models) >= 1

    # check logs
    assert (tmp_path / "logs" / "metrics_log.csv").exists()
    log_df = pd.read_csv(tmp_path / "logs" / "metrics_log.csv")
    assert not log_df.empty

    # ensure the mocked RandomizedSearchCV was instantiated
    mock_random_search.assert_called_once()

