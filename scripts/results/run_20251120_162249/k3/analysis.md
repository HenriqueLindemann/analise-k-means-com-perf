# K-means Performance Analysis Report

**Generated**: 2025-11-20 16:23:11

## Executive Summary

**Overall Speedup**: 1.57x

The optimized version is **1.57x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.154s | ±0.002s |
| Optimized | 0.098s | ±0.000s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 666,374,784 | 417,391,506 | 0.63x | +37.4% (Better) |
| Instructions | 1,810,918,151 | 1,042,194,133 | 0.58x | +42.4% (Better) |
| IPC | 2.72 | 2.50 | 0.92x | -8.1% (Worse) |
| Cache references | 15,748,216 | 16,100,656 | 1.02x | -2.2% (Worse) |
| Cache misses | 10,263,298 | 6,390,549 | 0.62x | +37.7% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 555,324,216 | 467,004,659 | 0.84x | +15.9% (Better) |
| L1 dcache misses | 9,785,676 | 13,966,872 | 1.43x | -42.7% (Worse) |
| L1 miss rate (%) | 1.76 | 2.99 | 1.70x | -69.9% (Worse) |
| LLC loads | 1,902,653 | 1,398,085 | 0.73x | +26.5% (Better) |
| LLC misses | 1,826,113 | 1,117,372 | 0.61x | +38.8% (Better) |
| LLC miss rate (%) | 95.98 | 79.92 | 0.83x | +16.7% (Better) |
| Branches | 177,206,369 | 84,831,671 | 0.48x | +52.1% (Better) |
| Branch misses | 49,085 | 68,768 | 1.40x | -40.1% (Worse) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
