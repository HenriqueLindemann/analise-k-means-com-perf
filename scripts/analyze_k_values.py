#!/usr/bin/env python3
"""
Analisa resultados de benchmarks com diferentes valores de K
Gera gráficos mostrando como as métricas variam com K
"""

import sys
import re
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def parse_perf_output(perf_file):
    """Parse perf stat output e extrai métricas para 3 versões"""
    with open(perf_file, 'r') as f:
        content = f.read()

    # Extrair tempos de execução para as 3 versões
    times_naive = re.findall(r'naive VERSION.*?(\d+\.\d+)', content, re.DOTALL)
    times_opt_no_unroll = re.findall(r'optimized_no_unroll VERSION.*?(\d+\.\d+)', content, re.DOTALL)
    times_opt = re.findall(r'(?<!_)optimized VERSION.*?(\d+\.\d+)', content, re.DOTALL)

    # Converter para float (em segundos)
    times_naive = [float(t) / 1000.0 for t in times_naive]
    times_opt_no_unroll = [float(t) / 1000.0 for t in times_opt_no_unroll]
    times_opt = [float(t) / 1000.0 for t in times_opt]

    # Calcular média e desvio padrão
    time_naive = np.mean(times_naive) if times_naive else 0
    time_naive_std = np.std(times_naive) if times_naive else 0
    time_opt_no_unroll = np.mean(times_opt_no_unroll) if times_opt_no_unroll else 0
    time_opt_no_unroll_std = np.std(times_opt_no_unroll) if times_opt_no_unroll else 0
    time_opt = np.mean(times_opt) if times_opt else 0
    time_opt_std = np.std(times_opt) if times_opt else 0

    # Função auxiliar para extrair métricas do perf
    def extract_metric(pattern, section):
        match = re.search(pattern, section, re.MULTILINE)
        if match:
            value = match.group(1).replace(',', '').replace('.', '')
            return float(value)
        return 0

    # Dividir em 3 seções: naive, optimized_no_unroll, optimized
    sections = re.split(r'={40}', content)
    naive_section = ""
    opt_no_unroll_section = ""
    opt_section = ""

    for section in sections:
        if 'naive VERSION' in section:
            naive_section = section
        elif 'optimized_no_unroll VERSION' in section:
            opt_no_unroll_section = section
        elif 'optimized VERSION' in section and 'optimized_no_unroll' not in section:
            opt_section = section

    metrics = {
        'time_naive': time_naive,
        'time_naive_std': time_naive_std,
        'time_opt_no_unroll': time_opt_no_unroll,
        'time_opt_no_unroll_std': time_opt_no_unroll_std,
        'time_opt': time_opt,
        'time_opt_std': time_opt_std,
    }

    # Padrões para extrair métricas
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

    # Métricas optimized_no_unroll
    patterns_opt_no_unroll = {
        'cycles_opt_no_unroll': r'(\d[\d,\.]*)\s+cpu_core/cycles/',
        'instructions_opt_no_unroll': r'(\d[\d,\.]*)\s+cpu_core/instructions/',
        'cache_refs_opt_no_unroll': r'(\d[\d,\.]*)\s+cpu_core/cache-references/',
        'cache_misses_opt_no_unroll': r'(\d[\d,\.]*)\s+cpu_core/cache-misses/',
        'l1_loads_opt_no_unroll': r'(\d[\d,\.]*)\s+cpu_core/L1-dcache-loads/',
        'l1_misses_opt_no_unroll': r'(\d[\d,\.]*)\s+cpu_core/L1-dcache-load-misses/',
        'branches_opt_no_unroll': r'(\d[\d,\.]*)\s+cpu_core/branches/',
        'branch_misses_opt_no_unroll': r'(\d[\d,\.]*)\s+cpu_core/branch-misses/',
    }

    for key, pattern in patterns_opt_no_unroll.items():
        metrics[key] = extract_metric(pattern, opt_no_unroll_section)

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

    # Calcular IPC para todas as versões
    if metrics['cycles_naive'] > 0:
        metrics['ipc_naive'] = metrics['instructions_naive'] / metrics['cycles_naive']
    else:
        metrics['ipc_naive'] = 0

    if metrics['cycles_opt_no_unroll'] > 0:
        metrics['ipc_opt_no_unroll'] = metrics['instructions_opt_no_unroll'] / metrics['cycles_opt_no_unroll']
    else:
        metrics['ipc_opt_no_unroll'] = 0

    if metrics['cycles_opt'] > 0:
        metrics['ipc_opt'] = metrics['instructions_opt'] / metrics['cycles_opt']
    else:
        metrics['ipc_opt'] = 0

    # Calcular cache miss rates para todas as versões
    if metrics['cache_refs_naive'] > 0:
        metrics['cache_miss_rate_naive'] = 100 * metrics['cache_misses_naive'] / metrics['cache_refs_naive']
    else:
        metrics['cache_miss_rate_naive'] = 0

    if metrics['cache_refs_opt_no_unroll'] > 0:
        metrics['cache_miss_rate_opt_no_unroll'] = 100 * metrics['cache_misses_opt_no_unroll'] / metrics['cache_refs_opt_no_unroll']
    else:
        metrics['cache_miss_rate_opt_no_unroll'] = 0

    if metrics['cache_refs_opt'] > 0:
        metrics['cache_miss_rate_opt'] = 100 * metrics['cache_misses_opt'] / metrics['cache_refs_opt']
    else:
        metrics['cache_miss_rate_opt'] = 0

    return metrics

