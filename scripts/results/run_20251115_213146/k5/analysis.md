# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:31:59

## Executive Summary

**Overall Speedup**: 2.20x

The optimized version is **2.20x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.899s | ±0.029s |
| Optimized | 0.863s | ±0.016s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 6,704,057,651 | 3,013,505,637 | 0.45x | +55.0% (Better) |
| Instructions | 20,230,442,902 | 7,869,021,155 | 0.39x | +61.1% (Better) |
| IPC | 3.02 | 2.61 | 0.87x | -13.5% (Worse) |
| Cache references | 143,256,810 | 145,097,774 | 1.01x | -1.3% (Worse) |
| Cache misses | 101,705,143 | 72,411,469 | 0.71x | +28.8% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 6,515,336,099 | 4,216,134,951 | 0.65x | +35.3% (Better) |
| L1 dcache misses | 6,509,253 | 43,101,341 | 6.62x | -562.2% (Worse) |
| L1 miss rate (%) | 0.10 | 1.02 | 10.20x | -920.0% (Worse) |
| Branches | 1,226,549,571 | 169,144,050 | 0.14x | +86.2% (Better) |
| Branch misses | 848,862 | 84,515 | 0.10x | +90.0% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
