# 📊 Stress Score Prediction App (Samsung Health Data)

This personal, educational project predicts your **daily stress score in real time** based on heart and stress metrics provided by the user, primarily exported from **Samsung Health**.

---

## 🔧 Project Structure

- `backend/`: Flask-based API serving ML predictions
- `frontend/`: React.js client UI
- `data/`: Raw and processed data *(excluded from Git)*
- `models/`: Trained model artifacts *(excluded from Git)*
- `logs/`: Model training logs *(excluded from Git)*
- `notebooks/`: EDA and offline feature engineering

---

## ⚙️ Key Features

- End-to-end ML pipeline: data ingestion, transformation, training, prediction
- Feature engineering using domain knowledge
- Model monitoring and retraining logic via `train_pipeline.py`
- React + Flask integration for real-time interaction
- Docker-ready architecture *(optional setup)*

---

## 🧪 Development Notes

⚠️ **Feature selection** was performed offline using Random Forest importance. For simplicity, this version uses a fixed feature set and 3 lagged versions. Future work will include dynamic feature selection pipelines.

⚠️ **MLflow** is not integrated in this initial version due to common persistence issues with Docker Compose and volume-based URI management. Retraining is required each time containers restart, which is time-consuming. This will be addressed in future iterations.

⚠️️ **config.py**  src/components/config.py is a placeholder for CI and that production config is kept externally; this documents the approach.

---

## 🚧 Development Status

This is **Version 1 (MVP)**. The following enhancements are planned:

- [x] CI/CD pipeline (GitHub Actions)
- [ ] MLflow-based experiment tracking and model registry
- [ ] Monitoring with Prometheus + Grafana
- [ ] Orchestration with Airflow or Prefect
- [ ] Full Docker Compose / Kubernetes deployment

---

## ⚠️ Legal & Privacy Disclaimer

This project uses data exported from the author's personal **Samsung Health** account.  
Samsung and Samsung Health are trademarks of **Samsung Electronics Co., Ltd.**

- This is a **non-commercial, educational portfolio** project.
- It is **not affiliated with, endorsed by, or sponsored by Samsung**.
- **All data used is personal and local.** No third-party or private user data is exposed or shared.

