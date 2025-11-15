# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:41:07

## Executive Summary

**Overall Speedup**: 1.02x

The optimized version is **1.02x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.151s | ±0.002s |
| Optimized | 0.149s | ±0.002s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 538,266,609 | 525,990,530 | 0.98x | +2.3% (Better) |
| Instructions | 1,383,930,496 | 1,655,907,370 | 1.20x | -19.7% (Worse) |
| IPC | 0 | 0 | 0.00x | +0.0% (Worse) |
| Cache references | 13,747,301 | 13,807,646 | 1.00x | -0.4% (Worse) |
| Cache misses | 10,956,926 | 6,605,095 | 0.60x | +39.7% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 404,322,861 | 664,890,954 | 1.64x | -64.4% (Worse) |
| L1 dcache misses | 1,276,458 | 5,238,417 | 4.10x | -310.4% (Worse) |
| L1 miss rate (%) | 0.32 | 0.79 | 2.47x | -146.9% (Worse) |
| Branches | 162,928,444 | 131,857,427 | 0.81x | +19.1% (Better) |
| Branch misses | 72,848 | 51,570 | 0.71x | +29.2% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
