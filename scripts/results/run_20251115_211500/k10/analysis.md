# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:24:16

## Executive Summary

**Overall Speedup**: 1.02x

The optimized version is **1.02x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.424s | ±0.008s |
| Optimized | 3.372s | ±0.003s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 14,951,198,552 | 14,728,880,838 | 0.99x | +1.5% (Better) |
| Instructions | 51,673,379,378 | 54,619,651,256 | 1.06x | -5.7% (Worse) |
| IPC | 3.46 | 3.71 | 1.07x | +7.3% (Better) |
| Cache references | 207,278,527 | 202,272,365 | 0.98x | +2.4% (Better) |
| Cache misses | 110,848,236 | 47,512,503 | 0.43x | +57.1% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 16,372,099,183 | 20,252,631,297 | 1.24x | -23.7% (Worse) |
| L1 dcache misses | 32,062,200 | 105,813,946 | 3.30x | -230.0% (Worse) |
| L1 miss rate (%) | 0.20 | 0.52 | 2.60x | -160.0% (Worse) |
| Branches | 2,339,532,335 | 1,738,748,674 | 0.74x | +25.7% (Better) |
| Branch misses | 840,040 | 60,976 | 0.07x | +92.7% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
