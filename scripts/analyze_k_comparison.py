#!/usr/bin/env python3
"""
Analisa e compara resultados de diferentes valores de K
Gera gráficos comparativos mostrando como as métricas variam com K
"""

import sys
import re
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def parse_perf_output(perf_file):
    """Parse perf stat output e extrai métricas"""
    with open(perf_file, 'r') as f:
        content = f.read()

    # Extrair tempos de execução
    times_naive = re.findall(r'naive VERSION.*?(\d+\.\d+)', content, re.DOTALL)
    times_opt = re.findall(r'optimized VERSION.*?(\d+\.\d+)', content, re.DOTALL)

    # Converter para float (em segundos)
    times_naive = [float(t) / 1000.0 for t in times_naive]
    times_opt = [float(t) / 1000.0 for t in times_opt]

    # Calcular média e desvio padrão
    time_naive = np.mean(times_naive) if times_naive else 0
    time_naive_std = np.std(times_naive) if times_naive else 0
    time_opt = np.mean(times_opt) if times_opt else 0
    time_opt_std = np.std(times_opt) if times_opt else 0

    # Função auxiliar para extrair métricas do perf
    def extract_metric(pattern, section):
        match = re.search(pattern, section, re.MULTILINE)
        if match:
            value = match.group(1).replace(',', '').replace('.', '')
            return float(value)
        return 0

    # Dividir em seções naive e optimized
    parts = content.split('optimized VERSION')
    naive_section = parts[0] if len(parts) > 0 else ""
    opt_section = parts[1] if len(parts) > 1 else ""

    metrics = {
        'time_naive': time_naive,
        'time_naive_std': time_naive_std,
        'time_opt': time_opt,
        'time_opt_std': time_opt_std,
    }

    # Padrões para extrair métricas (naive)
    patterns = {
        'cycles_naive': r'(\d[\d,\.]*)\s+cpu_core/cycles/',
        'instructions_naive': r'(\d[\d,\.]*)\s+cpu_core/instructions/',
        'cache_refs_naive': r'(\d[\d,\.]*)\s+cpu_core/cache-references/',
        'cache_misses_naive': r'(\d[\d,\.]*)\s+cpu_core/cache-misses/',
        'l1_loads_naive': r'(\d[\d,\.]*)\s+cpu_core/L1-dcache-loads/',
        'l1_misses_naive': r'(\d[\d,\.]*)\s+cpu_core/L1-dcache-load-misses/',
        'branches_naive': r'(\d[\d,\.]*)\s+cpu_core/branches/',
        'branch_misses_naive': r'(\d[\d,\.]*)\s+cpu_core/branch-misses/',
    }

    for key, pattern in patterns.items():
        metrics[key] = extract_metric(pattern, naive_section)

    # Métricas optimized
    patterns_opt = {
        'cycles_opt': r'(\d[\d,\.]*)\s+cpu_core/cycles/',
        'instructions_opt': r'(\d[\d,\.]*)\s+cpu_core/instructions/',
        'cache_refs_opt': r'(\d[\d,\.]*)\s+cpu_core/cache-references/',
        'cache_misses_opt': r'(\d[\d,\.]*)\s+cpu_core/cache-misses/',
        'l1_loads_opt': r'(\d[\d,\.]*)\s+cpu_core/L1-dcache-loads/',
        'l1_misses_opt': r'(\d[\d,\.]*)\s+cpu_core/L1-dcache-load-misses/',
        'branches_opt': r'(\d[\d,\.]*)\s+cpu_core/branches/',
        'branch_misses_opt': r'(\d[\d,\.]*)\s+cpu_core/branch-misses/',
    }

    for key, pattern in patterns_opt.items():
        metrics[key] = extract_metric(pattern, opt_section)

    # Calcular IPC
    if metrics['cycles_naive'] > 0:
        metrics['ipc_naive'] = metrics['instructions_naive'] / metrics['cycles_naive']
    else:
        metrics['ipc_naive'] = 0

    if metrics['cycles_opt'] > 0:
        metrics['ipc_opt'] = metrics['instructions_opt'] / metrics['cycles_opt']
    else:
        metrics['ipc_opt'] = 0

    return metrics

