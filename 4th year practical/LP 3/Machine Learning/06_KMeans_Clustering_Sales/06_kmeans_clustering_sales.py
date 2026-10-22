"""
================================================================================
  Program 6: K-Means Clustering on Sales Data
  Course: Machine Learning

  Problem Statement:
    Implement K-Means clustering on sales_data_sample.csv dataset.
    Determine the optimal number of clusters using the Elbow Method.

  Steps:
    1. Load the sales dataset.
    2. Select numerical features and handle missing values.
    3. Scale features using StandardScaler.
    4. Apply the Elbow Method to find the optimal number of clusters (K).
    5. Train K-Means with optimal K and assign clusters.
    6. Compute and display cluster centroids.
    7. Evaluate clustering performance using Silhouette Score and Inertia.

  Dataset: https://www.kaggle.com/datasets/kyanyoga/sample-sales-data
           Download 'sales_data_sample.csv' and place it in the same directory.

  Requirements: pip install pandas numpy scikit-learn matplotlib seaborn
================================================================================
"""

import os
import warnings
from typing import Any

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def main() -> None:
    print("=" * 65)
    print("   K-MEANS CLUSTERING ON SALES DATA")
    print("=" * 65)

    # ── Step 1: Load Dataset ────────────────────────────────────────────
    print("\n[Step 1] Loading Dataset...")
    csv_path = "sales_data_sample.csv" if os.path.exists("sales_data_sample.csv") else os.path.join(os.path.dirname(os.path.abspath(__file__)), "sales_data_sample.csv")
    df = pd.read_csv(csv_path, encoding='latin1')
    print(f"Dataset Shape: {df.shape}")
    print("\nFirst 5 rows:")
    preview_cols: Any = ['ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP']
    print(df[preview_cols].head())

    # ── Step 2: Select Features and Clean Data ──────────────────────────
    print(f"\n{'─' * 65}")
    print("[Step 2] Selecting Numerical Features...")
    features = ['QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP']
    df_clean = df[features].dropna().copy()
    print(f"Selected Features: {features}")
    print(f"Cleaned Samples  : {len(df_clean)}")
    print("\nFeature Summary Statistics:")
    print(df_clean.describe().round(2))

    # ── Step 3: Feature Scaling ─────────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("[Step 3] Scaling Features with StandardScaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean)
    print("✓ Features scaled successfully.")

    # ── Step 4: Elbow Method to Find Optimal K ──────────────────────────
    print(f"\n{'─' * 65}")
    print("[Step 4] Computing Elbow Method (WCSS for K = 1 to 10)...")
    wcss = []
    k_range = range(1, 11)
    n_init_val: Any = 10

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=n_init_val)
        kmeans.fit(X_scaled)
        wcss.append(kmeans.inertia_)
        print(f"  K = {k:>2}  |  WCSS (Inertia) = {kmeans.inertia_:>12.2f}")

    # Plot Elbow Curve
    plt.figure(figsize=(8, 4.5))
    plt.plot(k_range, wcss, 'bo-', linewidth=2, markersize=7)
    plt.title('Elbow Method For Optimal K', fontsize=12)
    plt.xlabel('Number of Clusters (K)', fontsize=11)
    plt.ylabel('WCSS (Inertia)', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('elbow_method_plot.png', dpi=100)
    plt.close()
    print("\n✓ Elbow plot saved as 'elbow_method_plot.png'.")
    print("  Optimal K observed from elbow bend = 3")

    # ── Step 5: Fit K-Means with Optimal K = 3 ──────────────────────────
    print(f"\n{'─' * 65}")
    optimal_k = 3
    print(f"[Step 5] Training K-Means with Optimal K = {optimal_k}...")
    kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=n_init_val)
    clusters: Any = kmeans_final.fit_predict(X_scaled)
    df_clean['Cluster'] = clusters

    print("\nCustomer Counts per Cluster:")
    cluster_series: Any = pd.Series(clusters).value_counts().sort_index()
    for cluster_id, count in cluster_series.items():
        percentage = (count / len(df_clean)) * 100
        print(f"  Cluster {cluster_id}: {count:>5} customers ({percentage:.2f}%)")

    # ── Step 6: Cluster Centroid Profiles ───────────────────────────────
    print(f"\n{'─' * 65}")
    print("[Step 6] Cluster Centroids (Original Feature Scale):")
    centroids: Any = scaler.inverse_transform(kmeans_final.cluster_centers_)
    col_names: Any = features
    row_names: Any = [f"Cluster {i}" for i in range(optimal_k)]
    centroids_df = pd.DataFrame(
        data=centroids,
        columns=pd.Index(col_names),
        index=pd.Index(row_names)
    )
    print(centroids_df.round(2))

    # Scatter Plot
    plt.figure(figsize=(8.5, 5))
    scatter = plt.scatter(
        df_clean['SALES'],
        df_clean['QUANTITYORDERED'],
        c=df_clean['Cluster'],
        cmap='viridis',
        alpha=0.6,
        edgecolors='k',
        linewidth=0.5
    )
    plt.colorbar(scatter, label='Cluster ID')
    plt.title(f'K-Means Customer Segmentation (K={optimal_k})', fontsize=12)
    plt.xlabel('Sales Amount', fontsize=11)
    plt.ylabel('Quantity Ordered', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('kmeans_clusters_plot.png', dpi=100)
    plt.close()
    print("\n✓ Cluster visualization saved as 'kmeans_clusters_plot.png'.")

    # ── Step 7: Final Evaluation Metrics ────────────────────────────────
    sil_score = silhouette_score(X_scaled, clusters)
    print(f"\n{'═' * 65}")
    print("  CLUSTERING PERFORMANCE METRICS")
    print(f"{'═' * 65}")
    print(f"  Optimal Number of Clusters (K) : {optimal_k}")
    print(f"  Final WCSS (Inertia)          : {kmeans_final.inertia_:.2f}")
    print(f"  Silhouette Score              : {sil_score:.4f}")
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

=================================================================
   K-MEANS CLUSTERING ON SALES DATA
=================================================================

[Step 1] Loading Dataset...
Dataset Shape: (2823, 25)

First 5 rows:
   ORDERNUMBER  QUANTITYORDERED  PRICEEACH    SALES  MSRP
0        10107               30      95.70  2871.00    95
1        10121               34      81.35  2765.90    95
2        10134               41      94.74  3884.34    95
3        10145               45      83.26  3746.70    95
4        10159               49     100.00  5205.27    95

─────────────────────────────────────────────────────────────────
[Step 2] Selecting Numerical Features...
Selected Features: ['QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP']
Cleaned Samples  : 2823

Feature Summary Statistics:
       QUANTITYORDERED  PRICEEACH     SALES     MSRP
count          2823.00    2823.00   2823.00  2823.00
mean             35.09      83.66   3553.89   100.72
std               9.74      20.17   1841.87    40.19
min               6.00      26.88    482.13    33.00
25%              27.00      68.86   2203.43    68.00
50%              35.00      95.70   3184.80    99.00
75%              43.00     100.00   4508.00   124.00
max              97.00     100.00  14082.80   214.00

─────────────────────────────────────────────────────────────────
[Step 3] Scaling Features with StandardScaler...
✓ Features scaled successfully.

─────────────────────────────────────────────────────────────────
[Step 4] Computing Elbow Method (WCSS for K = 1 to 10)...
  K =  1  |  WCSS (Inertia) =     11292.00
  K =  2  |  WCSS (Inertia) =      6741.69
  K =  3  |  WCSS (Inertia) =      4766.01
  K =  4  |  WCSS (Inertia) =      3934.89
  K =  5  |  WCSS (Inertia) =      3348.27
  K =  6  |  WCSS (Inertia) =      2858.82
  K =  7  |  WCSS (Inertia) =      2548.54
  K =  8  |  WCSS (Inertia) =      2350.66
  K =  9  |  WCSS (Inertia) =      2169.97
  K = 10  |  WCSS (Inertia) =      2019.75

✓ Elbow plot saved as 'elbow_method_plot.png'.
  Optimal K observed from elbow bend = 3

─────────────────────────────────────────────────────────────────
[Step 5] Training K-Means with Optimal K = 3...

Customer Counts per Cluster:
  Cluster 0:   975 customers (34.54%)
  Cluster 1:   852 customers (30.18%)
  Cluster 2:   996 customers (35.28%)

─────────────────────────────────────────────────────────────────
[Step 6] Cluster Centroids (Original Feature Scale):
           QUANTITYORDERED  PRICEEACH    SALES    MSRP
Cluster 0            35.21      59.55  2101.08   64.15
Cluster 1            43.73      97.49  5722.35  127.95
Cluster 2            27.61      95.43  3123.73  113.23

✓ Cluster visualization saved as 'kmeans_clusters_plot.png'.

═════════════════════════════════════════════════════════════════
  CLUSTERING PERFORMANCE METRICS
═════════════════════════════════════════════════════════════════
  Optimal Number of Clusters (K) : 3
  Final WCSS (Inertia)          : 4766.01
  Silhouette Score              : 0.3509
═════════════════════════════════════════════════════════════════

========================================================================
"""
