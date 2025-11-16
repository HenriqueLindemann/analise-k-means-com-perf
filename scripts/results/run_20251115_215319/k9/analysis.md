# K-means Performance Analysis Report

**Generated**: 2025-11-15 22:00:03

## Executive Summary

**Overall Speedup**: 1.21x

The optimized version is **1.21x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.210s | ±0.017s |
| Optimized | 2.649s | ±0.005s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 14,014,111,067 | 11,569,447,426 | 0.83x | +17.4% (Better) |
| Instructions | 47,624,806,753 | 42,637,260,421 | 0.90x | +10.5% (Better) |
| IPC | 3.40 | 3.69 | 1.08x | +8.4% (Better) |
| Cache references | 212,275,756 | 172,058,301 | 0.81x | +18.9% (Better) |
| Cache misses | 117,284,540 | 40,845,445 | 0.35x | +65.2% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 15,286,654,321 | 16,119,268,172 | 1.05x | -5.4% (Worse) |
| L1 dcache misses | 32,130,465 | 116,368,594 | 3.62x | -262.2% (Worse) |
| L1 miss rate (%) | 0.21 | 0.72 | 3.43x | -242.9% (Worse) |
| LLC loads | 4,068,307 | 3,128,300 | 0.77x | +23.1% (Better) |
| LLC misses | 3,322,345 | 2,152,957 | 0.65x | +35.2% (Better) |
| LLC miss rate (%) | 81.66 | 68.82 | 0.84x | +15.7% (Better) |
| Branches | 2,184,914,119 | 1,327,149,328 | 0.61x | +39.3% (Better) |
| Branch misses | 1,033,055 | 55,544 | 0.05x | +94.6% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
