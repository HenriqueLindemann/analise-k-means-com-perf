#!/usr/bin/env python3
"""
Script de depuração para analisar um único arquivo perf_raw.txt e imprimir as métricas extraídas.
"""

import sys
import re
from pathlib import Path
import numpy as np
import json

def parse_single_perf_file(perf_file):
    """Analisa a saída do perf stat de um único arquivo para várias versões."""
    print(f"--- DEBUG: Parsing file {perf_file} ---")
    try:
        with open(perf_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"--- DEBUG: File not found: {perf_file}")
        return {}

    parsed_sections = {}
    
    sections = re.split(r'={40}', content)
    
    version_map = {
        'naive VERSION': 'naive',
        'optimized_no_unroll VERSION': 'optimized_no_unroll',
        'optimized VERSION': 'optimized'
    }

    for i, section in enumerate(sections):
        if len(section.strip()) == 0:
            continue
        
        print(f"\n--- DEBUG: Processing section {i} ---")
        print("--- Section Content Start ---")
        print(section)
        print("--- Section Content End ---\n")
        
        current_version_key = None
        for title, key in version_map.items():
            if title in section:
                if key == 'optimized' and 'no_unroll' in section:
                    continue
                current_version_key = key
                break
        
        if not current_version_key:
            print(f"--- DEBUG: Section {i} did not match any known version title.")
            continue

        print(f"--- DEBUG: Matched version '{current_version_key}' for section {i} ---")
        
        metrics = {}
        
        def get_metric(metric_name, pattern, text):
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                value_str = match.group(1).replace(',', '')
                try:
                    metrics[metric_name] = float(value_str)
                    print(f"--- DEBUG: Matched '{metric_name}': raw='{match.group(1)}', parsed={metrics[metric_name]}")
                except (ValueError, TypeError):
                    print(f"--- DEBUG: ValueError for '{metric_name}' with raw value '{match.group(1)}'")
                    metrics[metric_name] = 0.0
            else:
                print(f"--- DEBUG: No match for '{metric_name}' with pattern '{pattern}'")
                metrics[metric_name] = 0.0

        # ... (rest of the function is the same)
        time_match = re.search(r'([\d.]+)\s+\+-\s+([\d.]+)\s+seconds time elapsed', section)
        if time_match:
            metrics['time'] = float(time_match.group(1))
            metrics['time_std'] = float(time_match.group(2))
        else:
            metrics['time'] = 0.0
            metrics['time_std'] = 0.0

        get_metric('cycles', r'(\d[\d,.]*)\s+cpu_core/cycles/', section)
        get_metric('instructions', r'(\d[\d,.]*)\s+cpu_core/instructions/', section)
        get_metric('cache_refs', r'(\d[\d,.]*)\s+cpu_core/cache-references/', section)
        get_metric('cache_misses', r'(\d[\d,.]*)\s+cpu_core/cache-misses/', section)
        
        if metrics.get('cycles', 0) > 0:
            ipc_match = re.search(r'#\s+([\d.,]+)\s+insn per cycle', section)
            if ipc_match:
                metrics['ipc'] = float(ipc_match.group(1).replace(',', '.'))
            else:
                metrics['ipc'] = metrics.get('instructions', 0) / metrics['cycles']
        else:
            metrics['ipc'] = 0.0
        
        parsed_sections[current_version_key] = metrics

    return parsed_sections

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 debug_parser.py <path_to_perf_raw.txt>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    # Executa a análise
    final_metrics = parse_single_perf_file(file_path)
    
    # Imprime o resultado de forma legível
    print("\n--- DEBUG: Final Parsed Metrics ---")
    print(json.dumps(final_metrics, indent=4))

if __name__ == '__main__':
    main()