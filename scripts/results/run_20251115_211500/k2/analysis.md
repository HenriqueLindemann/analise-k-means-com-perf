# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:15:05

## Executive Summary

**Overall Speedup**: 0.96x

The optimized version is **1.04x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.103s | ±0.001s |
| Optimized | 0.107s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 445,724,364 | 461,593,288 | 1.04x | -3.6% (Worse) |
| Instructions | 1,364,978,009 | 1,645,723,277 | 1.21x | -20.6% (Worse) |
| IPC | 3.06 | 3.57 | 1.16x | +16.4% (Better) |
| Cache references | 13,683,491 | 14,106,475 | 1.03x | -3.1% (Worse) |
| Cache misses | 10,345,085 | 5,202,603 | 0.50x | +49.7% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 403,280,663 | 667,285,881 | 1.65x | -65.5% (Worse) |
| L1 dcache misses | 2,527,830 | 11,442,646 | 4.53x | -352.7% (Worse) |
| L1 miss rate (%) | 0.63 | 1.71 | 2.71x | -171.4% (Worse) |
| Branches | 162,733,852 | 132,409,251 | 0.81x | +18.6% (Better) |
| Branch misses | 43,780 | 39,061 | 0.89x | +10.8% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
