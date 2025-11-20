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

def parse_perf_output(file_path):
    """Extrai métricas do output do perf usando uma abordagem de máquina de estados."""
    with open(file_path, 'r') as f:
        content = f.read()

    sections = content.split('========================================')
    results = {'naive': {}, 'optimized_no_unroll': {}, 'optimized': {}}
    current_version = None

    for section in sections:
        # Atualiza o estado da máquina (versão atual) se um título for encontrado
        if 'naive VERSION' in section:
            current_version = 'naive'
        elif 'optimized_no_unroll VERSION' in section:
            current_version = 'optimized_no_unroll'
        # Garante que 'optimized' não corresponda a 'optimized_no_unroll'
        elif 'optimized VERSION' in section and 'no_unroll' not in section:
            current_version = 'optimized'

        # Se uma versão foi definida, tenta analisar as métricas desta seção
        if current_version:
            # Extrai tempo e desvio padrão
            match = re.search(r'([\d.]+)\s+\+-\s+([\d.]+)\s+seconds time elapsed', section)
            if match and 'time' not in results[current_version]:
                results[current_version]['time'] = float(match.group(1))
                results[current_version]['time_std'] = float(match.group(2))

            # Extrai métricas brutas
            raw_metrics = {
                'cycles': r'(\d[\d,.]*)\s+cpu_core/cycles/',
                'instructions': r'(\d[\d,.]*)\s+cpu_core/instructions/',
                'cache_refs': r'(\d[\d,.]*)\s+cpu_core/cache-references/',
                'cache_misses': r'(\d[\d,.]*)\s+cpu_core/cache-misses/',
                'l1_loads': r'(\d[\d,.]*)\s+cpu_core/L1-dcache-loads/',
                'l1_misses': r'(\d[\d,.]*)\s+cpu_core/L1-dcache-load-misses/',
                'llc_loads': r'(\d[\d,.]*)\s+cpu_core/LLC-loads/',
                'llc_misses': r'(\d[\d,.]*)\s+cpu_core/LLC-load-misses/',
                'branches': r'(\d[\d,.]*)\s+cpu_core/branches/',
                'branch_misses': r'(\d[\d,.]*)\s+cpu_core/branch-misses/',
            }
            for key, pattern in raw_metrics.items():
                match = re.search(pattern, section)
                if match and key not in results[current_version]:
                     # Remove separadores de milhar e de decimal para conversão
                    value_str = match.group(1).replace(',', '').replace('.', '')
                    results[current_version][key] = int(value_str)

    # Achata o dicionário aninhado para o formato esperado pelas funções de plotagem
    flat_results = {}
    for version, metrics in results.items():
        if not metrics: continue
        version_key_map = {
            'naive': 'naive',
            'optimized_no_unroll': 'opt_no_unroll',
            'optimized': 'opt'
        }
        suffix = version_key_map[version]
        for name, value in metrics.items():
            if name == 'time_std':
                flat_results[f"time_{suffix}_std"] = value
            else:
                flat_results[f"{name}_{suffix}"] = value
    
    # Calcula métricas derivadas que podem não ter sido extraídas diretamente
    for suffix in ['naive', 'opt_no_unroll', 'opt']:
        if f'cycles_{suffix}' in flat_results and flat_results[f'cycles_{suffix}'] > 0:
            if f'ipc_{suffix}' not in flat_results:
                 flat_results[f'ipc_{suffix}'] = flat_results.get(f'instructions_{suffix}', 0) / flat_results[f'cycles_{suffix}']
        else:
            flat_results[f'ipc_{suffix}'] = 0

    return flat_results

