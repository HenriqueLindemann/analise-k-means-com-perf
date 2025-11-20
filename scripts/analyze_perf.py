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

    # Dividir em seções naive, optimized_no_unroll e optimized
    sections = content.split('========================================')

    results = {'naive': {}, 'optimized_no_unroll': {}, 'optimized': {}}
    current_version = None

    for section in sections:
        if 'naive VERSION' in section:
            current_version = 'naive'
        elif 'optimized_no_unroll VERSION' in section:
            current_version = 'optimized_no_unroll'
        elif 'optimized VERSION' in section:
            current_version = 'optimized'

        if current_version:
            # Extrair métricas
            # Formato: número cpu_core/metric_name/
            # Números podem ter . ou , como separadores de milhares

            # Cycles
            match = re.search(r'([\d.,]+)\s+cpu_core/cycles/', section)
            if match:
                value = match.group(1).replace('.', '').replace(',', '')
                results[current_version]['cycles'] = int(value)

            # Instructions
            match = re.search(r'([\d.,]+)\s+cpu_core/instructions/', section)
            if match:
                value = match.group(1).replace('.', '').replace(',', '')
                results[current_version]['instructions'] = int(value)

            # IPC (pode estar na linha de instructions ou separado)
            match = re.search(r'#\s+([\d.,]+)\s+insn per cycle', section)
            if match:
                ipc_str = match.group(1).replace(',', '.')
                results[current_version]['ipc'] = float(ipc_str)

            # Cache references
            match = re.search(r'([\d.,]+)\s+cpu_core/cache-references/', section)
            if match:
                value = match.group(1).replace('.', '').replace(',', '')
                results[current_version]['cache_refs'] = int(value)

            # Cache misses
            match = re.search(r'([\d.,]+)\s+cpu_core/cache-misses/', section)
            if match:
                value = match.group(1).replace('.', '').replace(',', '')
                results[current_version]['cache_misses'] = int(value)

            # Cache miss rate
            match = re.search(r'cache-misses/.*#\s+([\d.,]+)%', section)
            if match:
                rate_str = match.group(1).replace(',', '.')
                results[current_version]['cache_miss_rate'] = float(rate_str)

            # L1 dcache loads
            match = re.search(r'([\d.,]+)\s+cpu_core/L1-dcache-loads/', section)
            if match:
                value = match.group(1).replace('.', '').replace(',', '')
                results[current_version]['l1_loads'] = int(value)

            # L1 dcache load misses
            match = re.search(r'([\d.,]+)\s+cpu_core/L1-dcache-load-misses/', section)
            if match:
                value = match.group(1).replace('.', '').replace(',', '')
                results[current_version]['l1_misses'] = int(value)

            # L1 miss rate
            match = re.search(r'L1-dcache-load-misses/.*#\s+([\d.,]+)%', section)
            if match:
                rate_str = match.group(1).replace(',', '.')
                results[current_version]['l1_miss_rate'] = float(rate_str)

            # LLC loads
            match = re.search(r'([\d.,]+)\s+cpu_core/LLC-loads/', section)
            if match:
                value = match.group(1).replace('.', '').replace(',', '')
                results[current_version]['llc_loads'] = int(value)

            # LLC misses
            match = re.search(r'([\d.,]+)\s+cpu_core/LLC-load-misses/', section)
            if match:
                value = match.group(1).replace('.', '').replace(',', '')
                results[current_version]['llc_misses'] = int(value)

            # LLC miss rate
            match = re.search(r'LLC-load-misses/.*#\s+([\d.,]+)%', section)
            if match:
                rate_str = match.group(1).replace(',', '.')
                results[current_version]['llc_miss_rate'] = float(rate_str)

            # Branches
            match = re.search(r'([\d.,]+)\s+cpu_core/branches/', section)
            if match:
                value = match.group(1).replace('.', '').replace(',', '')
                results[current_version]['branches'] = int(value)

            # Branch misses
            match = re.search(r'([\d.,]+)\s+cpu_core/branch-misses/', section)
            if match:
                value = match.group(1).replace('.', '').replace(',', '')
                results[current_version]['branch_misses'] = int(value)

            # Branch miss rate
            match = re.search(r'branch-misses/.*#\s+([\d.,]+)%', section)
            if match:
                rate_str = match.group(1).replace(',', '.')
                results[current_version]['branch_miss_rate'] = float(rate_str)

            # Time
            match = re.search(r'([\d.]+)\s+\+-\s+([\d.]+)\s+seconds time elapsed', section)
            if match:
                results[current_version]['time'] = float(match.group(1))
                results[current_version]['time_std'] = float(match.group(2))

    # Calcular IPC se não foi extraído
    for version in ['naive', 'optimized_no_unroll', 'optimized']:
        if 'ipc' not in results[version] or results[version].get('ipc', 0) == 0:
            cycles = results[version].get('cycles', 0)
            instructions = results[version].get('instructions', 0)
            if cycles > 0 and instructions > 0:
                results[version]['ipc'] = instructions / cycles

    return results

