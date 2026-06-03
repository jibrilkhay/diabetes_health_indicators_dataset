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
chemin = "/Users/florentaccaries/diabetes_binary_health_indicators_BRFSS2015.csv"
Original_data = pd.read_csv(chemin)
matplotlib.use('MacOSX') 

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
# TABLE POUR RÉGRESSION LOGISTIQUE (SANS DOUBLONS)
# ============================================================
con.execute("DROP TABLE IF EXISTS diabetes_clean; CREATE TABLE diabetes_clean AS SELECT DISTINCT * FROM diabetes_eda;")

con.execute("""
DROP TABLE IF EXISTS diabetes_features_logistic;
CREATE TABLE diabetes_features_logistic AS
SELECT
    Diabetes_binary,
    Smoker, HvyAlcoholConsump, Sex, NoDocbcCost, AnyHealthcare, CholCheck,
    (PhysActivity + Fruits + Veggies) AS Healthy_Lifestyle,
    CASE WHEN BMI < 25 THEN 0 WHEN BMI >= 25 AND BMI < 30 THEN 1 WHEN BMI >= 30 THEN 2 ELSE NULL END AS BMI_Risk,
    (CASE WHEN BMI < 25 THEN 0 WHEN BMI >= 25 AND BMI < 30 THEN 1 WHEN BMI >= 30 THEN 2 ELSE 0 END + HighBP + HighChol) AS Metabolic_Risk,
    (HighBP + HighChol + HeartDiseaseorAttack + Stroke) AS Cardio_Risk,
    (Education + Income) AS Socio_Economic_Level,
    (GenHlth + 2 * DiffWalk + PhysHlth / 30.0 + MentHlth / 30.0) AS Health_Risk,
    (Age * BMI) AS Age_BMI_Interaction
FROM diabetes_clean
WHERE Diabetes_binary IN (0, 1);
""")

# ============================================================
# TABLE ÉQUILIBRÉE 50/50
# ============================================================
nb_diabetiques = con.execute("SELECT COUNT(*) FROM diabetes_features_logistic WHERE Diabetes_binary = 1;").fetchone()[0]

con.execute(f"""
DROP TABLE IF EXISTS diabetes_logistic_balanced;
CREATE TABLE diabetes_logistic_balanced AS
SELECT * FROM diabetes_features_logistic WHERE Diabetes_binary = 1
UNION ALL
SELECT * FROM (
    SELECT * FROM diabetes_features_logistic WHERE Diabetes_binary = 0 ORDER BY RANDOM() LIMIT {nb_diabetiques}
);
""")

balanced_data = con.execute("SELECT * FROM diabetes_logistic_balanced").df()
full_data = con.execute("SELECT * FROM diabetes_features_logistic").df()

# ============================================================
# 5 & 6. MACHINE LEARNING ET AFFICHAGE RÉSULTATS
# ============================================================
X = balanced_data.drop("Diabetes_binary", axis=1)
y = balanced_data["Diabetes_binary"]

# Entraînement sur données équilibrées
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)

model = Pipeline([
    ("scaler", StandardScaler()),
    ("logreg", LogisticRegression(max_iter=1000))
])
model.fit(X_train, y_train)

# --- PRÉDICTIONS ---
# 1. Sur le jeu de test équilibré (50/50)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# 2. Sur le dataset complet (Réalité 85/15)
X_full = full_data.drop("Diabetes_binary", axis=1)
y_full = full_data["Diabetes_binary"]
y_full_pred = model.predict(X_full)
y_full_proba = model.predict_proba(X_full)[:, 1]

# --- AFFICHAGES CONSOLE ---
print("\n" + "="*60)
print(" 1. RÉSULTATS SUR DATASET ÉQUILIBRÉ (TEST SET 50/50)")
print("="*60)
print(classification_report(y_test, y_pred, target_names=["Sain (0)", "Diabétique (1)"]))
print(f"ROC AUC : {roc_auc_score(y_test, y_proba):.3f}\n")

print("="*60)
print(" 2. RÉSULTATS SUR DATASET COMPLET NON ÉQUILIBRÉ (RÉALITÉ)")
print("="*60)
print(classification_report(y_full, y_full_pred, target_names=["Sain (0)", "Diabétique (1)"]))
print(f"ROC AUC : {roc_auc_score(y_full, y_full_proba):.3f}\n")

# --- AFFICHAGES GRAPHIQUES (MATRICES DE CONFUSION) ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Matrice 1 (Équilibrée)
cm_bal = confusion_matrix(y_test, y_pred)
sns.heatmap(cm_bal, annot=True, fmt='d', cmap='Blues', linewidths=1, linecolor='black', ax=axes[0],
            xticklabels=['Prédit: Sain', 'Prédit: Diab.'], yticklabels=['Vrai: Sain', 'Vrai: Diab.'])
axes[0].set_title('Matrice de Confusion\n(Test sur Échantillon 50/50)', fontsize=14, pad=15)

# Matrice 2 (Complète)
cm_full = confusion_matrix(y_full, y_full_pred)
sns.heatmap(cm_full, annot=True, fmt='d', cmap='Oranges', linewidths=1, linecolor='black', ax=axes[1],
            xticklabels=['Prédit: Sain', 'Prédit: Diab.'], yticklabels=['Vrai: Sain', 'Vrai: Diab.'])
axes[1].set_title('Matrice de Confusion\n(Test sur Dataset Complet - Réalité)', fontsize=14, pad=15)

plt.tight_layout()
plt.show()
