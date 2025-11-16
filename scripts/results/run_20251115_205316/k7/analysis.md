# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:55:51

## Executive Summary

**Overall Speedup**: 0.85x

The optimized version is **1.18x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.921s | ±0.022s |
| Optimized | 1.087s | ±0.015s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 2,729,428,544 | 3,021,487,464 | 1.11x | -10.7% (Worse) |
| Instructions | 8,442,266,469 | 9,914,742,736 | 1.17x | -17.4% (Worse) |
| IPC | 3.09 | 3.28 | 1.06x | +6.1% (Better) |
| Cache references | 45,550,263 | 48,105,577 | 1.06x | -5.6% (Worse) |
| Cache misses | 27,591,408 | 17,349,930 | 0.63x | +37.1% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 2,682,590,924 | 3,817,258,211 | 1.42x | -42.3% (Worse) |
| L1 dcache misses | 3,004,709 | 21,554,613 | 7.17x | -617.4% (Worse) |
| L1 miss rate (%) | 0.11 | 0.56 | 5.09x | -409.1% (Worse) |
| Branches | 473,733,225 | 372,604,773 | 0.79x | +21.3% (Better) |
| Branch misses | 543,238 | 86,736 | 0.16x | +84.0% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
