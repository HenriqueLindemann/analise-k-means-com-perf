# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:05:34

## Executive Summary

**Overall Speedup**: 2.25x

The optimized version is **2.25x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.102s | ±0.017s |
| Optimized | 0.491s | ±0.016s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 4,644,022,449 | 2,007,999,647 | 0.43x | +56.8% (Better) |
| Instructions | 15,323,819,997 | 5,419,111,914 | 0.35x | +64.6% (Better) |
| IPC | 3.30 | 2.70 | 0.82x | -18.2% (Worse) |
| Cache references | 93,589,805 | 92,191,815 | 0.99x | +1.5% (Better) |
| Cache misses | 64,010,719 | 30,789,607 | 0.48x | +51.9% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 4,883,226,508 | 2,734,722,014 | 0.56x | +44.0% (Better) |
| L1 dcache misses | 4,139,454 | 38,588,112 | 9.32x | -832.2% (Worse) |
| L1 miss rate (%) | 0.08 | 1.41 | 17.62x | -1662.5% (Worse) |
| LLC loads | 1,225,581 | 1,772,522 | 1.45x | -44.6% (Worse) |
| LLC misses | 982,939 | 1,008,133 | 1.03x | -2.6% (Worse) |
| LLC miss rate (%) | 80.20 | 56.88 | 0.71x | +29.1% (Better) |
| Branches | 910,244,929 | 133,557,925 | 0.15x | +85.3% (Better) |
| Branch misses | 866,864 | 87,111 | 0.10x | +90.0% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
