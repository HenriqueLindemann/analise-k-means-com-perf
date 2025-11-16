# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:56:11

## Executive Summary

**Overall Speedup**: 0.97x

The optimized version is **1.03x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.601s | ±0.006s |
| Optimized | 0.618s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 2,622,954,351 | 2,692,900,329 | 1.03x | -2.7% (Worse) |
| Instructions | 8,435,998,024 | 9,905,294,311 | 1.17x | -17.4% (Worse) |
| IPC | 3.22 | 3.68 | 1.14x | +14.4% (Better) |
| Cache references | 45,024,460 | 47,634,532 | 1.06x | -5.8% (Worse) |
| Cache misses | 26,135,675 | 12,621,150 | 0.48x | +51.7% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 2,680,548,276 | 3,814,634,247 | 1.42x | -42.3% (Worse) |
| L1 dcache misses | 20,221,901 | 33,339,328 | 1.65x | -64.9% (Worse) |
| L1 miss rate (%) | 0.75 | 0.87 | 1.16x | -16.0% (Worse) |
| LLC loads | 2,712,831 | 1,470,168 | 0.54x | +45.8% (Better) |
| LLC misses | 2,516,911 | 1,101,460 | 0.44x | +56.2% (Better) |
| LLC miss rate (%) | 92.78 | 74.92 | 0.81x | +19.2% (Better) |
| Branches | 472,887,543 | 371,537,126 | 0.79x | +21.4% (Better) |
| Branch misses | 497,045 | 45,364 | 0.09x | +90.9% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
