#!/bin/bash

echo "Initializing the credit scoring environment..."

# Create a Python environment with uv
echo "Creating the Python environment with uv..."
uv venv
source .venv/bin/activate

# Install dependencies from pyproject.toml
echo "Installing dependencies..."
uv pip install --editable . 

echo "Environment ready. Launch notebooks in VSCode or Jupyter."

jupyter lab
