#!/bin/bash

echo "Initialisation de l’environnement Projet 6 OpenClassrooms..."

# Créer environnement Python avec uv
echo "Création de l’environnement Python avec uv..."
uv venv
source .venv/bin/activate

# Installer les dépendances à partir de pyproject.toml
echo "Installation des dépendances..."
uv pip install --editable . 

# Lancer l’UI MLflow
echo "Lancement de MLflow UI sur http://localhost:8889"
.venv/bin/mlflow ui --host 0.0.0.0 --port 8889 &

echo "Environnement prêt. Lancez vos notebooks depuis VSCode ou Jupyter."

jupyter lab