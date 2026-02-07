# Credit Scoring with MLflow Tracking

> A production-oriented credit risk modeling workflow with full MLflow experiment tracking, feature engineering, model selection, and threshold tuning.

## Project Overview

This project builds a machine learning pipeline to predict the probability of default for loan applicants. It focuses on practical model development and experiment management, using MLflow to track parameters, metrics, and model artifacts across multiple experiments.

## What This Project Is / Is Not

**This project is:**
- A complete credit-scoring workflow from raw data to trained model
- An MLflow-tracked experiment suite with reproducible runs
- A baseline for risk modeling and cost-sensitive decision thresholds

**This project is not:**
- A production-ready scoring service
- A real-time inference system
- A fairness or regulatory compliance audit

## MLflow Emphasis

MLflow is used throughout the modeling workflow to:
- Track experiment parameters and metrics
- Compare candidate models (baseline and advanced)
- Store trained artifacts and assessment outputs
- Make model selection decisions reproducible

The notebooks show how each experiment is logged and compared in MLflow.

## Repository Structure

```
data/                      # Raw and output datasets (CSV tracked with Git LFS)
models/                    # Model artifacts (downloaded from Hugging Face)
notebooks/                 # End-to-end workflow notebooks
src/                       # Training script and utilities
pyproject.toml             # Dependencies
install.sh                 # Helper to set up the environment
```

## Folder Notes

- `data/raw/` holds the original CSVs tracked via Git LFS.
- `data/output/` is for derived datasets created by notebooks or `src/train.py`.
- `models/` stores the model downloaded from Hugging Face.
- `mlruns/` is the local MLflow tracking directory (kept with a `.keep` placeholder).

## Data Notes

- The raw CSVs are versioned with Git LFS.
- Derived datasets are written to `data/output/` and should not be committed.

## Workflow Summary

1. **Data prep** (`01_data_preparation.ipynb`)
   - Feature selection and cleaning
   - Train/test split and dataset export

2. **Baseline experiments** (`02_mlflow_experiments.ipynb`)
   - Baseline models and MLflow logging
   - Initial metric comparisons

3. **Algorithmic models** (`03_model_comparison.ipynb`)
   - RandomForest, XGBoost, CatBoost comparisons
   - Cross-validation and MLflow tracking

4. **Hyperparameter optimization** (`04_hyperparameter_optimization.ipynb`)
   - Optuna tuning
   - Threshold optimization for cost-sensitive decisions
   - Best model tracking in MLflow

## Training Script

A lightweight training script replaces the old `00_*` notebooks:

```bash
python src/train.py
```

It builds compact feature datasets and trains a baseline XGBoost model.

## Models

The model is hosted publicly on Hugging Face and downloaded on demand.

```bash
python src/download_model.py
```

Python usage:

```python
from huggingface_hub import hf_hub_download
import joblib

path = hf_hub_download(
    repo_id="dworsleytonks/credit-scoring-xgb",
    filename="credit_scoring_xgb.pkl",
    local_dir="models",
    local_dir_use_symlinks=False,
)
model = joblib.load(path)
```


## License

MIT License