def generate_comparison_graphs(k_values, all_metrics, output_dir):
    """Gera gráficos comparativos para 3 versões"""

    output_path = Path(output_dir) / "k_comparison" / "graphs"
    output_path.mkdir(parents=True, exist_ok=True)

    # Preparar dados para as 3 versões
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

    instructions_naive = [all_metrics[k]['instructions_naive'] / 1e9 for k in k_vals]
    instructions_opt_no_unroll = [all_metrics[k]['instructions_opt_no_unroll'] / 1e9 for k in k_vals]
    instructions_opt = [all_metrics[k]['instructions_opt'] / 1e9 for k in k_vals]

    cache_misses_naive = [all_metrics[k]['cache_misses_naive'] / 1e6 for k in k_vals]
    cache_misses_opt_no_unroll = [all_metrics[k]['cache_misses_opt_no_unroll'] / 1e6 for k in k_vals]
    cache_misses_opt = [all_metrics[k]['cache_misses_opt'] / 1e6 for k in k_vals]

    # Calcular cache hit rate para todas as versões
    cache_hit_rate_naive = [(all_metrics[k]['cache_refs_naive'] - all_metrics[k]['cache_misses_naive']) / all_metrics[k]['cache_refs_naive'] * 100
                            if all_metrics[k]['cache_refs_naive'] > 0 else 0 for k in k_vals]
    cache_hit_rate_opt_no_unroll = [(all_metrics[k]['cache_refs_opt_no_unroll'] - all_metrics[k]['cache_misses_opt_no_unroll']) / all_metrics[k]['cache_refs_opt_no_unroll'] * 100
                                     if all_metrics[k]['cache_refs_opt_no_unroll'] > 0 else 0 for k in k_vals]
    cache_hit_rate_opt = [(all_metrics[k]['cache_refs_opt'] - all_metrics[k]['cache_misses_opt']) / all_metrics[k]['cache_refs_opt'] * 100
                          if all_metrics[k]['cache_refs_opt'] > 0 else 0 for k in k_vals]

    ipc_naive = [all_metrics[k]['ipc_naive'] for k in k_vals]
    ipc_opt_no_unroll = [all_metrics[k]['ipc_opt_no_unroll'] for k in k_vals]
    ipc_opt = [all_metrics[k]['ipc_opt'] for k in k_vals]

    branches_naive = [all_metrics[k]['branches_naive'] / 1e9 for k in k_vals]
    branches_opt_no_unroll = [all_metrics[k]['branches_opt_no_unroll'] / 1e9 for k in k_vals]
    branches_opt = [all_metrics[k]['branches_opt'] / 1e9 for k in k_vals]

    speedup_naive = [1.0 for _ in k_vals]
    speedup_opt_no_unroll = [all_metrics[k]['time_naive'] / all_metrics[k]['time_opt_no_unroll'] if all_metrics[k].get('time_opt_no_unroll', 0) > 0 else 0 for k in k_vals]
    speedup_opt = [all_metrics[k]['time_naive'] / all_metrics[k]['time_opt'] if all_metrics[k].get('time_opt', 0) > 0 else 0 for k in k_vals]

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

    # 3. Instructions vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, instructions_naive, marker='o', label='Naive (AoS)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, instructions_opt_no_unroll, marker='s', label='Optimized (SoA, no-unroll)',
             linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, instructions_opt, marker='^', label='Optimized (SoA, with-unroll)',
             linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Instructions (billions)', fontsize=12)
    plt.title('Number of Instructions vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'instructions_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. Cache Misses vs K
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

    # 5. Cache Hit Rate vs K
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, cache_hit_rate_naive, marker='o', label='Naive (AoS)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, cache_hit_rate_opt_no_unroll, marker='s', label='Optimized (SoA, no-unroll)',
             linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, cache_hit_rate_opt, marker='^', label='Optimized (SoA, with-unroll)',
             linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Cache Hit Rate (%)', fontsize=12)
    plt.title('Cache Hit Rate vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'cache_hit_rate_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 6. IPC vs K
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

    # 7. Branches vs K
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

    # 8. Speedup vs K (Relativo ao Naive)
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, speedup_naive, marker='o', linestyle='--', label='Naive (Baseline)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, speedup_opt_no_unroll, marker='s', label='Speedup (No-Unroll vs Naive)', linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, speedup_opt, marker='^', label='Speedup (With-Unroll vs Naive)', linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Speedup (relative to Naive)', fontsize=12)
    plt.title('Speedup vs K (Relative to Naive)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'speedup_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 9. Cache Miss Rate vs K (porcentagem)
    cache_miss_rate_naive = [(all_metrics[k]['cache_misses_naive'] / all_metrics[k]['cache_refs_naive'] * 100)
                              if all_metrics[k].get('cache_refs_naive', 0) > 0 else 0 for k in k_vals]
    cache_miss_rate_opt_no_unroll = [(all_metrics[k]['cache_misses_opt_no_unroll'] / all_metrics[k]['cache_refs_opt_no_unroll'] * 100)
                                      if all_metrics[k].get('cache_refs_opt_no_unroll', 0) > 0 else 0 for k in k_vals]
    cache_miss_rate_opt = [(all_metrics[k]['cache_misses_opt'] / all_metrics[k]['cache_refs_opt'] * 100)
                            if all_metrics[k].get('cache_refs_opt', 0) > 0 else 0 for k in k_vals]

    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, cache_miss_rate_naive, marker='o', label='Naive (AoS)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, cache_miss_rate_opt_no_unroll, marker='s', label='Optimized (SoA, no-unroll)',
             linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, cache_miss_rate_opt, marker='^', label='Optimized (SoA, with-unroll)',
             linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Cache Miss Rate (%) - L2/L3', fontsize=12)
    plt.title('General Cache Miss Rate vs K (L2/L3)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'cache_miss_rate_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 10. L1 Cache Miss Rate vs K
    l1_miss_rate_naive = [(all_metrics[k]['l1_misses_naive'] / all_metrics[k]['l1_loads_naive'] * 100)
                          if all_metrics[k].get('l1_loads_naive', 0) > 0 else 0 for k in k_vals]
    l1_miss_rate_opt_no_unroll = [(all_metrics[k]['l1_misses_opt_no_unroll'] / all_metrics[k]['l1_loads_opt_no_unroll'] * 100)
                                   if all_metrics[k].get('l1_loads_opt_no_unroll', 0) > 0 else 0 for k in k_vals]
    l1_miss_rate_opt = [(all_metrics[k]['l1_misses_opt'] / all_metrics[k]['l1_loads_opt'] * 100)
                        if all_metrics[k].get('l1_loads_opt', 0) > 0 else 0 for k in k_vals]

    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, l1_miss_rate_naive, marker='o', label='Naive (AoS)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, l1_miss_rate_opt_no_unroll, marker='s', label='Optimized (SoA, no-unroll)',
             linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, l1_miss_rate_opt, marker='^', label='Optimized (SoA, with-unroll)',
             linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('L1 Cache Miss Rate (%)', fontsize=12)
    plt.title('L1 Data Cache Miss Rate vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'l1_cache_miss_rate_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 11. LLC (L3) Cache Miss Rate vs K
    llc_miss_rate_naive = [(all_metrics[k]['llc_misses_naive'] / all_metrics[k]['llc_loads_naive'] * 100)
                           if all_metrics[k].get('llc_loads_naive', 0) > 0 else 0 for k in k_vals]
    llc_miss_rate_opt_no_unroll = [(all_metrics[k]['llc_misses_opt_no_unroll'] / all_metrics[k]['llc_loads_opt_no_unroll'] * 100)
                                    if all_metrics[k].get('llc_loads_opt_no_unroll', 0) > 0 else 0 for k in k_vals]
    llc_miss_rate_opt = [(all_metrics[k]['llc_misses_opt'] / all_metrics[k]['llc_loads_opt'] * 100)
                         if all_metrics[k].get('llc_loads_opt', 0) > 0 else 0 for k in k_vals]

    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, llc_miss_rate_naive, marker='o', label='Naive (AoS)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, llc_miss_rate_opt_no_unroll, marker='s', label='Optimized (SoA, no-unroll)',
             linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, llc_miss_rate_opt, marker='^', label='Optimized (SoA, with-unroll)',
             linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('LLC (L3) Miss Rate (%)', fontsize=12)
    plt.title('Last Level Cache Miss Rate vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'llc_miss_rate_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 12. Comparação de todos os níveis de cache em um só gráfico
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    # L1 Cache
    ax1.plot(k_vals, l1_miss_rate_naive, marker='o', label='Naive', linewidth=2, markersize=6, color='#3498db')
    ax1.plot(k_vals, l1_miss_rate_opt_no_unroll, marker='s', label='No-Unroll', linewidth=2, markersize=6, color='#e74c3c')
    ax1.plot(k_vals, l1_miss_rate_opt, marker='^', label='With-Unroll', linewidth=2, markersize=6, color='#2ecc71')
    ax1.set_xlabel('K', fontsize=11)
    ax1.set_ylabel('L1 Miss Rate (%)', fontsize=11)
    ax1.set_title('L1 Data Cache', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(k_vals)

    # L2/L3 Cache (general)
    ax2.plot(k_vals, cache_miss_rate_naive, marker='o', label='Naive', linewidth=2, markersize=6, color='#3498db')
    ax2.plot(k_vals, cache_miss_rate_opt_no_unroll, marker='s', label='No-Unroll', linewidth=2, markersize=6, color='#e74c3c')
    ax2.plot(k_vals, cache_miss_rate_opt, marker='^', label='With-Unroll', linewidth=2, markersize=6, color='#2ecc71')
    ax2.set_xlabel('K', fontsize=11)
    ax2.set_ylabel('Miss Rate (%)', fontsize=11)
    ax2.set_title('L2/L3 Cache', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(k_vals)

    # LLC (L3)
    ax3.plot(k_vals, llc_miss_rate_naive, marker='o', label='Naive', linewidth=2, markersize=6, color='#3498db')
    ax3.plot(k_vals, llc_miss_rate_opt_no_unroll, marker='s', label='No-Unroll', linewidth=2, markersize=6, color='#e74c3c')
    ax3.plot(k_vals, llc_miss_rate_opt, marker='^', label='With-Unroll', linewidth=2, markersize=6, color='#2ecc71')
    ax3.set_xlabel('K', fontsize=11)
    ax3.set_ylabel('LLC Miss Rate (%)', fontsize=11)
    ax3.set_title('Last Level Cache (L3)', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_xticks(k_vals)

    plt.tight_layout()
    plt.savefig(output_path / 'all_cache_levels_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 13. Número de Instruções vs K (absoluto em bilhões)
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, instructions_naive, marker='o', label='Naive (AoS)', linewidth=2, markersize=8, color='#3498db')
    plt.plot(k_vals, instructions_opt_no_unroll, marker='s', label='Optimized (SoA, no-unroll)',
             linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(k_vals, instructions_opt, marker='^', label='Optimized (SoA, with-unroll)',
             linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('K (number of clusters)', fontsize=12)
    plt.ylabel('Number of Instructions (billions)', fontsize=12)
    plt.title('Number of Instructions vs K', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_vals)
    plt.tight_layout()
    plt.savefig(output_path / 'instructions_count_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 14. Gráfico comparativo multi-métrica (3 versões)
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Performance Metrics vs. K', fontsize=16, fontweight='bold')

    metrics_data = [
        (time_naive, time_opt_no_unroll, time_opt, 'Time (s)', axes[0, 0]),
        (cycles_naive, cycles_opt_no_unroll, cycles_opt, 'Cycles (B)', axes[0, 1]),
        (cache_misses_naive, cache_misses_opt_no_unroll, cache_misses_opt, 'Cache Misses (M)', axes[0, 2]),
        (ipc_naive, ipc_opt_no_unroll, ipc_opt, 'IPC', axes[1, 0]),
        (branches_naive, branches_opt_no_unroll, branches_opt, 'Branches (B)', axes[1, 1]),
        (speedup_naive, speedup_opt_no_unroll, speedup_opt, 'Speedup vs Naive', axes[1, 2])
    ]

    for data_tuple in metrics_data:
        d_naive, d_opt_no_unroll, d_opt, ylabel, ax = data_tuple
        ax.plot(k_vals, d_naive, marker='o', label='Naive', linewidth=2, markersize=6, color='#3498db')
        ax.plot(k_vals, d_opt_no_unroll, marker='s', label='No-Unroll', linewidth=2, markersize=6, color='#e74c3c')
        ax.plot(k_vals, d_opt, marker='^', label='With-Unroll', linewidth=2, markersize=6, color='#2ecc71')

        if ylabel == 'Speedup vs Naive':
            ax.lines[0].set_linestyle('--') # Linha base Naive

        ax.set_xlabel('K', fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(ylabel, fontsize=11, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(k_vals)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path / 'all_metrics_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\nComparison graphs generated:")
    for graph in ['time_vs_k', 'cycles_vs_k', 'cache_misses_vs_k', 'cache_miss_rate_vs_k',
                  'l1_cache_miss_rate_vs_k', 'llc_miss_rate_vs_k', 'all_cache_levels_vs_k',
                  'ipc_vs_k', 'branches_vs_k', 'speedup_vs_k', 'instructions_count_vs_k', 'all_metrics_vs_k']:
        print(f"  - {output_path / (graph + '.png')}")

def generate_text_analysis(k_values, all_metrics, output_file):
    """Gera análise em texto para 3 versões"""

    k_vals = sorted([int(k) for k in k_values])

    with open(output_file, 'w') as f:
        f.write("=" * 100 + "\n")
        f.write("  K-MEANS COMPARISON: IMPACT OF K ON PERFORMANCE (3 VERSIONS)\n")
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
