"""
================================================================================
  Program 3: Bank Customer Churn Prediction using Neural Network
  Course: Machine Learning

  Description:
    Build a neural network classifier to predict whether a bank customer
    will leave (churn) in the next 6 months.
    Steps:
      1. Read the dataset
      2. Separate features and target, split into train/test
      3. Normalize train and test data
      4. Build and train the neural network model
      5. Print accuracy score and confusion matrix

  Dataset: https://www.kaggle.com/barelydedicated/bank-customer-churn-modeling
           'Churn_Modelling.csv' in the same directory.

  Requirements: pip install pandas numpy scikit-learn (and keras/torch/tensorflow)
================================================================================
"""

import os
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

warnings.filterwarnings('ignore')

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()

# Detect available neural network library
# Ensure Keras uses PyTorch backend to avoid macOS threading crashes
os.environ['KERAS_BACKEND'] = 'torch'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

MODEL_BACKEND = "None"
try:
    import keras
    from keras import layers, models
    MODEL_BACKEND = "Keras"
except Exception:
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Dropout, Input
        MODEL_BACKEND = "TensorFlow"
    except Exception:
        from sklearn.neural_network import MLPClassifier
        MODEL_BACKEND = "sklearn_MLP"


def main():
    print("=" * 65)
    print("   BANK CUSTOMER CHURN PREDICTION — NEURAL NETWORK")
    print("=" * 65)

    # ── Step 1: Read the Dataset ────────────────────────────────────────
    print("\n  [Step 1] Reading Dataset...")
    csv_path = os.path.join(SCRIPT_DIR, "Churn_Modelling.csv")
    df = pd.read_csv(csv_path)
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"\n  First 5 rows:")
    print(df.head())

    # ── Step 2: Feature and Target Separation ───────────────────────────
    print(f"\n{'─' * 65}")
    print("  [Step 2] Preparing Features and Target...")

    # Drop irrelevant columns
    df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1, errors='ignore')

    # Encode categorical variables
    le_geo = LabelEncoder()
    le_gen = LabelEncoder()
    df['Geography'] = le_geo.fit_transform(df['Geography'])
    df['Gender'] = le_gen.fit_transform(df['Gender'])

    # Separate features (X) and target (y)
    X = df.drop('Exited', axis=1)
    y = df['Exited']

    print(f"  Features: {list(X.columns)}")
    print(f"  Target  : Exited (0 = Stayed, 1 = Churned)")
    print(f"\n  Class Distribution:")
    print(f"    Stayed  (0): {(y == 0).sum()}")
    print(f"    Churned (1): {(y == 1).sum()}")

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\n  Training set: {X_train.shape[0]} samples")
    print(f"  Test set    : {X_test.shape[0]} samples")

    # ── Step 3: Normalize the Data ──────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  [Step 3] Normalizing Data...")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("  ✓ StandardScaler applied to train and test data.")

    # ── Step 4: Build and Train the Neural Network ─────────────────────
    print(f"\n{'─' * 65}")
    print(f"  [Step 4] Building Neural Network Model (Backend: {MODEL_BACKEND})...")

    if MODEL_BACKEND == "Keras":
        model = models.Sequential([
            layers.Input(shape=(X_train_scaled.shape[1],)),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        print("\n  Model Architecture:")
        model.summary()

        print("\n  Training the neural network (30 epochs)...")
        history = model.fit(
            X_train_scaled, y_train.values,
            epochs=30,
            batch_size=32,
            validation_split=0.1,
            verbose=0
        )
        final_train_acc = history.history['accuracy'][-1]
        final_val_acc = history.history['val_accuracy'][-1]
        print(f"  Final Training Accuracy  : {final_train_acc:.4f}")
        print(f"  Final Validation Accuracy: {final_val_acc:.4f}")

        y_pred_prob = model.predict(X_test_scaled, verbose=0)
        y_pred = (y_pred_prob > 0.5).astype(int).flatten()

    elif MODEL_BACKEND == "TensorFlow":
        model = Sequential([
            Input(shape=(X_train_scaled.shape[1],)),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(32, activation='relu'),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        print("\n  Model Architecture:")
        model.summary()

        print("\n  Training the model (30 epochs)...")
        history = model.fit(
            X_train_scaled, y_train.values,
            epochs=30,
            batch_size=32,
            validation_split=0.1,
            verbose=0
        )
        y_pred_prob = model.predict(X_test_scaled, verbose=0)
        y_pred = (y_pred_prob > 0.5).astype(int).flatten()

    else:
        # Standard Scikit-Learn Multi-Layer Perceptron Fallback
        print("\n  Using Scikit-Learn MLPClassifier (Multi-Layer Perceptron)...")
        mlp = MLPClassifier(
            hidden_layer_sizes=(64, 32, 16),
            activation='relu',
            solver='adam',
            max_iter=50,
            random_state=42
        )
        mlp.fit(X_train_scaled, y_train)
        y_pred = mlp.predict(X_test_scaled)

    # ── Step 5: Evaluate the Model ──────────────────────────────────────
    print(f"\n{'═' * 65}")
    print("  [Step 5] MODEL EVALUATION")
    print(f"{'═' * 65}")

    # Accuracy
    acc = accuracy_score(y_test, y_pred)
    print(f"\n  Accuracy Score: {acc:.4f}  ({acc*100:.2f}%)")

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n  Confusion Matrix:")
    print(f"                    Predicted")
    print(f"                  Stayed  Churned")
    print(f"  Actual Stayed    {cm[0][0]:<8} {cm[0][1]}")
    print(f"  Actual Churned   {cm[1][0]:<8} {cm[1][1]}")

    # Classification Report
    print(f"\n  Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Stayed', 'Churned']))

    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()
