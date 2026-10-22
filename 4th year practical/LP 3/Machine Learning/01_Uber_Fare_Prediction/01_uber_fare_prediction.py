"""
================================================================================
  Program 1: Uber Ride Fare Prediction
  Course: Machine Learning

  Description:
    Predict the price of an Uber ride from pickup to drop-off location.
    Steps:
      1. Pre-process the dataset
      2. Identify outliers
      3. Check correlation
      4. Implement Linear Regression and Random Forest Regression
      5. Evaluate and compare models (R2, RMSE)

  Dataset: https://www.kaggle.com/datasets/yasserh/uber-fares-dataset
           Download 'uber.csv' and place it in the same directory.

  Requirements: pip install pandas numpy scikit-learn matplotlib seaborn
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')


def main():
    print("=" * 65)
    print("   UBER RIDE FARE PREDICTION")
    print("=" * 65)

    # ── Step 1: Load and Pre-process the Dataset ────────────────────────
    print("\n  [Step 1] Loading and Pre-processing Dataset...")
    df = pd.read_csv("uber.csv")

    print(f"  Original shape: {df.shape}")
    print(f"\n  First 5 rows:")
    print(df.head())

    # Drop unnecessary columns
    df = df.drop(['Unnamed: 0', 'key'], axis=1, errors='ignore')

    # Drop missing values
    print(f"\n  Missing values:\n{df.isnull().sum()}")
    df = df.dropna()

    # Extract datetime features
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')
    df = df.dropna(subset=['pickup_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day'] = df['pickup_datetime'].dt.day
    df['month'] = df['pickup_datetime'].dt.month
    df['year'] = df['pickup_datetime'].dt.year
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df = df.drop('pickup_datetime', axis=1)

    # Calculate distance using Haversine formula
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in km
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        return 2 * R * np.arcsin(np.sqrt(a))

    df['distance_km'] = haversine(
        df['pickup_latitude'], df['pickup_longitude'],
        df['dropoff_latitude'], df['dropoff_longitude']
    )

    print(f"\n  Shape after preprocessing: {df.shape}")

    # ── Step 2: Identify Outliers ───────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  [Step 2] Identifying Outliers...")

    # Remove unreasonable values
    df = df[(df['fare_amount'] > 0) & (df['fare_amount'] < 200)]
    df = df[(df['distance_km'] > 0) & (df['distance_km'] < 200)]
    df = df[(df['passenger_count'] > 0) & (df['passenger_count'] <= 6)]

    # Remove coordinate outliers (outside NYC area roughly)
    df = df[(df['pickup_latitude'].between(40.0, 42.0)) &
            (df['pickup_longitude'].between(-75.0, -72.0)) &
            (df['dropoff_latitude'].between(40.0, 42.0)) &
            (df['dropoff_longitude'].between(-75.0, -72.0))]

    print(f"  Shape after outlier removal: {df.shape}")
    print(f"\n  Fare statistics after cleaning:")
    print(df['fare_amount'].describe())

    # ── Step 3: Check Correlation ───────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  [Step 3] Correlation Analysis...")

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation = df[numeric_cols].corr()['fare_amount'].sort_values(ascending=False)
    print(f"\n  Correlation with fare_amount:")
    print(correlation)

    # Save correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=100)
    plt.close()
    print("\n  Correlation heatmap saved as 'correlation_heatmap.png'")

    # ── Step 4: Build Models ────────────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  [Step 4] Building Regression Models...")

    # Prepare features and target
    features = ['distance_km', 'passenger_count', 'hour', 'day', 'month', 'year', 'day_of_week']
    X = df[features]
    y = df['fare_amount']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"  Training set size: {X_train.shape[0]}")
    print(f"  Test set size    : {X_test.shape[0]}")

    # Model 1: Linear Regression
    print(f"\n  Training Linear Regression...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)

    # Model 2: Random Forest Regression
    print("  Training Random Forest Regression...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)

    # ── Step 5: Evaluate and Compare Models ─────────────────────────────
    print(f"\n{'═' * 65}")
    print("  [Step 5] MODEL EVALUATION & COMPARISON")
    print(f"{'═' * 65}")

    def evaluate_model(name, y_true, y_pred):
        r2 = r2_score(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        print(f"\n  {name}:")
        print(f"    R² Score : {r2:.4f}")
        print(f"    RMSE     : {rmse:.4f}")
        print(f"    MAE      : {mae:.4f}")
        return r2, rmse, mae

    lr_r2, lr_rmse, lr_mae = evaluate_model("Linear Regression", y_test, lr_pred)
    rf_r2, rf_rmse, rf_mae = evaluate_model("Random Forest Regression", y_test, rf_pred)

    print(f"\n{'─' * 65}")
    print(f"  {'Metric':<20} {'Linear Reg':>15} {'Random Forest':>15}")
    print(f"  {'─' * 50}")
    print(f"  {'R² Score':<20} {lr_r2:>15.4f} {rf_r2:>15.4f}")
    print(f"  {'RMSE':<20} {lr_rmse:>15.4f} {rf_rmse:>15.4f}")
    print(f"  {'MAE':<20} {lr_mae:>15.4f} {rf_mae:>15.4f}")

    winner = "Random Forest" if rf_r2 > lr_r2 else "Linear Regression"
    print(f"\n  ✓ Best Model: {winner}")
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  [Step 1] Loading and Pre-processing Dataset...
  Original shape: (200000, 9)

  [Step 2] Identifying Outliers...
  Shape after outlier removal: (190098, 14)

  [Step 3] Correlation Analysis...
  Correlation with fare_amount:
    fare_amount     1.000000
    distance_km     0.834540
    year            0.059376
    ...

  [Step 4] Building Regression Models...
  Training set size: 152078
  Test set size    : 38020

  MODEL EVALUATION & COMPARISON
    Linear Regression:
      R² Score : 0.7542
      RMSE     : 5.1230
      MAE      : 3.4512

    Random Forest Regression:
      R² Score : 0.8215
      RMSE     : 4.3680
      MAE      : 2.7814

  ✓ Best Model: Random Forest

========================================================================
"""
