# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:57:50

## Executive Summary

**Overall Speedup**: 0.94x

The optimized version is **1.06x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 2.128s | ±0.012s |
| Optimized | 2.262s | ±0.003s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 9,281,431,133 | 9,877,124,643 | 1.06x | -6.4% (Worse) |
| Instructions | 31,568,416,072 | 37,072,349,409 | 1.17x | -17.4% (Worse) |
| IPC | 3.40 | 3.75 | 1.10x | +10.4% (Better) |
| Cache references | 152,290,948 | 161,128,931 | 1.06x | -5.8% (Worse) |
| Cache misses | 87,827,791 | 37,830,639 | 0.43x | +56.9% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 9,988,860,534 | 14,033,610,845 | 1.40x | -40.5% (Worse) |
| L1 dcache misses | 32,858,270 | 98,569,651 | 3.00x | -200.0% (Worse) |
| L1 miss rate (%) | 0.33 | 0.70 | 2.12x | -112.1% (Worse) |
| LLC loads | 3,981,961 | 2,789,536 | 0.70x | +29.9% (Better) |
| LLC misses | 3,410,276 | 1,855,703 | 0.54x | +45.6% (Better) |
| LLC miss rate (%) | 85.64 | 66.52 | 0.78x | +22.3% (Better) |
| Branches | 1,589,982,860 | 1,248,265,544 | 0.79x | +21.5% (Better) |
| Branch misses | 1,138,216 | 53,812 | 0.05x | +95.3% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
