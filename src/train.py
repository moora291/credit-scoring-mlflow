"""Train a baseline XGBoost credit-scoring model from raw Home Credit data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier


# Input data location (tracked via Git LFS).
RAW_DATA_DIR = Path("../data/raw")
# Derived datasets are written here; keep out of version control.
OUTPUT_DATA_DIR = Path("../data/output")
# Trained model artifact (intentionally not tracked in Git).
MODEL_OUTPUT = Path("../models/credit_scoring_xgb.joblib")


def load_raw_tables(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the core raw tables needed for feature engineering."""
    # Core tables used across notebooks and the baseline script.
    train_raw = pd.read_csv(data_dir / "application_train.csv")
    test_raw = pd.read_csv(data_dir / "application_test.csv")
    bureau = pd.read_csv(data_dir / "bureau.csv")
    return train_raw, test_raw, bureau


def preprocess(df: pd.DataFrame, bureau_df: pd.DataFrame | None = None, is_train: bool = True) -> pd.DataFrame:
    """Build a compact feature set for the baseline model.

    Notes:
    - Some feature names are kept from the original project for compatibility
      with downstream notebooks.
    """
    # Minimal feature table for a fast, reproducible baseline.
    df_result = pd.DataFrame()
    df_result["id"] = df["SK_ID_CURR"]
    df_result["age"] = (-df["DAYS_BIRTH"] / 365).round().astype(int)
    df_result["revenu_annuel"] = df["AMT_INCOME_TOTAL"]
    df_result["nombre_enfants"] = df["CNT_CHILDREN"]
    df_result["anciennete"] = (-df["DAYS_EMPLOYED"] / 365).replace(365243 / 365, 0).round(1)
    df_result["score_client"] = df[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].mean(axis=1)
    # Combine contract + education to encode a coarse product category.
    df_result["categorie_produit"] = LabelEncoder().fit_transform(
        df["NAME_CONTRACT_TYPE"] + "_" + df["NAME_EDUCATION_TYPE"]
    )
    df_result["montant_credit"] = df["AMT_CREDIT"]
    df_result["taux_endettement"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
    df_result["niveau_education"] = LabelEncoder().fit_transform(df["NAME_EDUCATION_TYPE"].fillna("Unknown"))
    df_result["statut_familial"] = LabelEncoder().fit_transform(df["NAME_FAMILY_STATUS"].fillna("Unknown"))

    # Add a simple credit history signal from bureau data.
    if bureau_df is not None:
        nb_retards = bureau_df[bureau_df["CREDIT_DAY_OVERDUE"] > 0].groupby("SK_ID_CURR").size()
        df_result["historique_impayes"] = df["SK_ID_CURR"].map(nb_retards).fillna(0).astype(int)
    else:
        df_result["historique_impayes"] = 0

    if is_train:
        df_result["target"] = df["TARGET"]
    return df_result


def build_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate train/test datasets and save them to the output folder."""
    # Load raw data and build the compact feature tables.
    train_raw, test_raw, bureau = load_raw_tables(RAW_DATA_DIR)
    df_train = preprocess(train_raw, bureau, is_train=True)
    df_test = preprocess(test_raw, bureau, is_train=False)

    # Persist derived datasets for notebook workflows.
    OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df_train.to_csv(OUTPUT_DATA_DIR / "dataset_train.csv", index=False)
    df_test.to_csv(OUTPUT_DATA_DIR / "dataset_test.csv", index=False)

    return df_train, df_test


def train_xgboost(df_train: pd.DataFrame) -> XGBClassifier:
    """Train an XGBoost classifier with class imbalance handling."""
    # Split features/target and compute class-imbalance ratio.
    X = df_train.drop(columns=["target", "id"])
    y = df_train["target"]
    scale = y.value_counts()[0] / y.value_counts()[1]

    model = XGBClassifier(
        scale_pos_weight=scale,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(X, y)
    return model


def main() -> None:
    """Run the end-to-end training pipeline."""
    # Build datasets and train the baseline model.
    df_train, _ = build_datasets()
    model = train_xgboost(df_train)
    # Save the trained artifact for local use (not committed).
    MODEL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    dump(model, MODEL_OUTPUT)
    print(f"Model saved to {MODEL_OUTPUT}")


if __name__ == "__main__":
    main()
