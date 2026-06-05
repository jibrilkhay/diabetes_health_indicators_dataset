# Diabetes Health Indicators Analysis

## Présentation

Ce projet analyse les facteurs de santé associés au diabète à partir du jeu de données **Diabetes Health Indicators BRFSS 2015**.

L’objectif est d’étudier comment des variables comme l’hypertension, le cholestérol, le BMI, l’âge, l’activité physique ou l’état de santé général sont liées à la présence du diabète.

## Problématique

Quels indicateurs de santé sont les plus fortement associés à la présence du diabète, et comment certaines combinaisons de variables permettent-elles de mieux expliquer le risque ?

## Jeu de données

Source : Kaggle, **Diabetes Health Indicators Dataset**

Fichiers CSV possibles :

- `diabetes_012_health_indicators_BRFSS2015.csv`
- `diabetes_binary_5050split_health_indicators_BRFSS2015.csv`
- `diabetes_binary_health_indicators_BRFSS2015.csv`

Les fichiers de données ne sont pas versionnés dans ce dépôt. Ils doivent être téléchargés depuis Kaggle puis placés dans le dossier [data](C:/Users/khjib/Documents/data/data).

## Variables principales

- `Diabetes_binary`
- `HighBP`
- `HighChol`
- `BMI`
- `Smoker`
- `PhysActivity`
- `Fruits`
- `Veggies`
- `GenHlth`
- `Age`
- `Income`
- `Education`

## Méthodologie

Le projet suit les grandes étapes suivantes :

1. chargement des données
2. exploration des variables
3. création d’une table EDA
4. visualisations
5. analyse des corrélations
6. étude de combinaisons de variables
7. régression logistique
8. comparaison entre jeu équilibré et jeu déséquilibré
9. interprétation des résultats

Des compléments sont disponibles dans :

- [docs/dataset_description.md](C:/Users/khjib/Documents/data/docs/dataset_description.md)
- [docs/methodology.md](C:/Users/khjib/Documents/data/docs/methodology.md)

## Résultats principaux

Les facteurs les plus associés au diabète dans cette étude sont notamment :

- l’hypertension
- le cholestérol élevé
- un BMI élevé
- l’âge
- l’état de santé général
- les difficultés physiques et de mobilité

## Structure du dépôt

```text
diabetes-health-indicators-analysis/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- data/
|   `-- README.md
|-- src/
|   `-- README.md
|-- outputs/
|   |-- figures/
|   `-- reports/
|-- docs/
`-- notebooks/
    `-- README.md
```

## Visualisations

Les figures générées sont disponibles dans [outputs/figures](C:/Users/khjib/Documents/data/outputs/figures).

## Rapports

Les rapports du projet sont disponibles dans [outputs/reports](C:/Users/khjib/Documents/data/outputs/reports).

## Installation

```bash
python -m venv venv
source venv/bin/activate
```

Sous Windows :

```powershell
venv\Scripts\activate
```

Puis :

```bash
pip install -r requirements.txt
```

## Lancement

Exemple :

```bash
python src/logistic_regression_balanced_vs_imbalanced.py
```

Remarque : certains scripts conservent des chemins absolus issus de l’environnement d’origine. Ils ont été laissés tels quels afin de ne pas modifier la logique initiale du projet.

## Limites

- les données sont déclaratives
- elles ne permettent pas d’établir une causalité directe
- le dataset concerne la population américaine
- les types de diabète peuvent être mélangés dans la cible
- les résultats ne constituent pas un outil médical de diagnostic

## Technologies utilisées

- Python
- Pandas
- DuckDB
- Matplotlib
- Seaborn
- Scikit-learn
- Régression logistique

## Auteurs

- Jibril Khay
- Yassine El Hadiri
- Florent Accaries

Les noms ont été conservés à partir des documents déjà présents dans le projet.
