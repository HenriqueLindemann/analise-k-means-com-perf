# K-means Performance Analysis Report

**Generated**: 2025-11-15 21:21:41

## Executive Summary

**Overall Speedup**: 1.22x

The optimized version is **1.22x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.216s | ±0.011s |
| Optimized | 2.639s | ±0.005s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 14,019,711,813 | 11,507,390,745 | 0.82x | +17.9% (Better) |
| Instructions | 47,624,748,043 | 42,636,054,828 | 0.90x | +10.5% (Better) |
| IPC | 3.40 | 3.71 | 1.09x | +9.1% (Better) |
| Cache references | 212,331,885 | 172,391,503 | 0.81x | +18.8% (Better) |
| Cache misses | 118,525,967 | 41,031,716 | 0.35x | +65.4% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 15,285,589,830 | 16,120,097,472 | 1.05x | -5.5% (Worse) |
| L1 dcache misses | 28,336,685 | 87,604,527 | 3.09x | -209.2% (Worse) |
| L1 miss rate (%) | 0.19 | 0.54 | 2.84x | -184.2% (Worse) |
| Branches | 2,184,814,886 | 1,327,057,309 | 0.61x | +39.3% (Better) |
| Branch misses | 1,033,034 | 58,137 | 0.06x | +94.4% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
