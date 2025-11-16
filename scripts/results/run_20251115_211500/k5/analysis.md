# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:16:24

## Executive Summary

**Overall Speedup**: 2.26x

The optimized version is **2.26x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.384s | ±0.011s |
| Optimized | 0.614s | ±0.007s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 6,037,919,216 | 2,630,903,721 | 0.44x | +56.4% (Better) |
| Instructions | 20,212,458,371 | 7,878,905,297 | 0.39x | +61.0% (Better) |
| IPC | 3.35 | 2.99 | 0.89x | -10.5% (Worse) |
| Cache references | 143,065,343 | 144,561,892 | 1.01x | -1.0% (Worse) |
| Cache misses | 87,932,564 | 44,092,611 | 0.50x | +49.9% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 6,515,162,278 | 4,213,334,102 | 0.65x | +35.3% (Better) |
| L1 dcache misses | 18,184,907 | 86,255,453 | 4.74x | -374.3% (Worse) |
| L1 miss rate (%) | 0.28 | 2.05 | 7.32x | -632.1% (Worse) |
| Branches | 1,226,414,324 | 167,304,037 | 0.14x | +86.4% (Better) |
| Branch misses | 775,888 | 45,083 | 0.06x | +94.2% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
