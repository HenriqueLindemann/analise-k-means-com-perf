# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:53:25

## Executive Summary

**Overall Speedup**: 1.02x

The optimized version is **1.02x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.107s | ±0.002s |
| Optimized | 0.105s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 463,425,221 | 455,161,535 | 0.98x | +1.8% (Better) |
| Instructions | 1,369,804,039 | 1,647,610,516 | 1.20x | -20.3% (Worse) |
| IPC | 2.96 | 3.62 | 1.22x | +22.5% (Better) |
| Cache references | 13,687,712 | 14,505,534 | 1.06x | -6.0% (Worse) |
| Cache misses | 9,985,919 | 5,417,222 | 0.54x | +45.8% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 402,382,940 | 666,084,982 | 1.66x | -65.5% (Worse) |
| L1 dcache misses | 4,302,172 | 7,435,021 | 1.73x | -72.8% (Worse) |
| L1 miss rate (%) | 1.07 | 1.12 | 1.05x | -4.7% (Worse) |
| LLC loads | 1,207,749 | 1,298,068 | 1.07x | -7.5% (Worse) |
| LLC misses | 1,158,149 | 721,022 | 0.62x | +37.7% (Better) |
| LLC miss rate (%) | 95.89 | 55.55 | 0.58x | +42.1% (Better) |
| Branches | 162,658,904 | 133,490,860 | 0.82x | +17.9% (Better) |
| Branch misses | 44,745 | 39,798 | 0.89x | +11.1% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
