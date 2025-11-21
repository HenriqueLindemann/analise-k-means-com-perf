# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:20:45

## Executive Summary

**Overall Speedup**: 1.75x

The optimized version is **1.75x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.447s | ±0.021s |
| Optimized | 0.828s | ±0.007s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 6,314,782,195 | 3,602,145,123 | 0.57x | +43.0% (Better) |
| Instructions | 19,933,124,798 | 10,413,923,618 | 0.52x | +47.8% (Better) |
| IPC | 3.16 | 2.89 | 0.92x | -8.4% (Worse) |
| Cache references | 143,008,716 | 144,832,715 | 1.01x | -1.3% (Worse) |
| Cache misses | 86,124,348 | 36,559,527 | 0.42x | +57.6% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 6,509,582,001 | 4,186,873,704 | 0.64x | +35.7% (Better) |
| L1 dcache misses | 47,935,329 | 68,195,761 | 1.42x | -42.3% (Worse) |
| L1 miss rate (%) | 0.74 | 1.63 | 2.20x | -120.3% (Worse) |
| LLC loads | 6,097,565 | 2,050,672 | 0.34x | +66.4% (Better) |
| LLC misses | 5,584,521 | 1,527,791 | 0.27x | +72.6% (Better) |
| LLC miss rate (%) | 91.59 | 74.50 | 0.81x | +18.7% (Better) |
| Branches | 1,225,814,812 | 307,210,537 | 0.25x | +74.9% (Better) |
| Branch misses | 784,175 | 1,978,742 | 2.52x | -152.3% (Worse) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
