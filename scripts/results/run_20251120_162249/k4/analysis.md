# K-means Performance Analysis Report

**Generated**: 2025-11-20 16:23:35

## Executive Summary

**Overall Speedup**: 1.96x

The optimized version is **1.96x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.327s | ±0.006s |
| Optimized | 0.167s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 1,424,269,540 | 716,291,812 | 0.50x | +49.7% (Better) |
| Instructions | 4,176,064,159 | 1,909,888,789 | 0.46x | +54.3% (Better) |
| IPC | 2.93 | 2.67 | 0.91x | -9.1% (Worse) |
| Cache references | 32,462,604 | 32,555,480 | 1.00x | -0.3% (Worse) |
| Cache misses | 20,142,349 | 11,205,471 | 0.56x | +44.4% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 1,295,818,944 | 929,092,840 | 0.72x | +28.3% (Better) |
| L1 dcache misses | 15,312,551 | 24,091,803 | 1.57x | -57.3% (Worse) |
| L1 miss rate (%) | 1.18 | 2.59 | 2.19x | -119.5% (Worse) |
| LLC loads | 2,513,182 | 1,412,271 | 0.56x | +43.8% (Better) |
| LLC misses | 2,389,437 | 1,226,302 | 0.51x | +48.7% (Better) |
| LLC miss rate (%) | 95.08 | 86.83 | 0.91x | +8.7% (Better) |
| Branches | 327,584,684 | 95,741,361 | 0.29x | +70.8% (Better) |
| Branch misses | 514,997 | 68,773 | 0.13x | +86.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
