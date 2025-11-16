# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:53:20

## Executive Summary

**Overall Speedup**: 0.97x

The optimized version is **1.03x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.143s | ±0.002s |
| Optimized | 0.146s | ±0.003s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 514,604,521 | 519,043,196 | 1.01x | -0.9% (Worse) |
| Instructions | 1,382,527,026 | 1,653,416,711 | 1.20x | -19.6% (Worse) |
| IPC | 2.69 | 3.19 | 1.19x | +18.6% (Better) |
| Cache references | 13,690,680 | 13,965,341 | 1.02x | -2.0% (Worse) |
| Cache misses | 10,933,378 | 6,736,730 | 0.62x | +38.4% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 404,803,863 | 665,417,348 | 1.64x | -64.4% (Worse) |
| L1 dcache misses | 1,161,405 | 5,293,482 | 4.56x | -355.8% (Worse) |
| L1 miss rate (%) | 0.29 | 0.80 | 2.76x | -175.9% (Worse) |
| Branches | 162,824,846 | 132,344,447 | 0.81x | +18.7% (Better) |
| Branch misses | 71,416 | 51,986 | 0.73x | +27.2% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
