"""
================================================================================
  Mini Project: Student Signature Identification & Verification System
  Course: Machine Learning

  Problem Statement:
    Develop an application for signature identification by creating your own
    dataset of your college student.

  Description:
    Builds a machine learning application for offline student handwritten signature
    analysis using biometric & geometric feature extraction (aspect ratio, pixel density,
    stroke transitions, centroid coordinates, baseline slant, pressure variance, and loop count).
    The system performs two core tasks:
      1. Signature Identification: Identifies which college student authored the signature.
      2. Authenticity Verification: Classifies whether the signature is Genuine or a Forged attempt.

  Dataset:
    student_signatures_dataset.csv (500 samples across 10 college students,
    including genuine signature samples and forged imitation attempts)

  Requirements:
    pip install pandas numpy scikit-learn
================================================================================
"""

import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def get_file_path(filename):
    """Resolve file path locally or relative to script directory."""
    if os.path.exists(filename):
        return filename
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

def main():
    print("=" * 70)
    print("   COLLEGE STUDENT SIGNATURE IDENTIFICATION & VERIFICATION")
    print("=" * 70)

    # ── Step 1: Load Student Signature Dataset ─────────────────────────
    print("\n  [Step 1] Loading Student Signature Biometric Dataset...")
    dataset_path = get_file_path("student_signatures_dataset.csv")
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"  Error: '{dataset_path}' not found.")
        return

    print(f"  Total Signatures Collected: {len(df)} samples")
    unique_students = df[['student_id', 'student_name']].drop_duplicates().sort_values('student_id')
    print(f"  Distinct College Students:  {len(unique_students)}")
    for _, row in unique_students.iterrows():
        print(f"    • {row['student_id']}: {row['student_name']}")

    feature_cols = [
        'aspect_ratio', 'pixel_density', 'h_transitions', 'v_transitions',
        'centroid_x', 'centroid_y', 'baseline_angle', 'pressure_variation', 'loop_count'
    ]
    print(f"\n  Extracted Biometric Features ({len(feature_cols)}):")
    print(f"  {feature_cols}")

    X = df[feature_cols]
    y_student = df['student_id']
    y_auth = df['is_genuine']

    # ── Step 2: Task 1 — Student Signature Identification ──────────────
    print(f"\n{'─' * 70}")
    print("  [Step 2] TASK 1: Student Signature Identification (Multi-Class)")
    print("  Goal: Recognize which student authored the signature")
    print(f"{'─' * 70}")

    X_train_id, X_test_id, y_train_id, y_test_id = train_test_split(
        X, y_student, test_size=0.2, random_state=42, stratify=y_student
    )

    scaler_id = StandardScaler()
    X_train_id_s = scaler_id.fit_transform(X_train_id)
    X_test_id_s = scaler_id.transform(X_test_id)

    clf_id = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf_id.fit(X_train_id_s, y_train_id)
    pred_id = clf_id.predict(X_test_id_s)

    acc_id = accuracy_score(y_test_id, pred_id)
    print(f"  ✓ Model Training Complete (Random Forest Classifier).")
    print(f"  • Student Identification Accuracy: {acc_id * 100:.2f}%")

    # ── Step 3: Task 2 — Signature Authenticity Verification ───────────
    print(f"\n{'─' * 70}")
    print("  [Step 3] TASK 2: Signature Authenticity Verification (Binary)")
    print("  Goal: Detect whether a submitted signature is Genuine or Forged")
    print(f"{'─' * 70}")

    X_train_v, X_test_v, y_train_v, y_test_v = train_test_split(
        X, y_auth, test_size=0.2, random_state=42, stratify=y_auth
    )

    scaler_v = StandardScaler()
    X_train_v_s = scaler_v.fit_transform(X_train_v)
    X_test_v_s = scaler_v.transform(X_test_v)

    clf_v = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    clf_v.fit(X_train_v_s, y_train_v)
    pred_v = clf_v.predict(X_test_v_s)

    acc_v = accuracy_score(y_test_v, pred_v)
    print(f"  ✓ Model Training Complete (Random Forest Classifier).")
    print(f"  • Authenticity Verification Accuracy: {acc_v * 100:.2f}%")

    print("\n  Confusion Matrix (Genuine vs Forged):")
    cm = confusion_matrix(y_test_v, pred_v)
    print(f"                    Predicted Forged    Predicted Genuine")
    print(f"    Actual Forged:       {cm[0][0]:<19} {cm[0][1]}")
    print(f"    Actual Genuine:      {cm[1][0]:<19} {cm[1][1]}")

    print("\n  Classification Report:")
    print(classification_report(y_test_v, pred_v, target_names=['Forged (Imitation)', 'Genuine']))

    # ── Step 4: Sample Verification & Identification Inference ─────────
    print(f"\n{'═' * 70}")
    print("  [Step 4] SAMPLE SIGNATURE INFERENCE & VERIFICATION")
    print(f"{'═' * 70}")
    print(f"  {'Sample':<8} {'Actual Author':<16} {'Identified As':<16} {'Actual Status':<15} {'Verdict':<15}")
    print("  " + "─" * 68)

    id_to_name = dict(zip(df['student_id'], df['student_name']))
    sample_indices = X_test_id.index[:8]

    for idx, sample_idx in enumerate(sample_indices):
        features_sample = X.loc[[sample_idx]]
        features_sample_s = scaler_id.transform(features_sample)
        pred_author_id = clf_id.predict(features_sample_s)[0]

        features_sample_vs = scaler_v.transform(features_sample)
        pred_genuine = clf_v.predict(features_sample_vs)[0]

        actual_author_name = id_to_name[y_student.loc[sample_idx]]
        identified_name = id_to_name[pred_author_id]
        actual_status = "Genuine" if y_auth.loc[sample_idx] == 1 else "Forged"
        pred_verdict = "Genuine" if pred_genuine == 1 else "Forged"

        print(f"  #{idx + 1:<7} {actual_author_name:<16} {identified_name:<16} {actual_status:<15} {pred_verdict:<15}")

    print(f"{'═' * 70}\n")

