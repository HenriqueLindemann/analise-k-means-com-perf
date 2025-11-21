# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:23:52

## Executive Summary

**Overall Speedup**: 2.52x

The optimized version is **2.52x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 2.123s | ±0.015s |
| Optimized | 0.841s | ±0.011s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 9,262,078,089 | 3,612,906,959 | 0.39x | +61.0% (Better) |
| Instructions | 31,126,735,719 | 10,150,275,396 | 0.33x | +67.4% (Better) |
| IPC | 3.36 | 2.81 | 0.84x | -16.4% (Worse) |
| Cache references | 152,192,141 | 159,421,854 | 1.05x | -4.8% (Worse) |
| Cache misses | 88,833,292 | 41,546,831 | 0.47x | +53.2% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 9,990,969,535 | 5,066,161,341 | 0.51x | +49.3% (Better) |
| L1 dcache misses | 28,055,865 | 80,013,246 | 2.85x | -185.2% (Worse) |
| L1 miss rate (%) | 0.28 | 1.58 | 5.64x | -464.3% (Worse) |
| LLC loads | 3,392,597 | 2,335,396 | 0.69x | +31.2% (Better) |
| LLC misses | 2,860,977 | 1,696,157 | 0.59x | +40.7% (Better) |
| LLC miss rate (%) | 84.33 | 72.63 | 0.86x | +13.9% (Better) |
| Branches | 1,590,606,462 | 174,398,646 | 0.11x | +89.0% (Better) |
| Branch misses | 1,135,047 | 72,145 | 0.06x | +93.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
