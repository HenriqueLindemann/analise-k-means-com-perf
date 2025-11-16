# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:47:25

## Executive Summary

**Overall Speedup**: 2.09x

The optimized version is **2.09x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 2.079s | ±0.043s |
| Optimized | 0.995s | ±0.012s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 6,456,230,973 | 2,885,034,322 | 0.45x | +55.3% (Better) |
| Instructions | 20,224,425,643 | 7,881,046,769 | 0.39x | +61.0% (Better) |
| IPC | 3.13 | 2.73 | 0.87x | -12.8% (Worse) |
| Cache references | 143,637,580 | 145,174,310 | 1.01x | -1.1% (Worse) |
| Cache misses | 96,719,715 | 57,810,031 | 0.60x | +40.2% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 6,513,764,520 | 4,210,151,169 | 0.65x | +35.4% (Better) |
| L1 dcache misses | 6,374,478 | 43,111,539 | 6.76x | -576.3% (Worse) |
| L1 miss rate (%) | 0.10 | 1.02 | 10.20x | -920.0% (Worse) |
| LLC loads | 1,457,529 | 1,686,507 | 1.16x | -15.7% (Worse) |
| LLC misses | 1,144,916 | 1,350,937 | 1.18x | -18.0% (Worse) |
| LLC miss rate (%) | 78.55 | 80.10 | 1.02x | -2.0% (Worse) |
| Branches | 1,227,189,358 | 167,850,433 | 0.14x | +86.3% (Better) |
| Branch misses | 848,381 | 78,000 | 0.09x | +90.8% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
