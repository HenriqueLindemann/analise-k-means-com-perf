# K-means Performance Analysis Report

**Generated**: 2025-11-15 22:02:40

## Executive Summary

**Overall Speedup**: 1.04x

The optimized version is **1.04x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.521s | ±0.023s |
| Optimized | 3.377s | ±0.003s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 15,382,544,011 | 14,754,434,519 | 0.96x | +4.1% (Better) |
| Instructions | 51,680,311,183 | 54,621,720,339 | 1.06x | -5.7% (Worse) |
| IPC | 3.36 | 3.70 | 1.10x | +10.2% (Better) |
| Cache references | 207,271,097 | 202,013,334 | 0.97x | +2.5% (Better) |
| Cache misses | 103,863,537 | 47,253,730 | 0.45x | +54.5% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 16,373,356,599 | 20,252,796,061 | 1.24x | -23.7% (Worse) |
| L1 dcache misses | 91,587,138 | 117,057,375 | 1.28x | -27.8% (Worse) |
| L1 miss rate (%) | 0.56 | 0.58 | 1.04x | -3.6% (Worse) |
| LLC loads | 10,005,897 | 3,231,639 | 0.32x | +67.7% (Better) |
| LLC misses | 8,895,859 | 2,103,009 | 0.24x | +76.4% (Better) |
| LLC miss rate (%) | 88.91 | 65.08 | 0.73x | +26.8% (Better) |
| Branches | 2,340,147,551 | 1,738,563,135 | 0.74x | +25.7% (Better) |
| Branch misses | 833,116 | 61,303 | 0.07x | +92.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