def print_comparison(results):
    """Imprime comparação formatada"""

    naive = results['naive']
    opt_no_unroll = results['optimized_no_unroll']
    opt = results['optimized']

    print("\n" + "="*80)
    print("  K-MEANS PERFORMANCE ANALYSIS (perf) - 3 VERSIONS")
    print("="*80 + "\n")

    # Tempo
    print("TIME")
    print("-" * 80)
    print(f"  Naive:              {naive.get('time', 0):.3f} ± {naive.get('time_std', 0):.3f} seconds")
    print(f"  Opt (no-unroll):    {opt_no_unroll.get('time', 0):.3f} ± {opt_no_unroll.get('time_std', 0):.3f} seconds")
    print(f"  Opt (with-unroll):  {opt.get('time', 0):.3f} ± {opt.get('time_std', 0):.3f} seconds")
    print()
    speedup_no_unroll = naive.get('time', 1) / opt_no_unroll.get('time', 1)
    speedup_unroll = naive.get('time', 1) / opt.get('time', 1)
    speedup_unroll_effect = opt_no_unroll.get('time', 1) / opt.get('time', 1)
    print(f"  Speedup (naive→no-unroll):  {speedup_no_unroll:.2f}x")
    print(f"  Speedup (naive→with-unroll): {speedup_unroll:.2f}x")
    print(f"  Speedup (unroll effect):     {speedup_unroll_effect:.2f}x {'✓ UNROLL HELPS!' if speedup_unroll_effect > 1 else '✗ NO BENEFIT'}")
    print()

    # Tabela comparativa
    print("DETAILED METRICS")
    print("-" * 100)
    print(f"{'Metric':<25} {'Naive':>15} {'No-Unroll':>15} {'With-Unroll':>15} {'N→NU':>8} {'N→WU':>8} {'NU→WU':>8}")
    print("-" * 100)

    def print_metric(name, key, lower_better=True):
        n = naive.get(key, 0)
        nu = opt_no_unroll.get(key, 0)
        wu = opt.get(key, 0)
        ratio_nu = nu / n if n > 0 else 0
        ratio_wu = wu / n if n > 0 else 0
        ratio_unroll = wu / nu if nu > 0 else 0

        print(f"{name:<25} {n:>15,} {nu:>15,} {wu:>15,} {ratio_nu:>8.2f}x {ratio_wu:>8.2f}x {ratio_unroll:>8.2f}x")

    def print_metric_float(name, key, lower_better=True):
        n = naive.get(key, 0)
        nu = opt_no_unroll.get(key, 0)
        wu = opt.get(key, 0)
        ratio_nu = nu / n if n > 0 else 0
        ratio_wu = wu / n if n > 0 else 0
        ratio_unroll = wu / nu if nu > 0 else 0

        print(f"{name:<25} {n:>15.2f} {nu:>15.2f} {wu:>15.2f} {ratio_nu:>8.2f}x {ratio_wu:>8.2f}x {ratio_unroll:>8.2f}x")

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

    print_metric("LLC loads", "llc_loads", lower_better=True)
    print_metric("LLC misses", "llc_misses", lower_better=True)
    print_metric_float("LLC miss rate (%)", "llc_miss_rate", lower_better=True)
    print()

    print_metric("Branches", "branches", lower_better=True)
    print_metric("Branch misses", "branch_misses", lower_better=True)
    print_metric_float("Branch miss rate (%)", "branch_miss_rate", lower_better=True)

    print("\n" + "="*100)

    # Summary
    print("\nKEY INSIGHTS:")
    print("-" * 100)

    # Unroll effect
    if speedup_unroll_effect > 1.05:
        improvement = (speedup_unroll_effect - 1) * 100
        print(f"✓✓ UNROLL EFFECT: {speedup_unroll_effect:.2f}x speedup ({improvement:.1f}% faster with unroll!)")
    elif speedup_unroll_effect > 1.0:
        improvement = (speedup_unroll_effect - 1) * 100
        print(f"✓ Unroll helps slightly: {speedup_unroll_effect:.2f}x ({improvement:.1f}% faster)")
    else:
        print(f"✗ Unroll has no benefit or makes it worse: {speedup_unroll_effect:.2f}x")

    # Cache comparison
    if opt.get('cache_misses', 1) < opt_no_unroll.get('cache_misses', 0):
        improvement = (1 - opt['cache_misses'] / opt_no_unroll['cache_misses']) * 100
        print(f"✓ Unroll reduces cache misses by {improvement:.1f}%")

    # IPC comparison
    if opt.get('ipc', 0) > opt_no_unroll.get('ipc', 1):
        improvement = (opt['ipc'] / opt_no_unroll['ipc'] - 1) * 100
        print(f"✓ Unroll improves IPC by {improvement:.1f}%")

    # Overall
    if speedup_unroll > 1:
        print(f"✓ Overall best speedup (naive→with-unroll): {speedup_unroll:.2f}x faster")
    else:
        print(f"✗ Overall slowdown: {1/speedup_unroll:.2f}x slower")

