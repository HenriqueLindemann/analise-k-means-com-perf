# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:04:42

## Executive Summary

**Overall Speedup**: 1.28x

The optimized version is **1.28x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.126s | ±0.000s |
| Optimized | 0.098s | ±0.003s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 487,474,407 | 402,168,009 | 0.83x | +17.5% (Better) |
| Instructions | 1,391,743,019 | 988,465,674 | 0.71x | +29.0% (Better) |
| IPC | 2.86 | 2.46 | 0.86x | -13.9% (Worse) |
| Cache references | 13,931,435 | 14,480,223 | 1.04x | -3.9% (Worse) |
| Cache misses | 11,047,971 | 7,018,895 | 0.64x | +36.5% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 405,107,753 | 412,004,359 | 1.02x | -1.7% (Worse) |
| L1 dcache misses | 982,141 | 8,011,173 | 8.16x | -715.7% (Worse) |
| L1 miss rate (%) | 0.24 | 1.94 | 8.08x | -708.3% (Worse) |
| LLC loads | 783,764 | 1,096,896 | 1.40x | -40.0% (Worse) |
| LLC misses | 733,569 | 731,492 | 1.00x | +0.3% (Better) |
| LLC miss rate (%) | 93.60 | 66.69 | 0.71x | +28.7% (Better) |
| Branches | 163,467,437 | 85,751,558 | 0.52x | +47.5% (Better) |
| Branch misses | 66,072 | 73,596 | 1.11x | -11.4% (Worse) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
