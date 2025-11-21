# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:05:00

## Executive Summary

**Overall Speedup**: 1.52x

The optimized version is **1.52x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.311s | ±0.004s |
| Optimized | 0.205s | ±0.002s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 1,330,549,244 | 865,532,533 | 0.65x | +34.9% (Better) |
| Instructions | 4,175,144,405 | 2,403,048,727 | 0.58x | +42.4% (Better) |
| IPC | 3.14 | 2.78 | 0.88x | -11.5% (Worse) |
| Cache references | 32,580,533 | 32,571,855 | 1.00x | +0.0% (Better) |
| Cache misses | 22,909,032 | 11,025,147 | 0.48x | +51.9% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 1,296,616,107 | 949,058,299 | 0.73x | +26.8% (Better) |
| L1 dcache misses | 4,226,308 | 7,827,966 | 1.85x | -85.2% (Worse) |
| L1 miss rate (%) | 0.33 | 0.82 | 2.48x | -148.5% (Worse) |
| LLC loads | 1,205,117 | 821,520 | 0.68x | +31.8% (Better) |
| LLC misses | 1,115,509 | 726,284 | 0.65x | +34.9% (Better) |
| LLC miss rate (%) | 92.56 | 88.41 | 0.96x | +4.5% (Better) |
| Branches | 328,041,397 | 127,958,961 | 0.39x | +61.0% (Better) |
| Branch misses | 533,813 | 400,975 | 0.75x | +24.9% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