def generate_comparison_graphs(k_values, all_metrics, output_dir):
    """Gera gráficos comparativos"""

    output_path = Path(output_dir) / "k_comparison" / "graphs"
    output_path.mkdir(parents=True, exist_ok=True)

    # Preparar dados
    k_vals = sorted([int(k) for k in k_values])

    time_naive = [all_metrics[k]['time_naive'] for k in k_vals]
    time_opt = [all_metrics[k]['time_opt'] for k in k_vals]
    time_naive_std = [all_metrics[k]['time_naive_std'] for k in k_vals]
    time_opt_std = [all_metrics[k]['time_opt_std'] for k in k_vals]

    cycles_naive = [all_metrics[k]['cycles_naive'] / 1e9 for k in k_vals]
    cycles_opt = [all_metrics[k]['cycles_opt'] / 1e9 for k in k_vals]

    cache_misses_naive = [all_metrics[k]['cache_misses_naive'] / 1e6 for k in k_vals]
    cache_misses_opt = [all_metrics[k]['cache_misses_opt'] / 1e6 for k in k_vals]

    ipc_naive = [all_metrics[k]['ipc_naive'] for k in k_vals]
    ipc_opt = [all_metrics[k]['ipc_opt'] for k in k_vals]

    branches_naive = [all_metrics[k]['branches_naive'] / 1e9 for k in k_vals]
    branches_opt = [all_metrics[k]['branches_opt'] / 1e9 for k in k_vals]

    speedup = [all_metrics[k]['time_naive'] / all_metrics[k]['time_opt'] if all_metrics[k]['time_opt'] > 0 else 0 for k in k_vals]

    # 1. Tempo de execução vs K
    plt.figure(figsize=(10, 6))
    plt.errorbar(k_vals, time_naive, yerr=time_naive_std, marker='o', label='Naive', capsize=5, linewidth=2, markersize=8)
    plt.errorbar(k_vals, time_opt, yerr=time_opt_std, marker='s', label='Optimized', capsize=5, linewidth=2, markersize=8)
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Execution Time vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'time_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Cycles vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, cycles_naive, marker='o', label='Naive', linewidth=2, markersize=8)
    plt.plot(k_vals, cycles_opt, marker='s', label='Optimized', linewidth=2, markersize=8)
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('CPU Cycles (billions)', fontsize=12)
    plt.title('CPU Cycles vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'cycles_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Cache Misses vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, cache_misses_naive, marker='o', label='Naive', linewidth=2, markersize=8)
    plt.plot(k_vals, cache_misses_opt, marker='s', label='Optimized', linewidth=2, markersize=8)
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Cache Misses (millions)', fontsize=12)
    plt.title('Cache Misses vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'cache_misses_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. IPC vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, ipc_naive, marker='o', label='Naive', linewidth=2, markersize=8)
    plt.plot(k_vals, ipc_opt, marker='s', label='Optimized', linewidth=2, markersize=8)
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Instructions Per Cycle (IPC)', fontsize=12)
    plt.title('IPC vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'ipc_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 5. Branches vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, branches_naive, marker='o', label='Naive', linewidth=2, markersize=8)
    plt.plot(k_vals, branches_opt, marker='s', label='Optimized', linewidth=2, markersize=8)
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Branches (billions)', fontsize=12)
    plt.title('Branch Instructions vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'branches_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 6. Speedup vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, speedup, marker='o', linewidth=2, markersize=8, color='green')
    plt.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, label='No speedup')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Speedup (Naive / Optimized)', fontsize=12)
    plt.title('Speedup vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'speedup_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 7. Gráfico comparativo multi-métrica
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    metrics_data = [
        (time_naive, time_opt, 'Time (s)', axes[0, 0]),
        (cycles_naive, cycles_opt, 'Cycles (B)', axes[0, 1]),
        (cache_misses_naive, cache_misses_opt, 'Cache Misses (M)', axes[0, 2]),
        (ipc_naive, ipc_opt, 'IPC', axes[1, 0]),
        (branches_naive, branches_opt, 'Branches (B)', axes[1, 1]),
        (speedup, None, 'Speedup', axes[1, 2])
    ]

    for naive_data, opt_data, ylabel, ax in metrics_data:
        if opt_data is not None:
            ax.plot(k_vals, naive_data, marker='o', label='Naive', linewidth=2, markersize=6)
            ax.plot(k_vals, opt_data, marker='s', label='Optimized', linewidth=2, markersize=6)
            ax.legend(fontsize=9)
        else:
            ax.plot(k_vals, naive_data, marker='o', linewidth=2, markersize=6, color='green')
            ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1)
        ax.set_xlabel('K', fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(ylabel, fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(k_vals)

    plt.tight_layout()
    plt.savefig(output_path / 'all_metrics_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\nComparison graphs generated:")
    for graph in ['time_vs_k', 'cycles_vs_k', 'cache_misses_vs_k', 'ipc_vs_k', 'branches_vs_k', 'speedup_vs_k', 'all_metrics_vs_k']:
        print(f"  - {output_path / (graph + '.png')}")

def generate_text_analysis(k_values, all_metrics, output_file):
    """Gera análise em texto"""

    k_vals = sorted([int(k) for k in k_values])

    with open(output_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("  K-MEANS COMPARISON: IMPACT OF K ON PERFORMANCE\n")
        f.write("=" * 80 + "\n\n")

        f.write("EXECUTION TIME\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'K':<5} {'Naive (s)':<15} {'Optimized (s)':<15} {'Speedup':<10}\n")
        f.write("-" * 80 + "\n")

        for k in k_vals:
            m = all_metrics[k]
            speedup = m['time_naive'] / m['time_opt'] if m['time_opt'] > 0 else 0
            f.write(f"{k:<5} {m['time_naive']:<15.3f} {m['time_opt']:<15.3f} {speedup:<10.2f}x\n")

        f.write("\n")
        f.write("DETAILED METRICS BY K\n")
        f.write("-" * 80 + "\n")

        for k in k_vals:
            m = all_metrics[k]
            f.write(f"\nK = {k}\n")
            f.write("-" * 40 + "\n")
            f.write(f"  Naive:\n")
            f.write(f"    Time:           {m['time_naive']:.3f} s\n")
            f.write(f"    Cycles:         {m['cycles_naive']/1e9:.2f} B\n")
            f.write(f"    Instructions:   {m['instructions_naive']/1e9:.2f} B\n")
            f.write(f"    IPC:            {m['ipc_naive']:.2f}\n")
            f.write(f"    Cache misses:   {m['cache_misses_naive']/1e6:.2f} M\n")
            f.write(f"    Branches:       {m['branches_naive']/1e9:.2f} B\n")
            f.write(f"    Branch misses:  {m['branch_misses_naive']/1e6:.2f} M\n")

            f.write(f"\n  Optimized:\n")
            f.write(f"    Time:           {m['time_opt']:.3f} s\n")
            f.write(f"    Cycles:         {m['cycles_opt']/1e9:.2f} B\n")
            f.write(f"    Instructions:   {m['instructions_opt']/1e9:.2f} B\n")
            f.write(f"    IPC:            {m['ipc_opt']:.2f}\n")
            f.write(f"    Cache misses:   {m['cache_misses_opt']/1e6:.2f} M\n")
            f.write(f"    Branches:       {m['branches_opt']/1e9:.2f} B\n")
            f.write(f"    Branch misses:  {m['branch_misses_opt']/1e6:.2f} M\n")

            speedup = m['time_naive'] / m['time_opt'] if m['time_opt'] > 0 else 0
            f.write(f"\n  Speedup:          {speedup:.2f}x\n")

        f.write("\n" + "=" * 80 + "\n")

def main():
    if len(sys.argv) < 3:
        print("Usage: analyze_k_comparison.py <results_dir> <k_values>")
        sys.exit(1)

    results_dir = sys.argv[1]
    k_values = sys.argv[2].split()

    print(f"Analyzing K comparison for: {k_values}")

    # Coletar métricas para cada K
    all_metrics = {}
    for k in k_values:
        perf_file = Path(results_dir) / f"k{k}" / "perf_raw.txt"
        if not perf_file.exists():
            print(f"Warning: {perf_file} not found, skipping K={k}")
            continue

        print(f"  Processing K={k}...")
        all_metrics[int(k)] = parse_perf_output(perf_file)

    if not all_metrics:
        print("Error: No valid results found")
        sys.exit(1)

    # Gerar análise em texto
    text_output = Path(results_dir) / "k_comparison" / "k_analysis.txt"
    text_output.parent.mkdir(exist_ok=True)
    generate_text_analysis(all_metrics.keys(), all_metrics, text_output)
    print(f"\nText analysis saved to: {text_output}")

    # Gerar gráficos
    generate_comparison_graphs(all_metrics.keys(), all_metrics, results_dir)

    print("\nK comparison analysis complete!")

if __name__ == '__main__':
    main()
