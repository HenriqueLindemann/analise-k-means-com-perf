# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:53:37

## Executive Summary

**Overall Speedup**: 1.07x

The optimized version is **1.07x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.149s | ±0.002s |
| Optimized | 0.140s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 647,827,737 | 605,153,882 | 0.93x | +6.6% (Better) |
| Instructions | 1,826,410,481 | 2,164,695,617 | 1.19x | -18.5% (Worse) |
| IPC | 2.82 | 3.58 | 1.27x | +26.9% (Better) |
| Cache references | 15,774,909 | 15,862,119 | 1.01x | -0.6% (Worse) |
| Cache misses | 10,155,637 | 5,321,014 | 0.52x | +47.6% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 555,410,151 | 875,148,275 | 1.58x | -57.6% (Worse) |
| L1 dcache misses | 9,658,517 | 13,555,817 | 1.40x | -40.4% (Worse) |
| L1 miss rate (%) | 1.74 | 1.55 | 0.89x | +10.9% (Better) |
| LLC loads | 1,805,587 | 1,059,099 | 0.59x | +41.3% (Better) |
| LLC misses | 1,732,557 | 861,355 | 0.50x | +50.3% (Better) |
| LLC miss rate (%) | 95.96 | 81.33 | 0.85x | +15.2% (Better) |
| Branches | 177,269,081 | 141,305,575 | 0.80x | +20.3% (Better) |
| Branch misses | 51,720 | 40,015 | 0.77x | +22.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
