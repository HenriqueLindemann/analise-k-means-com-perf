# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:53:32

## Executive Summary

**Overall Speedup**: 0.94x

The optimized version is **1.06x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.182s | ±0.003s |
| Optimized | 0.193s | ±0.003s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 658,040,789 | 687,257,869 | 1.04x | -4.4% (Worse) |
| Instructions | 1,823,490,985 | 2,168,335,063 | 1.19x | -18.9% (Worse) |
| IPC | 2.77 | 3.16 | 1.14x | +13.9% (Better) |
| Cache references | 15,853,741 | 16,110,765 | 1.02x | -1.6% (Worse) |
| Cache misses | 12,123,391 | 7,235,222 | 0.60x | +40.3% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 556,875,173 | 876,930,479 | 1.57x | -57.5% (Worse) |
| L1 dcache misses | 1,311,040 | 6,127,059 | 4.67x | -367.3% (Worse) |
| L1 miss rate (%) | 0.24 | 0.70 | 2.92x | -191.7% (Worse) |
| Branches | 177,608,428 | 142,220,063 | 0.80x | +19.9% (Better) |
| Branch misses | 77,724 | 54,783 | 0.70x | +29.5% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
