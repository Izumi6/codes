"""
LP-5 Deep Learning - Practical 3
Convolutional Neural Network (CNN) for Image Classification

Problem Statement:
Use MNIST Fashion Dataset and create a classifier to classify fashion clothing
into categories.

Dataset:
Fashion MNIST (60,000 training images, 10,000 testing images, 28x28 grayscale, 10 classes)

Sample Output:
Train Images: 60000, Test Images: 10000
Image Shape: (28, 28, 1), Number of Classes: 10
Test Loss: 0.3374
Test Accuracy: 87.99%

Sample Predictions:
Sample 1: True = Ankle boot, Predicted = Ankle boot
Sample 2: True = Pullover, Predicted = Pullover
Sample 3: True = Trouser, Predicted = Trouser
Sample 4: True = Trouser, Predicted = Trouser
Sample 5: True = Shirt, Predicted = Shirt
"""

import os
import warnings
warnings.filterwarnings('ignore')

# Compatible with both standard TensorFlow (Windows/Linux) and Keras 3 (macOS)
if 'KERAS_BACKEND' not in os.environ:
    os.environ['KERAS_BACKEND'] = 'torch'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np

try:
    import keras
    from keras.datasets import fashion_mnist
    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
except ImportError:
    from tensorflow.keras.datasets import fashion_mnist
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input

def main():
    # 1. Load Dataset
    (X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

    # 2. Reshape and Normalize (scale pixel values to [0, 1])
    X_train = np.expand_dims(X_train.astype('float32') / 255.0, -1)
    X_test = np.expand_dims(X_test.astype('float32') / 255.0, -1)

    print(f"Train Images: {len(X_train)}, Test Images: {len(X_test)}")
    print(f"Image Shape: {X_train.shape[1:]}, Number of Classes: 10")

    # Class names for Fashion MNIST
    class_names = [
        'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
        'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
    ]

    # 3. Build Convolutional Neural Network
    model = Sequential([
        Input(shape=(28, 28, 1)),
        Conv2D(32, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
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
        epochs=4,
        batch_size=128,
        verbose=0
    )

    # 6. Evaluate Model on Test Set
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Loss: {loss:.4f}")
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

    # 7. Sample Predictions
    predictions = model.predict(X_test[:5], verbose=0).argmax(axis=1)

    print("\nSample Predictions:")
    for i in range(5):
        true_label = class_names[y_test[i]]
        pred_label = class_names[predictions[i]]
        print(f"Sample {i+1}: True = {true_label}, Predicted = {pred_label}")

    # 8. Generate and Save Prediction Image Grid
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(13, 3.2))
        for i in range(5):
            plt.subplot(1, 5, i + 1)
            plt.imshow(X_test[i].squeeze(), cmap='gray')
            true_label = class_names[y_test[i]]
            pred_label = class_names[predictions[i]]
            color = 'green' if true_label == pred_label else 'red'
            plt.title(f"Pred: {pred_label}\nTrue: {true_label}", color=color, fontsize=10, fontweight='bold')
            plt.axis('off')

        plt.tight_layout()
        plot_path = os.path.join(os.path.dirname(__file__), 'fashion_mnist_predictions.png')
        plt.savefig(plot_path, dpi=120)
        print(f"Plot saved as 'fashion_mnist_predictions.png'")
        plt.close()
    except Exception as e:
        pass

if __name__ == '__main__':
    main()

