"""
LP-5 Deep Learning - Practical 4
Recurrent Neural Network (RNN) for Time Series Analysis

Problem Statement:
Use the Google stock prices dataset and design a time series analysis
and prediction system using RNN.

Dataset:
- Google_Stock_Price_Train.csv (2,299 daily stock records, 2008-2016)
- Google_Stock_Price_Test.csv (220 daily stock records, 2017)

Sample Output:
Train Records: 2299, Test Records: 220
Input Sequence Shape: (2239, 60, 1)
Root Mean Squared Error (RMSE): 15.08
Mean Absolute Error (MAE): 11.28

Sample Predictions (Actual vs Predicted Google Stock Price):
3/15/2017 -> Actual: 867.94, Predicted: 868.52, Difference: 0.58
3/16/2017 -> Actual: 870.53, Predicted: 868.77, Difference: 1.76
3/17/2017 -> Actual: 873.68, Predicted: 873.77, Difference: 0.09
3/20/2017 -> Actual: 869.48, Predicted: 877.98, Difference: 8.50
3/21/2017 -> Actual: 870.06, Predicted: 876.01, Difference: 5.95
"""

import os
import warnings
warnings.filterwarnings('ignore')

# Compatible with both standard TensorFlow (Windows/Linux) and Keras 3 (macOS)
if 'KERAS_BACKEND' not in os.environ:
    os.environ['KERAS_BACKEND'] = 'torch'
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

try:
    import keras
    from keras.models import Sequential
    from keras.layers import SimpleRNN, Dense, Dropout, Input
except ImportError:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import SimpleRNN, Dense, Dropout, Input

def get_file_path(filename):
    if os.path.exists(filename):
        return filename
    return os.path.join(os.path.dirname(__file__), filename)

def main():
    # 1. Load Training Dataset
    train_path = get_file_path('Google_Stock_Price_Train.csv')
    train_df = pd.read_csv(train_path)
    train_df.columns = train_df.columns.str.lower()
    train_data = train_df[['open']].values

    # 2. Load Testing Dataset
    test_path = get_file_path('Google_Stock_Price_Test.csv')
    test_df = pd.read_csv(test_path)
    test_df.columns = test_df.columns.str.lower()
    actual_test_prices = test_df[['open']].values

    print(f"Train Records: {len(train_df)}, Test Records: {len(test_df)}")

    # 3. Feature Scaling (MinMaxScaler to [0, 1])
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_train_data = scaler.fit_transform(train_data)

    # 4. Create 60-timestep Training Sequences
    timesteps = 60
    X_train, y_train = [], []
    for i in range(timesteps, len(scaled_train_data)):
        X_train.append(scaled_train_data[i - timesteps:i, 0])
        y_train.append(scaled_train_data[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    print(f"Input Sequence Shape: {X_train.shape}")

    # 5. Build Recurrent Neural Network (RNN) Architecture
    model = Sequential([
        Input(shape=(timesteps, 1)),
        SimpleRNN(units=50, return_sequences=True),
        Dropout(0.2),
        SimpleRNN(units=50),
        Dropout(0.2),
        Dense(units=1)  # Predict next day open price
    ])

    # 6. Compile Model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 7. Train Model
    model.fit(
        X_train,
        y_train,
        epochs=15,
        batch_size=32,
        verbose=0
    )

    # 8. Prepare Test Data
    total_data = pd.concat((train_df['open'], test_df['open']), axis=0)
    inputs = total_data[len(total_data) - len(test_df) - timesteps:].values
    inputs = inputs.reshape(-1, 1)
    inputs = scaler.transform(inputs)

    X_test = []
    for i in range(timesteps, len(inputs)):
        X_test.append(inputs[i - timesteps:i, 0])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # 9. Predict and Inverse Scale
    predicted_scaled = model.predict(X_test, verbose=0)
    predicted_prices = scaler.inverse_transform(predicted_scaled)

    # 10. Evaluate Performance
    rmse = np.sqrt(mean_squared_error(actual_test_prices, predicted_prices))
    mae = mean_absolute_error(actual_test_prices, predicted_prices)
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")

    # 11. Sample Predictions
    print("\nSample Predictions (Actual vs Predicted Google Stock Price):")
    for i in range(5):
        date_val = test_df['date'].iloc[i]
        actual = actual_test_prices[i][0]
        predicted = predicted_prices[i][0]
        diff = abs(actual - predicted)
        print(f"{date_val} -> Actual: {actual:.2f}, Predicted: {predicted:.2f}, Difference: {diff:.2f}")

    # 12. Generate and Save Plot
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 6))
        plt.plot(actual_test_prices, color='#e74c3c', linewidth=2, label='Real Google Stock Price')
        plt.plot(predicted_prices, color='#2980b9', linewidth=2, linestyle='--', label='Predicted Google Stock Price (RNN)')
        plt.title('Google Stock Price Prediction using Recurrent Neural Network (RNN)', fontsize=13, fontweight='bold')
        plt.xlabel('Time (Trading Days)', fontsize=11)
        plt.ylabel('Google Stock Price ($)', fontsize=11)
        plt.legend(fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.5)

        plt.tight_layout()
        plot_path = os.path.join(os.path.dirname(__file__), 'google_stock_price_prediction.png')
        plt.savefig(plot_path, dpi=120)
        print(f"Plot saved as 'google_stock_price_prediction.png'")
        plt.close()
    except Exception as e:
        pass

if __name__ == '__main__':
    main()

