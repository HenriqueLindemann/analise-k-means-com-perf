# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:19:28

## Executive Summary

**Overall Speedup**: 0.94x

The optimized version is **1.06x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 2.129s | ±0.012s |
| Optimized | 2.256s | ±0.002s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 9,293,964,696 | 9,851,896,286 | 1.06x | -6.0% (Worse) |
| Instructions | 31,576,382,107 | 37,072,492,357 | 1.17x | -17.4% (Worse) |
| IPC | 3.40 | 3.76 | 1.11x | +10.8% (Better) |
| Cache references | 152,215,400 | 161,156,822 | 1.06x | -5.9% (Worse) |
| Cache misses | 87,646,876 | 37,917,201 | 0.43x | +56.7% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 9,988,873,181 | 14,037,421,160 | 1.41x | -40.5% (Worse) |
| L1 dcache misses | 34,026,014 | 88,208,730 | 2.59x | -159.2% (Worse) |
| L1 miss rate (%) | 0.34 | 0.63 | 1.85x | -85.3% (Worse) |
| Branches | 1,590,342,513 | 1,249,094,280 | 0.79x | +21.5% (Better) |
| Branch misses | 1,134,781 | 54,854 | 0.05x | +95.2% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
