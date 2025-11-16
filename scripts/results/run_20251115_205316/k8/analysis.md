# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:57:17

## Executive Summary

**Overall Speedup**: 1.04x

The optimized version is **1.04x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.440s | ±0.035s |
| Optimized | 3.314s | ±0.132s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 9,947,466,074 | 10,729,192,401 | 1.08x | -7.9% (Worse) |
| Instructions | 31,590,686,964 | 37,094,839,872 | 1.17x | -17.4% (Worse) |
| IPC | 3.18 | 3.46 | 1.09x | +8.9% (Better) |
| Cache references | 153,514,571 | 162,772,017 | 1.06x | -6.0% (Worse) |
| Cache misses | 89,661,939 | 48,745,538 | 0.54x | +45.6% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 9,992,735,583 | 14,044,826,627 | 1.41x | -40.6% (Worse) |
| L1 dcache misses | 9,059,229 | 69,856,322 | 7.71x | -671.1% (Worse) |
| L1 miss rate (%) | 0.09 | 0.50 | 5.56x | -455.6% (Worse) |
| Branches | 1,592,165,072 | 1,252,229,110 | 0.79x | +21.4% (Better) |
| Branch misses | 1,259,905 | 133,528 | 0.11x | +89.4% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
