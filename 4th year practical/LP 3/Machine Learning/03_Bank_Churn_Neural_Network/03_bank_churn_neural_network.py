"""
================================================================================
  Program 3: Bank Customer Churn Prediction using Neural Network
  Course: Machine Learning

  Problem Statement:
    Given a bank customer, build a neural network-based classifier that can
    determine whether they will leave (churn) or not in the next 6 months.

  Steps:
    1. Read the dataset.
    2. Distinguish the feature and target set and divide into training and test sets.
    3. Normalize the train and test data.
    4. Initialize and build the model. Identify points of improvement and implement changes.
    5. Print the accuracy score and confusion matrix.

  Dataset: https://www.kaggle.com/barelydedicated/bank-customer-churn-modeling
           Download 'Churn_Modelling.csv' and place it in the same directory.

  Requirements: pip install pandas numpy scikit-learn tensorflow keras
================================================================================
"""

import os
import warnings
from typing import Any

# Suppress backend warnings and verbose logs
warnings.filterwarnings('ignore')
os.environ.setdefault('KERAS_BACKEND', 'torch')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Neural Network Framework Import
try:
    import keras
    from keras.models import Sequential
    from keras.layers import Input, Dense, Dropout
except Exception:
    from tensorflow.keras.models import Sequential  # type: ignore
    from tensorflow.keras.layers import Input, Dense, Dropout  # type: ignore


def main() -> None:
    print("=" * 65)
    print("   BANK CUSTOMER CHURN PREDICTION — NEURAL NETWORK")
    print("=" * 65)

    # ── Step 1: Read the Dataset ────────────────────────────────────────
    print("\n[Step 1] Reading Dataset...")
    csv_path = "Churn_Modelling.csv" if os.path.exists("Churn_Modelling.csv") else os.path.join(os.path.dirname(os.path.abspath(__file__)), "Churn_Modelling.csv")
    df = pd.read_csv(csv_path)
    print(f"Shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())

    # ── Step 2: Feature and Target Separation & Train-Test Split ─────────
    print(f"\n{'─' * 65}")
    print("[Step 2] Distinguishing Features and Target, Train-Test Split...")

    # Drop non-predictive identifier columns
    df_clean = df.drop(columns=['RowNumber', 'CustomerId', 'Surname'], errors='ignore')

    # Encode categorical features
    le_geo = LabelEncoder()
    le_gender = LabelEncoder()
    df_clean['Geography'] = le_geo.fit_transform(df_clean['Geography'])
    df_clean['Gender'] = le_gender.fit_transform(df_clean['Gender'])

    # Separate features (X) and target (y)
    X = df_clean.drop(columns=['Exited'])
    y = df_clean['Exited']

    print(f"Features ({len(X.columns)}): {list(X.columns)}")
    print("Target: Exited (0 = Stayed, 1 = Churned)")
    print(f"Class Distribution: Stayed (0) = {(y == 0).sum()}, Churned (1) = {(y == 1).sum()}")

    # Train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training set: {len(X_train)} samples")
    print(f"Testing set : {len(X_test)} samples")

    # ── Step 3: Normalize Train and Test Data ────────────────────────────
    print(f"\n{'─' * 65}")
    print("[Step 3] Normalizing Train and Test Data...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("✓ StandardScaler applied to train and test features.")

    # ── Step 4: Initialize, Build and Train the Neural Network ──────────
    print(f"\n{'─' * 65}")
    print("[Step 4] Initializing and Building Neural Network Model...")

    model = Sequential([
        Input(shape=(X_train_scaled.shape[1],)),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    print("\nModel Architecture:")
    model.summary()

    print("\nTraining the Neural Network (30 Epochs, Batch Size = 32)...")
    v_silent: Any = 0
    history: Any = model.fit(
        X_train_scaled, y_train,
        epochs=30,
        batch_size=32,
        validation_split=0.1,
        verbose=v_silent
    )

    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    print("✓ Training completed successfully.")
    print(f"  Final Training Accuracy  : {final_train_acc:.4f} ({final_train_acc*100:.2f}%)")
    print(f"  Final Validation Accuracy: {final_val_acc:.4f} ({final_val_acc*100:.2f}%)")

    # ── Step 5: Evaluate the Model (Accuracy & Confusion Matrix) ─────────
    print(f"\n{'═' * 65}")
    print("  [Step 5] MODEL EVALUATION")
    print(f"{'═' * 65}")

    # Predict churn probability and threshold at 0.5
    y_pred_prob: Any = model.predict(X_test_scaled, verbose=v_silent)
    y_pred = (y_pred_prob > 0.5).astype(int).flatten()

    # Accuracy Score
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy Score: {acc:.4f} ({acc*100:.2f}%)")

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print("                    Predicted: Stayed (0)   Predicted: Churned (1)")
    print(f"  Actual Stayed (0)        {cm[0][0]:<23} {cm[0][1]}")
    print(f"  Actual Churned (1)       {cm[1][0]:<23} {cm[1][1]}")

    # Classification Report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Stayed (0)', 'Churned (1)']))
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

=================================================================
   BANK CUSTOMER CHURN PREDICTION — NEURAL NETWORK
=================================================================

[Step 1] Reading Dataset...
Shape: (10000, 14)

First 5 rows:
   RowNumber  CustomerId   Surname  CreditScore Geography  Gender  Age  ...
0          1    15634602  Hargrave          619    France  Female   42  ...
1          2    15647311      Hill          608     Spain  Female   41  ...
2          3    15619304      Onio          502    France  Female   42  ...
3          4    15701354      Boni          699    France  Female   39  ...
4          5    15737888  Mitchell          850     Spain  Female   43  ...

─────────────────────────────────────────────────────────────────
[Step 2] Distinguishing Features and Target, Train-Test Split...
Features (10): ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
Target: Exited (0 = Stayed, 1 = Churned)
Class Distribution: Stayed (0) = 7963, Churned (1) = 2037
Training set: 8000 samples
Testing set : 2000 samples

─────────────────────────────────────────────────────────────────
[Step 3] Normalizing Train and Test Data...
✓ StandardScaler applied to train and test features.

─────────────────────────────────────────────────────────────────
[Step 4] Initializing and Building Neural Network Model...

Training the Neural Network (30 Epochs, Batch Size = 32)...
✓ Training completed successfully.
  Final Training Accuracy  : 0.8642 (86.42%)
  Final Validation Accuracy: 0.8575 (85.75%)

═════════════════════════════════════════════════════════════════
  [Step 5] MODEL EVALUATION
═════════════════════════════════════════════════════════════════

Accuracy Score: 0.8625 (86.25%)

Confusion Matrix:
                    Predicted: Stayed (0)   Predicted: Churned (1)
  Actual Stayed (0)        1530                    77
  Actual Churned (1)       198                     195

Classification Report:
              precision    recall  f1-score   support

  Stayed (0)       0.89      0.95      0.92      1607
 Churned (1)       0.72      0.50      0.59       393

    accuracy                           0.86      2000
   macro avg       0.80      0.72      0.75      2000
weighted avg       0.85      0.86      0.85      2000

═════════════════════════════════════════════════════════════════

========================================================================
"""
