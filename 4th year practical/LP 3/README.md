# SPPU 4th Year BE Computer / IT — Laboratory Practice III (LP-3)

This repository contains fully tested, standardized, and clean implementations of all practical assignments and mini projects for **Savitribai Phule Pune University (SPPU) BE Computer Engineering & Information Technology — Lab Practice 3 (LP-3)**.

---

## 📁 Repository Structure

```
LP 3/
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
│       ├── 01_titanic_survival_prediction.ipynb
│       └── titanic.csv
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
├── Blockchain/
│   ├── 01_02_metamask_wallet_setup.py
│   ├── 03_bank_account_smart_contract.sol
│   ├── 04_student_data_smart_contract.sol
│   ├── 05_blockchain_survey_report.py
│   └── Mini Project/
│       └── 01_evoting_dapp.sol
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd "4th year practical/LP 3"
   ```

2. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🤖 1. Machine Learning (ML) Practicals

All Machine Learning assignments are provided as clean, standalone **Jupyter Notebooks (`.ipynb`)**. They run seamlessly in **VS Code** (with the Jupyter extension), **JupyterLab / Notebook**, and **Google Colab**.

| Assignment | Title | Algorithm / Technique | Dataset |
| :--- | :--- | :--- | :--- |
| **01** | Uber Fare Prediction | Linear Regression vs Random Forest, Haversine Distance | `uber.csv` |
| **02** | Email Spam Classification | K-Nearest Neighbors (KNN) & Support Vector Machine (SVM) | `emails.csv` |
| **03** | Bank Customer Churn | Artificial Neural Network (ANN) / Deep Learning | `Churn_Modelling.csv` |
| **04** | Gradient Descent | Gradient Descent Optimization from Scratch on $y=(x+3)^2$ | None (Synthetic) |
| **05** | Diabetes Prediction | KNN with Hyperparameter Tuning (K vs Error Rate) | `diabetes.csv` |
| **06** | Sales Customer Segmentation | K-Means Clustering & Elbow Method (WCSS, Silhouette) | `sales_data_sample.csv` |
| **Mini Project** | Titanic Survival Prediction | Random Forest Classification with Feature Importance | `titanic.csv` |

### How to Run:
- **In VS Code**: Simply click on any `.ipynb` file in the sidebar and click **"Run All"** (or use `Shift + Enter` to step through cells).
- **In Jupyter Notebook**:
  ```bash
  jupyter notebook "LP 3/Machine Learning/01_Uber_Fare_Prediction/01_uber_fare_prediction.ipynb"
  ```

---

## ⚡ 2. Design and Analysis of Algorithms (DAA) Practicals

All DAA practicals are implemented in **pure, standard Python** without any third-party dependencies.

> 💡 **User-Friendly Demo Mode**: Each script accepts interactive input from the keyboard, but also supports pressing **Enter** to instantly run standard textbook sample inputs for quick lab viva and testing without crashing!

| Assignment | Title | Approach / Strategy | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **01** | Fibonacci Step Count | Recursive vs Iterative vs Memoized DP | $O(2^n)$ vs $O(n)$ | $O(n)$ vs $O(1)$ |
| **02** | Job Sequencing | Greedy Method (sorted by profit) | $O(n^2)$ | $O(n)$ |
| **03** | Fractional Knapsack | Greedy Method (sorted by value/weight) | $O(n \log n)$ | $O(n)$ |
| **04** | 0/1 Knapsack | Dynamic Programming & Branch and Bound | $O(n \cdot W)$ | $O(n \cdot W)$ |
| **05** | Binomial Coefficients | Pascal's Triangle DP Matrix | $O(n \cdot k)$ | $O(n \cdot k)$ |
| **06** | 8-Queens Problem | Backtracking (with 1st Queen pre-placed) | $O(n!)$ | $O(n)$ |
| **Mini 01** | Multithreaded Matrix Multiplication | Multithreading benchmark vs Single-threaded | Benchmark | Benchmark |
| **Mini 02** | Multithreaded Merge Sort | Parallel divide-and-conquer using Threads | $O(n \log n)$ | $O(n)$ |
| **Mini 03** | String Pattern Matching | Naive String Search vs Rabin-Karp Rolling Hash | $O(n \cdot m)$ vs $O(n+m)$ | $O(1)$ |

### How to Run:
```bash
python3 "Design and Analysis of Algorithms/01_fibonacci_step_count.py"
```

---

## ⛓️ 3. Blockchain Technology Practicals

All Solidity contracts have been validated with the Solidity compiler `0.8.x` and are ready for deployment in **Remix IDE** or **MetaMask Testnets**.

| Assignment | Title | Technology / Implementation | Deployment Target |
| :--- | :--- | :--- | :--- |
| **01 & 02** | MetaMask Setup & Ether Spending | Interactive Guide & Gas Cost Calculator | Browser MetaMask Extension |
| **03** | Bank Account Smart Contract | Solidity (`deposit`, `withdraw`, `getBalance`, Events) | Remix IDE / Sepolia Testnet |
| **04** | Student Data Smart Contract | Solidity (Struct, Dynamic Array, Fallback function) | Remix IDE / Sepolia Testnet |
| **05** | Blockchain Survey Report | Multi-domain comparative survey (DeFi, Healthcare, etc.) | Terminal / Python Report |
| **Mini Project** | Decentralized E-Voting DApp | Decentralized Voting, Candidate Registry, Ballot counting | Remix IDE / Sepolia Testnet |

### How to Test Smart Contracts in Remix IDE:
1. Open [Remix Ethereum IDE](https://remix.ethereum.org/).
2. Create a new file (e.g. `BankAccount.sol`) and paste the contract code.
3. In **Solidity Compiler** tab, select compiler version `0.8.20` or higher and click **Compile**.
4. In **Deploy & Run Transactions** tab, select environment:
   - `Remix VM` (for instant local simulated blockchain testing)
   - `Injected Provider - MetaMask` (for Sepolia testnet testing)
5. Click **Deploy** and interact with the contract methods directly in the Remix UI!

---

## 📦 GitHub Upload Guidelines

A `.gitignore` file is included in this repository to prevent uploading:
- `archive (2).zip` (273 MB) — Exceeds GitHub's 100 MB hard limit.
- `Machine Learning/Data/` (1.4 GB) — Unused Indian stock market CSV archives.
- System cache and temporary files (`.DS_Store`, `__pycache__`, `.ipynb_checkpoints`).

To push this repository to GitHub:
```bash
git init
git add .
git commit -m "Initial commit of SPPU 4th Year LP-3 Practicals"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```
