# K-means Performance Analysis Report

**Generated**: 2025-11-20 14:36:44

## Executive Summary

**Overall Speedup**: 2.76x

The optimized version is **2.76x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 2.180s | ±0.008s |
| Optimized | 0.791s | ±0.005s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 9,395,374,686 | 3,345,735,948 | 0.36x | +64.4% (Better) |
| Instructions | 31,143,306,422 | 9,821,652,013 | 0.32x | +68.5% (Better) |
| IPC | 3.31 | 2.94 | 0.89x | -11.4% (Worse) |
| Cache references | 152,468,922 | 159,372,439 | 1.05x | -4.5% (Worse) |
| Cache misses | 98,095,915 | 47,591,386 | 0.49x | +51.5% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 9,985,113,351 | 4,949,717,616 | 0.50x | +50.4% (Better) |
| L1 dcache misses | 16,651,269 | 66,248,955 | 3.98x | -297.9% (Worse) |
| L1 miss rate (%) | 0.17 | 1.34 | 7.88x | -688.2% (Worse) |
| LLC loads | 2,476,824 | 2,044,030 | 0.83x | +17.5% (Better) |
| LLC misses | 2,001,795 | 1,608,890 | 0.80x | +19.6% (Better) |
| LLC miss rate (%) | 80.82 | 78.71 | 0.97x | +2.6% (Better) |
| Branches | 1,589,474,596 | 176,383,236 | 0.11x | +88.9% (Better) |
| Branch misses | 1,169,303 | 71,131 | 0.06x | +93.9% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
