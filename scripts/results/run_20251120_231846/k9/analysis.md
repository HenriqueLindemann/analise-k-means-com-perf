# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:26:02

## Executive Summary

**Overall Speedup**: 3.46x

The optimized version is **3.46x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.225s | ±0.017s |
| Optimized | 0.932s | ±0.016s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 14,082,800,584 | 4,001,541,788 | 0.28x | +71.6% (Better) |
| Instructions | 46,808,601,006 | 13,538,490,389 | 0.29x | +71.1% (Better) |
| IPC | 3.32 | 3.38 | 1.02x | +1.8% (Better) |
| Cache references | 212,134,979 | 169,831,033 | 0.80x | +19.9% (Better) |
| Cache misses | 121,322,724 | 42,884,592 | 0.35x | +64.7% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 15,285,698,382 | 5,851,405,242 | 0.38x | +61.7% (Better) |
| L1 dcache misses | 32,276,025 | 78,063,743 | 2.42x | -141.9% (Worse) |
| L1 miss rate (%) | 0.21 | 1.33 | 6.33x | -533.3% (Worse) |
| LLC loads | 4,108,403 | 2,135,979 | 0.52x | +48.0% (Better) |
| LLC misses | 3,369,556 | 1,540,756 | 0.46x | +54.3% (Better) |
| LLC miss rate (%) | 82.02 | 72.13 | 0.88x | +12.1% (Better) |
| Branches | 2,184,904,276 | 223,177,566 | 0.10x | +89.8% (Better) |
| Branch misses | 1,040,401 | 75,081 | 0.07x | +92.8% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
