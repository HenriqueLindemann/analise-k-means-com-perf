# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:43:07

## Executive Summary

**Overall Speedup**: 0.91x

The optimized version is **1.10x slower** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.715s | ±0.010s |
| Optimized | 1.880s | ±0.018s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 4,912,597,258 | 5,174,139,587 | 1.05x | -5.3% (Worse) |
| Instructions | 15,496,969,296 | 17,350,657,294 | 1.12x | -12.0% (Worse) |
| IPC | 0 | 0 | 0.00x | +0.0% (Worse) |
| Cache references | 93,875,165 | 92,360,636 | 0.98x | +1.6% (Better) |
| Cache misses | 59,401,392 | 31,507,610 | 0.53x | +47.0% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 4,880,418,080 | 6,755,071,720 | 1.38x | -38.4% (Worse) |
| L1 dcache misses | 4,936,990 | 39,765,634 | 8.05x | -705.5% (Worse) |
| L1 miss rate (%) | 0.10 | 0.59 | 5.90x | -490.0% (Worse) |
| Branches | 910,929,498 | 653,239,511 | 0.72x | +28.3% (Better) |
| Branch misses | 900,925 | 109,873 | 0.12x | +87.8% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
