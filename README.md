# Projet 6 – Implémentez un modèle de scoring

Ce projet s'inscrit dans le cadre du parcours **"Data Scientist / AI Engineer"** chez OpenClassrooms. Il vise à construire un modèle de scoring de crédit bancaire optimisé selon un coût métier.

## Objectif

Concevoir une solution complète de machine learning pour :
- Prédire la capacité de remboursement d’un client,
- Minimiser un coût métier asymétrique,
- Optimiser les hyperparamètres et le seuil de décision,
- Industrialiser le modèle via MLflow.

## Étapes du projet

### 1. Préparation des données
- Nettoyage et sélection des variables pertinentes à partir d’un jeu de données brut.
- Séparation train/test.
- Sauvegarde des datasets au format `.parquet`.

> Voir `notebooks/01_preparation_donnees.ipynb`

### 2. Expérimentations de base
- Entraînement de modèles simples (Dummy, LogisticRegression).
- Calcul du coût métier.
- Suivi des runs avec MLflow.

> Voir `notebooks/02_experimentations_mlflow.ipynb`

### 3. Modélisation algorithmique
- Entraînement de modèles avancés : RandomForest, XGBoost, CatBoost.
- Comparaison via validation croisée.
- Choix d’un modèle de référence.

> Voir `notebooks/03_modele_algorithmique.ipynb`

### 4. Optimisation du modèle
- Optimisation des hyperparamètres avec Optuna.
- Recherche du meilleur seuil de décision entre 0.05 et 0.95.
- Enregistrement du modèle, du seuil optimal, et du coût minimal avec MLflow.

> Voir `notebooks/04_optimisation_hyperparametres.ipynb`

## Résultats

- Modèle final : **XGBoost** optimisé.
- Seuil optimal : `0.1`
- Coût métier minimum : `712`
- Enregistrement MLflow : Oui

## Structure du projet

```
projet6/
├── data/                    # Données sources et sorties (parquet, csv)
│   └── output/              # Données prêtes à l’emploi
├── notebooks/               # Notebooks de chaque étape
├── models/                  # Modèle entraîné sauvegardé
├── src/                     # Script d'entraînement principal
├── mlruns/                  # Dossier de tracking MLflow
├── train_model.py           # Script principal d’entraînement
├── pyproject.toml           # Dépendances (gestion avec uv ou poetry)
└── install.sh               # Script d’installation rapide
```

## Lancer l'entraînement

```bash
./install.sh
```

## Crédits et encadrement

**Auteur :** David Worsley-Tonks  
**Mentor :** Elie Wanko  
**Structure :** OpenClassrooms — Master AI Engineer - Projet 6