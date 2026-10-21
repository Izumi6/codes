"""
LP-5 Deep Learning - Practical 1
Linear Regression using Deep Neural Network (DNN)

Problem Statement:
Implement Boston housing price prediction problem by Linear regression
using Deep Neural network. Use Boston House price prediction dataset.

Dataset:
BostonHousing.csv (506 samples, 13 input features, 1 target variable 'medv')

Sample Output:
Dataset Shape: (506, 14)
Training Samples: 404, Testing Samples: 102
Mean Squared Error (MSE): 11.68
Root Mean Squared Error (RMSE): 3.42
Mean Absolute Error (MAE): 2.23
R2 Score: 0.8408

Sample Predictions (Actual vs Predicted in $1000s):
Sample 1: Actual = 23.60, Predicted = 27.25, Difference = 3.65
Sample 2: Actual = 32.40, Predicted = 34.06, Difference = 1.66
Sample 3: Actual = 13.60, Predicted = 16.83, Difference = 3.23
Sample 4: Actual = 22.80, Predicted = 26.20, Difference = 3.40
Sample 5: Actual = 16.10, Predicted = 16.30, Difference = 0.20
"""

import os
import warnings
warnings.filterwarnings('ignore')

# Compatible with both standard TensorFlow (Windows/Linux) and Keras 3 (macOS)
if 'KERAS_BACKEND' not in os.environ:
    os.environ['KERAS_BACKEND'] = 'torch'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

try:
    import keras
    from keras.models import Sequential
    from keras.layers import Dense, Input
except ImportError:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Input

def main():
    # 1. Load Dataset
    data_path = 'BostonHousing.csv'
    if not os.path.exists(data_path):
        data_path = os.path.join(os.path.dirname(__file__), 'BostonHousing.csv')

    df = pd.read_csv(data_path)
    print(f"Dataset Shape: {df.shape}")

    # 2. Features and Target
    X = df.drop(columns=['medv']).values
    y = df['medv'].values

    # 3. Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training Samples: {len(X_train)}, Testing Samples: {len(X_test)}")

    # 4. Standardize Features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 5. Build Deep Neural Network Model
    model = Sequential([
        Input(shape=(13,)),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1)  # Linear output for regression
    ])

    # 6. Compile Model
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # 7. Train Model
    model.fit(
        X_train_scaled,
        y_train,
        epochs=60,
        batch_size=16,
        verbose=0
    )

    # 8. Evaluate on Test Set
    y_pred = model.predict(X_test_scaled, verbose=0).flatten()

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"R2 Score: {r2:.4f}")

    # 9. Display Sample Predictions
    print("\nSample Predictions (Actual vs Predicted in $1000s):")
    for i in range(5):
        diff = abs(y_test[i] - y_pred[i])
        print(f"Sample {i+1}: Actual = {y_test[i]:.2f}, Predicted = {y_pred[i]:.2f}, Difference = {diff:.2f}")

if __name__ == '__main__':
    main()
