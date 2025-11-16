# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:01:43

## Executive Summary

**Overall Speedup**: 1.00x

The optimized version is **1.00x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 5.595s | ±0.033s |
| Optimized | 5.591s | ±0.032s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 16,166,842,212 | 16,327,792,184 | 1.01x | -1.0% (Worse) |
| Instructions | 51,696,654,383 | 54,648,057,047 | 1.06x | -5.7% (Worse) |
| IPC | 3.20 | 3.35 | 1.05x | +4.7% (Better) |
| Cache references | 209,572,681 | 204,273,909 | 0.97x | +2.5% (Better) |
| Cache misses | 117,768,685 | 66,422,689 | 0.56x | +43.6% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 16,379,311,030 | 20,255,016,980 | 1.24x | -23.7% (Worse) |
| L1 dcache misses | 11,367,312 | 87,711,844 | 7.72x | -671.6% (Worse) |
| L1 miss rate (%) | 0.07 | 0.43 | 6.14x | -514.3% (Worse) |
| Branches | 2,342,166,039 | 1,741,710,039 | 0.74x | +25.6% (Better) |
| Branch misses | 1,014,140 | 229,090 | 0.23x | +77.4% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
