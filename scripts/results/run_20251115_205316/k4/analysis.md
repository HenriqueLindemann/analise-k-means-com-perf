# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:53:50

## Executive Summary

**Overall Speedup**: 1.00x

The optimized version is **1.00x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.415s | ±0.005s |
| Optimized | 0.416s | ±0.005s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 1,443,376,544 | 1,464,384,928 | 1.01x | -1.5% (Worse) |
| Instructions | 4,203,284,177 | 4,963,604,768 | 1.18x | -18.1% (Worse) |
| IPC | 2.91 | 3.39 | 1.16x | +16.4% (Better) |
| Cache references | 32,568,751 | 32,856,495 | 1.01x | -0.9% (Worse) |
| Cache misses | 23,831,471 | 13,004,854 | 0.55x | +45.4% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 1,297,515,955 | 1,986,690,893 | 1.53x | -53.1% (Worse) |
| L1 dcache misses | 2,059,825 | 11,264,784 | 5.47x | -446.9% (Worse) |
| L1 miss rate (%) | 0.16 | 0.57 | 3.56x | -256.2% (Worse) |
| Branches | 328,003,462 | 247,837,704 | 0.76x | +24.4% (Better) |
| Branch misses | 551,249 | 62,895 | 0.11x | +88.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