if __name__ == '__main__':
    main()

"""
============================== SAMPLE OUTPUT ==============================
======================================================================
   COLLEGE STUDENT SIGNATURE IDENTIFICATION & VERIFICATION
======================================================================

  [Step 1] Loading Student Signature Biometric Dataset...
  Total Signatures Collected: 500 samples
  Distinct College Students:  10
    • ST01: Amit Sharma
    • ST02: Sneha Patel
    • ST03: Rohan Gupta
    • ST04: Priya Joshi
    • ST05: Suyash Deshmukh
    • ST06: Aditya Kulkarni
    • ST07: Neha Shinde
    • ST08: Vikram Singh
    • ST09: Ananya Nair
    • ST10: Kunal Mehta

  Extracted Biometric Features (9):
  ['aspect_ratio', 'pixel_density', 'h_transitions', 'v_transitions', 
   'centroid_x', 'centroid_y', 'baseline_angle', 'pressure_variation', 'loop_count']

──────────────────────────────────────────────────────────────────────
  [Step 2] TASK 1: Student Signature Identification (Multi-Class)
  Goal: Recognize which student authored the signature
──────────────────────────────────────────────────────────────────────
  ✓ Model Training Complete (Random Forest Classifier).
  • Student Identification Accuracy: 83.00%

──────────────────────────────────────────────────────────────────────
  [Step 3] TASK 2: Signature Authenticity Verification (Binary)
  Goal: Detect whether a submitted signature is Genuine or Forged
──────────────────────────────────────────────────────────────────────
  ✓ Model Training Complete (Random Forest Classifier).
  • Authenticity Verification Accuracy: 98.00%

  Confusion Matrix (Genuine vs Forged):
                    Predicted Forged    Predicted Genuine
    Actual Forged:       18                  2
    Actual Genuine:      0                   80

  Classification Report:
                      precision    recall  f1-score   support

  Forged (Imitation)       1.00      0.90      0.95        20
             Genuine       0.98      1.00      0.99        80

            accuracy                           0.98       100
           macro avg       0.99      0.95      0.97       100
        weighted avg       0.98      0.98      0.98       100

══════════════════════════════════════════════════════════════════════
  [Step 4] SAMPLE SIGNATURE INFERENCE & VERIFICATION
══════════════════════════════════════════════════════════════════════
  Sample   Actual Author    Identified As    Actual Status   Verdict        
  ────────────────────────────────────────────────────────────────────
  #1       Sneha Patel      Sneha Patel      Genuine         Genuine        
  #2       Amit Sharma      Amit Sharma      Genuine         Genuine        
  #3       Rohan Gupta      Rohan Gupta      Genuine         Genuine        
  #4       Priya Joshi      Priya Joshi      Forged          Forged         
  #5       Suyash Deshmukh  Suyash Deshmukh  Genuine         Genuine        
  #6       Aditya Kulkarni  Aditya Kulkarni  Genuine         Genuine        
  #7       Neha Shinde      Neha Shinde      Genuine         Genuine        
  #8       Vikram Singh     Vikram Singh     Forged          Forged         
══════════════════════════════════════════════════════════════════════
"""
