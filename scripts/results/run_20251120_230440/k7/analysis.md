# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:05:46

## Executive Summary

**Overall Speedup**: 2.24x

The optimized version is **2.24x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.640s | ±0.027s |
| Optimized | 0.286s | ±0.004s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 2,619,057,177 | 1,168,618,693 | 0.45x | +55.4% (Better) |
| Instructions | 8,291,769,331 | 3,090,444,838 | 0.37x | +62.7% (Better) |
| IPC | 3.17 | 2.64 | 0.84x | -16.5% (Worse) |
| Cache references | 45,625,443 | 47,252,463 | 1.04x | -3.6% (Worse) |
| Cache misses | 30,662,485 | 16,015,480 | 0.52x | +47.8% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 2,678,909,855 | 1,480,686,796 | 0.55x | +44.7% (Better) |
| L1 dcache misses | 7,311,806 | 31,599,037 | 4.32x | -332.2% (Worse) |
| L1 miss rate (%) | 0.27 | 2.13 | 7.89x | -688.9% (Worse) |
| LLC loads | 1,477,968 | 1,348,859 | 0.91x | +8.7% (Better) |
| LLC misses | 1,336,048 | 1,130,752 | 0.85x | +15.4% (Better) |
| LLC miss rate (%) | 90.40 | 83.83 | 0.93x | +7.3% (Better) |
| Branches | 471,139,830 | 106,397,904 | 0.23x | +77.4% (Better) |
| Branch misses | 525,826 | 81,633 | 0.16x | +84.5% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
