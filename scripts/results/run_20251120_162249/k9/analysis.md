# K-means Performance Analysis Report

**Generated**: 2025-11-20 16:31:05

## Executive Summary

**Overall Speedup**: 3.72x

The optimized version is **3.72x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.228s | ±0.011s |
| Optimized | 0.867s | ±0.008s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 14,099,562,525 | 3,722,061,314 | 0.26x | +73.6% (Better) |
| Instructions | 46,802,846,582 | 10,917,170,482 | 0.23x | +76.7% (Better) |
| IPC | 3.32 | 2.93 | 0.88x | -11.6% (Worse) |
| Cache references | 211,860,476 | 169,569,156 | 0.80x | +20.0% (Better) |
| Cache misses | 116,540,267 | 44,507,859 | 0.38x | +61.8% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 15,287,044,877 | 5,451,852,732 | 0.36x | +64.3% (Better) |
| L1 dcache misses | 37,911,142 | 88,159,101 | 2.33x | -132.5% (Worse) |
| L1 miss rate (%) | 0.25 | 1.62 | 6.48x | -548.0% (Worse) |
| LLC loads | 4,619,936 | 2,512,853 | 0.54x | +45.6% (Better) |
| LLC misses | 3,880,201 | 1,733,837 | 0.45x | +55.3% (Better) |
| LLC miss rate (%) | 83.99 | 69.00 | 0.82x | +17.8% (Better) |
| Branches | 2,185,122,590 | 181,228,721 | 0.08x | +91.7% (Better) |
| Branch misses | 1,032,080 | 75,627 | 0.07x | +92.7% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
