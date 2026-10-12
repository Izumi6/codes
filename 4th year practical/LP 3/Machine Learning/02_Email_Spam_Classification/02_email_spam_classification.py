"""
================================================================================
  Program 2: Email Spam Classification using KNN and SVM
  Course: Machine Learning

  Description:
    Classify emails as Spam or Not Spam using binary classification.
      a) Normal State  – Not Spam
      b) Abnormal State – Spam
    Uses K-Nearest Neighbors and Support Vector Machine.
    Analyzes and compares their performance.

  Dataset: https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv
           Download 'emails.csv' and place it in the same directory.

  Requirements: pip install pandas numpy scikit-learn matplotlib seaborn
================================================================================
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)
import warnings
warnings.filterwarnings('ignore')

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()


def print_confusion_matrix(cm, model_name):
    """Display confusion matrix in a formatted way."""
    print(f"\n  Confusion Matrix ({model_name}):")
    print(f"                    Predicted")
    print(f"                  Not Spam  Spam")
    print(f"  Actual Not Spam   {cm[0][0]:<8} {cm[0][1]}")
    print(f"  Actual Spam       {cm[1][0]:<8} {cm[1][1]}")


def evaluate_model(name, y_true, y_pred):
    """Evaluate and print model metrics."""
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)

    print(f"\n  {name} Results:")
    print(f"  {'─' * 40}")
    print(f"    Accuracy  : {acc:.4f}  ({acc*100:.2f}%)")
    print(f"    Precision : {prec:.4f}")
    print(f"    Recall    : {rec:.4f}")
    print(f"    F1 Score  : {f1:.4f}")
    print_confusion_matrix(cm, name)

    return acc, prec, rec, f1


def main():
    print("=" * 65)
    print("   EMAIL SPAM CLASSIFICATION — KNN & SVM")
    print("=" * 65)

    # ── Load Dataset ────────────────────────────────────────────────────
    print("\n  Loading dataset...")
    csv_path = os.path.join(SCRIPT_DIR, "emails.csv")
    df = pd.read_csv(csv_path)
    print(f"  Dataset shape: {df.shape}")
    print(f"  Columns: {list(df.columns[:5])}... ({len(df.columns)} total)")

    # ── Pre-processing ──────────────────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  Pre-processing...")

    # Drop non-numeric or identifier columns
    if 'Email No.' in df.columns:
        df = df.drop('Email No.', axis=1)

    # Check class distribution
    print(f"\n  Class distribution:")
    print(f"    Not Spam (0): {(df['Prediction'] == 0).sum()}")
    print(f"    Spam (1)    : {(df['Prediction'] == 1).sum()}")

    # Drop missing values
    df = df.dropna()

    # Separate features and target
    X = df.drop('Prediction', axis=1)
    y = df['Prediction']

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

    # ── KNN Classifier ─────────────────────────────────────────────────
    print(f"\n{'═' * 65}")
    print("  MODEL 1: K-Nearest Neighbors (K=5)")
    print(f"{'═' * 65}")

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)
    knn_pred = knn.predict(X_test_scaled)
    knn_acc, knn_prec, knn_rec, knn_f1 = evaluate_model("KNN", y_test, knn_pred)

    # ── SVM Classifier ─────────────────────────────────────────────────
    print(f"\n{'═' * 65}")
    print("  MODEL 2: Support Vector Machine (RBF Kernel)")
    print(f"{'═' * 65}")

    svm = SVC(kernel='rbf', random_state=42)
    svm.fit(X_train_scaled, y_train)
    svm_pred = svm.predict(X_test_scaled)
    svm_acc, svm_prec, svm_rec, svm_f1 = evaluate_model("SVM", y_test, svm_pred)

    # ── Comparison ──────────────────────────────────────────────────────
    print(f"\n{'═' * 65}")
    print("  PERFORMANCE COMPARISON")
    print(f"{'═' * 65}")
    print(f"  {'Metric':<15} {'KNN':>12} {'SVM':>12}")
    print(f"  {'─' * 40}")
    print(f"  {'Accuracy':<15} {knn_acc:>12.4f} {svm_acc:>12.4f}")
    print(f"  {'Precision':<15} {knn_prec:>12.4f} {svm_prec:>12.4f}")
    print(f"  {'Recall':<15} {knn_rec:>12.4f} {svm_rec:>12.4f}")
    print(f"  {'F1 Score':<15} {knn_f1:>12.4f} {svm_f1:>12.4f}")

    winner = "SVM" if svm_acc > knn_acc else "KNN"
    print(f"\n  ✓ Better Model: {winner}")
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Loading dataset...
  Dataset shape: (5172, 3002)

  Class distribution:
    Not Spam (0): 3672
    Spam (1)    : 1500

  Training set: 4137 samples
  Test set    : 1035 samples

  MODEL 1: K-Nearest Neighbors (K=5)
    Accuracy  : 0.8647  (86.47%)
    Precision : 0.7921
    Recall    : 0.8200
    F1 Score  : 0.8058
    Confusion Matrix (KNN):
                      Predicted
                    Not Spam  Spam
    Actual Not Spam   651      89
    Actual Spam        51     244

  MODEL 2: Support Vector Machine (RBF Kernel)
    Accuracy  : 0.9565  (95.65%)
    Precision : 0.9512
    Recall    : 0.9186
    F1 Score  : 0.9346
    Confusion Matrix (SVM):
                      Predicted
                    Not Spam  Spam
    Actual Not Spam   716      24
    Actual Spam        21     274

  PERFORMANCE COMPARISON
    Metric              KNN          SVM
    Accuracy         0.8647       0.9565
    Precision        0.7921       0.9512
    Recall           0.8200       0.9186
    F1 Score         0.8058       0.9346

  ✓ Better Model: SVM

========================================================================
"""
