***************************** AJOUT DES PLOTS***********************************************


# ==============================
# PLOTS EDA - DIABETES PROJECT
# ==============================

import matplotlib.pyplot as plt
import seaborn as sns

# Récupérer la table diabetes_eda depuis DuckDB
eda_data = con.execute("""
SELECT *
FROM diabetes_eda
""").df()


# ==============================
# 1. Distribution diabète / non diabète
# ==============================

plt.figure(figsize=(6, 4))
sns.countplot(data=eda_data, x="Diabetes_status")
plt.title("Distribution du statut diabétique")
plt.xlabel("Statut diabétique")
plt.ylabel("Nombre de patients")
plt.show()


# ==============================
# 2. Pourcentage diabète / non diabète
# ==============================

diabetes_counts = eda_data["Diabetes_status"].value_counts(normalize=True) * 100

plt.figure(figsize=(6, 4))
sns.barplot(x=diabetes_counts.index, y=diabetes_counts.values)
plt.title("Pourcentage de patients diabétiques / non diabétiques")
plt.xlabel("Statut diabétique")
plt.ylabel("Pourcentage (%)")
plt.show()


# ==============================
# 3. Boxplots des variables numériques
# ==============================

plt.figure(figsize=(15, 15))

for i, col in enumerate(['BMI', 'GenHlth', 'MentHlth', 'PhysHlth', 'Age', 'Education', 'Income']):
    plt.subplot(4, 2, i + 1)
    sns.boxplot(x=eda_data[col])
    plt.title(f"Boxplot de {col}")

plt.tight_layout()
plt.show()


# ==============================
# 4. Boxplots selon le statut diabétique
# ==============================

plt.figure(figsize=(15, 15))

for i, col in enumerate(['BMI', 'GenHlth', 'MentHlth', 'PhysHlth', 'Age', 'Education', 'Income']):
    plt.subplot(4, 2, i + 1)
    sns.boxplot(data=eda_data, x="Diabetes_status", y=col)
    plt.title(f"{col} selon le statut diabétique")

plt.tight_layout()
plt.show()


# ==============================
# 5. Distribution du BMI selon diabète
# ==============================

plt.figure(figsize=(8, 5))
sns.histplot(data=eda_data, x="BMI", hue="Diabetes_status", kde=True, bins=30)
plt.title("Distribution du BMI selon le statut diabétique")
plt.xlabel("BMI")
plt.ylabel("Nombre de patients")
plt.show()


# ==============================
# 6. Diabète selon catégorie de BMI
# ==============================

plt.figure(figsize=(8, 5))
sns.countplot(data=eda_data, x="BMI_category", hue="Diabetes_status")
plt.title("Statut diabétique selon la catégorie de BMI")
plt.xlabel("Catégorie BMI")
plt.ylabel("Nombre de patients")
plt.xticks(rotation=45)
plt.show()


# ==============================
# 7. Diabète selon l'âge
# ==============================

plt.figure(figsize=(12, 5))
sns.countplot(data=eda_data, x="Age_label", hue="Diabetes_status")
plt.title("Statut diabétique selon le groupe d'âge")
plt.xlabel("Groupe d'âge")
plt.ylabel("Nombre de patients")
plt.xticks(rotation=45)
plt.show()


# ==============================
# 8. Taux de diabète par âge
# ==============================

age_diabetes_rate = con.execute("""
SELECT 
    Age,
    Age_label,
    AVG(Diabetes_binary) * 100 AS diabetes_rate
FROM diabetes_eda
GROUP BY Age, Age_label
ORDER BY Age
""").df()

plt.figure(figsize=(12, 5))
sns.barplot(data=age_diabetes_rate, x="Age_label", y="diabetes_rate")
plt.title("Taux de diabète par groupe d'âge")
plt.xlabel("Groupe d'âge")
plt.ylabel("Taux de diabète (%)")
plt.xticks(rotation=45)
plt.show()


# ==============================
# 9. Diabète selon hypertension
# ==============================

plt.figure(figsize=(7, 5))
sns.countplot(data=eda_data, x="HighBP_label", hue="Diabetes_status")
plt.title("Statut diabétique selon l'hypertension")
plt.xlabel("Hypertension")
plt.ylabel("Nombre de patients")
plt.show()


# ==============================
# 10. Taux de diabète selon hypertension
# ==============================

highbp_rate = con.execute("""
SELECT 
    HighBP_label,
    AVG(Diabetes_binary) * 100 AS diabetes_rate
FROM diabetes_eda
GROUP BY HighBP_label
""").df()

plt.figure(figsize=(7, 5))
sns.barplot(data=highbp_rate, x="HighBP_label", y="diabetes_rate")
plt.title("Taux de diabète selon l'hypertension")
plt.xlabel("Hypertension")
plt.ylabel("Taux de diabète (%)")
plt.show()


# ==============================
# 11. Diabète selon cholestérol
# ==============================

plt.figure(figsize=(7, 5))
sns.countplot(data=eda_data, x="HighChol_label", hue="Diabetes_status")
plt.title("Statut diabétique selon le cholestérol")
plt.xlabel("Cholestérol")
plt.ylabel("Nombre de patients")
plt.show()


# ==============================
# 12. Taux de diabète selon cholestérol
# ==============================

chol_rate = con.execute("""
SELECT 
    HighChol_label,
    AVG(Diabetes_binary) * 100 AS diabetes_rate
FROM diabetes_eda
GROUP BY HighChol_label
""").df()

