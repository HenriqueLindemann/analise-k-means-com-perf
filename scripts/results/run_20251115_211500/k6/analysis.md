# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:17:16

## Executive Summary

**Overall Speedup**: 1.01x

The optimized version is **1.01x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.061s | ±0.010s |
| Optimized | 1.046s | ±0.003s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 4,630,272,529 | 4,565,601,030 | 0.99x | +1.4% (Better) |
| Instructions | 15,486,668,037 | 17,339,498,583 | 1.12x | -12.0% (Worse) |
| IPC | 3.34 | 3.80 | 1.14x | +13.6% (Better) |
| Cache references | 93,014,434 | 91,469,317 | 0.98x | +1.7% (Better) |
| Cache misses | 56,008,711 | 22,534,665 | 0.40x | +59.8% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 4,876,674,408 | 6,749,926,531 | 1.38x | -38.4% (Worse) |
| L1 dcache misses | 23,980,125 | 67,356,933 | 2.81x | -180.9% (Worse) |
| L1 miss rate (%) | 0.49 | 1.00 | 2.04x | -104.1% (Worse) |
| Branches | 909,489,993 | 652,202,130 | 0.72x | +28.3% (Better) |
| Branch misses | 835,320 | 46,613 | 0.06x | +94.4% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
