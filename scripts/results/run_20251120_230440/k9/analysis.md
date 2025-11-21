# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:06:36

## Executive Summary

**Overall Speedup**: 3.64x

The optimized version is **3.64x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.430s | ±0.051s |
| Optimized | 0.942s | ±0.006s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 14,370,081,545 | 3,987,144,511 | 0.28x | +72.3% (Better) |
| Instructions | 46,807,991,869 | 13,551,170,637 | 0.29x | +71.0% (Better) |
| IPC | 3.26 | 3.40 | 1.04x | +4.3% (Better) |
| Cache references | 211,946,692 | 169,892,710 | 0.80x | +19.8% (Better) |
| Cache misses | 133,163,442 | 47,578,407 | 0.36x | +64.3% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 15,290,037,792 | 5,844,239,107 | 0.38x | +61.8% (Better) |
| L1 dcache misses | 19,185,252 | 58,584,857 | 3.05x | -205.4% (Worse) |
| L1 miss rate (%) | 0.13 | 1.00 | 7.69x | -669.2% (Worse) |
| LLC loads | 2,880,907 | 1,860,036 | 0.65x | +35.4% (Better) |
| LLC misses | 2,310,940 | 1,423,501 | 0.62x | +38.4% (Better) |
| LLC miss rate (%) | 80.22 | 76.53 | 0.95x | +4.6% (Better) |
| Branches | 2,185,315,595 | 225,935,636 | 0.10x | +89.7% (Better) |
| Branch misses | 1,089,713 | 87,299 | 0.08x | +92.0% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
