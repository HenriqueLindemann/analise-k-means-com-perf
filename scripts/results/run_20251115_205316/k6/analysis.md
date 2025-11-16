# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:55:17

## Executive Summary

**Overall Speedup**: 0.96x

The optimized version is **1.04x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.510s | ±0.011s |
| Optimized | 1.566s | ±0.010s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 4,864,112,887 | 5,028,767,991 | 1.03x | -3.4% (Worse) |
| Instructions | 15,499,260,369 | 17,351,408,408 | 1.12x | -11.9% (Worse) |
| IPC | 3.19 | 3.45 | 1.08x | +8.3% (Better) |
| Cache references | 93,743,568 | 92,302,337 | 0.98x | +1.5% (Better) |
| Cache misses | 59,049,457 | 25,979,975 | 0.44x | +56.0% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 4,880,827,077 | 6,753,359,099 | 1.38x | -38.4% (Worse) |
| L1 dcache misses | 5,243,656 | 39,361,928 | 7.51x | -650.7% (Worse) |
| L1 miss rate (%) | 0.11 | 0.58 | 5.27x | -427.3% (Worse) |
| Branches | 911,032,332 | 652,868,526 | 0.72x | +28.3% (Better) |
| Branch misses | 878,285 | 90,565 | 0.10x | +89.7% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
