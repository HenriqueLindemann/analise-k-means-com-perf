# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:18:53

## Executive Summary

**Overall Speedup**: 1.22x

The optimized version is **1.22x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.109s | ±0.001s |
| Optimized | 0.089s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 470,008,932 | 381,880,473 | 0.81x | +18.8% (Better) |
| Instructions | 1,370,013,729 | 987,429,622 | 0.72x | +27.9% (Better) |
| IPC | 2.91 | 2.59 | 0.89x | -11.3% (Worse) |
| Cache references | 13,666,490 | 13,884,311 | 1.02x | -1.6% (Worse) |
| Cache misses | 9,608,974 | 5,907,851 | 0.61x | +38.5% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 403,107,792 | 412,228,909 | 1.02x | -2.3% (Worse) |
| L1 dcache misses | 6,806,164 | 8,357,283 | 1.23x | -22.8% (Worse) |
| L1 miss rate (%) | 1.69 | 2.03 | 1.20x | -20.1% (Worse) |
| LLC loads | 1,529,836 | 1,124,593 | 0.74x | +26.5% (Better) |
| LLC misses | 1,475,409 | 816,959 | 0.55x | +44.6% (Better) |
| LLC miss rate (%) | 96.44 | 72.64 | 0.75x | +24.7% (Better) |
| Branches | 162,671,678 | 83,613,194 | 0.51x | +48.6% (Better) |
| Branch misses | 44,647 | 66,709 | 1.49x | -49.4% (Worse) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
