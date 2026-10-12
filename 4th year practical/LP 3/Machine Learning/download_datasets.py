"""
Dataset Downloader for ML Practicals
=====================================
Run this script to download all required Kaggle datasets.

You'll need your Kaggle credentials (username & API key).
Get them from: https://www.kaggle.com/settings → API → Create New Token

Usage: python3 download_datasets.py
"""

import os
import subprocess
import sys

DATASETS = {
    "01_Uber_Fare_Prediction": {
        "kaggle_id": "yasserh/uber-fares-dataset",
        "desc": "Uber Fares Dataset"
    },
    "02_Email_Spam_Classification": {
        "kaggle_id": "balaka18/email-spam-classification-dataset-csv",
        "desc": "Email Spam Classification"
    },
    "06_KMeans_Clustering_Sales": {
        "kaggle_id": "kyanyoga/sample-sales-data",
        "desc": "Sample Sales Data"
    }
}

# Datasets already downloaded or not from Kaggle
SKIP = ["03_Bank_Churn_Neural_Network", "04_Gradient_Descent", "05_KNN_Diabetes"]


def main():
    print("=" * 60)
    print("   ML PRACTICALS — DATASET DOWNLOADER")
    print("=" * 60)

    # Check kaggle credentials
    kaggle_dir = os.path.expanduser("~/.kaggle")
    kaggle_json = os.path.join(kaggle_dir, "kaggle.json")

    if not os.path.exists(kaggle_json):
        print("\n  Kaggle API key not found!")
        print("  Steps to set up:")
        print("  1. Go to https://www.kaggle.com/settings")
        print("  2. Scroll to 'API' section → Click 'Create New Token'")
        print("  3. A file 'kaggle.json' will be downloaded")
        print(f"  4. Move it to: {kaggle_dir}/")
        print(f"     mkdir -p {kaggle_dir}")
        print(f"     mv ~/Downloads/kaggle.json {kaggle_json}")
        print(f"     chmod 600 {kaggle_json}")

        # Ask for manual input
        print("\n  Or enter your credentials now:")
        username = input("  Kaggle Username: ").strip()
        api_key = input("  Kaggle API Key : ").strip()

        if username and api_key:
            os.makedirs(kaggle_dir, exist_ok=True)
            with open(kaggle_json, 'w') as f:
                f.write(f'{{"username":"{username}","key":"{api_key}"}}')
            os.chmod(kaggle_json, 0o600)
            print("  ✓ Credentials saved!")
        else:
            print("  Skipping... Please set up credentials and try again.")
            return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    kaggle_bin = os.path.expanduser("~/Library/Python/3.9/bin/kaggle")

    for folder, info in DATASETS.items():
        target_dir = os.path.join(base_dir, folder)
        print(f"\n  Downloading: {info['desc']}...")
        print(f"  Target: {target_dir}")

        cmd = [kaggle_bin, "datasets", "download", "-d", info["kaggle_id"],
               "--unzip", "-p", target_dir]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print(f"  ✓ Downloaded successfully!")
            else:
                print(f"  ✗ Error: {result.stderr.strip()}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")

    # List all files
    print(f"\n{'═' * 60}")
    print("  DOWNLOAD SUMMARY")
    print(f"{'═' * 60}")
    for folder in sorted(os.listdir(base_dir)):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path) and not folder.startswith('.'):
            files = os.listdir(folder_path)
            csv_files = [f for f in files if f.endswith('.csv')]
            status = "✓" if csv_files else "✗"
            print(f"  {status} {folder}/")
            for f in csv_files:
                size = os.path.getsize(os.path.join(folder_path, f))
                print(f"      {f} ({size/1024:.0f} KB)")

    print(f"{'═' * 60}\n")


if __name__ == "__main__":
    main()
