# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:15:36

## Executive Summary

**Overall Speedup**: 1.11x

The optimized version is **1.11x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.330s | ±0.005s |
| Optimized | 0.298s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 1,436,598,166 | 1,298,226,621 | 0.90x | +9.6% (Better) |
| Instructions | 4,188,734,436 | 4,964,978,371 | 1.19x | -18.5% (Worse) |
| IPC | 2.92 | 3.82 | 1.31x | +31.2% (Better) |
| Cache references | 32,559,805 | 32,946,706 | 1.01x | -1.2% (Worse) |
| Cache misses | 19,614,717 | 9,278,245 | 0.47x | +52.7% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 1,298,159,790 | 1,983,891,959 | 1.53x | -52.8% (Worse) |
| L1 dcache misses | 22,848,833 | 21,075,537 | 0.92x | +7.8% (Better) |
| L1 miss rate (%) | 1.76 | 1.06 | 0.60x | +39.8% (Better) |
| Branches | 327,713,113 | 246,555,415 | 0.75x | +24.8% (Better) |
| Branch misses | 505,533 | 41,701 | 0.08x | +91.8% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
