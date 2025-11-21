# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:19:08

## Executive Summary

**Overall Speedup**: 1.38x

The optimized version is **1.38x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.146s | ±0.002s |
| Optimized | 0.105s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 631,729,978 | 454,754,842 | 0.72x | +28.0% (Better) |
| Instructions | 1,811,140,711 | 1,217,421,104 | 0.67x | +32.8% (Better) |
| IPC | 2.87 | 2.68 | 0.93x | -6.6% (Worse) |
| Cache references | 15,700,238 | 15,915,954 | 1.01x | -1.4% (Worse) |
| Cache misses | 10,343,342 | 5,871,219 | 0.57x | +43.2% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 555,308,639 | 479,115,541 | 0.86x | +13.7% (Better) |
| L1 dcache misses | 8,238,858 | 7,695,248 | 0.93x | +6.6% (Better) |
| L1 miss rate (%) | 1.48 | 1.61 | 1.09x | -8.8% (Worse) |
| LLC loads | 1,571,368 | 945,520 | 0.60x | +39.8% (Better) |
| LLC misses | 1,504,012 | 745,833 | 0.50x | +50.4% (Better) |
| LLC miss rate (%) | 95.71 | 78.88 | 0.82x | +17.6% (Better) |
| Branches | 177,666,786 | 100,919,575 | 0.57x | +43.2% (Better) |
| Branch misses | 49,579 | 266,997 | 5.39x | -438.5% (Worse) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
