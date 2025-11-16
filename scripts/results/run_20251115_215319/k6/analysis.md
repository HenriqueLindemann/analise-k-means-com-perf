# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:55:37

## Executive Summary

**Overall Speedup**: 1.04x

The optimized version is **1.04x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.082s | ±0.011s |
| Optimized | 1.037s | ±0.002s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 4,720,824,945 | 4,524,270,296 | 0.96x | +4.2% (Better) |
| Instructions | 15,490,819,794 | 17,337,441,893 | 1.12x | -11.9% (Worse) |
| IPC | 3.28 | 3.83 | 1.17x | +16.8% (Better) |
| Cache references | 93,097,157 | 91,581,501 | 0.98x | +1.6% (Better) |
| Cache misses | 54,670,024 | 22,655,115 | 0.41x | +58.6% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 4,877,142,416 | 6,749,800,087 | 1.38x | -38.4% (Worse) |
| L1 dcache misses | 39,296,394 | 48,074,811 | 1.22x | -22.3% (Worse) |
| L1 miss rate (%) | 0.81 | 0.71 | 0.88x | +12.3% (Better) |
| LLC loads | 4,766,483 | 1,557,781 | 0.33x | +67.3% (Better) |
| LLC misses | 4,363,467 | 1,138,137 | 0.26x | +73.9% (Better) |
| LLC miss rate (%) | 91.54 | 73.06 | 0.80x | +20.2% (Better) |
| Branches | 909,664,850 | 651,602,629 | 0.72x | +28.4% (Better) |
| Branch misses | 831,886 | 46,893 | 0.06x | +94.4% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
