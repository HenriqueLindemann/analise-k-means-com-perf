# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:06:08

## Executive Summary

**Overall Speedup**: 2.80x

The optimized version is **2.80x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 2.336s | ±0.058s |
| Optimized | 0.834s | ±0.004s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 9,653,729,326 | 3,542,683,850 | 0.37x | +63.3% (Better) |
| Instructions | 31,204,598,822 | 10,162,159,385 | 0.33x | +67.4% (Better) |
| IPC | 3.23 | 2.87 | 0.89x | -11.3% (Worse) |
| Cache references | 152,062,756 | 159,474,055 | 1.05x | -4.9% (Worse) |
| Cache misses | 96,385,851 | 47,373,159 | 0.49x | +50.9% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 9,987,288,038 | 5,041,888,823 | 0.50x | +49.5% (Better) |
| L1 dcache misses | 35,513,873 | 39,017,479 | 1.10x | -9.9% (Worse) |
| L1 miss rate (%) | 0.36 | 0.77 | 2.14x | -113.9% (Worse) |
| LLC loads | 4,823,423 | 1,454,542 | 0.30x | +69.8% (Better) |
| LLC misses | 4,308,576 | 1,094,890 | 0.25x | +74.6% (Better) |
| LLC miss rate (%) | 89.33 | 75.27 | 0.84x | +15.7% (Better) |
| Branches | 1,591,811,829 | 176,614,624 | 0.11x | +88.9% (Better) |
| Branch misses | 1,187,465 | 84,313 | 0.07x | +92.9% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
