# K-means Performance Analysis Report

**Generated**: 2025-11-20 14:34:29

## Executive Summary

**Overall Speedup**: 2.23x

The optimized version is **2.23x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.511s | ±0.008s |
| Optimized | 0.678s | ±0.007s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 6,156,171,561 | 2,747,751,822 | 0.45x | +55.4% (Better) |
| Instructions | 19,956,397,645 | 7,788,510,756 | 0.39x | +61.0% (Better) |
| IPC | 3.24 | 2.83 | 0.87x | -12.6% (Worse) |
| Cache references | 143,550,803 | 144,723,459 | 1.01x | -0.8% (Worse) |
| Cache misses | 98,219,237 | 51,464,918 | 0.52x | +47.6% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 6,509,154,193 | 4,038,094,521 | 0.62x | +38.0% (Better) |
| L1 dcache misses | 6,479,489 | 46,943,415 | 7.24x | -624.5% (Worse) |
| L1 miss rate (%) | 0.10 | 1.16 | 11.60x | -1060.0% (Worse) |
| LLC loads | 1,510,472 | 1,825,548 | 1.21x | -20.9% (Worse) |
| LLC misses | 1,206,085 | 1,478,498 | 1.23x | -22.6% (Worse) |
| LLC miss rate (%) | 79.85 | 80.99 | 1.01x | -1.4% (Worse) |
| Branches | 1,226,211,771 | 167,257,405 | 0.14x | +86.4% (Better) |
| Branch misses | 826,175 | 71,186 | 0.09x | +91.4% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
