import pandas as pd
import duckdb
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# ==============================
# 1. Charger le CSV
# ==============================
chemin = "/Users/khjib/downloads/archive/diabetes_binary_health_indicators_BRFSS2015.csv"
Original_data = pd.read_csv(chemin)

con = duckdb.connect()
con.register("Original_data", Original_data)

# ==============================
# 2. Créer la table brute
# ==============================
con.execute("DROP TABLE IF EXISTS diabetes_raw; CREATE TABLE diabetes_raw AS SELECT * FROM Original_data;")

# ==============================
# 3. Créer la table EDA (Simplifiée ici pour le gain de place, j'ai gardé ton code exact en mémoire)
# ==============================
con.execute("""
DROP TABLE IF EXISTS diabetes_eda;
CREATE TABLE diabetes_eda AS SELECT * FROM diabetes_raw;
""")
# (Note : J'ai gardé `SELECT *` ici pour raccourcir l'affichage, mais dans ton vrai fichier, 
# garde bien tout ton gros bloc SQL avec les CASE WHEN de la partie 3, ça marche très bien !)

# J'ai désactivé les prints de l'EDA (Parties 4 à 11) pour ne pas polluer ton terminal
# print("--- 4. Aperçu de la table ---")
# ...

# ============================================================
# FEATURE ENGINEERING VISUEL 
# ============================================================
con.execute("""
DROP TABLE IF EXISTS diabetes_combined_features;
CREATE TABLE diabetes_combined_features AS
SELECT
    *,
    (PhysActivity + Fruits + Veggies) AS Healthy_Lifestyle,
    CASE
        WHEN BMI < 25 THEN 0
        WHEN BMI >= 25 AND BMI < 30 THEN 1
        WHEN BMI >= 30 THEN 2
        ELSE NULL
    END AS BMI_Risk,
    (
        CASE
            WHEN BMI < 25 THEN 0
            WHEN BMI >= 25 AND BMI < 30 THEN 1
            WHEN BMI >= 30 THEN 2
            ELSE 0
        END
        + HighBP + HighChol
    ) AS Metabolic_Risk,
    (HighBP + HighChol + HeartDiseaseorAttack + Stroke) AS Cardio_Risk,
    (Education + Income) AS Socio_Economic_Level,
    (GenHlth + 2 * DiffWalk + PhysHlth / 30.0 + MentHlth / 30.0) AS Health_Risk,
    (Age * BMI) AS Age_BMI_Interaction
FROM diabetes_eda;
""")

# ============================================================
# PREUVE DE LA COMBINAISON : Metabolic_Risk
# Metabolic_Risk = BMI_Risk + HighBP + HighChol
# ============================================================


# ============================================================
# 1. Vérifier les tendances individuelles
# ============================================================

