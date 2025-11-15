# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:43:43

## Executive Summary

**Overall Speedup**: 0.91x

The optimized version is **1.10x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.975s | ±0.011s |
| Optimized | 1.076s | ±0.007s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 2,732,038,481 | 3,021,760,996 | 1.11x | -10.6% (Worse) |
| Instructions | 8,432,962,486 | 9,916,566,704 | 1.18x | -17.6% (Worse) |
| IPC | 0 | 0 | 0.00x | +0.0% (Worse) |
| Cache references | 45,582,843 | 48,171,457 | 1.06x | -5.7% (Worse) |
| Cache misses | 27,578,383 | 16,715,384 | 0.61x | +39.4% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 2,681,859,531 | 3,816,306,802 | 1.42x | -42.3% (Worse) |
| L1 dcache misses | 2,941,841 | 21,800,045 | 7.41x | -641.0% (Worse) |
| L1 miss rate (%) | 0.11 | 0.57 | 5.18x | -418.2% (Worse) |
| Branches | 473,483,557 | 372,548,127 | 0.79x | +21.3% (Better) |
| Branch misses | 550,216 | 82,893 | 0.15x | +84.9% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
