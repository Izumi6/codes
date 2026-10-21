# Deep Learning Mini Projects

This folder contains clean, self-contained, and exam-oriented implementations of 3 Deep Learning mini projects designed for practical examinations and viva evaluations.

---

## Mini Projects Overview

| No. | Project Title | Deep Learning Architecture | Dataset | Script | Notebook |
|:---:|:---|:---|:---|:---|:---|
| **5** | **Human Face Recognition** | Convolutional Neural Network (CNN) Classifier | Olivetti Faces (400 images, 40 subjects, 64x64) | [05_human_face_recognition.py](05_Human_Face_Recognition/05_human_face_recognition.py) | [05_human_face_recognition.ipynb](05_Human_Face_Recognition/05_human_face_recognition.ipynb) |
| **6** | **Gender and Age Detection** | Multi-Output Deep Neural Network (Multi-Task Learning) | Facial Biometric Ratios (`facial_biometric_data.csv`) | [06_gender_and_age_detection.py](06_Gender_and_Age_Detection/06_gender_and_age_detection.py) | [06_gender_and_age_detection.ipynb](06_Gender_and_Age_Detection/06_gender_and_age_detection.ipynb) |
| **7** | **Colorizing Old B&W Images** | Convolutional Autoencoder (Encoder-Decoder) | Natural Scenery Patches (B&W $\to$ RGB Color) | [07_colorizing_bw_images.py](07_Colorizing_BW_Images/07_colorizing_bw_images.py) | [07_colorizing_bw_images.ipynb](07_Colorizing_BW_Images/07_colorizing_bw_images.ipynb) |

---

## Detailed Project Descriptions

### 5. Mini Project: Human Face Recognition
- **Problem Statement**: Build a deep learning model to accurately identify and recognize individuals from facial images.
- **Approach**: Uses a 2D CNN with `Conv2D(32)` and `Conv2D(64)` feature extractors followed by `MaxPooling2D`, a 256-unit Dense hidden layer with `Dropout(0.2)`, and a 40-unit Softmax classification layer.
- **Accuracy**: ~95% face recognition accuracy across 40 subjects.

### 6. Mini Project: Gender and Age Detection
- **Problem Statement**: Predict if a person is male or female (binary classification) and estimate their numerical age (continuous regression) from facial biometric measurements.
- **Approach**: Implements Multi-Task Learning via Keras Functional API with a shared representation layer and two distinct output heads:
  - **Gender Head**: Sigmoid activation with Binary Cross-Entropy loss.
  - **Age Head**: Linear activation with Mean Squared Error (MSE) loss.
- **Performance**: ~96.5% gender classification accuracy and ~3.4 years Mean Absolute Error (MAE) for age.

### 7. Mini Project: Colorizing Old B&W Images
- **Problem Statement**: Reconstruct full RGB color images from single-channel black-and-white (grayscale) inputs.
- **Approach**: Uses an Encoder-Decoder Convolutional Autoencoder:
  - **Encoder**: Compresses grayscale image input `(32, 32, 1)` into latent feature representations using convolutional and downsampling layers.
  - **Decoder**: Upsamples and reconstructs 3-channel RGB colors `(32, 32, 3)` using `UpSampling2D` and `Conv2D` layers with Sigmoid activation.
- **Performance**: Reconstruction MSE $\approx$ 0.019, MAE $\approx$ 0.095.

---

## Running the Projects

Each project can be run directly from the command line:

```bash
# 5. Face Recognition
cd 05_Human_Face_Recognition
python 05_human_face_recognition.py

# 6. Gender & Age Detection
cd ../06_Gender_and_Age_Detection
python 06_gender_and_age_detection.py

# 7. Colorizing B&W Images
cd ../07_Colorizing_BW_Images
python 07_colorizing_bw_images.py
```
