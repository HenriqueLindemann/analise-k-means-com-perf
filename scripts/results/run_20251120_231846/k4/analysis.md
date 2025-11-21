# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:19:30

## Executive Summary

**Overall Speedup**: 1.49x

The optimized version is **1.49x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.315s | ±0.005s |
| Optimized | 0.211s | ±0.002s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 1,371,921,894 | 914,944,411 | 0.67x | +33.3% (Better) |
| Instructions | 4,168,084,137 | 2,397,730,108 | 0.58x | +42.5% (Better) |
| IPC | 3.04 | 2.62 | 0.86x | -13.7% (Worse) |
| Cache references | 32,813,630 | 32,858,595 | 1.00x | -0.1% (Worse) |
| Cache misses | 20,596,171 | 9,831,304 | 0.48x | +52.3% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 1,293,613,405 | 954,628,910 | 0.74x | +26.2% (Better) |
| L1 dcache misses | 13,401,095 | 23,724,067 | 1.77x | -77.0% (Worse) |
| L1 miss rate (%) | 1.04 | 2.49 | 2.39x | -139.4% (Worse) |
| LLC loads | 2,156,725 | 1,414,895 | 0.66x | +34.4% (Better) |
| LLC misses | 2,000,947 | 1,003,118 | 0.50x | +49.9% (Better) |
| LLC miss rate (%) | 92.78 | 70.90 | 0.76x | +23.6% (Better) |
| Branches | 327,738,598 | 126,795,431 | 0.39x | +61.3% (Better) |
| Branch misses | 515,680 | 407,069 | 0.79x | +21.1% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
