#!/usr/bin/env python3
"""
Plota os resultados do K-means computado em C
Apenas visualização, sem reprocessamento
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv_file = sys.argv[1] if len(sys.argv) > 1 else 'clusters_optimized.csv'

print(f"Loading {csv_file}...")
df = pd.read_csv(csv_file)
print(f"Loaded {len(df):,} points")

# Features e clusters
features = ['global_active_power', 'global_reactive_power', 'voltage',
            'global_intensity', 'sub_metering_1', 'sub_metering_2', 'sub_metering_3']
clusters = df['cluster'].values
k = len(np.unique(clusters))

print(f"Clusters: {k}")

# Criar figura
fig, axes = plt.subplots(3, 3, figsize=(16, 12))
colors = plt.cm.Set1(np.arange(k))

# Plots de distribuição por feature
for idx, feature in enumerate(features):
    ax = axes[idx // 3, idx % 3]

    # Box plot por cluster
    data_by_cluster = [df[df['cluster'] == i][feature].values for i in range(k)]
    bp = ax.boxplot(data_by_cluster, labels=[f'C{i}' for i in range(k)],
                    patch_artist=True, widths=0.6)

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    short_name = feature.replace('global_', '').replace('sub_metering_', 'sm').replace('_', ' ').title()
    ax.set_title(short_name, fontweight='bold')
    ax.set_xlabel('Cluster')
    ax.grid(True, alpha=0.3, axis='y')

# Distribuição de pontos
ax = axes[2, 1]
cluster_counts = [np.sum(clusters == i) for i in range(k)]
ax.bar(range(k), cluster_counts, color=colors, edgecolor='black', linewidth=2)
ax.set_xlabel('Cluster ID', fontweight='bold')
ax.set_ylabel('Points', fontweight='bold')
ax.set_title('Cluster Distribution', fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

for i, count in enumerate(cluster_counts):
    pct = 100.0 * count / len(df)
    ax.text(i, count, f'{count}\n({pct:.1f}%)', ha='center', va='bottom', fontweight='bold')

# Scatter: Power vs Voltage (colorido por cluster)
ax = axes[2, 2]
for i in range(k):
    mask = clusters == i
    ax.scatter(df[mask]['global_active_power'], df[mask]['voltage'],
               c=[colors[i]], label=f'C{i}', alpha=0.6, s=8)
ax.set_xlabel('Global Active Power', fontweight='bold')
ax.set_ylabel('Voltage', fontweight='bold')
ax.set_title('Power vs Voltage', fontweight='bold')
ax.legend(markerscale=2)
ax.grid(True, alpha=0.3)

plt.suptitle(f'K-means Results (K={k}, N={len(df):,})', fontsize=14, fontweight='bold')
plt.tight_layout()

output = csv_file.replace('.csv', '_plot.png')
plt.savefig(output, dpi=150, bbox_inches='tight')
print(f"\nSaved: {output}")

# Stats
print("\n=== Cluster Stats ===")
for i in range(k):
    cluster_data = df[df['cluster'] == i]
    print(f"Cluster {i}: {len(cluster_data):>7} points ({100*len(cluster_data)/len(df):5.2f}%)")

plt.show()
