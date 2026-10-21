# Laboratory Practice 5 (LP-5): Deep Learning

SPPU BE Computer Engineering (2019 Pattern)

This repository contains workable, clean, and simple implementations for all Deep Learning laboratory assignments with executable Python scripts (`.py`), pre-computed Jupyter Notebooks (`.ipynb`), and local datasets.

---

## Practical Overview

| No. | Practical Name | Technique | Dataset | Script | Notebook | Visual Graph |
|:---:|:---|:---|:---|:---|:---|:---|
| **1** | Boston Housing Price Prediction | Deep Neural Network (DNN) Regression | Boston Housing (`BostonHousing.csv`) | [01_boston_housing_regression.py](01_Boston_Housing_Price_Prediction/01_boston_housing_regression.py) | [01_boston_housing_regression.ipynb](01_Boston_Housing_Price_Prediction/01_boston_housing_regression.ipynb) | [Loss & Predictions Plot](01_Boston_Housing_Price_Prediction/boston_housing_prediction.png) |
| **2** | Movie Review Sentiment Classification | Deep Neural Network (DNN) Binary Classification | IMDB Movie Reviews (Top 10,000 words) | [02_imdb_movie_review_classification.py](02_IMDB_Movie_Review_Classification/02_imdb_movie_review_classification.py) | [02_imdb_movie_review_classification.ipynb](02_IMDB_Movie_Review_Classification/02_imdb_movie_review_classification.ipynb) | [Training Metrics Plot](02_IMDB_Movie_Review_Classification/imdb_training_metrics.png) |
| **3** | Fashion Clothing Classification | Convolutional Neural Network (CNN) | Fashion MNIST (10 Clothing Categories) | [03_fashion_mnist_cnn.py](03_Fashion_MNIST_CNN/03_fashion_mnist_cnn.py) | [03_fashion_mnist_cnn.ipynb](03_Fashion_MNIST_CNN/03_fashion_mnist_cnn.ipynb) | — |
| **4** | Google Stock Price Forecasting | Recurrent Neural Network (RNN / SimpleRNN) | Google Stock Price (`Train` & `Test` CSV) | [04_google_stock_price_rnn.py](04_Google_Stock_Price_RNN/04_google_stock_price_rnn.py) | [04_google_stock_price_rnn.ipynb](04_Google_Stock_Price_RNN/04_google_stock_price_rnn.ipynb) | [Stock Price Forecast Plot](04_Google_Stock_Price_RNN/google_stock_price_prediction.png) |
| **5** | Human Face Recognition | Convolutional Neural Network (CNN) | Olivetti Faces (400 images, 40 subjects) | [05_human_face_recognition.py](mini%20projects%20of%20deep%20learning/05_Human_Face_Recognition/05_human_face_recognition.py) | [05_human_face_recognition.ipynb](mini%20projects%20of%20deep%20learning/05_Human_Face_Recognition/05_human_face_recognition.ipynb) | — |
| **6** | Gender and Age Detection | Multi-Output Deep Neural Network | Facial Biometrics (`facial_biometric_data.csv`) | [06_gender_and_age_detection.py](mini%20projects%20of%20deep%20learning/06_Gender_and_Age_Detection/06_gender_and_age_detection.py) | [06_gender_and_age_detection.ipynb](mini%20projects%20of%20deep%20learning/06_Gender_and_Age_Detection/06_gender_and_age_detection.ipynb) | — |
| **7** | Colorizing Old B&W Images | Convolutional Autoencoder (Encoder-Decoder) | Natural Scenery Patches (B&W $\to$ RGB) | [07_colorizing_bw_images.py](mini%20projects%20of%20deep%20learning/07_Colorizing_BW_Images/07_colorizing_bw_images.py) | [07_colorizing_bw_images.ipynb](mini%20projects%20of%20deep%20learning/07_Colorizing_BW_Images/07_colorizing_bw_images.ipynb) | [Colorization Comparison](mini%20projects%20of%20deep%20learning/07_Colorizing_BW_Images/colorization_comparison.png) |

---

See [mini projects of deep learning/README.md](mini%20projects%20of%20deep%20learning/README.md) for detailed documentation on the mini projects.

## Detailed Practical Descriptions

### Practical 1: Linear Regression using Deep Neural Network
- **Problem Statement**: Implement Boston housing price prediction problem by Linear regression using Deep Neural network. Use Boston House price prediction dataset.
- **Architecture**: Sequential DNN with input size 13, two hidden layers (`Dense(64, relu)`, `Dense(32, relu)`), and linear output layer (`Dense(1)`).
- **Key Metrics**: MSE, RMSE, MAE, and $R^2$ Score.
- **Folder**: `01_Boston_Housing_Price_Prediction/`

### Practical 2: Binary Classification using Deep Neural Network
- **Problem Statement**: Classify movie reviews into "positive" and "negative" reviews based on text content using IMDB dataset.
- **Architecture**: Multi-hot binary word vector encoding (10,000 vocab), two hidden layers (`Dense(16, relu)`, `Dense(16, relu)`), and sigmoid output layer (`Dense(1)`).
- **Key Metrics**: Binary Cross-Entropy Loss, Accuracy (~88%).
- **Folder**: `02_IMDB_Movie_Review_Classification/`

### Practical 3: Convolutional Neural Network (CNN)
- **Problem Statement**: Use MNIST Fashion Dataset and create a classifier to classify fashion clothing into categories.
- **Architecture**: 2D Convolution layers (`Conv2D(32)`, `Conv2D(64)`), MaxPooling layers (`2x2`), Flatten, Dense hidden layer, and 10-way Softmax output layer.
- **Key Metrics**: Sparse Categorical Cross-Entropy, Test Accuracy (~90%).
- **Folder**: `03_Fashion_MNIST_CNN/`

### Practical 4: Recurrent Neural Network (RNN)
- **Problem Statement**: Use Google stock prices dataset and design a time series analysis and prediction system using RNN.
- **Architecture**: 60-timestep sliding window, 2 stacked `SimpleRNN(units=50)` with `Dropout(0.2)`, and single linear output `Dense(1)`.
- **Key Metrics**: RMSE, MAE, and Actual vs Predicted stock price table.
- **Folder**: `04_Google_Stock_Price_RNN/`

---

## Setup & Running Instructions

### Requirements
Ensure you have Python 3.8+ installed along with standard machine learning libraries:
```bash
pip install numpy pandas scikit-learn matplotlib
# Install TensorFlow (Windows/Linux) or Keras with PyTorch/TensorFlow backend
pip install tensorflow
# OR for Keras 3:
pip install keras torch
```

### Running Scripts
Navigate to each practical's directory and execute the python script:
```bash
# Practical 1
cd "01_Boston_Housing_Price_Prediction"
python 01_boston_housing_regression.py

# Practical 2
cd "../02_IMDB_Movie_Review_Classification"
python 02_imdb_movie_review_classification.py

# Practical 3
cd "../03_Fashion_MNIST_CNN"
python 03_fashion_mnist_cnn.py

# Practical 4
cd "../04_Google_Stock_Price_RNN"
python 04_google_stock_price_rnn.py
```

### Viewing Jupyter Notebooks
Each directory includes a pre-run Jupyter Notebook (`.ipynb`) with complete outputs rendered so you can view them directly on GitHub or run in Jupyter Lab / Notebook / Google Colab.
