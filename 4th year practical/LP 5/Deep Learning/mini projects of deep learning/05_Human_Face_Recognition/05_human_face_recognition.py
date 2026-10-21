"""
LP-5 Deep Learning - Mini Project 5
Human Face Recognition using Convolutional Neural Network (CNN)

Problem Statement:
Design and implement a human face recognition system using Deep Learning
to accurately classify and recognize faces of different individuals.

Dataset:
Olivetti Faces dataset (400 grayscale images of 40 distinct individuals,
10 images per individual, 64x64 pixels)

Sample Output:
Loaded Faces: 400 images of 40 distinct subjects
Image Shape: (64, 64, 1)
Training Faces: 320, Testing Faces: 80
Test Loss: 0.2326
Recognition Accuracy: 95.00%

Sample Predictions:
Sample 1: Actual Subject = Person 2, Recognized as = Person 2 (Match: True)
Sample 2: Actual Subject = Person 36, Recognized as = Person 36 (Match: True)
Sample 3: Actual Subject = Person 19, Recognized as = Person 19 (Match: True)
Sample 4: Actual Subject = Person 17, Recognized as = Person 17 (Match: True)
Sample 5: Actual Subject = Person 40, Recognized as = Person 40 (Match: True)
"""

import os
import warnings
warnings.filterwarnings('ignore')

# Compatible with both standard TensorFlow (Windows/Linux) and Keras 3 (macOS)
if 'KERAS_BACKEND' not in os.environ:
    os.environ['KERAS_BACKEND'] = 'torch'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
from sklearn.datasets import fetch_olivetti_faces
from sklearn.model_selection import train_test_split

try:
    import keras
    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
except ImportError:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input

def main():
    # 1. Load Olivetti Faces Dataset
    faces = fetch_olivetti_faces()
    X = np.expand_dims(faces.images.astype('float32'), -1)  # Reshape to (400, 64, 64, 1)
    y = faces.target                                        # Subject labels (0 to 39)

    print(f"Loaded Faces: {len(X)} images of {len(np.unique(y))} distinct subjects")
    print(f"Image Shape: {X.shape[1:]}")

    # 2. Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training Faces: {len(X_train)}, Testing Faces: {len(X_test)}")

    # 3. Build Convolutional Neural Network
    model = Sequential([
        Input(shape=(64, 64, 1)),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.2),
        Dense(40, activation='softmax')  # 40 distinct subjects
    ])

    # 4. Compile Model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # 5. Train Model
    model.fit(
        X_train,
        y_train,
        epochs=25,
        batch_size=32,
        verbose=0
    )

    # 6. Evaluate Model on Test Set
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Loss: {loss:.4f}")
    print(f"Recognition Accuracy: {accuracy * 100:.2f}%")

    # 7. Sample Predictions
    predictions = model.predict(X_test[:5], verbose=0).argmax(axis=1)

    print("\nSample Predictions:")
    for i in range(5):
        act_person = y_test[i] + 1
        pred_person = predictions[i] + 1
        match = (act_person == pred_person)
        print(f"Sample {i+1}: Actual Subject = Person {act_person}, Recognized as = Person {pred_person} (Match: {match})")

if __name__ == '__main__':
    main()
