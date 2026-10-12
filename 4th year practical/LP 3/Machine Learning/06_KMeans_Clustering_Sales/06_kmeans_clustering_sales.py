"""
================================================================================
  Program 6: K-Means Clustering on Sales Data
  Course: Machine Learning

  Description:
    Implement K-Means clustering on sales_data_sample.csv dataset.
    Determine the optimal number of clusters using the Elbow Method.

  Dataset: https://www.kaggle.com/datasets/kyanyoga/sample-sales-data
           Download 'sales_data_sample.csv' and place it in the same directory.

  Requirements: pip install pandas numpy scikit-learn matplotlib seaborn
================================================================================
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()


def main():
    print("=" * 65)
    print("   K-MEANS CLUSTERING ON SALES DATA")
    print("=" * 65)

    # ── Load Dataset ────────────────────────────────────────────────────
    print("\n  Loading dataset...")
    csv_path = os.path.join(SCRIPT_DIR, "sales_data_sample.csv")
    df = pd.read_csv(csv_path, encoding='latin1')
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")

    # ── Pre-processing ──────────────────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  Pre-processing...")

    # Select relevant numeric features for clustering
    features = ['QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP']
    df_cluster = df[features].copy()

    # Drop missing values
    df_cluster = df_cluster.dropna()
    print(f"  Selected features: {features}")
    print(f"  Shape after cleaning: {df_cluster.shape}")
    print(f"\n  Feature Statistics:")
    print(df_cluster.describe())

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_cluster)
    print("\n  ✓ Features scaled using StandardScaler")

    # ── Elbow Method ────────────────────────────────────────────────────
    print(f"\n{'─' * 65}")
    print("  Elbow Method — Finding Optimal Number of Clusters...")

    inertias = []
    silhouette_scores = []
    k_range = range(2, 11)

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        sil_score = silhouette_score(X_scaled, kmeans.labels_)
        silhouette_scores.append(sil_score)
        print(f"    K={k:>2}  |  Inertia: {kmeans.inertia_:>12.2f}  |  Silhouette: {sil_score:.4f}")

    # Plot Elbow Curve
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Number of Clusters (K)')
    ax1.set_ylabel('Inertia (WCSS)')
    ax1.set_title('Elbow Method')
    ax1.grid(True, alpha=0.3)

    ax2.plot(k_range, silhouette_scores, 'rs-', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Clusters (K)')
    ax2.set_ylabel('Silhouette Score')
    ax2.set_title('Silhouette Score vs K')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    elbow_path = os.path.join(SCRIPT_DIR, 'elbow_method_plot.png')
    plt.savefig(elbow_path, dpi=100)
    plt.close()
    print(f"\n  Elbow plot saved as '{elbow_path}'")

    # ── Final Clustering ────────────────────────────────────────────────
    optimal_k = 3  # Typically found from elbow plot
    # Auto-detect: pick K with highest silhouette score
    best_k = list(k_range)[np.argmax(silhouette_scores)]
    print(f"\n  Best K by Silhouette Score: {best_k}")

    print(f"\n{'═' * 65}")
    print(f"  FINAL K-MEANS CLUSTERING (K = {best_k})")
    print(f"{'═' * 65}")

    kmeans_final = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    clusters = kmeans_final.fit_predict(X_scaled)

    df_cluster['Cluster'] = clusters

    # Cluster Summary
    print(f"\n  Cluster Distribution:")
    for i in range(best_k):
        count = (clusters == i).sum()
        print(f"    Cluster {i}: {count} samples ({count/len(clusters)*100:.1f}%)")

    print(f"\n  Cluster Centers (original scale):")
    centers = scaler.inverse_transform(kmeans_final.cluster_centers_)
    centers_df = pd.DataFrame(centers, columns=features)
    centers_df.index = [f"Cluster {i}" for i in range(best_k)]
    print(centers_df.round(2))

    # Final metrics
    final_sil = silhouette_score(X_scaled, clusters)
    print(f"\n  Silhouette Score: {final_sil:.4f}")
    print(f"  Inertia (WCSS) : {kmeans_final.inertia_:.2f}")

    # Scatter plot of clusters
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(df_cluster['SALES'], df_cluster['QUANTITYORDERED'],
                          c=clusters, cmap='viridis', alpha=0.6, edgecolors='k', linewidth=0.5)
    plt.colorbar(scatter, label='Cluster')
    plt.xlabel('Sales')
    plt.ylabel('Quantity Ordered')
    plt.title(f'K-Means Clustering (K={best_k})')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    cluster_path = os.path.join(SCRIPT_DIR, 'kmeans_clusters_plot.png')
    plt.savefig(cluster_path, dpi=100)
    plt.close()
    print(f"  Cluster plot saved as '{cluster_path}'")
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Loading dataset...
  Shape: (2823, 25)

  Pre-processing...
  Selected features: ['QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP']
  Shape after cleaning: (2823, 4)

  Elbow Method — Finding Optimal Number of Clusters...
    K= 2  |  Inertia:      7584.32  |  Silhouette: 0.4521
    K= 3  |  Inertia:      5623.18  |  Silhouette: 0.4012
    K= 4  |  Inertia:      4521.44  |  Silhouette: 0.3756
    K= 5  |  Inertia:      3842.91  |  Silhouette: 0.3524
    ...

  Best K by Silhouette Score: 2

  FINAL K-MEANS CLUSTERING (K = 2)

  Cluster Distribution:
    Cluster 0: 1985 samples (70.3%)
    Cluster 1: 838 samples (29.7%)

  Cluster Centers (original scale):
              QUANTITYORDERED  PRICEEACH    SALES    MSRP
  Cluster 0            28.45      82.14  2356.28   89.52
  Cluster 1            42.67     100.38  5812.45  126.34

  Silhouette Score: 0.4521
  Inertia (WCSS) : 7584.32

========================================================================
"""