plt.figure(figsize=(7, 5))
sns.barplot(data=chol_rate, x="HighChol_label", y="diabetes_rate")
plt.title("Taux de diabète selon le cholestérol")
plt.xlabel("Cholestérol")
plt.ylabel("Taux de diabète (%)")
plt.show()


# ==============================
# 13. Santé générale selon diabète
# ==============================

plt.figure(figsize=(8, 5))
sns.countplot(data=eda_data, x="GenHlth_label", hue="Diabetes_status")
plt.title("Santé générale selon le statut diabétique")
plt.xlabel("Santé générale")
plt.ylabel("Nombre de patients")
plt.xticks(rotation=45)
plt.show()


# ==============================
# 14. Taux de diabète selon santé générale
# ==============================

genhlth_rate = con.execute("""
SELECT 
    GenHlth,
    GenHlth_label,
    AVG(Diabetes_binary) * 100 AS diabetes_rate
FROM diabetes_eda
GROUP BY GenHlth, GenHlth_label
ORDER BY GenHlth
""").df()

plt.figure(figsize=(8, 5))
sns.barplot(data=genhlth_rate, x="GenHlth_label", y="diabetes_rate")
plt.title("Taux de diabète selon la santé générale")
plt.xlabel("Santé générale")
plt.ylabel("Taux de diabète (%)")
plt.xticks(rotation=45)
plt.show()


# ==============================
# 15. Difficulté à marcher selon diabète
# ==============================

plt.figure(figsize=(7, 5))
sns.countplot(data=eda_data, x="DiffWalk", hue="Diabetes_status")
plt.title("Difficulté à marcher selon le statut diabétique")
plt.xlabel("Difficulté à marcher : 0 = Non, 1 = Oui")
plt.ylabel("Nombre de patients")
plt.show()


# ==============================
# 16. Activité physique selon diabète
# ==============================

plt.figure(figsize=(7, 5))
sns.countplot(data=eda_data, x="PhysActivity", hue="Diabetes_status")
plt.title("Activité physique selon le statut diabétique")
plt.xlabel("Activité physique : 0 = Non, 1 = Oui")
plt.ylabel("Nombre de patients")
plt.show()


# ==============================
# 17. Revenu selon diabète
# ==============================

plt.figure(figsize=(10, 5))
sns.countplot(data=eda_data, x="Income_label", hue="Diabetes_status")
plt.title("Statut diabétique selon le revenu")
plt.xlabel("Revenu")
plt.ylabel("Nombre de patients")
plt.xticks(rotation=45)
plt.show()


# ==============================
# 18. Taux de diabète selon revenu
# ==============================

income_rate = con.execute("""
SELECT 
    Income,
    Income_label,
    AVG(Diabetes_binary) * 100 AS diabetes_rate
FROM diabetes_eda
GROUP BY Income, Income_label
ORDER BY Income
""").df()

plt.figure(figsize=(10, 5))
sns.barplot(data=income_rate, x="Income_label", y="diabetes_rate")
plt.title("Taux de diabète selon le revenu")
plt.xlabel("Revenu")
plt.ylabel("Taux de diabète (%)")
plt.xticks(rotation=45)
plt.show()


# ==============================
# 19. Éducation selon diabète
# ==============================

plt.figure(figsize=(8, 5))
sns.countplot(data=eda_data, x="Education", hue="Diabetes_status")
plt.title("Statut diabétique selon le niveau d'éducation")
plt.xlabel("Niveau d'éducation")
plt.ylabel("Nombre de patients")
plt.show()


# ==============================
# 20. Taux de diabète selon éducation
# ==============================

education_rate = con.execute("""
SELECT 
    Education,
    AVG(Diabetes_binary) * 100 AS diabetes_rate
FROM diabetes_eda
GROUP BY Education
ORDER BY Education
""").df()

plt.figure(figsize=(8, 5))
sns.barplot(data=education_rate, x="Education", y="diabetes_rate")
plt.title("Taux de diabète selon le niveau d'éducation")
plt.xlabel("Niveau d'éducation")
plt.ylabel("Taux de diabète (%)")
plt.show()


# ==============================
# 21. Heatmap de corrélation
# ==============================

numeric_cols = [
    "Diabetes_binary", "HighBP", "HighChol", "CholCheck", "BMI",
    "Smoker", "Stroke", "HeartDiseaseorAttack", "PhysActivity",
    "Fruits", "Veggies", "HvyAlcoholConsump", "AnyHealthcare",
    "NoDocbcCost", "GenHlth", "MentHlth", "PhysHlth",
    "DiffWalk", "Sex", "Age", "Education", "Income"
]

plt.figure(figsize=(15, 10))
sns.heatmap(eda_data[numeric_cols].corr(), annot=True, cmap="YlOrRd", fmt=".2f")
plt.title("Matrice de corrélation")
plt.show()


# ==============================
# 22. Corrélation avec la variable cible
# ==============================

corr_target = eda_data[numeric_cols].corr()["Diabetes_binary"].sort_values(ascending=False)

plt.figure(figsize=(8, 8))
sns.barplot(x=corr_target.values, y=corr_target.index)
plt.title("Corrélation des variables avec Diabetes_binary")
plt.xlabel("Corrélation")
plt.ylabel("Variables")
plt.show()
