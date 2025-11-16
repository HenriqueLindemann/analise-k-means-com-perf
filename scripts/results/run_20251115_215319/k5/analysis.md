# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:54:45

## Executive Summary

**Overall Speedup**: 2.20x

The optimized version is **2.20x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.385s | ±0.011s |
| Optimized | 0.628s | ±0.007s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 6,041,283,394 | 2,692,688,436 | 0.45x | +55.4% (Better) |
| Instructions | 20,203,400,481 | 7,881,283,202 | 0.39x | +61.0% (Better) |
| IPC | 3.34 | 2.93 | 0.88x | -12.5% (Worse) |
| Cache references | 143,254,654 | 144,912,719 | 1.01x | -1.2% (Worse) |
| Cache misses | 88,074,232 | 42,824,744 | 0.49x | +51.4% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 6,513,546,634 | 4,211,029,403 | 0.65x | +35.3% (Better) |
| L1 dcache misses | 22,107,937 | 106,750,516 | 4.83x | -382.9% (Worse) |
| L1 miss rate (%) | 0.34 | 2.54 | 7.47x | -647.1% (Worse) |
| LLC loads | 3,100,097 | 3,682,460 | 1.19x | -18.8% (Worse) |
| LLC misses | 2,709,106 | 2,723,615 | 1.01x | -0.5% (Worse) |
| LLC miss rate (%) | 87.39 | 73.96 | 0.85x | +15.4% (Better) |
| Branches | 1,225,709,677 | 167,074,501 | 0.14x | +86.4% (Better) |
| Branch misses | 775,737 | 45,124 | 0.06x | +94.2% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
