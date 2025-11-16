# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:59:19

## Executive Summary

**Overall Speedup**: 1.18x

The optimized version is **1.18x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 5.195s | ±0.032s |
| Optimized | 4.397s | ±0.020s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 15,058,543,010 | 12,814,742,086 | 0.85x | +14.9% (Better) |
| Instructions | 47,655,630,362 | 42,659,628,875 | 0.90x | +10.5% (Better) |
| IPC | 3.16 | 3.33 | 1.05x | +5.2% (Better) |
| Cache references | 214,472,932 | 174,022,712 | 0.81x | +18.9% (Better) |
| Cache misses | 123,420,345 | 56,712,351 | 0.46x | +54.0% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 15,286,794,704 | 16,120,549,045 | 1.05x | -5.5% (Worse) |
| L1 dcache misses | 12,085,231 | 76,143,422 | 6.30x | -530.1% (Worse) |
| L1 miss rate (%) | 0.08 | 0.47 | 5.87x | -487.5% (Worse) |
| Branches | 2,186,618,596 | 1,330,373,472 | 0.61x | +39.2% (Better) |
| Branch misses | 1,201,137 | 181,670 | 0.15x | +84.9% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
