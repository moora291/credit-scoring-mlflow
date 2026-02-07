"""Download the public credit-scoring model from Hugging Face."""

from __future__ import annotations

from pathlib import Path

from huggingface_hub import hf_hub_download


MODEL_REPO = "dworsleytonks/credit-scoring-xgb"
MODEL_FILENAME = "credit_scoring_xgb.pkl"
OUTPUT_DIR = Path("../models")


def download_model() -> Path:
    """Fetch the model artifact and return the local path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    local_path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILENAME,
        local_dir=OUTPUT_DIR,
        local_dir_use_symlinks=False,
    )
    return Path(local_path)


if __name__ == "__main__":
    path = download_model()
    print(f"Model downloaded to {path}")
