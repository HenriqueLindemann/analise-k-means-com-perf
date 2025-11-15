# K-means Performance Analysis Report

**Generated**: 2025-11-15 00:10:18

## Executive Summary

**Overall Speedup**: 1.09x

The optimized version is **1.09x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.875s | ±0.028s |
| Optimized | 1.716s | ±0.048s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 7,011,135,712 | 6,901,734,708 | 0.98x | +1.6% (Better) |
| Instructions | 22,814,924,062 | 26,441,157,443 | 1.16x | -15.9% (Worse) |
| IPC | 3.25 | 3.83 | 1.18x | +17.8% (Better) |
| Cache references | 147,107,815 | 147,161,383 | 1.00x | -0.0% (Worse) |
| Cache misses | 93,676,633 | 41,700,151 | 0.45x | +55.5% (Better) |
| Cache miss rate (%) | 63.68 | 28.34 | 0.45x | +55.5% (Better) |
| L1 dcache loads | 6,763,190,571 | 12,409,594,586 | 1.83x | -83.5% (Worse) |
| L1 dcache misses | 4,492,053 | 48,823,872 | 10.87x | -986.9% (Worse) |
| L1 miss rate (%) | 0.07 | 0.39 | 5.57x | -457.1% (Worse) |
| Branches | 1,499,638,322 | 1,500,788,412 | 1.00x | -0.1% (Worse) |
| Branch misses | 866,626 | 992,659 | 1.15x | -14.5% (Worse) |
| Branch miss rate (%) | 0.06 | 0.07 | 1.17x | -16.7% (Worse) |
