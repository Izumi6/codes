"""
================================================================================
  Program 5: K-Nearest Neighbors on Diabetes Dataset
  Course: Machine Learning

  Description:
    Implement KNN algorithm on diabetes.csv dataset.
    Compute: Confusion Matrix, Accuracy, Error Rate, Precision, and Recall.

  Dataset: https://www.kaggle.com/datasets/abdallamahgoub/diabetes
           Download 'diabetes.csv' and place it in the same directory.

  Requirements: pip install pandas numpy scikit-learn matplotlib seaborn
================================================================================
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (confusion_matrix, accuracy_score,
                             precision_score, recall_score)
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()


def main():
    print("=" * 65)
    print("   KNN CLASSIFICATION ON DIABETES DATASET")
    print("=" * 65)

    # ── Load Dataset ────────────────────────────────────────────────────
    print("\n  Loading dataset...")
    csv_path = os.path.join(SCRIPT_DIR, "diabetes.csv")
    df = pd.read_csv(csv_path)
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"\n  First 5 rows:")
    print(df.head())
    print(f"\n  Statistical Summary:")
    print(df.describe())

    # ── Pre-processing ──────────────────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  Pre-processing...")

    # Replace 0 values with NaN for columns where 0 is not valid
    cols_with_zero = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in cols_with_zero:
        if col in df.columns:
            df[col] = df[col].replace(0, np.nan)
            df[col] = df[col].fillna(df[col].median())

    # Separate features and target
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']

    print(f"\n  Class Distribution:")
    print(f"    Non-Diabetic (0): {(y == 0).sum()}")
    print(f"    Diabetic (1)    : {(y == 1).sum()}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\n  Training set: {X_train.shape[0]} samples")
    print(f"  Test set    : {X_test.shape[0]} samples")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ── Find Optimal K ──────────────────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  Finding optimal K value...")

    error_rates = []
    k_range = range(1, 21)

    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train_scaled, y_train)
        pred = knn.predict(X_test_scaled)
        error_rates.append(1 - accuracy_score(y_test, pred))

    optimal_k = list(k_range)[np.argmin(error_rates)]
    print(f"  Optimal K = {optimal_k} (lowest error rate: {min(error_rates):.4f})")

    # Plot K vs Error Rate
    plt.figure(figsize=(8, 5))
    plt.plot(k_range, error_rates, 'bo-', linewidth=2, markersize=6)
    plt.axvline(x=optimal_k, color='r', linestyle='--', label=f'Optimal K={optimal_k}')
    plt.xlabel('K Value')
    plt.ylabel('Error Rate')
    plt.title('K vs Error Rate')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plot_path = os.path.join(SCRIPT_DIR, 'knn_k_vs_error.png')
    plt.savefig(plot_path, dpi=100)
    plt.close()
    print(f"  Plot saved as '{plot_path}'")

    # ── Train Final Model ───────────────────────────────────────────────
    print(f"\n{'═' * 65}")
    print(f"  KNN MODEL (K = {optimal_k})")
    print(f"{'═' * 65}")

    knn_final = KNeighborsClassifier(n_neighbors=optimal_k)
    knn_final.fit(X_train_scaled, y_train)
    y_pred = knn_final.predict(X_test_scaled)

    # ── Evaluation Metrics ──────────────────────────────────────────────
    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    error_rate = 1 - acc
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)

    print(f"\n  Confusion Matrix:")
    print(f"                       Predicted")
    print(f"                    Non-Diab  Diabetic")
    print(f"  Actual Non-Diab    {cm[0][0]:<10} {cm[0][1]}")
    print(f"  Actual Diabetic    {cm[1][0]:<10} {cm[1][1]}")

    print(f"\n  Performance Metrics:")
    print(f"  {'─' * 40}")
    print(f"    Accuracy   : {acc:.4f}  ({acc*100:.2f}%)")
    print(f"    Error Rate : {error_rate:.4f}  ({error_rate*100:.2f}%)")
    print(f"    Precision  : {prec:.4f}")
    print(f"    Recall     : {rec:.4f}")
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Loading dataset...
  Shape: (768, 9)
  Columns: ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']

  Class Distribution:
    Non-Diabetic (0): 500
    Diabetic (1)    : 268

  Training set: 614 samples
  Test set    : 154 samples

  Finding optimal K value...
  Optimal K = 11 (lowest error rate: 0.2078)

  KNN MODEL (K = 11)

  Confusion Matrix:
                       Predicted
                    Non-Diab  Diabetic
  Actual Non-Diab    85         14
  Actual Diabetic    18         37

  Performance Metrics:
    Accuracy   : 0.7922  (79.22%)
    Error Rate : 0.2078  (20.78%)
    Precision  : 0.7255
    Recall     : 0.6727

========================================================================
"""
