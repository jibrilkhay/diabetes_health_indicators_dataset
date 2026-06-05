# Dossier source

Ce dossier regroupe les scripts d’analyse du projet, sans modification de leur logique de fond.

## Rôle des fichiers

- `data_preparation.py` : script le plus complet. Il charge les données, construit la table EDA, crée des variables combinées, prépare les tables pour la régression logistique, équilibre les données puis évalue le modèle.
- `eda_with_plot_test.py` : script d’exploration plus léger qui se termine par une visualisation ciblée.
- `plot_generation.py` : script principal de génération des graphiques EDA et des visualisations de corrélation.
- `feature_combination_experiments.py` : script d’expérimentation servant à justifier certaines variables combinées, notamment `Metabolic_Risk`.
- `logistic_regression_balanced_vs_imbalanced.py` : script centré sur la comparaison entre un jeu équilibré et un jeu déséquilibré.
- `features_reference.py` : liste de référence des variables finales et des variables combinées.
- `diabetes_eda_table.sql` : définition SQL de la table `diabetes_eda`.

## Remarque

Certains scripts se recouvrent partiellement car ils correspondent à différentes étapes du projet :

- exploration
- visualisation
- validation des combinaisons de variables
- comparaison finale des modèles

Seules les répétitions les plus évidentes ont été nettoyées. Le déroulé analytique a été conservé.
