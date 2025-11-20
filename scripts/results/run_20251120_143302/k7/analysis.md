# K-means Performance Analysis Report

**Generated**: 2025-11-20 14:35:35

## Executive Summary

**Overall Speedup**: 2.50x

The optimized version is **2.50x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.626s | ±0.007s |
| Optimized | 0.250s | ±0.002s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 2,695,005,416 | 1,060,120,597 | 0.39x | +60.7% (Better) |
| Instructions | 8,312,018,512 | 2,987,254,402 | 0.36x | +64.1% (Better) |
| IPC | 3.08 | 2.82 | 0.91x | -8.6% (Worse) |
| Cache references | 45,255,297 | 46,932,531 | 1.04x | -3.7% (Worse) |
| Cache misses | 27,933,739 | 15,455,550 | 0.55x | +44.7% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 2,678,341,642 | 1,448,951,374 | 0.54x | +45.9% (Better) |
| L1 dcache misses | 20,099,604 | 24,795,412 | 1.23x | -23.4% (Worse) |
| L1 miss rate (%) | 0.75 | 1.71 | 2.28x | -128.0% (Worse) |
| LLC loads | 2,855,107 | 1,174,143 | 0.41x | +58.9% (Better) |
| LLC misses | 2,655,198 | 999,834 | 0.38x | +62.3% (Better) |
| LLC miss rate (%) | 93.00 | 85.15 | 0.92x | +8.4% (Better) |
| Branches | 472,724,634 | 105,381,743 | 0.22x | +77.7% (Better) |
| Branch misses | 525,981 | 62,479 | 0.12x | +88.1% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
