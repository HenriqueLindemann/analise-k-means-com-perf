# K-means Performance Analysis Report

**Generated**: 2025-11-20 14:33:19

## Executive Summary

**Overall Speedup**: 1.47x

The optimized version is **1.47x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.150s | ±0.002s |
| Optimized | 0.102s | ±0.001s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 608,817,302 | 411,608,879 | 0.68x | +32.4% (Better) |
| Instructions | 1,812,817,352 | 1,051,666,326 | 0.58x | +42.0% (Better) |
| IPC | 2.98 | 2.56 | 0.86x | -14.2% (Worse) |
| Cache references | 15,816,576 | 15,920,861 | 1.01x | -0.7% (Worse) |
| Cache misses | 11,427,627 | 7,165,681 | 0.63x | +37.3% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 556,327,014 | 465,242,659 | 0.84x | +16.4% (Better) |
| L1 dcache misses | 2,747,003 | 7,368,183 | 2.68x | -168.2% (Worse) |
| L1 miss rate (%) | 0.49 | 1.58 | 3.22x | -222.4% (Worse) |
| LLC loads | 978,661 | 1,119,983 | 1.14x | -14.4% (Worse) |
| LLC misses | 928,551 | 869,970 | 0.94x | +6.3% (Better) |
| LLC miss rate (%) | 94.88 | 77.68 | 0.82x | +18.1% (Better) |
| Branches | 177,373,865 | 86,300,994 | 0.49x | +51.3% (Better) |
| Branch misses | 72,904 | 63,991 | 0.88x | +12.2% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
