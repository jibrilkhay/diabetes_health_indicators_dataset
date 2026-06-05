# diabetes_health_indicators_dataset

## 📊 Documentation du Jeu de Données : Indicateurs de Santé du Diabète (BRFSS 2015)

Ce document récapitule les informations essentielles concernant le jeu de données **Diabetes Health Indicators** issu de Kaggle, son dictionnaire de variables, ainsi qu'un avis critique sur l'utilisation de ces données pour la prédiction du diabète de type 2.

## 📋 1. Contexte et Origine

Ce jeu de données provient du **BRFSS (Behavioral Risk Factor Surveillance System)** de l'année 2015, une enquête téléphonique annuelle menée par le **CDC (Centers for Disease Control and Prevention)** aux États-Unis.

Le diabète est une maladie chronique majeure : **34,2 millions d'Américains** sont diabétiques et **88 millions** sont prédiabétiques, dont une grande majorité l'ignore.

L'objectif initial de ce dataset est d'explorer les facteurs de risque et de tenter de construire des modèles prédictifs. Nous avons personnellement choisi le jeu de données avec les **2 classes binaires**.

### Les 3 fichiers disponibles

- `diabetes_012_health_indicators` : **253 680 lignes**, 3 classes (`0 = sain`, `1 = prédiabète`, `2 = diabète`). Dataset déséquilibré.
- `diabetes_binary_5050split_health_indicators` : **70 692 lignes**, binaire (`0 = sain`, `1 = prédiabétique/diabétique`). Dataset parfaitement équilibré (`50/50`).
- `diabetes_binary_health_indicators` : **253 680 lignes**, binaire. Dataset déséquilibré.

## ⚠️ 2. Limites Critiques du Dataset

Une analyse approfondie du dataset révèle des biais méthodologiques fondamentaux. **Ce jeu de données n'est pas adapté pour prédire qui va développer un diabète à l'avenir.**

### Causalité inverse

Les données sont une photographie de l'état actuel. Un patient diagnostiqué diabétique a souvent déjà changé son mode de vie, comme la perte de poids, une meilleure alimentation ou plus de sport, pour se soigner. Le modèle risque donc d'apprendre que "manger sainement = avoir le diabète", ce qui fausse totalement les prédictions.

### Mélange des types de diabète

Les diabètes de type 1, auto-immun, et de type 2, lié au mode de vie, sont regroupés dans la même variable cible, ce qui dilue les corrélations.

### Les "faux sains"

De nombreuses personnes classées comme "saines" (`0`) peuvent être en phase de prédiabète non diagnostiqué, ce qui ajoute du bruit au modèle.

## 💡 Véritable objectif

Notre but ici est donc d'utiliser ce dataset pour comprendre si, à un instant donné, une personne ayant certains marqueurs associés au diabète a de grandes chances de le développer ou de l'avoir développé.

La question métier est donc d'analyser les différentes corrélations pour mieux comprendre les facteurs associés à un mode de vie sain et réduire au maximum le risque de diabète.

## 📖 3. Dictionnaire des Variables (Features)

Le dataset contient **21 variables explicatives**. Voici leur signification avant regroupement de certaines lors du prétraitement.

### Indicateurs Médicaux

- `HighBP` : Hypertension artérielle diagnostiquée par un professionnel de santé (`0 = Non`, `1 = Oui`).
- `HighChol` : Taux de cholestérol sanguin élevé diagnostiqué par un professionnel (`0 = Non`, `1 = Oui`).
- `CholCheck` : Dépistage du cholestérol effectué au cours des 5 dernières années (`0 = Non`, `1 = Oui`).
- `BMI` : Indice de Masse Corporelle (IMC).
- `Stroke` : Antécédent d'Accident Vasculaire Cérébral (AVC) (`0 = Non`, `1 = Oui`).
- `HeartDiseaseorAttack` : Maladie coronarienne ou infarctus du myocarde signalés (`0 = Non`, `1 = Oui`).
- `GenHlth` : Évaluation subjective de la santé générale, sur une échelle de `1 = excellente` à `5 = mauvaise`.
- `MentHlth` : Nombre de jours de mauvaise santé mentale sur les 30 derniers jours (`0 à 30`).
- `PhysHlth` : Nombre de jours de mauvaise santé physique sur les 30 derniers jours (`0 à 30`).
- `DiffWalk` : Difficulté sérieuse à marcher ou à monter des escaliers (`0 = Non`, `1 = Oui`).

### Mode de Vie et Comportement

- `Smoker` : A fumé au moins 100 cigarettes dans sa vie (`0 = Non`, `1 = Oui`).
- `PhysActivity` : A pratiqué une activité physique, hors travail, dans les 30 derniers jours (`0 = Non`, `1 = Oui`).
- `Fruits` : Consomme des fruits au moins 1 fois par jour (`0 = Non`, `1 = Oui`).
- `Veggies` : Consomme des légumes au moins 1 fois par jour (`0 = Non`, `1 = Oui`).
- `HvyAlcoholConsump` : Grosse consommation d'alcool, supérieure à 14 verres par semaine pour un homme ou 7 pour une femme (`0 = Non`, `1 = Oui`).

### Facteurs Socio-Démographiques et Accès aux Soins

- `AnyHealthcare` : Possède une couverture maladie ou une assurance (`0 = Non`, `1 = Oui`).
- `NoDocbcCost` : A dû renoncer à voir un médecin pour des raisons financières dans les 12 derniers mois (`0 = Non`, `1 = Oui`).
- `Sex` : Sexe du répondant (`0 = Femme`, `1 = Homme`).
- `Age` : Tranche d'âge, sur 14 niveaux.
- `Education` : Niveau d'études atteint, de `1 à 6`.
- `Income` : Niveau de revenu annuel du ménage, de `1 à 8`.
