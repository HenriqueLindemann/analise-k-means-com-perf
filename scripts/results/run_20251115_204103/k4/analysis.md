# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:41:27

## Executive Summary

**Overall Speedup**: 0.91x

The optimized version is **1.10x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.503s | ±0.010s |
| Optimized | 0.552s | ±0.007s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 1,409,040,072 | 1,507,748,808 | 1.07x | -7.0% (Worse) |
| Instructions | 4,210,316,177 | 4,971,178,597 | 1.18x | -18.1% (Worse) |
| IPC | 0 | 0 | 0.00x | +0.0% (Worse) |
| Cache references | 32,696,096 | 32,949,829 | 1.01x | -0.8% (Worse) |
| Cache misses | 22,702,029 | 12,413,142 | 0.55x | +45.3% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 1,297,251,459 | 1,985,552,240 | 1.53x | -53.1% (Worse) |
| L1 dcache misses | 2,433,484 | 10,888,452 | 4.47x | -347.4% (Worse) |
| L1 miss rate (%) | 0.19 | 0.55 | 2.89x | -189.5% (Worse) |
| Branches | 328,396,753 | 247,342,332 | 0.75x | +24.7% (Better) |
| Branch misses | 550,692 | 65,617 | 0.12x | +88.1% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
