#!/bin/bash

echo "Initialisation de l’environnement Projet 6 OpenClassrooms..."

# Créer environnement Python avec uv
echo "Création de l’environnement Python avec uv..."
uv venv
source .venv/bin/activate

# Installer les dépendances à partir de pyproject.toml
echo "Installation des dépendances..."
uv pip install --editable . 

echo "Environnement prêt. Lancez vos notebooks depuis VSCode ou Jupyter."

jupyter lab