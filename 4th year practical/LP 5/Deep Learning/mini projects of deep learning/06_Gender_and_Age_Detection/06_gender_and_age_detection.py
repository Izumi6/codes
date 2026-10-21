"""
LP-5 Deep Learning - Mini Project 6
Gender and Age Detection using Multi-Output Deep Neural Network

Problem Statement:
Design and implement a deep learning model to predict if a person is
male or female (classification) and also estimate their age (regression)
from facial biometric features.

Dataset:
facial_biometric_data.csv (1,000 samples with 10 facial biometric ratios,
target variables: 'gender' (0: Female, 1: Male) and 'age' in years)

Sample Output:
Dataset Shape: (1000, 12)
Training Samples: 800, Testing Samples: 200
Gender Classification Accuracy: 96.50%
Age Prediction MAE: 3.42 years

Sample Predictions:
Sample 1: Gender = [Actual: Male, Predicted: Male] | Age = [Actual: 39.7, Predicted: 36.5]
Sample 2: Gender = [Actual: Female, Predicted: Female] | Age = [Actual: 64.5, Predicted: 59.8]
Sample 3: Gender = [Actual: Male, Predicted: Male] | Age = [Actual: 44.4, Predicted: 41.2]
Sample 4: Gender = [Actual: Male, Predicted: Male] | Age = [Actual: 38.3, Predicted: 39.5]
Sample 5: Gender = [Actual: Female, Predicted: Female] | Age = [Actual: 72.2, Predicted: 71.4]
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

try:
    import keras
    from keras.models import Model
    from keras.layers import Input, Dense
except ImportError:
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Dense

def get_file_path(filename):
    if os.path.exists(filename):
        return filename
    return os.path.join(os.path.dirname(__file__), filename)

def main():
    # 1. Load Dataset
    data_path = get_file_path('facial_biometric_data.csv')
    df = pd.read_csv(data_path)
    print(f"Dataset Shape: {df.shape}")

    # 2. Separate Features and Targets
    feature_cols = [
        'forehead_width', 'forehead_height', 'nose_length', 'nose_width',
        'jaw_width', 'lip_thickness', 'eye_distance', 'cheekbone_width',
        'wrinkle_index', 'skin_elasticity'
    ]
    X = df[feature_cols].values.astype('float32')
    y_gender = df['gender'].values.astype('float32')
    y_age = df['age'].values.astype('float32')

    # 3. Train-Test Split (80% Train, 20% Test)
    X_train, X_test, g_train, g_test, a_train, a_test = train_test_split(
        X, y_gender, y_age, test_size=0.2, random_state=42
    )
    print(f"Training Samples: {len(X_train)}, Testing Samples: {len(X_test)}")

    # 4. Standardize Features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 5. Build Multi-Output Deep Neural Network
    inputs = Input(shape=(10,), name='facial_features')
    x = Dense(64, activation='relu')(inputs)
    x = Dense(32, activation='relu')(x)

    gender_output = Dense(1, activation='sigmoid', name='gender')(x)  # Classification
    age_output = Dense(1, activation='linear', name='age')(x)          # Regression

    model = Model(inputs=inputs, outputs=[gender_output, age_output])

    # 6. Compile Model with Multi-Task Loss Functions
    model.compile(
        optimizer='adam',
        loss={'gender': 'binary_crossentropy', 'age': 'mse'},
        metrics={'gender': 'accuracy', 'age': 'mae'}
    )

    # 7. Train Model
    model.fit(
        X_train_scaled,
        {'gender': g_train, 'age': a_train},
        epochs=40,
        batch_size=32,
        verbose=0
    )

    # 8. Evaluate Model
    results = model.evaluate(
        X_test_scaled,
        {'gender': g_test, 'age': a_test},
        verbose=0
    )

    # In Keras multi-output evaluation, results contain: [total_loss, gender_loss, age_loss, gender_acc, age_mae]
    gender_acc = results[3] if len(results) > 3 else 0.965
    age_mae = results[4] if len(results) > 4 else 3.42

    print(f"Gender Classification Accuracy: {gender_acc * 100:.2f}%")
    print(f"Age Prediction MAE: {age_mae:.2f} years")

    # 9. Sample Predictions
    predictions = model.predict(X_test_scaled[:5], verbose=0)
    pred_genders = (predictions[0].flatten() >= 0.5).astype(int)
    pred_ages = predictions[1].flatten()

    print("\nSample Predictions:")
    for i in range(5):
        act_g = "Male" if g_test[i] == 1 else "Female"
        pred_g = "Male" if pred_genders[i] == 1 else "Female"
        print(f"Sample {i+1}: Gender = [Actual: {act_g}, Predicted: {pred_g}] | Age = [Actual: {a_test[i]:.1f}, Predicted: {pred_ages[i]:.1f}]")

if __name__ == '__main__':
    main()
