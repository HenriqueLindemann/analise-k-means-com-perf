# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:54:32

## Executive Summary

**Overall Speedup**: 2.25x

The optimized version is **2.25x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 2.008s | ±0.028s |
| Optimized | 0.891s | ±0.009s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 6,362,220,807 | 2,779,927,959 | 0.44x | +56.3% (Better) |
| Instructions | 20,234,530,196 | 7,896,038,152 | 0.39x | +61.0% (Better) |
| IPC | 3.18 | 2.84 | 0.89x | -10.7% (Worse) |
| Cache references | 143,720,414 | 144,889,016 | 1.01x | -0.8% (Worse) |
| Cache misses | 93,541,663 | 49,170,968 | 0.53x | +47.4% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 6,513,599,027 | 4,217,299,659 | 0.65x | +35.3% (Better) |
| L1 dcache misses | 6,666,172 | 41,096,402 | 6.16x | -516.5% (Worse) |
| L1 miss rate (%) | 0.10 | 0.97 | 9.70x | -870.0% (Worse) |
| Branches | 1,226,845,528 | 167,893,613 | 0.14x | +86.3% (Better) |
| Branch misses | 853,969 | 73,443 | 0.09x | +91.4% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