def generate_graphs(results, output_dir):
    """Gera gráficos de comparação de performance"""

    naive = results['naive']
    opt_no_unroll = results['optimized_no_unroll']
    opt = results['optimized']

    output_path = Path(output_dir) / 'graphs' / 'performance'
    output_path.mkdir(parents=True, exist_ok=True)

    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    colors = ['#3498db', '#e74c3c', '#2ecc71']  # Blue, Red, Green

    # 1. Execution time comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    versions = ['Naive\n(AoS)', 'Optimized\n(SoA, no-unroll)', 'Optimized\n(SoA, with-unroll)']
    times = [naive.get('time', 0), opt_no_unroll.get('time', 0), opt.get('time', 0)]
    bars = ax.bar(versions, times, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Version', fontsize=12, fontweight='bold')
    ax.set_title('Execution Time Comparison', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(times) * 1.15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height * 1.02,
                f'{height:.3f}s',
                ha='center', va='bottom', fontweight='bold', fontsize=11)

    plt.tight_layout()
    plt.savefig(output_path / 'execution_time.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Cache misses comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    cache_misses = [naive.get('cache_misses', 0) / 1e6, opt_no_unroll.get('cache_misses', 0) / 1e6, opt.get('cache_misses', 0) / 1e6]
    bars = ax.bar(versions, cache_misses, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Cache Misses (millions)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Version', fontsize=12, fontweight='bold')
    ax.set_title('Cache Misses Comparison', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(cache_misses) * 1.15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height * 1.02,
                f'{height:.1f}M',
                ha='center', va='bottom', fontweight='bold', fontsize=11)

    plt.tight_layout()
    plt.savefig(output_path / 'cache_misses.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. IPC comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    ipc_values = [naive.get('ipc', 0), opt_no_unroll.get('ipc', 0), opt.get('ipc', 0)]
    bars = ax.bar(versions, ipc_values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('IPC (Instructions Per Cycle)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Version', fontsize=12, fontweight='bold')
    ax.set_title('IPC Comparison', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(ipc_values) * 1.15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height * 1.02,
                f'{height:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)

    plt.tight_layout()
    plt.savefig(output_path / 'ipc.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. Multi-metric comparison (LOG scale)
    fig, ax = plt.subplots(figsize=(14, 8))

    metrics_for_comparison = {
        'Time\n(s)': (naive.get('time', 1), opt_no_unroll.get('time', 1), opt.get('time', 1)),
        'Cycles\n(billions)': (naive.get('cycles', 1) / 1e9, opt_no_unroll.get('cycles', 1) / 1e9, opt.get('cycles', 1) / 1e9),
        'Instructions\n(billions)': (naive.get('instructions', 1) / 1e9, opt_no_unroll.get('instructions', 1) / 1e9, opt.get('instructions', 1) / 1e9),
        'Cache Misses\n(millions)': (naive.get('cache_misses', 1) / 1e6, opt_no_unroll.get('cache_misses', 1) / 1e6, opt.get('cache_misses', 1) / 1e6),
        'L1 Misses\n(millions)': (naive.get('l1_misses', 1) / 1e6, opt_no_unroll.get('l1_misses', 1) / 1e6, opt.get('l1_misses', 1) / 1e6),
        'Branches\n(millions)': (naive.get('branches', 1) / 1e6, opt_no_unroll.get('branches', 1) / 1e6, opt.get('branches', 1) / 1e6),
    }

    x = np.arange(len(metrics_for_comparison))
    width = 0.25

    naive_vals = [v[0] for v in metrics_for_comparison.values()]
    no_unroll_vals = [v[1] for v in metrics_for_comparison.values()]
    opt_vals = [v[2] for v in metrics_for_comparison.values()]

    bars1 = ax.bar(x - width, naive_vals, width, label='Naive',
                   color=colors[0], alpha=0.8, edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x, no_unroll_vals, width, label='Opt (no-unroll)',
                   color=colors[1], alpha=0.8, edgecolor='black', linewidth=1.2)
    bars3 = ax.bar(x + width, opt_vals, width, label='Opt (with-unroll)',
                   color=colors[2], alpha=0.8, edgecolor='black', linewidth=1.2)

    ax.set_ylabel('Value (log scale)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Metric', fontsize=12, fontweight='bold')
    ax.set_title('Performance Metrics Comparison (Log Scale)', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_for_comparison.keys(), fontsize=10, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3, which='both', linestyle='--')

    plt.tight_layout()
    plt.savefig(output_path / 'metrics_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 5. Unroll Effect - Improvement from no-unroll to with-unroll
    fig, ax = plt.subplots(figsize=(10, 6))

    unroll_effects = {
        'Execution Time': ((opt_no_unroll.get('time', 1) - opt.get('time', 1)) / opt_no_unroll.get('time', 1) * 100),
        'Cycles': ((opt_no_unroll.get('cycles', 1) - opt.get('cycles', 1)) / opt_no_unroll.get('cycles', 1) * 100),
        'Instructions': ((opt_no_unroll.get('instructions', 1) - opt.get('instructions', 1)) / opt_no_unroll.get('instructions', 1) * 100),
        'Cache Misses': ((opt_no_unroll.get('cache_misses', 1) - opt.get('cache_misses', 1)) / opt_no_unroll.get('cache_misses', 1) * 100),
        'Branches': ((opt_no_unroll.get('branches', 1) - opt.get('branches', 1)) / opt_no_unroll.get('branches', 1) * 100),
    }

    metrics_names = list(unroll_effects.keys())
    improvement_values = list(unroll_effects.values())
    colors_improvement = ['#2ecc71' if v > 0 else '#e74c3c' for v in improvement_values]

    bars = ax.barh(metrics_names, improvement_values, color=colors_improvement,
                   alpha=0.8, edgecolor='black', linewidth=1.2)
    ax.set_xlabel('Improvement (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Metric', fontsize=12, fontweight='bold')
    ax.set_title('UNROLL EFFECT: Improvement (No-Unroll → With-Unroll)', fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1.5)
    ax.grid(axis='x', alpha=0.3, linestyle='--')

    # Set xlim to prevent overlap with y-axis labels
    max_abs = max(abs(min(improvement_values)), abs(max(improvement_values)))
    ax.set_xlim(-max_abs * 1.2, max_abs * 1.2)

    for i, (bar, val) in enumerate(zip(bars, improvement_values)):
        # Position text outside the bar
        offset = max_abs * 0.03
        ax.text(val + (offset if val > 0 else -offset), i, f'{val:+.1f}%',
                ha='left' if val > 0 else 'right', va='center', fontweight='bold', fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path / 'unroll_effect.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 6. Cache Hierarchy Comparison (L1 vs LLC)
    fig, ax = plt.subplots(figsize=(10, 6))

    cache_levels = ['L1 Data Cache', 'Last Level Cache (LLC)']
    x = np.arange(len(cache_levels))
    width = 0.25

    naive_miss_rates = [
        naive.get('l1_miss_rate', 0),
        naive.get('llc_miss_rate', 0)
    ]
    no_unroll_miss_rates = [
        opt_no_unroll.get('l1_miss_rate', 0),
        opt_no_unroll.get('llc_miss_rate', 0)
    ]
    opt_miss_rates = [
        opt.get('l1_miss_rate', 0),
        opt.get('llc_miss_rate', 0)
    ]

    bars1 = ax.bar(x - width, naive_miss_rates, width,
                   label='Naive (AoS)', color=colors[0], alpha=0.8,
                   edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x, no_unroll_miss_rates, width,
                   label='Opt (no-unroll)', color=colors[1], alpha=0.8,
                   edgecolor='black', linewidth=1.2)
    bars3 = ax.bar(x + width, opt_miss_rates, width,
                   label='Opt (with-unroll)', color=colors[2], alpha=0.8,
                   edgecolor='black', linewidth=1.2)

    ax.set_ylabel('Miss Rate (%) - Log Scale', fontsize=12, fontweight='bold')
    ax.set_xlabel('Cache Level', fontsize=12, fontweight='bold')
    ax.set_title('Cache Hierarchy Miss Rates (Log Scale)', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels(cache_levels, fontsize=10, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3, which='both', linestyle='--')

    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height * 1.02,
                        f'{height:.2f}%',
                        ha='center', va='bottom', fontweight='bold', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path / 'cache_hierarchy.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 7. Efficiency Metrics Dashboard
    fig, ax = plt.subplots(figsize=(12, 7))

    # Calculate derived metrics
    naive_branch_accuracy = 100 - naive.get('branch_miss_rate', 0)
    no_unroll_branch_accuracy = 100 - opt_no_unroll.get('branch_miss_rate', 0)
    opt_branch_accuracy = 100 - opt.get('branch_miss_rate', 0)

    naive_l1_hit_rate = 100 - naive.get('l1_miss_rate', 0)
    no_unroll_l1_hit_rate = 100 - opt_no_unroll.get('l1_miss_rate', 0)
    opt_l1_hit_rate = 100 - opt.get('l1_miss_rate', 0)

    naive_llc_hit_rate = 100 - naive.get('llc_miss_rate', 0)
    no_unroll_llc_hit_rate = 100 - opt_no_unroll.get('llc_miss_rate', 0)
    opt_llc_hit_rate = 100 - opt.get('llc_miss_rate', 0)

    efficiency_metrics = ['IPC\n(higher=better)', 'Branch Prediction\nAccuracy (%)',
                         'L1 Cache\nHit Rate (%)', 'LLC\nHit Rate (%)']
    x = np.arange(len(efficiency_metrics))
    width = 0.25

    naive_efficiency = [
        naive.get('ipc', 0),
        naive_branch_accuracy,
        naive_l1_hit_rate,
        naive_llc_hit_rate
    ]
    no_unroll_efficiency = [
        opt_no_unroll.get('ipc', 0),
        no_unroll_branch_accuracy,
        no_unroll_l1_hit_rate,
        no_unroll_llc_hit_rate
    ]
    opt_efficiency = [
        opt.get('ipc', 0),
        opt_branch_accuracy,
        opt_l1_hit_rate,
        opt_llc_hit_rate
    ]

    bars1 = ax.bar(x - width, naive_efficiency, width,
                   label='Naive (AoS)', color=colors[0], alpha=0.8,
                   edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x, no_unroll_efficiency, width,
                   label='Opt (no-unroll)', color=colors[1], alpha=0.8,
                   edgecolor='black', linewidth=1.2)
    bars3 = ax.bar(x + width, opt_efficiency, width,
                   label='Opt (with-unroll)', color=colors[2], alpha=0.8,
                   edgecolor='black', linewidth=1.2)


    ax.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax.set_xlabel('Efficiency Metric', fontsize=12, fontweight='bold')
    ax.set_title('Efficiency Metrics Dashboard', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(efficiency_metrics, fontsize=10, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    max_val = max(max(naive_efficiency), max(no_unroll_efficiency), max(opt_efficiency))
    ax.set_ylim(0, max_val * 1.15)

    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for i, bar in enumerate(bars):
            height = bar.get_height()
            text = f'{height:.2f}' if i == 0 else f'{height:.1f}%'
            ax.text(bar.get_x() + bar.get_width()/2., height * 1.02,
                    text, ha='center', va='bottom', fontweight='bold', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path / 'efficiency_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 8. Memory Access Cost Analysis (MPKI - Misses Per Kilo Instructions)
    fig, ax = plt.subplots(figsize=(12, 7))

    # Calculate MPKI for different cache levels
    naive_l1_mpki = (naive.get('l1_misses', 0) / naive.get('instructions', 1)) * 1000
    no_unroll_l1_mpki = (opt_no_unroll.get('l1_misses', 0) / opt_no_unroll.get('instructions', 1)) * 1000
    opt_l1_mpki = (opt.get('l1_misses', 0) / opt.get('instructions', 1)) * 1000
    
    naive_llc_mpki = (naive.get('llc_misses', 0) / naive.get('instructions', 1)) * 1000
    no_unroll_llc_mpki = (opt_no_unroll.get('llc_misses', 0) / opt_no_unroll.get('instructions', 1)) * 1000
    opt_llc_mpki = (opt.get('llc_misses', 0) / opt.get('instructions', 1)) * 1000
    
    mpki_types = ['L1 MPKI', 'LLC MPKI']
    x = np.arange(len(mpki_types))
    width = 0.25

    naive_mpki = [naive_l1_mpki, naive_llc_mpki]
    no_unroll_mpki = [no_unroll_l1_mpki, no_unroll_llc_mpki]
    opt_mpki = [opt_l1_mpki, opt_llc_mpki]

    bars1 = ax.bar(x - width, naive_mpki, width,
                   label='Naive (AoS)', color=colors[0], alpha=0.8,
                   edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x, no_unroll_mpki, width,
                   label='Opt (no-unroll)', color=colors[1], alpha=0.8,
                   edgecolor='black', linewidth=1.2)
    bars3 = ax.bar(x + width, opt_mpki, width,
                   label='Opt (with-unroll)', color=colors[2], alpha=0.8,
                   edgecolor='black', linewidth=1.2)

    ax.set_ylabel('MPKI (Misses Per 1000 Instructions) - Log Scale', fontsize=12, fontweight='bold')
    ax.set_xlabel('Cache Level', fontsize=12, fontweight='bold')
    ax.set_title('Memory Access Cost Analysis (MPKI) - Log Scale', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels(mpki_types, fontsize=10, fontweight='bold')
    ax.legend(fontsize=11, loc='upper center')
    ax.grid(axis='y', alpha=0.3, which='both', linestyle='--')

    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height * 1.02,
                        f'{height:.2f}',
                        ha='center', va='bottom', fontweight='bold', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path / 'memory_access_cost.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 9. Instruction Mix Analysis
    fig, ax = plt.subplots(figsize=(12, 7))

    # Calculate derived metrics about instruction execution
    naive_cycles_per_inst = naive.get('cycles', 1) / naive.get('instructions', 1)
    no_unroll_cycles_per_inst = opt_no_unroll.get('cycles', 1) / opt_no_unroll.get('instructions', 1)
    opt_cycles_per_inst = opt.get('cycles', 1) / opt.get('instructions', 1)

    naive_inst_per_cache_miss = naive.get('instructions', 1) / naive.get('cache_misses', 1) if naive.get('cache_misses', 0) > 0 else 0
    no_unroll_inst_per_cache_miss = opt_no_unroll.get('instructions', 1) / opt_no_unroll.get('cache_misses', 1) if opt_no_unroll.get('cache_misses', 0) > 0 else 0
    opt_inst_per_cache_miss = opt.get('instructions', 1) / opt.get('cache_misses', 1) if opt.get('cache_misses', 0) > 0 else 0

    naive_inst_per_branch = naive.get('instructions', 1) / naive.get('branches', 1) if naive.get('branches', 0) > 0 else 0
    no_unroll_inst_per_branch = opt_no_unroll.get('instructions', 1) / opt_no_unroll.get('branches', 1) if opt_no_unroll.get('branches', 0) > 0 else 0
    opt_inst_per_branch = opt.get('instructions', 1) / opt.get('branches', 1) if opt.get('branches', 0) > 0 else 0

    inst_metrics = ['Cycles Per\nInstruction\n(lower=better)',
                   'Instructions Per\nCache Miss\n(higher=better)',
                   'Instructions Per\nBranch\n(neutral)']
    x = np.arange(len(inst_metrics))
    width = 0.25

    naive_inst_analysis = [
        naive_cycles_per_inst,
        naive_inst_per_cache_miss,
        naive_inst_per_branch
    ]
    no_unroll_inst_analysis = [
        no_unroll_cycles_per_inst,
        no_unroll_inst_per_cache_miss,
        no_unroll_inst_per_branch
    ]
    opt_inst_analysis = [
        opt_cycles_per_inst,
        opt_inst_per_cache_miss,
        opt_inst_per_branch
    ]

    bars1 = ax.bar(x - width, naive_inst_analysis, width,
                   label='Naive (AoS)', color=colors[0], alpha=0.8,
                   edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x, no_unroll_inst_analysis, width,
                   label='Opt (no-unroll)', color=colors[1], alpha=0.8,
                   edgecolor='black', linewidth=1.2)
    bars3 = ax.bar(x + width, opt_inst_analysis, width,
                   label='Opt (with-unroll)', color=colors[2], alpha=0.8,
                   edgecolor='black', linewidth=1.2)

    ax.set_ylabel('Value - Log Scale', fontsize=12, fontweight='bold')
    ax.set_xlabel('Metric', fontsize=12, fontweight='bold')
    ax.set_title('Instruction Execution Analysis (Log Scale)', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels(inst_metrics, fontsize=9, fontweight='bold')
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(axis='y', alpha=0.3, which='both', linestyle='--')
    
    # Set y-axis limits to avoid overlap
    max_y_val = max(max(naive_inst_analysis), max(no_unroll_inst_analysis), max(opt_inst_analysis))
    ax.set_ylim(min(min(naive_inst_analysis), min(no_unroll_inst_analysis), min(opt_inst_analysis)) * 0.8, max_y_val * 1.5)

    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height * 1.05,
                        f'{height:.2f}',
                        ha='center', va='bottom', fontweight='bold', fontsize=8, rotation=90)

    plt.tight_layout()
    plt.savefig(output_path / 'instruction_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

    return [
        'execution_time.png',
        'cache_misses.png',
        'ipc.png',
        'metrics_comparison.png',
        'improvements.png',
        'cache_hierarchy.png',
        'efficiency_dashboard.png',
        'memory_access_cost.png',
        'instruction_analysis.png'
    ]

def generate_cluster_visualizations(k, dataset_path, output_dir):
    """Gera visualizações dos clusters usando ambas as versões"""
    import subprocess
    from pathlib import Path

    output_path = Path(output_dir) / 'graphs' / 'clusters'
    output_path.mkdir(parents=True, exist_ok=True)
    base_output_path = Path(output_dir)

    # Gerar clusters para ambas as versões
    for version in ['naive', 'optimized']:
        cluster_file = base_output_path / f'clusters_{version}.csv'

        # Executar cluster_save
        cmd = f'bin/cluster_save {version} {k} {dataset_path} {base_output_path / "clusters"}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Warning: Failed to generate clusters for {version}")
            continue

    # Gerar plots combinados
    naive_file = base_output_path / 'clusters_naive.csv'
    opt_file = base_output_path / 'clusters_optimized.csv'

    if naive_file.exists() and opt_file.exists():
        # Importar pandas para análise
        import pandas as pd

        naive_df = pd.read_csv(naive_file)
        opt_df = pd.read_csv(opt_file)

        # 1. Scatter plot comparando clusters (primeiras 2 features)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Naive
        scatter1 = ax1.scatter(naive_df.iloc[:, 0], naive_df.iloc[:, 1],
                              c=naive_df['cluster'], cmap='tab10',
                              alpha=0.5, s=10, edgecolors='none')
        ax1.set_xlabel('Global Active Power', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Global Reactive Power', fontsize=11, fontweight='bold')
        ax1.set_title('K-means Clustering - Naive', fontsize=13, fontweight='bold')
        ax1.grid(alpha=0.3)
        plt.colorbar(scatter1, ax=ax1, label='Cluster ID')

        # Optimized
        scatter2 = ax2.scatter(opt_df.iloc[:, 0], opt_df.iloc[:, 1],
                              c=opt_df['cluster'], cmap='tab10',
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

        naive_counts = naive_df['cluster'].value_counts().sort_index()
        opt_counts = opt_df['cluster'].value_counts().sort_index()

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
        feature_cols = [col for col in naive_df.columns if col != 'cluster']
        naive_means = naive_df.groupby('cluster')[feature_cols].mean()
        opt_means = opt_df.groupby('cluster')[feature_cols].mean()

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
            ('LLC loads', 'llc_loads', True),
            ('LLC misses', 'llc_misses', True),
            ('LLC miss rate (%)', 'llc_miss_rate', True),
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
        print("Usage: python3 analyze_perf.py <perf_results.txt> [output.md] [k] [dataset_path]")
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

        # Gerar visualizações de clusters se fornecidos k e dataset_path
        if len(sys.argv) > 4:
            k = int(sys.argv[3])
            dataset_path = sys.argv[4]
            print(f"\nGenerating cluster visualizations (K={k})...")
            try:
                cluster_graphs = generate_cluster_visualizations(k, dataset_path, output_dir)
                if cluster_graphs:
                    print(f"\nCluster visualizations generated:")
                    for graph in cluster_graphs:
                        print(f"  - {output_dir / graph}")
            except Exception as e:
                print(f"Warning: Failed to generate cluster visualizations: {e}")
