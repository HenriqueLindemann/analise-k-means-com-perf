# K-means Performance Analysis Report

**Generated**: 2025-11-20 14:33:07

## Executive Summary

**Overall Speedup**: 1.25x

The optimized version is **1.25x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.117s | ±0.001s |
| Optimized | 0.094s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 475,520,423 | 373,594,959 | 0.79x | +21.4% (Better) |
| Instructions | 1,381,201,772 | 927,829,453 | 0.67x | +32.8% (Better) |
| IPC | 2.90 | 2.48 | 0.86x | -14.5% (Worse) |
| Cache references | 13,740,231 | 13,840,608 | 1.01x | -0.7% (Worse) |
| Cache misses | 10,691,554 | 6,214,570 | 0.58x | +41.9% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 405,062,897 | 399,197,562 | 0.99x | +1.4% (Better) |
| L1 dcache misses | 1,788,765 | 8,069,843 | 4.51x | -351.1% (Worse) |
| L1 miss rate (%) | 0.44 | 2.02 | 4.59x | -359.1% (Worse) |
| LLC loads | 895,811 | 1,140,055 | 1.27x | -27.3% (Worse) |
| LLC misses | 848,572 | 975,791 | 1.15x | -15.0% (Worse) |
| LLC miss rate (%) | 94.73 | 85.59 | 0.90x | +9.6% (Better) |
| Branches | 162,569,522 | 84,502,564 | 0.52x | +48.0% (Better) |
| Branch misses | 68,121 | 62,951 | 0.92x | +7.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
