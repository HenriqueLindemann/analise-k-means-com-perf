# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:17:50

## Executive Summary

**Overall Speedup**: 0.97x

The optimized version is **1.03x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.598s | ±0.006s |
| Optimized | 0.614s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 2,607,509,824 | 2,674,028,110 | 1.03x | -2.6% (Worse) |
| Instructions | 8,438,053,005 | 9,906,256,396 | 1.17x | -17.4% (Worse) |
| IPC | 3.24 | 3.70 | 1.14x | +14.5% (Better) |
| Cache references | 45,085,285 | 47,726,254 | 1.06x | -5.9% (Worse) |
| Cache misses | 25,927,633 | 12,697,549 | 0.49x | +51.0% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 2,679,822,725 | 3,814,870,201 | 1.42x | -42.4% (Worse) |
| L1 dcache misses | 20,065,078 | 25,365,718 | 1.26x | -26.4% (Worse) |
| L1 miss rate (%) | 0.75 | 0.66 | 0.88x | +12.0% (Better) |
| Branches | 473,000,963 | 371,368,506 | 0.79x | +21.5% (Better) |
| Branch misses | 497,730 | 43,859 | 0.09x | +91.2% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
