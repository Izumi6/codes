# SPPU 4th Year BE Computer / IT — Laboratory Practice III (LP-3)

This repository contains fully tested, standardized, and clean implementations of all practical assignments and mini projects for **Savitribai Phule Pune University (SPPU) BE Computer Engineering & Information Technology — Lab Practice 3 (LP-3)**.

---

## 📁 Repository Structure

```
LP 3/
├── Blockchain/
│   ├── 01_02_metamask_wallet_setup.py
│   ├── 03_bank_account_smart_contract.sol
│   ├── 04_student_data_smart_contract.sol
│   ├── 05_blockchain_survey_report.py
│   └── Mini Project/
│       ├── 01_evoting_dapp.sol
│       ├── 02_transparent_charity_dapp.sol
│       └── 03_health_medical_records.sol
│
├── Machine Learning/
│   ├── 01_Uber_Fare_Prediction/
│   │   ├── 01_uber_fare_prediction.ipynb
│   │   └── uber.csv
│   ├── 02_Email_Spam_Classification/
│   │   ├── 02_email_spam_classification.ipynb
│   │   └── emails.csv
│   ├── 03_Bank_Churn_Neural_Network/
│   │   ├── 03_bank_churn_neural_network.ipynb
│   │   └── Churn_Modelling.csv
│   ├── 04_Gradient_Descent/
│   │   └── 04_gradient_descent.ipynb
│   ├── 05_KNN_Diabetes/
│   │   ├── 05_knn_diabetes.ipynb
│   │   └── diabetes.csv
│   ├── 06_KMeans_Clustering_Sales/
│   │   ├── 06_kmeans_clustering_sales.ipynb
│   │   └── sales_data_sample.csv
│   └── Mini Project/
│       ├── 01_titanic_survival_prediction.py
│       ├── 01_titanic_survival_prediction.ipynb
│       ├── titanic.csv
│       ├── 02_indian_stock_market_prediction.py
│       ├── 02_indian_stock_market_prediction.ipynb
│       ├── indian_stock_market_2000_2020.csv
│       ├── 03_signature_identification.py
│       ├── 03_signature_identification.ipynb
│       └── student_signatures_dataset.csv
│
├── Design and Analysis of Algorithms/
│   ├── 01_fibonacci_step_count.py
│   ├── 02_job_sequencing_greedy.py
│   ├── 03_fractional_knapsack_greedy.py
│   ├── 04_01_knapsack_dp_bb.py
│   ├── 05_binomial_coefficients_dp.py
│   ├── 06_eight_queens_backtracking.py
│   └── Mini Project/
│       ├── 01_matrix_multiplication_threaded.py
│       ├── 02_merge_sort_threaded.py
│       └── 03_string_matching_naive_rabin_karp.py
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation & Setup

1. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Windows Lab PC Compatibility:**
   All Python codes use standard libraries (`pandas`, `numpy`, `scikit-learn`) and require no extra compiler setup.

---

## 🔗 1. Blockchain Technology (BT) Mini Projects

| File | Mini Project Title | Description | Testing Environment |
| :--- | :--- | :--- | :--- |
| `01_evoting_dapp.sol` | **E-Voting System dApp** | Decentralized voting with admin voter verification, tamper-proof ballot, one vote per address. | Remix IDE / Remix VM |
| `02_transparent_charity_dapp.sol` | **Transparent & Genuine Charity** | Milestone-based charity funding with donor voting on fund release to beneficiaries/vendors. | Remix IDE / Remix VM |
| `03_health_medical_records.sol` | **Health & Medical Records EHR** | Patient-controlled electronic health records with doctor authorization, revocation, and IPFS hash tracking. | Remix IDE / Remix VM |

---

## 🤖 2. Machine Learning (ML) Mini Projects

| File | Mini Project Title | Algorithm / Techniques | Dataset |
| :--- | :--- | :--- | :--- |
| `01_titanic_survival_prediction.py` | **Titanic Shipwreck Survival Prediction** | Random Forest Classifier, Feature Preprocessing | `titanic.csv` |
| `02_indian_stock_market_prediction.py` | **Indian Stock Market Return & Trend Prediction (2000-2020)** | Random Forest Classifier (Ups & Downs) & Regressor (Returns) | `indian_stock_market_2000_2020.csv` |
| `03_signature_identification.py` | **Student Handwritten Signature Identification & Verification** | Biometric geometric features, Multi-class Identification & Genuine/Forgery Verification | `student_signatures_dataset.csv` |

---

## ⚡ 3. Design and Analysis of Algorithms (DAA) Mini Projects

| File | Mini Project Title | Algorithm / Techniques | Complexity / Features |
| :--- | :--- | :--- | :--- |
| `01_matrix_multiplication_threaded.py` | **Multithreaded Matrix Multiplication** | Single-threaded vs One thread per row vs One thread per cell | Time comparison across $50\times 50$ to $150\times 150$ matrices |
| `02_merge_sort_threaded.py` | **Multithreaded Merge Sort** | Sequential vs Multithreaded Merge Sort, Best & Worst case analysis | Divide & Conquer with Python `threading` |
| `03_string_matching_naive_rabin_karp.py` | **Naive vs Rabin-Karp String Matching** | Rolling Hash vs Brute-force character comparison | Detailed comparison counts & runtimes |
