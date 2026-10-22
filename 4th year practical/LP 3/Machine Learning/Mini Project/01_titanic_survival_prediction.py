"""
================================================================================
  Mini Project: Titanic Survival Prediction
  Course: Machine Learning

  Description:
    Build a machine learning model to predict whether a passenger survived
    the Titanic shipwreck using features like Age, Sex, Pclass, etc.

  Dataset: https://www.kaggle.com/competitions/titanic/data
           'titanic.csv' should be in the same directory.

  Requirements: pip install pandas numpy scikit-learn
================================================================================
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=" * 65)
    print("   TITANIC SURVIVAL PREDICTION")
    print("=" * 65)

    # ── Step 1: Load Dataset ───────────────────────────────────────────
    print("\n  [Step 1] Loading Dataset...")
    try:
        df = pd.read_csv("titanic.csv")
    except FileNotFoundError:
        print("  Error: 'titanic.csv' not found in the current directory.")
        return

    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")

    # ── Step 2: Data Preprocessing ─────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  [Step 2] Preprocessing Data...")

    # Drop columns that are mostly unique or have too many missing values
    columns_to_drop = ['PassengerId', 'Name', 'Ticket', 'Cabin']
    df = df.drop(columns=columns_to_drop)

    # Handle missing values
    # Fill missing 'Age' with the median age
    df['Age'] = df['Age'].fillna(df['Age'].median())
    # Fill missing 'Embarked' with the most frequent value
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
    # Fill missing 'Fare' with median (if any, though usually none in train set)
    df['Fare'] = df['Fare'].fillna(df['Fare'].median())

    print(f"  Dropped columns: {columns_to_drop}")
    print("  Filled missing values in 'Age' and 'Embarked'.")

    # Encode categorical variables
    le_sex = LabelEncoder()
    df['Sex'] = le_sex.fit_transform(df['Sex'])  # male: 1, female: 0

    le_embarked = LabelEncoder()
    df['Embarked'] = le_embarked.fit_transform(df['Embarked'])

    print("  Encoded 'Sex' and 'Embarked' to numeric values.")

    # ── Step 3: Train-Test Split ───────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  [Step 3] Splitting Data...")

    X = df.drop('Survived', axis=1)
    y = df['Survived']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"  Training set : {X_train.shape[0]} samples")
    print(f"  Test set     : {X_test.shape[0]} samples")

    # Feature Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # ── Step 4: Build and Train Model ──────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  [Step 4] Training Model (Random Forest Classifier)...")

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print("  ✓ Model training complete.")

    # ── Step 5: Evaluate Model ─────────────────────────────────────────
    print(f"\n{'═' * 65}")
    print("  [Step 5] MODEL EVALUATION")
    print(f"{'═' * 65}")

    y_pred = model.predict(X_test)

    # Accuracy
    acc = accuracy_score(y_test, y_pred)
    print(f"\n  Accuracy Score: {acc:.4f} ({acc * 100:.2f}%)")

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n  Confusion Matrix:")
    print("                    Predicted")
    print("                  Died  Survived")
    print(f"  Actual Died      {cm[0][0]:<5} {cm[0][1]}")
    print(f"  Actual Survived  {cm[1][0]:<5} {cm[1][1]}")

    # Classification Report
    print(f"\n  Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Died', 'Survived']))

    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  [Step 1] Loading Dataset...
  Shape: (891, 12)

  [Step 2] Preprocessing Data...
  Dropped columns: ['PassengerId', 'Name', 'Ticket', 'Cabin']
  Filled missing values in 'Age' and 'Embarked'.
  Encoded 'Sex' and 'Embarked' to numeric values.

  [Step 3] Splitting Data...
  Training set : 712 samples
  Test set     : 179 samples

  [Step 4] Training Model (Random Forest Classifier)...
  ✓ Model training complete.

  [Step 5] MODEL EVALUATION
  Accuracy Score: 0.8212 (82.12%)

  Confusion Matrix:
                    Predicted
                  Died  Survived
  Actual Died      92    13
  Actual Survived  19    55

  Classification Report:
                precision    recall  f1-score   support
        Died       0.83      0.88      0.85       105
    Survived       0.81      0.74      0.77        74

========================================================================
"""
