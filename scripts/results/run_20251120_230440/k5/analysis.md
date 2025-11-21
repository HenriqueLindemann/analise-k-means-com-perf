# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:05:18

## Executive Summary

**Overall Speedup**: 1.74x

The optimized version is **1.74x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.470s | ±0.007s |
| Optimized | 0.845s | ±0.005s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 6,187,239,875 | 3,562,072,473 | 0.58x | +42.4% (Better) |
| Instructions | 19,960,204,008 | 10,417,621,216 | 0.52x | +47.8% (Better) |
| IPC | 3.23 | 2.92 | 0.91x | -9.3% (Worse) |
| Cache references | 143,632,045 | 145,746,088 | 1.01x | -1.5% (Worse) |
| Cache misses | 98,625,508 | 42,867,791 | 0.43x | +56.5% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 6,513,219,960 | 4,182,214,368 | 0.64x | +35.8% (Better) |
| L1 dcache misses | 5,924,650 | 36,145,314 | 6.10x | -510.1% (Worse) |
| L1 miss rate (%) | 0.09 | 0.86 | 9.56x | -855.6% (Worse) |
| LLC loads | 1,450,304 | 1,705,999 | 1.18x | -17.6% (Worse) |
| LLC misses | 1,127,895 | 1,049,123 | 0.93x | +7.0% (Better) |
| LLC miss rate (%) | 77.77 | 61.50 | 0.79x | +20.9% (Better) |
| Branches | 1,226,380,941 | 307,881,100 | 0.25x | +74.9% (Better) |
| Branch misses | 823,141 | 2,001,860 | 2.43x | -143.2% (Worse) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