def generate_k_analysis_graphs(k_values, all_metrics, output_dir):
    """Gera gráficos mostrando métricas em função de K para 3 versões"""

    output_path = Path(output_dir) / "graphs"
    output_path.mkdir(exist_ok=True)

    # Preparar dados
    k_vals = sorted([int(k) for k in k_values])

    time_naive = [all_metrics[k]['time_naive'] for k in k_vals]
    time_opt_no_unroll = [all_metrics[k]['time_opt_no_unroll'] for k in k_vals]
    time_opt = [all_metrics[k]['time_opt'] for k in k_vals]
    time_naive_std = [all_metrics[k]['time_naive_std'] for k in k_vals]
    time_opt_no_unroll_std = [all_metrics[k]['time_opt_no_unroll_std'] for k in k_vals]
    time_opt_std = [all_metrics[k]['time_opt_std'] for k in k_vals]

    cycles_naive = [all_metrics[k]['cycles_naive'] / 1e9 for k in k_vals]
    cycles_opt_no_unroll = [all_metrics[k]['cycles_opt_no_unroll'] / 1e9 for k in k_vals]
    cycles_opt = [all_metrics[k]['cycles_opt'] / 1e9 for k in k_vals]

    cache_misses_naive = [all_metrics[k]['cache_misses_naive'] / 1e6 for k in k_vals]
    cache_misses_opt_no_unroll = [all_metrics[k]['cache_misses_opt_no_unroll'] / 1e6 for k in k_vals]
    cache_misses_opt = [all_metrics[k]['cache_misses_opt'] / 1e6 for k in k_vals]

    ipc_naive = [all_metrics[k]['ipc_naive'] for k in k_vals]
    ipc_opt_no_unroll = [all_metrics[k]['ipc_opt_no_unroll'] for k in k_vals]
    ipc_opt = [all_metrics[k]['ipc_opt'] for k in k_vals]

    branches_naive = [all_metrics[k]['branches_naive'] / 1e9 for k in k_vals]
    branches_opt_no_unroll = [all_metrics[k]['branches_opt_no_unroll'] / 1e9 for k in k_vals]
    branches_opt = [all_metrics[k]['branches_opt'] / 1e9 for k in k_vals]

    speedup_naive_to_opt = [all_metrics[k]['time_naive'] / all_metrics[k]['time_opt'] if all_metrics[k]['time_opt'] > 0 else 0 for k in k_vals]
    speedup_unroll_effect = [all_metrics[k]['time_opt_no_unroll'] / all_metrics[k]['time_opt'] if all_metrics[k]['time_opt'] > 0 else 0 for k in k_vals]

    # 1. Tempo de execução vs K
    plt.figure(figsize=(10, 6))
    plt.errorbar(k_vals, time_naive, yerr=time_naive_std, marker='o', label='Naive (AoS)',
                 capsize=5, linewidth=2, markersize=8, color='#3498db')
    plt.errorbar(k_vals, time_opt_no_unroll, yerr=time_opt_no_unroll_std, marker='s',
                 label='Optimized (SoA, no-unroll)', capsize=5, linewidth=2, markersize=8, color='#e74c3c')
    plt.errorbar(k_vals, time_opt, yerr=time_opt_std, marker='^', label='Optimized (SoA, with-unroll)',
                 capsize=5, linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Execution Time vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'time_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Cycles vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, cycles_naive, marker='o', label='Naive (AoS)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, cycles_opt_no_unroll, marker='s', label='Optimized (SoA, no-unroll)',
             linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, cycles_opt, marker='^', label='Optimized (SoA, with-unroll)',
             linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('CPU Cycles (billions)', fontsize=12)
    plt.title('CPU Cycles vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'cycles_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Cache Misses vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, cache_misses_naive, marker='o', label='Naive (AoS)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, cache_misses_opt_no_unroll, marker='s', label='Optimized (SoA, no-unroll)',
             linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, cache_misses_opt, marker='^', label='Optimized (SoA, with-unroll)',
             linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Cache Misses (millions)', fontsize=12)
    plt.title('Cache Misses vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'cache_misses_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. IPC vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, ipc_naive, marker='o', label='Naive (AoS)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, ipc_opt_no_unroll, marker='s', label='Optimized (SoA, no-unroll)',
             linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, ipc_opt, marker='^', label='Optimized (SoA, with-unroll)',
             linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Instructions Per Cycle (IPC)', fontsize=12)
    plt.title('IPC vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'ipc_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 5. Branches vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, branches_naive, marker='o', label='Naive (AoS)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, branches_opt_no_unroll, marker='s', label='Optimized (SoA, no-unroll)',
             linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, branches_opt, marker='^', label='Optimized (SoA, with-unroll)',
             linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Branches (billions)', fontsize=12)
    plt.title('Branch Instructions vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'branches_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 6. Speedup vs K (2 linhas: naive-to-opt e unroll effect)
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, speedup_naive_to_opt, marker='o', linewidth=2, markersize=8,
             color='#2ecc71', label='Speedup (Naive → With-Unroll)')
    plt.plot(k_vals, speedup_unroll_effect, marker='s', linewidth=2, markersize=8,
             color='#e67e22', label='Unroll Effect (No-Unroll → With-Unroll)')
    plt.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, label='No speedup')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Speedup', fontsize=12)
    plt.title('Speedup vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'speedup_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 7. Gráfico comparativo multi-métrica (3 versões)
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    metrics_data = [
        (time_naive, time_opt_no_unroll, time_opt, 'Time (s)', axes[0, 0]),
        (cycles_naive, cycles_opt_no_unroll, cycles_opt, 'Cycles (B)', axes[0, 1]),
        (cache_misses_naive, cache_misses_opt_no_unroll, cache_misses_opt, 'Cache Misses (M)', axes[0, 2]),
        (ipc_naive, ipc_opt_no_unroll, ipc_opt, 'IPC', axes[1, 0]),
        (branches_naive, branches_opt_no_unroll, branches_opt, 'Branches (B)', axes[1, 1]),
        (speedup_naive_to_opt, speedup_unroll_effect, None, 'Speedup', axes[1, 2])
    ]

    for i, data_tuple in enumerate(metrics_data):
        if i < 5:  # Regular metrics
            naive_data, opt_no_unroll_data, opt_data, ylabel, ax = data_tuple
            ax.plot(k_vals, naive_data, marker='o', label='Naive', linewidth=2, markersize=6, color='#3498db')
            ax.plot(k_vals, opt_no_unroll_data, marker='s', label='No-Unroll', linewidth=2, markersize=6, color='#e74c3c')
            ax.plot(k_vals, opt_data, marker='^', label='With-Unroll', linewidth=2, markersize=6, color='#2ecc71')
        else:  # Speedup plot
            speedup1, speedup2, _, ylabel, ax = data_tuple
            ax.plot(k_vals, speedup1, marker='o', linewidth=2, markersize=6, color='#2ecc71', label='N→WU')
            ax.plot(k_vals, speedup2, marker='s', linewidth=2, markersize=6, color='#e67e22', label='NU→WU')
            ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1)

        ax.set_xlabel('K', fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(ylabel, fontsize=11, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(k_vals)

    plt.tight_layout()
    plt.savefig(output_path / 'all_metrics_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\nGraphs generated:")
    print(f"  - {output_path / 'time_vs_k.png'}")
    print(f"  - {output_path / 'cycles_vs_k.png'}")
    print(f"  - {output_path / 'cache_misses_vs_k.png'}")
    print(f"  - {output_path / 'ipc_vs_k.png'}")
    print(f"  - {output_path / 'branches_vs_k.png'}")
    print(f"  - {output_path / 'speedup_vs_k.png'}")
    print(f"  - {output_path / 'all_metrics_vs_k.png'}")

def generate_text_analysis(k_values, all_metrics, output_file):
    """Gera análise em texto para 3 versões"""

    k_vals = sorted([int(k) for k in k_values])

    with open(output_file, 'w') as f:
        f.write("=" * 100 + "\n")
        f.write("  K-MEANS ANALYSIS: IMPACT OF K ON PERFORMANCE (3 VERSIONS)\n")
        f.write("=" * 100 + "\n\n")

        f.write("EXECUTION TIME COMPARISON\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'K':<5} {'Naive (s)':<15} {'No-Unroll (s)':<15} {'With-Unroll (s)':<18} {'N→WU':<10} {'NU→WU':<10}\n")
        f.write("-" * 100 + "\n")

        for k in k_vals:
            m = all_metrics[k]
            speedup_full = m['time_naive'] / m['time_opt'] if m['time_opt'] > 0 else 0
            speedup_unroll = m['time_opt_no_unroll'] / m['time_opt'] if m['time_opt'] > 0 else 0
            f.write(f"{k:<5} {m['time_naive']:<15.3f} {m['time_opt_no_unroll']:<15.3f} "
                   f"{m['time_opt']:<18.3f} {speedup_full:<10.2f}x {speedup_unroll:<10.2f}x\n")

        f.write("\n")
        f.write("DETAILED METRICS BY K\n")
        f.write("-" * 100 + "\n")

        for k in k_vals:
            m = all_metrics[k]
            f.write(f"\nK = {k}\n")
            f.write("-" * 60 + "\n")

            f.write(f"  Naive (AoS):\n")
            f.write(f"    Time:           {m['time_naive']:.3f} s\n")
            f.write(f"    Cycles:         {m['cycles_naive']/1e9:.2f} B\n")
            f.write(f"    Instructions:   {m['instructions_naive']/1e9:.2f} B\n")
            f.write(f"    IPC:            {m['ipc_naive']:.2f}\n")
            f.write(f"    Cache misses:   {m['cache_misses_naive']/1e6:.2f} M\n")
            f.write(f"    Branches:       {m['branches_naive']/1e9:.2f} B\n")
            f.write(f"    Branch misses:  {m['branch_misses_naive']/1e6:.2f} M\n")

            f.write(f"\n  Optimized (SoA, No-Unroll):\n")
            f.write(f"    Time:           {m['time_opt_no_unroll']:.3f} s\n")
            f.write(f"    Cycles:         {m['cycles_opt_no_unroll']/1e9:.2f} B\n")
            f.write(f"    Instructions:   {m['instructions_opt_no_unroll']/1e9:.2f} B\n")
            f.write(f"    IPC:            {m['ipc_opt_no_unroll']:.2f}\n")
            f.write(f"    Cache misses:   {m['cache_misses_opt_no_unroll']/1e6:.2f} M\n")
            f.write(f"    Branches:       {m['branches_opt_no_unroll']/1e9:.2f} B\n")
            f.write(f"    Branch misses:  {m['branch_misses_opt_no_unroll']/1e6:.2f} M\n")

            f.write(f"\n  Optimized (SoA, With-Unroll):\n")
            f.write(f"    Time:           {m['time_opt']:.3f} s\n")
            f.write(f"    Cycles:         {m['cycles_opt']/1e9:.2f} B\n")
            f.write(f"    Instructions:   {m['instructions_opt']/1e9:.2f} B\n")
            f.write(f"    IPC:            {m['ipc_opt']:.2f}\n")
            f.write(f"    Cache misses:   {m['cache_misses_opt']/1e6:.2f} M\n")
            f.write(f"    Branches:       {m['branches_opt']/1e9:.2f} B\n")
            f.write(f"    Branch misses:  {m['branch_misses_opt']/1e6:.2f} M\n")

            speedup_full = m['time_naive'] / m['time_opt'] if m['time_opt'] > 0 else 0
            speedup_unroll = m['time_opt_no_unroll'] / m['time_opt'] if m['time_opt'] > 0 else 0
            f.write(f"\n  Speedup (Naive → With-Unroll):     {speedup_full:.2f}x\n")
            f.write(f"  Unroll Effect (No-Unroll → With-Unroll): {speedup_unroll:.2f}x\n")

        f.write("\n" + "=" * 100 + "\n")

def main():
    if len(sys.argv) < 3:
        print("Usage: analyze_k_values.py <results_dir> <k_values>")
        sys.exit(1)

    results_dir = sys.argv[1]
    k_values = sys.argv[2].split()

    print(f"Analyzing results for K values: {k_values}")

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
    text_output = Path(results_dir) / "k_analysis.txt"
    generate_text_analysis(all_metrics.keys(), all_metrics, text_output)
    print(f"\nText analysis saved to: {text_output}")

    # Gerar gráficos
    generate_k_analysis_graphs(all_metrics.keys(), all_metrics, results_dir)

    print("\nAnalysis complete!")

if __name__ == '__main__':
    main()
