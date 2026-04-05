# warehouse-mlops
Logistics Warehouse ML Project (End‑to‑End MLOps)
🚚 Logistics Warehouse ML Project (End‑to‑End MLOps)
📌 Project Overview
This repository demonstrates a production‑ready MLOps pipeline built on the Kaggle Logistics Warehouse Dataset.
The goal is to show how to design, train, evaluate, and deploy machine learning models in a scalable, reproducible, and monitored environment using modern MLOps tooling.

🛠 Tech Stack
ZenML → pipeline orchestration

MLflow / Kubeflow → experiment tracking & model registry

Docker → containerization for reproducible environments

CI/CD (GitHub Actions) → automated testing, builds, and deployments

VS Code → local development with virtual environments

📂 Folder Structure
warehouse-mlops/

│── data/                  # raw & processed datasets
│── src/
│   ├── config/            # YAML configs
│   ├── data/              # ingestion, preprocessing
│   ├── features/          # feature engineering
│   ├── models/            # training, evaluation
│   ├── pipelines/         # ZenML pipelines
│   ├── utils/             # decorators, logging
│── tests/                 # pytest unit tests
│── Dockerfile
│── requirements.txt
│── .github/workflows/ci.yml

⚙️ Workflow
Data Ingestion → load raw CSV from Kaggle.

Preprocessing → handle missing values, scale numerics, encode categoricals.

Feature Engineering → domain‑specific transformations.

Model Training → RandomForest baseline, tracked in MLflow.

Threshold Check → only models with accuracy ≥ 0.80 are accepted and containerized.

Evaluation → classification report, logged metrics.

Deployment → Docker image built and pushed via CI/CD.

📈 Monitoring & Logging
Logs: All pipeline steps are decorated with logging (logs/project.log).

MLflow UI: Run mlflow ui to visualize metrics, parameters, and artifacts.

Thresholds: Models below 80% accuracy are rejected automatically.

Failure Handling:

CI/CD failure → rollback to last stable Docker image.

Monitoring drift → retrain pipeline when accuracy drops below threshold.

Logging failure → fallback to console logs, alerts in CI/CD pipeline.

🔄 CI/CD Strategy
Lint & Test: pytest runs on every push.

Build: Docker image built automatically.

Deploy: Only triggered if tests pass and accuracy ≥ 0.80.

Rollback: If deployment fails, revert to last stable image.

🧠 Strategy for Interviews
When explaining this project:

Problem Solving: Start with business KPIs (warehouse efficiency, demand prediction).

Scalability: Show how Docker + CI/CD ensures reproducibility.

Resilience: Emphasize monitoring, thresholds, and rollback strategies.

Collaboration: Config‑driven pipelines make results reproducible for teammates.

🚀 How to Run Locally
# Clone repo
git clone https://github.com/<your-username>/warehouse-mlops.git
cd warehouse-mlops

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run ZenML pipeline
python src/pipelines/warehouse_pipeline.py

# Start MLflow UI
mlflow ui

📜 License
MIT License – free to use and modify.
