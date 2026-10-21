"""
LP-5 Deep Learning - Practical 2
Binary Classification using Deep Neural Network (DNN)

Problem Statement:
Classify movie reviews into positive reviews and negative reviews,
just based on the text content of the reviews. Use IMDB dataset.

Dataset:
IMDB Movie Reviews Dataset (50,000 labeled reviews: 25,000 train, 25,000 test;
vocabulary limited to top 10,000 most frequent words)

Sample Output:
Training Samples: 25000, Testing Samples: 25000
Vocabulary Size: 10000
Test Loss: 0.3101
Test Accuracy: 87.91%

Sample Predictions:
Review 1: Actual = Negative, Predicted = Negative (Confidence: 0.16)
Review 2: Actual = Positive, Predicted = Positive (Confidence: 1.00)
Review 3: Actual = Positive, Predicted = Positive (Confidence: 0.74)
Review 4: Actual = Negative, Predicted = Positive (Confidence: 0.83)
Review 5: Actual = Positive, Predicted = Positive (Confidence: 0.97)
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
    from keras.datasets import imdb
    from keras.models import Sequential
    from keras.layers import Dense, Input
except ImportError:
    from tensorflow.keras.datasets import imdb
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Input

def vectorize_sequences(sequences, dimension=10000):
    """Encodes list of word indices into multi-hot binary vectors."""
    results = np.zeros((len(sequences), dimension), dtype='float32')
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.0
    return results

def main():
    # 1. Load IMDB Dataset (Top 10,000 most frequent words)
    (train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

    # 2. Vectorize Data
    X_train = vectorize_sequences(train_data, dimension=10000)
    X_test = vectorize_sequences(test_data, dimension=10000)
    y_train = np.asarray(train_labels, dtype='float32')
    y_test = np.asarray(test_labels, dtype='float32')

    print(f"Training Samples: {len(X_train)}, Testing Samples: {len(X_test)}")
    print("Vocabulary Size: 10000")

    # 3. Build Deep Neural Network Architecture
    model = Sequential([
        Input(shape=(10000,)),
        Dense(16, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')  # Probability of positive review
    ])

    # 4. Compile Model
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    # 5. Train Model
    model.fit(
        X_train,
        y_train,
        epochs=4,
        batch_size=512,
        verbose=0
    )

    # 6. Evaluate Model on Test Set
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Loss: {loss:.4f}")
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

    # 7. Sample Predictions
    predictions = model.predict(X_test[:5], verbose=0).flatten()

    print("\nSample Predictions:")
    for i in range(5):
        actual = "Positive" if y_test[i] == 1 else "Negative"
        predicted = "Positive" if predictions[i] >= 0.5 else "Negative"
        conf = predictions[i] if predicted == "Positive" else (1 - predictions[i])
        print(f"Review {i+1}: Actual = {actual}, Predicted = {predicted} (Confidence: {conf:.2f})")

    # 8. Generate and Save Plot
    try:
        import matplotlib.pyplot as plt
        epochs = range(1, len(history.history['loss']) + 1)

        plt.figure(figsize=(12, 4.5))

        plt.subplot(1, 2, 1)
        plt.plot(epochs, history.history['loss'], 'o-', color='#d62728', linewidth=2, label='Training Loss')
        plt.title('Training Loss over Epochs')
        plt.xlabel('Epochs')
        plt.ylabel('Loss (Binary Crossentropy)')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(epochs, [acc * 100 for acc in history.history['accuracy']], 's-', color='#1f77b4', linewidth=2, label='Training Accuracy')
        plt.title('Training Accuracy over Epochs')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy (%)')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()

        plt.tight_layout()
        plot_path = os.path.join(os.path.dirname(__file__), 'imdb_training_metrics.png')
        plt.savefig(plot_path, dpi=120)
        print(f"Plot saved as 'imdb_training_metrics.png'")
        plt.close()
    except Exception as e:
        pass

if __name__ == '__main__':
    main()

