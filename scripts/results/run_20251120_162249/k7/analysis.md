# K-means Performance Analysis Report

**Generated**: 2025-11-20 16:26:38

## Executive Summary

**Overall Speedup**: 2.46x

The optimized version is **2.46x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.611s | ±0.007s |
| Optimized | 0.249s | ±0.003s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 2,665,096,114 | 1,063,861,550 | 0.40x | +60.1% (Better) |
| Instructions | 8,305,435,882 | 2,986,292,332 | 0.36x | +64.0% (Better) |
| IPC | 3.12 | 2.81 | 0.90x | -9.9% (Worse) |
| Cache references | 45,017,430 | 46,914,374 | 1.04x | -4.2% (Worse) |
| Cache misses | 26,734,479 | 14,439,045 | 0.54x | +46.0% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 2,681,388,678 | 1,458,889,254 | 0.54x | +45.6% (Better) |
| L1 dcache misses | 19,033,198 | 27,886,076 | 1.47x | -46.5% (Worse) |
| L1 miss rate (%) | 0.71 | 1.91 | 2.69x | -169.0% (Worse) |
| LLC loads | 2,672,126 | 1,281,473 | 0.48x | +52.0% (Better) |
| LLC misses | 2,509,790 | 1,066,166 | 0.42x | +57.5% (Better) |
| LLC miss rate (%) | 93.92 | 83.20 | 0.89x | +11.4% (Better) |
| Branches | 472,768,254 | 104,560,655 | 0.22x | +77.9% (Better) |
| Branch misses | 497,005 | 71,793 | 0.14x | +85.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
