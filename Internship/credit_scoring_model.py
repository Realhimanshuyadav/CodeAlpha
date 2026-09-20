# ============================================================
# CREDIT SCORING MODEL - COMPLETE MACHINE LEARNING PROJECT
# Dataset: credit_scoring_dataset.csv
#
# Models:
#   1. Logistic Regression
#   2. Decision Tree
#   3. Random Forest
#
# Evaluation:
#   Accuracy, Precision, Recall, F1-Score, ROC-AUC
#   Confusion Matrix, ROC Curve, Feature Importance
# ============================================================

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    RocCurveDisplay
)


# ============================================================
# 1. LOAD DATASET
# ============================================================

FILE_NAME = "credit_scoring_dataset.csv"

try:
    df = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    print(f"ERROR: '{FILE_NAME}' was not found.")
    print("Put the CSV file in the same folder as this Python file.")
    raise SystemExit


print("\n" + "=" * 70)
print("CREDIT SCORING MODEL")
print("=" * 70)

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape before cleaning:")
print(df.shape)


# ============================================================
# 2. BASIC DATA EXPLORATION
# ============================================================

print("\n" + "=" * 70)
print("DATA INFORMATION")
print("=" * 70)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nDataset information:")
df.info()

print("\nStatistical summary:")
print(df.describe(include="all").T)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())


# ============================================================
# 3. REMOVE DUPLICATE ROWS
# ============================================================

duplicate_count = df.duplicated().sum()

if duplicate_count > 0:
    df = df.drop_duplicates().reset_index(drop=True)

print(f"\nRemoved duplicate rows: {duplicate_count}")
print("Dataset shape after duplicate removal:")
print(df.shape)


# ============================================================
# 4. TARGET VARIABLE
# ============================================================

TARGET = "creditworthy"

if TARGET not in df.columns:
    print(f"ERROR: Target column '{TARGET}' was not found.")
    raise SystemExit

print("\nTarget distribution:")
print(df[TARGET].value_counts())

print("\nTarget percentage:")
print((df[TARGET].value_counts(normalize=True) * 100).round(2))


# ============================================================
# 5. TARGET DISTRIBUTION GRAPH
# ============================================================

plt.figure(figsize=(7, 5))
df[TARGET].value_counts().sort_index().plot(kind="bar")
plt.title("Creditworthiness Distribution")
plt.xlabel("Creditworthy (0 = No, 1 = Yes)")
plt.ylabel("Number of Applicants")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# ============================================================
# 6. FEATURE ENGINEERING
# ============================================================

# Create Loan-to-Income Ratio.
# Missing values are intentionally allowed here because the
# preprocessing pipeline will handle them later.

df["loan_to_income"] = (
    df["loan_amount"] / df["annual_income"]
)

# Create Debt-to-Income Ratio.
df["debt_to_income"] = (
    df["total_debt"] / df["annual_income"]
)

# Replace infinite values caused by division by zero.
df.replace([np.inf, -np.inf], np.nan, inplace=True)

print("\nNew engineered features:")
print(" - loan_to_income")
print(" - debt_to_income")


# ============================================================
# 7. SEPARATE FEATURES (X) AND TARGET (y)
# ============================================================

X = df.drop(TARGET, axis=1)
y = df[TARGET].astype(int)


# ============================================================
# 8. IDENTIFY NUMERICAL AND CATEGORICAL FEATURES
# ============================================================

numeric_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

print("\nNumerical features:")
print(numeric_features)

print("\nCategorical features:")
print(categorical_features)


# ============================================================
# 9. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records :", len(X_test))


# ============================================================
# 10. DATA PREPROCESSING
# ============================================================

# Numerical:
#   Missing values -> median
#   Scaling -> StandardScaler
numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)

# Categorical:
#   Missing values -> most frequent
#   Encoding -> One-Hot Encoding
categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)


# ============================================================
# 11. CREATE MODELS
# ============================================================

logistic_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                random_state=42
            )
        )
    ]
)


decision_tree = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            DecisionTreeClassifier(
                max_depth=5,
                random_state=42
            )
        )
    ]
)


random_forest = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=200,
                random_state=42
            )
        )
    ]
)


models = {
    "Logistic Regression": logistic_model,
    "Decision Tree": decision_tree,
    "Random Forest": random_forest
}


# ============================================================
# 12. TRAIN MODELS AND EVALUATE
# ============================================================

results = []
predictions = {}
probabilities = {}

for name, model in models.items():

    print("\n" + "=" * 70)
    print(f"TRAINING: {name}")
    print("=" * 70)

    # Train
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    predictions[name] = y_pred
    probabilities[name] = y_prob

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(
        y_test, y_pred, zero_division=0
    )
    recall = recall_score(
        y_test, y_pred, zero_division=0
    )
    f1 = f1_score(
        y_test, y_pred, zero_division=0
    )
    roc_auc = roc_auc_score(
        y_test, y_prob
    )

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        "ROC-AUC": roc_auc
    })

    print(f"\nAccuracy : {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Precision: {precision:.4f} ({precision * 100:.2f}%)")
    print(f"Recall   : {recall:.4f} ({recall * 100:.2f}%)")
    print(f"F1-Score : {f1:.4f} ({f1 * 100:.2f}%)")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "Not Creditworthy",
                "Creditworthy"
            ],
            zero_division=0
        )
    )


