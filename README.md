diabetes_health_indicators_dataset
Présentation

Ce projet utilise le dataset Diabetes Health Indicators, issu de l’enquête américaine BRFSS 2015 menée par le CDC.
L’objectif est d’analyser des indicateurs de santé, de mode de vie et de profil socio-économique afin de prédire la présence d’un diabète à partir de données déclaratives.

Nous avons utilisé la version binaire du dataset :

diabetes_binary_health_indicators.csv

La variable cible est :

Diabetes_binary = 0 : pas de diabète
Diabetes_binary = 1 : diabète
Objectif du projet

Le but n’est pas de remplacer un diagnostic médical, mais de construire un outil de pré-diagnostic capable d’identifier des profils potentiellement à risque à partir d’un questionnaire simple.

Le projet cherche donc à répondre à la question suivante :

Quels indicateurs de santé et habitudes de vie sont associés à un risque plus élevé de diabète ?

Dataset

Le dataset contient 253 680 lignes et 21 variables explicatives.

Les variables peuvent être regroupées en trois catégories :

Indicateurs médicaux
HighBP : hypertension artérielle
HighChol : cholestérol élevé
CholCheck : contrôle du cholestérol
BMI : indice de masse corporelle
Stroke : antécédent d’AVC
HeartDiseaseorAttack : maladie cardiaque ou infarctus
GenHlth : santé générale déclarée
MentHlth : jours de mauvaise santé mentale
PhysHlth : jours de mauvaise santé physique
DiffWalk : difficulté à marcher
Mode de vie
Smoker : tabagisme
PhysActivity : activité physique
Fruits : consommation de fruits
Veggies : consommation de légumes
HvyAlcoholConsump : forte consommation d’alcool
Facteurs socio-démographiques
AnyHealthcare : accès à une couverture santé
NoDocbcCost : renoncement aux soins pour raisons financières
Sex : sexe
Age : tranche d’âge
Education : niveau d’étude
Income : niveau de revenu
Limites du dataset

Ce dataset présente plusieurs limites importantes :

Les données sont déclaratives, donc potentiellement imprécises.
Le dataset représente une situation à un instant donné : il ne permet pas de prouver une causalité.
Les types de diabète ne sont pas distingués.
Certains patients classés comme non diabétiques peuvent être non diagnostiqués.
Certaines variables sont binaires alors qu’une mesure continue serait plus informative.

Ainsi, le projet doit être interprété comme une analyse de profils associés au diabète, et non comme une preuve médicale causale.

Feature engineering

Afin d’améliorer l’interprétation et la modélisation, nous avons créé plusieurs variables synthétiques :

Feature	Formule	Interprétation
Healthy_Lifestyle	PhysActivity + Fruits + Veggies	Score simple de mode de vie sain
BMI_Risk	Catégorisation du BMI	Normal / surpoids / obésité
Metabolic_Risk	BMI_Risk + HighBP + HighChol	Risque métabolique
Cardio_Risk	HighBP + HighChol + HeartDiseaseorAttack + Stroke	Risque cardiovasculaire
Socio_Economic_Level	Education + Income	Niveau socio-économique
Health_Risk	GenHlth + 2*DiffWalk + PhysHlth/30 + MentHlth/30	État de santé global
Age_BMI_Interaction	Age * BMI	Interaction âge / BMI

Nous avons également étudié une combinaison multiplicative :

BMI_0_1 = (BMI - min(BMI)) / (max(BMI) - min(BMI))

BMI_BP_Chol_mult = BMI_0_1 × (1 + HighBP) × (1 + HighChol)

Cette variable permet de modéliser l’effet combiné du BMI, de l’hypertension et du cholestérol.
Elle ne représente pas une simple addition : elle introduit une interaction entre ces facteurs.

Modélisation

Le problème est traité comme une classification binaire.

Le modèle principal utilisé est une régression logistique, choisie pour son interprétabilité et sa pertinence sur une variable cible binaire.

Les métriques utilisées sont :

Accuracy
Precision
Recall
F1-score
ROC AUC

Le recall est particulièrement important dans ce projet, car il mesure la capacité du modèle à détecter les vrais patients diabétiques et donc à limiter les faux négatifs.

Résultat attendu

Le modèle permet d’identifier des profils à risque à partir de variables simples.
Il peut servir de premier filtre préventif, mais ne remplace pas un diagnostic médical.

Pistes d’amélioration

Plusieurs améliorations sont possibles :

Ajouter des données médicales plus précises : glycémie, HbA1c, antécédents familiaux.
Remplacer certaines variables binaires par des variables continues.
Tester des modèles non linéaires comme Random Forest ou XGBoost.
Ajouter des méthodes d’explicabilité comme SHAP.
Transformer le modèle en outil de prévention personnalisée.
Conclusion

Ce projet montre comment des données déclaratives peuvent être utilisées pour analyser les facteurs associés au diabète et construire un modèle de pré-diagnostic.

L’objectif principal est de mieux comprendre les profils à risque et d’orienter une démarche de prévention, tout en gardant à l’esprit les limites du dataset.
