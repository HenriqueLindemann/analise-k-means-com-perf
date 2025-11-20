# K-means Performance Analysis Report

**Generated**: 2025-11-20 14:33:36

## Executive Summary

**Overall Speedup**: 1.90x

The optimized version is **1.90x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.325s | ±0.005s |
| Optimized | 0.171s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 1,342,133,821 | 699,202,002 | 0.52x | +47.9% (Better) |
| Instructions | 4,178,377,850 | 1,911,809,830 | 0.46x | +54.2% (Better) |
| IPC | 3.11 | 2.73 | 0.88x | -12.2% (Worse) |
| Cache references | 32,565,130 | 32,458,572 | 1.00x | +0.3% (Better) |
| Cache misses | 22,517,650 | 13,050,599 | 0.58x | +42.0% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 1,297,007,543 | 929,532,267 | 0.72x | +28.3% (Better) |
| L1 dcache misses | 6,491,697 | 12,049,455 | 1.86x | -85.6% (Worse) |
| L1 miss rate (%) | 0.50 | 1.30 | 2.60x | -160.0% (Worse) |
| LLC loads | 1,461,131 | 996,882 | 0.68x | +31.8% (Better) |
| LLC misses | 1,370,579 | 879,011 | 0.64x | +35.9% (Better) |
| LLC miss rate (%) | 93.80 | 88.18 | 0.94x | +6.0% (Better) |
| Branches | 327,784,800 | 96,280,614 | 0.29x | +70.6% (Better) |
| Branch misses | 536,775 | 64,259 | 0.12x | +88.0% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
