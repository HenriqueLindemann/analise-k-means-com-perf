# K-means Performance Analysis Report

**Generated**: 2025-11-20 14:38:22

## Executive Summary

**Overall Speedup**: 3.72x

The optimized version is **3.72x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.332s | ±0.010s |
| Optimized | 0.896s | ±0.009s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 14,342,125,215 | 3,790,968,603 | 0.26x | +73.6% (Better) |
| Instructions | 46,818,514,018 | 10,904,305,602 | 0.23x | +76.7% (Better) |
| IPC | 3.26 | 2.88 | 0.88x | -11.9% (Worse) |
| Cache references | 212,627,532 | 169,791,398 | 0.80x | +20.1% (Better) |
| Cache misses | 130,803,074 | 48,116,450 | 0.37x | +63.2% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 15,286,439,099 | 5,454,752,376 | 0.36x | +64.3% (Better) |
| L1 dcache misses | 27,323,146 | 90,399,866 | 3.31x | -230.9% (Worse) |
| L1 miss rate (%) | 0.18 | 1.66 | 9.22x | -822.2% (Worse) |
| LLC loads | 3,910,984 | 2,474,096 | 0.63x | +36.7% (Better) |
| LLC misses | 3,203,061 | 1,911,847 | 0.60x | +40.3% (Better) |
| LLC miss rate (%) | 81.90 | 77.27 | 0.94x | +5.7% (Better) |
| Branches | 2,185,172,221 | 182,526,322 | 0.08x | +91.6% (Better) |
| Branch misses | 1,066,542 | 69,655 | 0.07x | +93.5% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