def plot_diabetes_rate_sql(column, title, xlabel=None):
    data = con.execute(f"""
    SELECT
        {column},
        COUNT(*) AS nb_patients,
        ROUND(AVG(Diabetes_binary) * 100, 2) AS diabetes_rate
    FROM diabetes_combined_features
    GROUP BY {column}
    ORDER BY {column};
    """).df()

    print("\n" + "="*70)
    print(title)
    print("="*70)
    print(data.to_string(index=False))

    plt.figure(figsize=(7, 4))
    sns.lineplot(data=data, x=column, y="diabetes_rate", marker="o")
    plt.title(title)
    plt.xlabel(xlabel if xlabel else column)
    plt.ylabel("Taux de diabète (%)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    return data


# BMI_Risk seul
bmi_risk_check = plot_diabetes_rate_sql(
    "BMI_Risk",
    "Taux de diabète selon BMI_Risk",
    "BMI_Risk : 0 = normal, 1 = surpoids, 2 = obèse"
)

# HighBP seul
highbp_check = plot_diabetes_rate_sql(
    "HighBP",
    "Taux de diabète selon HighBP",
    "HighBP : 0 = Non, 1 = Oui"
)

# HighChol seul
highchol_check = plot_diabetes_rate_sql(
    "HighChol",
    "Taux de diabète selon HighChol",
    "HighChol : 0 = Non, 1 = Oui"
)


# ============================================================
# 2. Vérifier automatiquement que chaque variable va dans le bon sens
# ============================================================

def check_monotonic_increasing(df, rate_col="diabetes_rate"):
    rates = df[rate_col].values
    return all(rates[i] <= rates[i+1] for i in range(len(rates)-1))


print("\n" + "="*70)
print("VÉRIFICATION DES TENDANCES INDIVIDUELLES")
print("="*70)

print("BMI_Risk tendance croissante :", check_monotonic_increasing(bmi_risk_check))
print("HighBP tendance croissante :", check_monotonic_increasing(highbp_check))
print("HighChol tendance croissante :", check_monotonic_increasing(highchol_check))


# ============================================================
# 3. Vérifier la tendance de la feature combinée Metabolic_Risk
# ============================================================

metabolic_check = con.execute("""
SELECT
    Metabolic_Risk,
    COUNT(*) AS nb_patients,
    ROUND(AVG(Diabetes_binary) * 100, 2) AS diabetes_rate
FROM diabetes_combined_features
GROUP BY Metabolic_Risk
ORDER BY Metabolic_Risk;
""").df()

print("\n" + "="*70)
print("TENDANCE DE LA FEATURE COMBINÉE : Metabolic_Risk")
print("="*70)
print(metabolic_check.to_string(index=False))

plt.figure(figsize=(7, 4))
sns.lineplot(
    data=metabolic_check,
    x="Metabolic_Risk",
    y="diabetes_rate",
    marker="o"
)
plt.title("Taux de diabète selon Metabolic_Risk = BMI_Risk + HighBP + HighChol")
plt.xlabel("Metabolic_Risk : 0 à 4")
plt.ylabel("Taux de diabète (%)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

metabolic_is_monotonic = check_monotonic_increasing(metabolic_check)

print("\nTendance monotone croissante de Metabolic_Risk :", metabolic_is_monotonic)


# ============================================================
# 4. Montrer l'effet cumulé avec une heatmap
# BMI_Risk + HighBP
# ============================================================

bmi_bp_heatmap = con.execute("""
SELECT
    BMI_Risk,
    HighBP,
    COUNT(*) AS nb_patients,
    ROUND(AVG(Diabetes_binary) * 100, 2) AS diabetes_rate
FROM diabetes_combined_features
GROUP BY BMI_Risk, HighBP
ORDER BY BMI_Risk, HighBP;
""").df()

print("\n" + "="*70)
print("EFFET CROISÉ : BMI_Risk + HighBP")
print("="*70)
print(bmi_bp_heatmap.to_string(index=False))

pivot_bmi_bp = bmi_bp_heatmap.pivot(
    index="BMI_Risk",
    columns="HighBP",
    values="diabetes_rate"
)

plt.figure(figsize=(6, 5))
sns.heatmap(pivot_bmi_bp, annot=True, fmt=".2f", cmap="YlOrRd")
plt.title("Taux de diabète (%) selon BMI_Risk et HighBP")
plt.xlabel("HighBP")
plt.ylabel("BMI_Risk")
plt.tight_layout()
plt.show()


# ============================================================
# 5. Montrer l'effet cumulé avec une heatmap
# BMI_Risk + HighChol
# ============================================================

bmi_chol_heatmap = con.execute("""
SELECT
    BMI_Risk,
    HighChol,
    COUNT(*) AS nb_patients,
    ROUND(AVG(Diabetes_binary) * 100, 2) AS diabetes_rate
FROM diabetes_combined_features
GROUP BY BMI_Risk, HighChol
ORDER BY BMI_Risk, HighChol;
""").df()

print("\n" + "="*70)
print("EFFET CROISÉ : BMI_Risk + HighChol")
print("="*70)
print(bmi_chol_heatmap.to_string(index=False))

pivot_bmi_chol = bmi_chol_heatmap.pivot(
    index="BMI_Risk",
    columns="HighChol",
    values="diabetes_rate"
)

plt.figure(figsize=(6, 5))
sns.heatmap(pivot_bmi_chol, annot=True, fmt=".2f", cmap="YlOrRd")
plt.title("Taux de diabète (%) selon BMI_Risk et HighChol")
plt.xlabel("HighChol")
plt.ylabel("BMI_Risk")
plt.tight_layout()
plt.show()


# ============================================================
# 6. Montrer les 3 variables ensemble
# BMI_Risk + HighBP + HighChol
# ============================================================

three_vars_check = con.execute("""
SELECT
    BMI_Risk,
    HighBP,
    HighChol,
    COUNT(*) AS nb_patients,
    ROUND(AVG(Diabetes_binary) * 100, 2) AS diabetes_rate
FROM diabetes_combined_features
GROUP BY BMI_Risk, HighBP, HighChol
ORDER BY BMI_Risk, HighBP, HighChol;
""").df()

print("\n" + "="*70)
print("EFFET CROISÉ : BMI_Risk + HighBP + HighChol")
print("="*70)
print(three_vars_check.to_string(index=False))

g = sns.catplot(
    data=three_vars_check,
    x="BMI_Risk",
    y="diabetes_rate",
    hue="HighBP",
    col="HighChol",
    kind="point",
    errorbar=None,
    height=5,
    aspect=1
)

g.set_axis_labels("BMI_Risk", "Taux de diabète (%)")
g.set_titles("HighChol = {col_name}")
g.fig.suptitle("Taux de diabète selon BMI_Risk, HighBP et HighChol", y=1.05)
plt.show()


# ============================================================
# 7. Comparaison modèle :
# variables séparées VS feature combinée
# ============================================================

comparison_data = con.execute("""
SELECT
    Diabetes_binary,
    BMI_Risk,
    HighBP,
    HighChol,
    Metabolic_Risk
FROM diabetes_combined_features
WHERE Diabetes_binary IN (0, 1)
  AND BMI_Risk IS NOT NULL;
""").df()

y = comparison_data["Diabetes_binary"]

X_separated = comparison_data[[
    "BMI_Risk",
    "HighBP",
    "HighChol"
]]

X_combined = comparison_data[[
    "Metabolic_Risk"
]]

X_sep_train, X_sep_test, y_train, y_test = train_test_split(
    X_separated,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_comb_train, X_comb_test, _, _ = train_test_split(
    X_combined,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

model_sep = Pipeline([
    ("scaler", StandardScaler()),
    ("logreg", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

model_comb = Pipeline([
    ("scaler", StandardScaler()),
    ("logreg", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

model_sep.fit(X_sep_train, y_train)
model_comb.fit(X_comb_train, y_train)

proba_sep = model_sep.predict_proba(X_sep_test)[:, 1]
proba_comb = model_comb.predict_proba(X_comb_test)[:, 1]

pred_sep = model_sep.predict(X_sep_test)
pred_comb = model_comb.predict(X_comb_test)

auc_sep = roc_auc_score(y_test, proba_sep)
auc_comb = roc_auc_score(y_test, proba_comb)

print("\n" + "="*70)
print("COMPARAISON MODÈLE : VARIABLES SÉPARÉES VS FEATURE COMBINÉE")
print("="*70)

print("ROC AUC avec variables séparées :")
print(round(auc_sep, 4))

print("\nROC AUC avec Metabolic_Risk uniquement :")
print(round(auc_comb, 4))

print("\nDifférence AUC combinée - séparées :")
print(round(auc_comb - auc_sep, 4))

print("\nRapport modèle variables séparées :")
print(classification_report(y_test, pred_sep, target_names=["Non diabétique", "Diabétique"]))

print("\nRapport modèle Metabolic_Risk seule :")
print(classification_report(y_test, pred_comb, target_names=["Non diabétique", "Diabétique"]))


# ============================================================
# 8. Graphique de comparaison ROC AUC
# ============================================================

auc_comparison = pd.DataFrame({
    "Model": [
        "Variables séparées\nBMI_Risk + HighBP + HighChol",
        "Feature combinée\nMetabolic_Risk"
    ],
    "ROC_AUC": [
        auc_sep,
        auc_comb
    ]
})

plt.figure(figsize=(8, 5))
sns.barplot(data=auc_comparison, x="Model", y="ROC_AUC")
plt.title("Comparaison ROC AUC : variables séparées vs feature combinée")
plt.ylabel("ROC AUC")
plt.xlabel("")
plt.ylim(0.5, 1)
plt.grid(True, axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

print("\nRésumé comparaison :")
print(auc_comparison.to_string(index=False))


# ============================================================
# 9. Conclusion automatique pour le notebook
# ============================================================

print("\n" + "="*70)
print("CONCLUSION POUR LA COMBINAISON Metabolic_Risk")
print("="*70)

if metabolic_is_monotonic:
    print("- Metabolic_Risk présente une tendance monotone croissante.")
    print("- Plus Metabolic_Risk augmente, plus le taux de diabète augmente.")
else:
    print("- Attention : Metabolic_Risk ne présente pas une tendance parfaitement monotone.")

if auc_comb >= auc_sep - 0.02:
    print("- Le modèle avec Metabolic_Risk garde une performance proche des variables séparées.")
    print("- Donc Metabolic_Risk résume correctement l'information des trois variables.")
else:
    print("- Le modèle avec Metabolic_Risk perd trop d'information.")
    print("- Dans ce cas, il vaut mieux garder les variables séparées.")

print("\nPhrase à mettre dans le rapport :")
print("""
Les variables BMI_Risk, HighBP et HighChol présentent chacune une tendance croissante avec le taux de diabète.
En les combinant dans Metabolic_Risk, on obtient un score de risque dont le taux de diabète augmente progressivement.
Cette relation monotone croissante montre que la feature combinée représente correctement l'accumulation de facteurs de risque métabolique.
La comparaison entre un modèle utilisant les variables séparées et un modèle utilisant Metabolic_Risk permet ensuite de vérifier que la combinaison conserve une information prédictive pertinente.
""")
