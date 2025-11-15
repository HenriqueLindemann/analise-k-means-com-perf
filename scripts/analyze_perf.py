#!/usr/bin/env python3
"""
Analisa resultados do perf e cria comparação formatada
"""

import sys
import re
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def parse_perf_output(file_path):
    """Extrai métricas do output do perf"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Dividir em seções naive e optimized
    sections = content.split('========================================')

    results = {'naive': {}, 'optimized': {}}
    current_version = None

    for section in sections:
        if 'naive VERSION' in section:
            current_version = 'naive'
        elif 'optimized VERSION' in section:
            current_version = 'optimized'

        if current_version:
            # Extrair métricas
            # Formato: número cpu_core/metric_name/

            # Cycles
            match = re.search(r'(\d+)\s+cpu_core/cycles/', section)
            if match:
                results[current_version]['cycles'] = int(match.group(1))

            # Instructions
            match = re.search(r'(\d+)\s+cpu_core/instructions/.*#\s+([\d.]+)\s+insn per cycle', section)
            if match:
                results[current_version]['instructions'] = int(match.group(1))
                results[current_version]['ipc'] = float(match.group(2))

            # Cache references
            match = re.search(r'(\d+)\s+cpu_core/cache-references/', section)
            if match:
                results[current_version]['cache_refs'] = int(match.group(1))

            # Cache misses
            match = re.search(r'(\d+)\s+cpu_core/cache-misses/.*#\s+([\d.]+)%', section)
            if match:
                results[current_version]['cache_misses'] = int(match.group(1))
                results[current_version]['cache_miss_rate'] = float(match.group(2))

            # L1 dcache loads
            match = re.search(r'(\d+)\s+cpu_core/L1-dcache-loads/', section)
            if match:
                results[current_version]['l1_loads'] = int(match.group(1))

            # L1 dcache load misses
            match = re.search(r'(\d+)\s+cpu_core/L1-dcache-load-misses/.*#\s+([\d.]+)%', section)
            if match:
                results[current_version]['l1_misses'] = int(match.group(1))
                results[current_version]['l1_miss_rate'] = float(match.group(2))

            # Branches
            match = re.search(r'(\d+)\s+cpu_core/branches/', section)
            if match:
                results[current_version]['branches'] = int(match.group(1))

            # Branch misses
            match = re.search(r'(\d+)\s+cpu_core/branch-misses/.*#\s+([\d.]+)%', section)
            if match:
                results[current_version]['branch_misses'] = int(match.group(1))
                results[current_version]['branch_miss_rate'] = float(match.group(2))

            # Time
            match = re.search(r'([\d.]+)\s+\+-\s+([\d.]+)\s+seconds time elapsed', section)
            if match:
                results[current_version]['time'] = float(match.group(1))
                results[current_version]['time_std'] = float(match.group(2))

    return results

def print_comparison(results):
    """Imprime comparação formatada"""

    naive = results['naive']
    opt = results['optimized']

    print("\n" + "="*80)
    print("  K-MEANS PERFORMANCE ANALYSIS (perf)")
    print("="*80 + "\n")

    # Tempo
    print("TIME")
    print("-" * 80)
    print(f"  Naive:     {naive.get('time', 0):.3f} ± {naive.get('time_std', 0):.3f} seconds")
    print(f"  Optimized: {opt.get('time', 0):.3f} ± {opt.get('time_std', 0):.3f} seconds")
    speedup = naive.get('time', 1) / opt.get('time', 1)
    print(f"  Speedup:   {speedup:.2f}x {'✓ FASTER' if speedup > 1 else '✗ SLOWER'}")
    print()

    # Tabela comparativa
    print("DETAILED METRICS")
    print("-" * 80)
    print(f"{'Metric':<25} {'Naive':>15} {'Optimized':>15} {'Ratio':>10} {'Status':>10}")
    print("-" * 80)

    def print_metric(name, key, lower_better=True):
        n = naive.get(key, 0)
        o = opt.get(key, 0)
        ratio = o / n if n > 0 else 0

        if lower_better:
            status = "✓ BETTER" if ratio < 1.0 else "✗ WORSE"
        else:
            status = "✓ BETTER" if ratio > 1.0 else "✗ WORSE"

        print(f"{name:<25} {n:>15,} {o:>15,} {ratio:>10.2f}x {status:>10}")

    def print_metric_float(name, key, lower_better=True):
        n = naive.get(key, 0)
        o = opt.get(key, 0)
        ratio = o / n if n > 0 else 0

        if lower_better:
            status = "✓ BETTER" if ratio < 1.0 else "✗ WORSE"
        else:
            status = "✓ BETTER" if ratio > 1.0 else "✗ WORSE"

        print(f"{name:<25} {n:>15.2f} {o:>15.2f} {ratio:>10.2f}x {status:>10}")

    print_metric("Cycles", "cycles", lower_better=True)
    print_metric("Instructions", "instructions", lower_better=True)
    print_metric_float("IPC", "ipc", lower_better=False)
    print()

    print_metric("Cache references", "cache_refs", lower_better=True)
    print_metric("Cache misses", "cache_misses", lower_better=True)
    print_metric_float("Cache miss rate (%)", "cache_miss_rate", lower_better=True)
    print()

    print_metric("L1 dcache loads", "l1_loads", lower_better=True)
    print_metric("L1 dcache misses", "l1_misses", lower_better=True)
    print_metric_float("L1 miss rate (%)", "l1_miss_rate", lower_better=True)
    print()

    print_metric("Branches", "branches", lower_better=True)
    print_metric("Branch misses", "branch_misses", lower_better=True)
    print_metric_float("Branch miss rate (%)", "branch_miss_rate", lower_better=True)

    print("\n" + "="*80)

    # Summary
    print("\nKEY INSIGHTS:")
    print("-" * 80)

    if opt.get('cache_misses', 1) < naive.get('cache_misses', 0):
        improvement = (1 - opt['cache_misses'] / naive['cache_misses']) * 100
        print(f"✓ Cache misses reduced by {improvement:.1f}% (SoA layout working!)")

    if opt.get('ipc', 0) > naive.get('ipc', 1):
        improvement = (opt['ipc'] / naive['ipc'] - 1) * 100
        print(f"✓ IPC improved by {improvement:.1f}% (better instruction throughput)")

    if opt.get('l1_misses', 0) > naive.get('l1_misses', 1):
        degradation = (opt['l1_misses'] / naive['l1_misses'] - 1) * 100
        print(f"✗ L1 misses increased by {degradation:.1f}% (SoA spread across more cache lines)")

    if speedup > 1:
        print(f"✓ Overall speedup: {speedup:.2f}x faster")
    else:
        print(f"✗ Overall slowdown: {1/speedup:.2f}x slower")

def generate_graphs(results, output_dir):
    """Gera gráficos de comparação de performance"""

    naive = results['naive']
    opt = results['optimized']

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    colors = ['#e74c3c', '#2ecc71']  # Red for naive, green for optimized

    # 1. Execution time comparison
    fig, ax = plt.subplots(figsize=(8, 5))
    versions = ['Naive', 'Optimized']
    times = [naive.get('time', 0), opt.get('time', 0)]
    bars = ax.bar(versions, times, color=colors, alpha=0.8, edgecolor='black')
    ax.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Execution Time Comparison', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}s',
                ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path / 'execution_time.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Cache misses comparison
    fig, ax = plt.subplots(figsize=(8, 5))
    cache_misses = [naive.get('cache_misses', 0) / 1e6, opt.get('cache_misses', 0) / 1e6]
    bars = ax.bar(versions, cache_misses, color=colors, alpha=0.8, edgecolor='black')
    ax.set_ylabel('Cache Misses (millions)', fontsize=12, fontweight='bold')
    ax.set_title('Cache Misses Comparison', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}M',
                ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path / 'cache_misses.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. IPC comparison
    fig, ax = plt.subplots(figsize=(8, 5))
    ipc_values = [naive.get('ipc', 0), opt.get('ipc', 0)]
    bars = ax.bar(versions, ipc_values, color=colors, alpha=0.8, edgecolor='black')
    ax.set_ylabel('IPC (Instructions Per Cycle)', fontsize=12, fontweight='bold')
    ax.set_title('IPC Comparison', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path / 'ipc.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. Multi-metric comparison (normalized)
    fig, ax = plt.subplots(figsize=(12, 6))

    metrics_for_comparison = {
        'Time': (naive.get('time', 1), opt.get('time', 1)),
        'Cycles': (naive.get('cycles', 1) / 1e9, opt.get('cycles', 1) / 1e9),
        'Cache Misses': (naive.get('cache_misses', 1) / 1e6, opt.get('cache_misses', 1) / 1e6),
        'L1 Misses': (naive.get('l1_misses', 1) / 1e6, opt.get('l1_misses', 1) / 1e6),
        'Cache Miss Rate': (naive.get('cache_miss_rate', 1), opt.get('cache_miss_rate', 1)),
    }

    x = np.arange(len(metrics_for_comparison))
    width = 0.35

    naive_vals = [v[0] for v in metrics_for_comparison.values()]
    opt_vals = [v[1] for v in metrics_for_comparison.values()]

    bars1 = ax.bar(x - width/2, naive_vals, width, label='Naive',
                   color=colors[0], alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x + width/2, opt_vals, width, label='Optimized',
                   color=colors[1], alpha=0.8, edgecolor='black')

    ax.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax.set_title('Performance Metrics Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_for_comparison.keys(), rotation=15, ha='right')
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path / 'metrics_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 5. Speedup/improvement summary
    fig, ax = plt.subplots(figsize=(10, 6))

    improvements = {
        'Execution Time': ((naive.get('time', 1) - opt.get('time', 1)) / naive.get('time', 1) * 100),
        'Cache Misses': ((naive.get('cache_misses', 1) - opt.get('cache_misses', 1)) / naive.get('cache_misses', 1) * 100),
        'IPC': ((opt.get('ipc', 0) - naive.get('ipc', 1)) / naive.get('ipc', 1) * 100),
        'Cycles': ((naive.get('cycles', 1) - opt.get('cycles', 1)) / naive.get('cycles', 1) * 100),
    }

    metrics_names = list(improvements.keys())
    improvement_values = list(improvements.values())
    colors_improvement = ['#2ecc71' if v > 0 else '#e74c3c' for v in improvement_values]

    bars = ax.barh(metrics_names, improvement_values, color=colors_improvement,
                   alpha=0.8, edgecolor='black')
    ax.set_xlabel('Improvement (%)', fontsize=12, fontweight='bold')
    ax.set_title('Performance Improvements (Optimized vs Naive)', fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(axis='x', alpha=0.3)

    for i, (bar, val) in enumerate(zip(bars, improvement_values)):
        ax.text(val + (2 if val > 0 else -2), i, f'{val:+.1f}%',
                ha='left' if val > 0 else 'right', va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path / 'improvements.png', dpi=300, bbox_inches='tight')
    plt.close()

    return [
        'execution_time.png',
        'cache_misses.png',
        'ipc.png',
        'metrics_comparison.png',
        'improvements.png'
    ]

def generate_cluster_visualizations(k, dataset_path, output_dir):
    """Gera visualizações dos clusters usando ambas as versões"""
    import subprocess
    from pathlib import Path

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Gerar clusters para ambas as versões
    for version in ['naive', 'optimized']:
        cluster_file = output_path / f'clusters_{version}.csv'

        # Executar cluster_save
        cmd = f'bin/cluster_save {version} {k} {dataset_path} {output_path / "clusters"}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Warning: Failed to generate clusters for {version}")
            continue

    # Gerar plots combinados
    naive_file = output_path / 'clusters_naive.csv'
    opt_file = output_path / 'clusters_optimized.csv'

    if naive_file.exists() and opt_file.exists():
        # Importar pandas para análise
        import pandas as pd

        naive_df = pd.read_csv(naive_file)
        opt_df = pd.read_csv(opt_file)

        # 1. Scatter plot comparando clusters (primeiras 2 features)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Naive
        scatter1 = ax1.scatter(naive_df.iloc[:, 0], naive_df.iloc[:, 1],
                              c=naive_df['cluster_id'], cmap='tab10',
                              alpha=0.5, s=10, edgecolors='none')
        ax1.set_xlabel('Global Active Power', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Global Reactive Power', fontsize=11, fontweight='bold')
        ax1.set_title('K-means Clustering - Naive', fontsize=13, fontweight='bold')
        ax1.grid(alpha=0.3)
        plt.colorbar(scatter1, ax=ax1, label='Cluster ID')

        # Optimized
        scatter2 = ax2.scatter(opt_df.iloc[:, 0], opt_df.iloc[:, 1],
                              c=opt_df['cluster_id'], cmap='tab10',
                              alpha=0.5, s=10, edgecolors='none')
        ax2.set_xlabel('Global Active Power', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Global Reactive Power', fontsize=11, fontweight='bold')
        ax2.set_title('K-means Clustering - Optimized', fontsize=13, fontweight='bold')
        ax2.grid(alpha=0.3)
        plt.colorbar(scatter2, ax=ax2, label='Cluster ID')

        plt.tight_layout()
        plt.savefig(output_path / 'clusters_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 2. Distribuição de pontos por cluster
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        naive_counts = naive_df['cluster_id'].value_counts().sort_index()
        opt_counts = opt_df['cluster_id'].value_counts().sort_index()

        ax1.bar(naive_counts.index, naive_counts.values, color='#e74c3c', alpha=0.8, edgecolor='black')
        ax1.set_xlabel('Cluster ID', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Number of Points', fontsize=11, fontweight='bold')
        ax1.set_title('Cluster Distribution - Naive', fontsize=13, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)

        ax2.bar(opt_counts.index, opt_counts.values, color='#2ecc71', alpha=0.8, edgecolor='black')
        ax2.set_xlabel('Cluster ID', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Number of Points', fontsize=11, fontweight='bold')
        ax2.set_title('Cluster Distribution - Optimized', fontsize=13, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'cluster_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 3. Heatmap das médias dos clusters
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Calcular médias por cluster
        feature_cols = [col for col in naive_df.columns if col != 'cluster_id']
        naive_means = naive_df.groupby('cluster_id')[feature_cols].mean()
        opt_means = opt_df.groupby('cluster_id')[feature_cols].mean()

        # Normalizar para visualização
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        naive_means_norm = scaler.fit_transform(naive_means)
        opt_means_norm = scaler.fit_transform(opt_means)

        im1 = ax1.imshow(naive_means_norm.T, aspect='auto', cmap='RdYlGn', interpolation='nearest')
        ax1.set_yticks(range(len(feature_cols)))
        ax1.set_yticklabels([col.replace('_', ' ').title() for col in feature_cols])
        ax1.set_xticks(range(len(naive_means)))
        ax1.set_xticklabels([f'C{i}' for i in naive_means.index])
        ax1.set_title('Cluster Centroids (Normalized) - Naive', fontsize=13, fontweight='bold')
        plt.colorbar(im1, ax=ax1, label='Normalized Value')

        im2 = ax2.imshow(opt_means_norm.T, aspect='auto', cmap='RdYlGn', interpolation='nearest')
        ax2.set_yticks(range(len(feature_cols)))
        ax2.set_yticklabels([col.replace('_', ' ').title() for col in feature_cols])
        ax2.set_xticks(range(len(opt_means)))
        ax2.set_xticklabels([f'C{i}' for i in opt_means.index])
        ax2.set_title('Cluster Centroids (Normalized) - Optimized', fontsize=13, fontweight='bold')
        plt.colorbar(im2, ax=ax2, label='Normalized Value')

        plt.tight_layout()
        plt.savefig(output_path / 'cluster_centroids_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()

        return [
            'clusters_comparison.png',
            'cluster_distribution.png',
            'cluster_centroids_heatmap.png'
        ]

    return []

def save_analysis_markdown(results, output_file):
    """Salva análise em formato markdown"""

    naive = results['naive']
    opt = results['optimized']

    with open(output_file, 'w') as f:
        f.write("# K-means Performance Analysis Report\n\n")

        # Metadata
        from datetime import datetime
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Summary
        f.write("## Executive Summary\n\n")
        speedup = naive.get('time', 1) / opt.get('time', 1)
        f.write(f"**Overall Speedup**: {speedup:.2f}x\n\n")

        if speedup > 1:
            f.write(f"The optimized version is **{speedup:.2f}x faster** than naive.\n\n")
        else:
            f.write(f"The optimized version is **{1/speedup:.2f}x slower** than naive.\n\n")

        # Time comparison
        f.write("## Execution Time\n\n")
        f.write("| Version | Time | Std Dev |\n")
        f.write("|---------|------|----------|\n")
        f.write(f"| Naive | {naive.get('time', 0):.3f}s | ±{naive.get('time_std', 0):.3f}s |\n")
        f.write(f"| Optimized | {opt.get('time', 0):.3f}s | ±{opt.get('time_std', 0):.3f}s |\n\n")

        # Detailed metrics
        f.write("## Performance Metrics\n\n")
        f.write("| Metric | Naive | Optimized | Ratio | Improvement |\n")
        f.write("|--------|-------|-----------|-------|-------------|\n")

        metrics = [
            ('Cycles', 'cycles', True),
            ('Instructions', 'instructions', True),
            ('IPC', 'ipc', False),
            ('Cache references', 'cache_refs', True),
            ('Cache misses', 'cache_misses', True),
            ('Cache miss rate (%)', 'cache_miss_rate', True),
            ('L1 dcache loads', 'l1_loads', True),
            ('L1 dcache misses', 'l1_misses', True),
            ('L1 miss rate (%)', 'l1_miss_rate', True),
            ('Branches', 'branches', True),
            ('Branch misses', 'branch_misses', True),
            ('Branch miss rate (%)', 'branch_miss_rate', True),
        ]

        for name, key, lower_better in metrics:
            n = naive.get(key, 0)
            o = opt.get(key, 0)
            ratio = o / n if n > 0 else 0

            if isinstance(n, float) and n < 100:
                n_str = f"{n:.2f}"
                o_str = f"{o:.2f}"
            else:
                n_str = f"{int(n):,}"
                o_str = f"{int(o):,}"

            if lower_better:
                improvement = ((n - o) / n * 100) if n > 0 else 0
                status = "Better" if ratio < 1.0 else "Worse"
            else:
                improvement = ((o - n) / n * 100) if n > 0 else 0
                status = "Better" if ratio > 1.0 else "Worse"

            f.write(f"| {name} | {n_str} | {o_str} | {ratio:.2f}x | {improvement:+.1f}% ({status}) |\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_perf.py <perf_results.txt> [output.md]")
        sys.exit(1)

    file_path = sys.argv[1]
    results = parse_perf_output(file_path)
    print_comparison(results)

    # Salvar análise em markdown se fornecido segundo argumento
    if len(sys.argv) > 2:
        output_md = sys.argv[2]
        save_analysis_markdown(results, output_md)
        print(f"\nMarkdown analysis saved to: {output_md}")

        # Gerar gráficos no mesmo diretório do markdown
        output_dir = Path(output_md).parent
        graph_files = generate_graphs(results, output_dir)
        print(f"\nGraphs generated:")
        for graph in graph_files:
            print(f"  - {output_dir / graph}")
