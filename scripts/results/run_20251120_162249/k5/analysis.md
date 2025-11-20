# K-means Performance Analysis Report

**Generated**: 2025-11-20 16:24:56

## Executive Summary

**Overall Speedup**: 2.27x

The optimized version is **2.27x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.447s | ±0.019s |
| Optimized | 0.637s | ±0.006s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 6,309,944,592 | 2,728,751,694 | 0.43x | +56.8% (Better) |
| Instructions | 19,934,059,526 | 7,784,362,666 | 0.39x | +60.9% (Better) |
| IPC | 3.16 | 2.85 | 0.90x | -9.7% (Worse) |
| Cache references | 143,151,845 | 144,704,926 | 1.01x | -1.1% (Worse) |
| Cache misses | 86,596,941 | 44,053,343 | 0.51x | +49.1% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 6,510,434,004 | 4,041,293,358 | 0.62x | +37.9% (Better) |
| L1 dcache misses | 51,475,373 | 73,341,541 | 1.42x | -42.5% (Worse) |
| L1 miss rate (%) | 0.79 | 1.81 | 2.29x | -129.1% (Worse) |
| LLC loads | 6,301,613 | 2,560,986 | 0.41x | +59.4% (Better) |
| LLC misses | 5,825,019 | 2,024,015 | 0.35x | +65.3% (Better) |
| LLC miss rate (%) | 92.44 | 79.03 | 0.85x | +14.5% (Better) |
| Branches | 1,225,853,221 | 165,719,608 | 0.14x | +86.5% (Better) |
| Branch misses | 784,635 | 75,071 | 0.10x | +90.4% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
