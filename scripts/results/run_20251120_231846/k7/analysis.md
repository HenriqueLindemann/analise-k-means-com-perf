# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:22:14

## Executive Summary

**Overall Speedup**: 2.27x

The optimized version is **2.27x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.595s | ±0.006s |
| Optimized | 0.261s | ±0.002s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 2,591,801,841 | 1,121,477,616 | 0.43x | +56.7% (Better) |
| Instructions | 8,308,594,777 | 3,096,864,444 | 0.37x | +62.7% (Better) |
| IPC | 3.21 | 2.76 | 0.86x | -13.9% (Worse) |
| Cache references | 45,080,170 | 47,134,151 | 1.05x | -4.6% (Worse) |
| Cache misses | 27,143,624 | 13,603,670 | 0.50x | +49.9% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 2,680,182,552 | 1,473,813,869 | 0.55x | +45.0% (Better) |
| L1 dcache misses | 15,153,946 | 25,733,315 | 1.70x | -69.8% (Worse) |
| L1 miss rate (%) | 0.57 | 1.75 | 3.07x | -207.0% (Worse) |
| LLC loads | 2,188,269 | 1,292,782 | 0.59x | +40.9% (Better) |
| LLC misses | 2,018,903 | 985,901 | 0.49x | +51.2% (Better) |
| LLC miss rate (%) | 92.26 | 76.26 | 0.83x | +17.3% (Better) |
| Branches | 472,853,434 | 104,999,245 | 0.22x | +77.8% (Better) |
| Branch misses | 499,978 | 67,693 | 0.14x | +86.5% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
