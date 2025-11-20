# K-means Performance Analysis Report

**Generated**: 2025-11-20 16:22:56

## Executive Summary

**Overall Speedup**: 1.30x

The optimized version is **1.30x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.110s | ±0.001s |
| Optimized | 0.085s | ±0.000s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 475,562,845 | 361,605,981 | 0.76x | +24.0% (Better) |
| Instructions | 1,371,489,249 | 924,183,048 | 0.67x | +32.6% (Better) |
| IPC | 2.88 | 2.56 | 0.89x | -11.4% (Worse) |
| Cache references | 13,656,614 | 14,050,948 | 1.03x | -2.9% (Worse) |
| Cache misses | 9,652,898 | 5,874,709 | 0.61x | +39.1% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 402,670,068 | 400,075,582 | 0.99x | +0.6% (Better) |
| L1 dcache misses | 5,243,302 | 7,160,706 | 1.37x | -36.6% (Worse) |
| L1 miss rate (%) | 1.30 | 1.79 | 1.38x | -37.7% (Worse) |
| LLC loads | 1,338,455 | 1,116,298 | 0.83x | +16.6% (Better) |
| LLC misses | 1,295,109 | 884,445 | 0.68x | +31.7% (Better) |
| LLC miss rate (%) | 96.76 | 79.23 | 0.82x | +18.1% (Better) |
| Branches | 162,347,964 | 84,199,512 | 0.52x | +48.1% (Better) |
| Branch misses | 44,659 | 69,936 | 1.57x | -56.6% (Worse) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