# ============================================================
# 13. MODEL COMPARISON TABLE
# ============================================================

results_df = pd.DataFrame(results)

print("\n" + "=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Precision": "{:.4f}".format,
            "Recall": "{:.4f}".format,
            "F1-Score": "{:.4f}".format,
            "ROC-AUC": "{:.4f}".format
        }
    )
)

# Save results
results_df.to_csv(
    "model_comparison_results.csv",
    index=False
)


# ============================================================
# 14. CONFUSION MATRICES
# ============================================================

for name in models.keys():

    y_pred = predictions[name]

    cm = confusion_matrix(y_test, y_pred)

    print("\n" + "=" * 70)
    print(f"CONFUSION MATRIX - {name}")
    print("=" * 70)

    print(cm)

    fig, ax = plt.subplots(figsize=(6, 5))

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=[
            "Not Creditworthy",
            "Creditworthy"
        ]
    )

    display.plot(
        ax=ax,
        values_format="d"
    )

    ax.set_title(f"{name} - Confusion Matrix")

    plt.tight_layout()
    plt.show()


# ============================================================
# 15. ROC-AUC CURVES
# ============================================================

plt.figure(figsize=(8, 6))

for name in models.keys():

    RocCurveDisplay.from_predictions(
        y_test,
        probabilities[name],
        name=name
    )

plt.title("ROC Curves - Credit Scoring Models")
plt.tight_layout()
plt.show()


# ============================================================
# 16. FEATURE IMPORTANCE - RANDOM FOREST
# ============================================================

rf_model = models["Random Forest"]

# Get fitted preprocessing object
fitted_preprocessor = rf_model.named_steps["preprocessor"]

# Get transformed feature names
feature_names = fitted_preprocessor.get_feature_names_out()

# Get Random Forest model
rf_classifier = rf_model.named_steps["classifier"]

# Feature importance values
importance = pd.Series(
    rf_classifier.feature_importances_,
    index=feature_names
).sort_values(ascending=False)

print("\n" + "=" * 70)
print("TOP 15 RANDOM FOREST FEATURE IMPORTANCES")
print("=" * 70)

print(importance.head(15))


# Plot top 10 features
top_features = importance.head(10).sort_values()

plt.figure(figsize=(9, 6))
top_features.plot(kind="barh")

plt.title("Top 10 Feature Importances - Random Forest")
plt.xlabel("Importance")
plt.ylabel("Feature")

plt.tight_layout()
plt.show()


# ============================================================
# 17. EXAMPLE PREDICTION FOR A NEW APPLICANT
# ============================================================

print("\n" + "=" * 70)
print("NEW APPLICANT PREDICTION")
print("=" * 70)

# Use the original input columns.
# Change these values to test another applicant.
new_applicant = pd.DataFrame({
    "age": [35],
    "annual_income": [65000],
    "employment_years": [8],
    "loan_amount": [12000],
    "total_debt": [15000],
    "credit_history_years": [7],
    "previous_defaults": [0],
    "employment_type": ["Salaried"],
    "loan_purpose": ["Personal"],
    "payment_history": ["Good"]
})

# Feature engineering must match the training data.
new_applicant["loan_to_income"] = (
    new_applicant["loan_amount"]
    / new_applicant["annual_income"]
)

new_applicant["debt_to_income"] = (
    new_applicant["total_debt"]
    / new_applicant["annual_income"]
)

new_applicant.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)


# Use Random Forest for demonstration.
rf_prediction = random_forest.predict(new_applicant)[0]
rf_probability = random_forest.predict_proba(
    new_applicant
)[0, 1]

print("\nApplicant details:")
print(new_applicant.to_string(index=False))

print("\nPredicted class:")

if rf_prediction == 1:
    print("CREDITWORTHY")
else:
    print("NOT CREDITWORTHY")

print(
    f"Probability of being creditworthy: "
    f"{rf_probability:.2%}"
)


# ============================================================
# 18. SAVE THE FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("PROJECT COMPLETED")
print("=" * 70)

print("""
Files generated:
1. model_comparison_results.csv

Graphs displayed:
1. Creditworthiness Distribution
2. Confusion Matrix for Logistic Regression
3. Confusion Matrix for Decision Tree
4. Confusion Matrix for Random Forest
5. ROC-AUC Curves
6. Random Forest Feature Importance

Models trained:
1. Logistic Regression
2. Decision Tree
3. Random Forest

Metrics calculated:
1. Accuracy
2. Precision
3. Recall
4. F1-Score
5. ROC-AUC
6. Confusion Matrix
""")

print("End of Credit Scoring Model.")
