# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:15:17

## Executive Summary

**Overall Speedup**: 1.05x

The optimized version is **1.05x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.146s | ±0.002s |
| Optimized | 0.138s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 632,172,785 | 599,353,670 | 0.95x | +5.2% (Better) |
| Instructions | 1,826,761,913 | 2,167,988,944 | 1.19x | -18.7% (Worse) |
| IPC | 2.89 | 3.62 | 1.25x | +25.2% (Better) |
| Cache references | 15,719,073 | 16,262,412 | 1.03x | -3.5% (Worse) |
| Cache misses | 10,252,899 | 5,489,926 | 0.54x | +46.5% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 555,168,586 | 875,926,635 | 1.58x | -57.8% (Worse) |
| L1 dcache misses | 9,612,476 | 11,314,371 | 1.18x | -17.7% (Worse) |
| L1 miss rate (%) | 1.73 | 1.29 | 0.75x | +25.4% (Better) |
| Branches | 177,408,766 | 142,286,136 | 0.80x | +19.8% (Better) |
| Branch misses | 51,090 | 40,519 | 0.79x | +20.7% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
