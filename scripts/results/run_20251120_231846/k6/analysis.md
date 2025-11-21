# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:21:40

## Executive Summary

**Overall Speedup**: 2.26x

The optimized version is **2.26x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.045s | ±0.006s |
| Optimized | 0.462s | ±0.005s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 4,560,963,705 | 1,980,221,503 | 0.43x | +56.6% (Better) |
| Instructions | 15,310,506,577 | 5,446,100,981 | 0.36x | +64.4% (Better) |
| IPC | 3.36 | 2.75 | 0.82x | -18.1% (Worse) |
| Cache references | 93,107,155 | 90,620,540 | 0.97x | +2.7% (Better) |
| Cache misses | 56,966,103 | 25,570,271 | 0.45x | +55.1% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 4,877,434,875 | 2,700,366,572 | 0.55x | +44.6% (Better) |
| L1 dcache misses | 13,060,353 | 52,199,278 | 4.00x | -299.7% (Worse) |
| L1 miss rate (%) | 0.27 | 1.93 | 7.15x | -614.8% (Worse) |
| LLC loads | 2,021,199 | 1,797,269 | 0.89x | +11.1% (Better) |
| LLC misses | 1,756,986 | 1,434,393 | 0.82x | +18.4% (Better) |
| LLC miss rate (%) | 86.93 | 79.81 | 0.92x | +8.2% (Better) |
| Branches | 909,673,551 | 132,127,781 | 0.15x | +85.5% (Better) |
| Branch misses | 833,479 | 70,371 | 0.08x | +91.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
