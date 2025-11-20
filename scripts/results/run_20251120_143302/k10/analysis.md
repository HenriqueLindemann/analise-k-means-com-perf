# K-means Performance Analysis Report

**Generated**: 2025-11-20 14:40:10

## Executive Summary

**Overall Speedup**: 3.23x

The optimized version is **3.23x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.549s | ±0.013s |
| Optimized | 1.099s | ±0.025s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 15,235,657,247 | 4,647,513,549 | 0.31x | +69.5% (Better) |
| Instructions | 50,878,801,746 | 13,255,888,018 | 0.26x | +73.9% (Better) |
| IPC | 3.34 | 2.85 | 0.85x | -14.6% (Worse) |
| Cache references | 207,817,332 | 199,077,560 | 0.96x | +4.2% (Better) |
| Cache misses | 120,398,357 | 55,366,647 | 0.46x | +54.0% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 16,375,005,268 | 6,599,557,406 | 0.40x | +59.7% (Better) |
| L1 dcache misses | 17,771,576 | 97,924,323 | 5.51x | -451.0% (Worse) |
| L1 miss rate (%) | 0.11 | 1.48 | 13.45x | -1245.5% (Worse) |
| LLC loads | 2,867,696 | 2,520,855 | 0.88x | +12.1% (Better) |
| LLC misses | 2,139,729 | 1,961,380 | 0.92x | +8.3% (Better) |
| LLC miss rate (%) | 74.61 | 77.81 | 1.04x | -4.3% (Worse) |
| Branches | 2,340,114,364 | 201,041,729 | 0.09x | +91.4% (Better) |
| Branch misses | 871,491 | 73,185 | 0.08x | +91.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
