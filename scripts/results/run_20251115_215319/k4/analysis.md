# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:53:56

## Executive Summary

**Overall Speedup**: 1.03x

The optimized version is **1.03x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.309s | ±0.005s |
| Optimized | 0.301s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 1,346,344,990 | 1,310,199,221 | 0.97x | +2.7% (Better) |
| Instructions | 4,199,406,579 | 4,965,161,173 | 1.18x | -18.2% (Worse) |
| IPC | 3.12 | 3.79 | 1.21x | +21.5% (Better) |
| Cache references | 32,548,997 | 32,970,939 | 1.01x | -1.3% (Worse) |
| Cache misses | 20,603,998 | 9,249,030 | 0.45x | +55.1% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 1,297,808,747 | 1,984,641,502 | 1.53x | -52.9% (Worse) |
| L1 dcache misses | 11,581,845 | 26,096,502 | 2.25x | -125.3% (Worse) |
| L1 miss rate (%) | 0.89 | 1.31 | 1.47x | -47.2% (Worse) |
| LLC loads | 1,945,065 | 1,507,304 | 0.77x | +22.5% (Better) |
| LLC misses | 1,833,058 | 1,016,416 | 0.55x | +44.6% (Better) |
| LLC miss rate (%) | 94.24 | 67.43 | 0.72x | +28.4% (Better) |
| Branches | 327,505,884 | 247,040,883 | 0.75x | +24.6% (Better) |
| Branch misses | 509,234 | 42,091 | 0.08x | +91.7% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
