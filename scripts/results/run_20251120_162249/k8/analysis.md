# K-means Performance Analysis Report

**Generated**: 2025-11-20 16:28:34

## Executive Summary

**Overall Speedup**: 2.74x

The optimized version is **2.74x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 2.139s | ±0.017s |
| Optimized | 0.780s | ±0.007s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 9,337,975,499 | 3,345,999,135 | 0.36x | +64.2% (Better) |
| Instructions | 31,127,594,466 | 9,821,644,073 | 0.32x | +68.4% (Better) |
| IPC | 3.33 | 2.94 | 0.88x | -11.9% (Worse) |
| Cache references | 152,152,919 | 159,460,457 | 1.05x | -4.8% (Worse) |
| Cache misses | 88,801,116 | 43,502,931 | 0.49x | +51.0% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 9,990,155,250 | 4,949,016,305 | 0.50x | +50.5% (Better) |
| L1 dcache misses | 32,538,465 | 76,730,488 | 2.36x | -135.8% (Worse) |
| L1 miss rate (%) | 0.33 | 1.55 | 4.70x | -369.7% (Worse) |
| LLC loads | 4,079,048 | 2,198,948 | 0.54x | +46.1% (Better) |
| LLC misses | 3,539,452 | 1,667,247 | 0.47x | +52.9% (Better) |
| LLC miss rate (%) | 86.77 | 75.82 | 0.87x | +12.6% (Better) |
| Branches | 1,590,422,350 | 175,493,747 | 0.11x | +89.0% (Better) |
| Branch misses | 1,135,657 | 74,922 | 0.07x | +93.4% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
