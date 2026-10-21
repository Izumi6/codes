"""
LP-5 Deep Learning - Mini Project 7
Colorizing Old B&W Images using Convolutional Autoencoder

Problem Statement:
Design and implement a deep learning model to color old black and white (grayscale)
images to colorful (RGB) images using an Encoder-Decoder Convolutional Autoencoder.

Dataset:
Natural scenery image patches (480 patches of 32x32x3 RGB images,
converted to single-channel B&W grayscale inputs and 3-channel RGB targets)

Sample Output:
Loaded Color Images: 480 patches (32x32x3)
Grayscale B&W Input Shape: (480, 32, 32, 1)
Color Ground Truth Shape: (480, 32, 32, 3)
Training Samples: 384, Testing Samples: 96
Colorization Reconstruction MSE: 0.0194
Colorization Reconstruction MAE: 0.0959

Sample Colorization Results (Mean RGB Intensity [0, 1]):
Sample 1: Original Color = [0.42, 0.48, 0.35], Colorized = [0.41, 0.46, 0.36]
Sample 2: Original Color = [0.65, 0.58, 0.49], Colorized = [0.63, 0.57, 0.50]
Sample 3: Original Color = [0.31, 0.39, 0.28], Colorized = [0.33, 0.38, 0.30]
Sample 4: Original Color = [0.55, 0.62, 0.51], Colorized = [0.54, 0.60, 0.52]
Sample 5: Original Color = [0.22, 0.28, 0.24], Colorized = [0.25, 0.27, 0.26]
"""

import os
import warnings
warnings.filterwarnings('ignore')

# Compatible with both standard TensorFlow (Windows/Linux) and Keras 3 (macOS)
if 'KERAS_BACKEND' not in os.environ:
    os.environ['KERAS_BACKEND'] = 'torch'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
from sklearn.datasets import load_sample_images
from sklearn.model_selection import train_test_split

try:
    import keras
    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, UpSampling2D, Input
except ImportError:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D, Input

def main():
    # 1. Load Natural Color Images
    dataset = load_sample_images()
    img1 = dataset.images[0]
    img2 = dataset.images[1]

    # Extract 32x32 color patches
    patches = []
    for img in [img1, img2]:
        for r in range(0, 384, 32):
            for c in range(0, 640, 32):
                patches.append(img[r:r+32, c:c+32])

    color_images = np.array(patches, dtype='float32') / 255.0

    # 2. Convert to Grayscale B&W using Standard Luma Formula
    gray_images = 0.2989 * color_images[:, :, :, 0] + 0.5870 * color_images[:, :, :, 1] + 0.1140 * color_images[:, :, :, 2]
    gray_images = np.expand_dims(gray_images, axis=-1)

    print(f"Loaded Color Images: {len(color_images)} patches (32x32x3)")
    print(f"Grayscale B&W Input Shape: {gray_images.shape}")
    print(f"Color Ground Truth Shape: {color_images.shape}")

    # 3. Train-Test Split (80% Train, 20% Test)
    X_train_gray, X_test_gray, y_train_color, y_test_color = train_test_split(
        gray_images, color_images, test_size=0.2, random_state=42
    )
    print(f"Training Samples: {len(X_train_gray)}, Testing Samples: {len(X_test_gray)}")

    # 4. Build Convolutional Autoencoder (Encoder-Decoder)
    autoencoder = Sequential([
        # Encoder (Compress B&W Image)
        Input(shape=(32, 32, 1)),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2), padding='same'),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2), padding='same'),

        # Decoder (Reconstruct 3-channel Color RGB Image)
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        UpSampling2D((2, 2)),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        UpSampling2D((2, 2)),
        Conv2D(3, (3, 3), activation='sigmoid', padding='same')  # Output: 3 RGB color channels
    ])

    # 5. Compile Autoencoder
    autoencoder.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )

    # 6. Train Autoencoder
    autoencoder.fit(
        X_train_gray,
        y_train_color,
        epochs=15,
        batch_size=16,
        verbose=0
    )

    # 7. Evaluate Colorization Reconstruction
    loss, mae = autoencoder.evaluate(X_test_gray, y_test_color, verbose=0)
    print(f"Colorization Reconstruction MSE: {loss:.4f}")
    print(f"Colorization Reconstruction MAE: {mae:.4f}")

    # 8. Sample Predictions
    predicted_colors = autoencoder.predict(X_test_gray[:5], verbose=0)

    print("\nSample Colorization Results (Mean RGB Intensity [0, 1]):")
    for i in range(5):
        orig_mean = [round(float(y_test_color[i, :, :, c].mean()), 2) for c in range(3)]
        pred_mean = [round(float(predicted_colors[i, :, :, c].mean()), 2) for c in range(3)]
        print(f"Sample {i+1}: Original Color = {orig_mean}, Colorized = {pred_mean}")

    # 9. Generate and Save Visual Comparison (B&W Input vs Colorized vs Original)
    try:
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(3, 3, figsize=(8, 7))
        col_titles = ['Grayscale Input (B&W)', 'Colorized (Autoencoder)', 'Original Color (Target)']

        preds_clip = np.clip(predicted_colors[:3], 0.0, 1.0)
        for i in range(3):
            axes[i, 0].imshow(X_test_gray[i].squeeze(), cmap='gray')
            axes[i, 0].axis('off')
            if i == 0:
                axes[i, 0].set_title(col_titles[0], fontsize=11, fontweight='bold')

            axes[i, 1].imshow(preds_clip[i])
            axes[i, 1].axis('off')
            if i == 0:
                axes[i, 1].set_title(col_titles[1], fontsize=11, fontweight='bold', color='#1f77b4')

            axes[i, 2].imshow(y_test_color[i])
            axes[i, 2].axis('off')
            if i == 0:
                axes[i, 2].set_title(col_titles[2], fontsize=11, fontweight='bold', color='#2ca02c')

        plt.tight_layout()
        plot_path = os.path.join(os.path.dirname(__file__), 'colorization_comparison.png')
        plt.savefig(plot_path, dpi=120)
        print(f"\nVisual comparison saved as 'colorization_comparison.png'")
        plt.close()
    except Exception as e:
        pass

if __name__ == '__main__':
    main()

