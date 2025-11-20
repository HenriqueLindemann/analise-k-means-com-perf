# K-means Performance Analysis Report

**Generated**: 2025-11-20 16:34:03

## Executive Summary

**Overall Speedup**: 3.18x

The optimized version is **3.18x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.459s | ±0.015s |
| Optimized | 1.087s | ±0.010s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 15,103,096,896 | 4,664,978,551 | 0.31x | +69.1% (Better) |
| Instructions | 50,867,640,384 | 13,257,093,026 | 0.26x | +73.9% (Better) |
| IPC | 3.37 | 2.84 | 0.84x | -15.6% (Worse) |
| Cache references | 207,027,173 | 199,089,892 | 0.96x | +3.8% (Better) |
| Cache misses | 111,805,740 | 49,770,373 | 0.45x | +55.5% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 16,372,222,382 | 6,602,718,015 | 0.40x | +59.7% (Better) |
| L1 dcache misses | 31,230,370 | 149,689,182 | 4.79x | -379.3% (Worse) |
| L1 miss rate (%) | 0.19 | 2.27 | 11.95x | -1094.7% (Worse) |
| LLC loads | 3,946,362 | 3,691,058 | 0.94x | +6.5% (Better) |
| LLC misses | 3,193,850 | 2,732,896 | 0.86x | +14.4% (Better) |
| LLC miss rate (%) | 80.93 | 74.04 | 0.91x | +8.5% (Better) |
| Branches | 2,339,291,749 | 199,896,428 | 0.09x | +91.5% (Better) |
| Branch misses | 839,069 | 78,530 | 0.09x | +90.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
