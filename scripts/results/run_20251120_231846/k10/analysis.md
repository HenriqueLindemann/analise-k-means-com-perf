# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:28:29

## Executive Summary

**Overall Speedup**: 3.09x

The optimized version is **3.09x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.422s | ±0.012s |
| Optimized | 1.107s | ±0.009s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 14,937,767,325 | 4,751,295,801 | 0.32x | +68.2% (Better) |
| Instructions | 50,869,265,608 | 16,519,056,773 | 0.32x | +67.5% (Better) |
| IPC | 3.41 | 3.48 | 1.02x | +2.1% (Better) |
| Cache references | 207,463,020 | 198,964,111 | 0.96x | +4.1% (Better) |
| Cache misses | 114,911,054 | 49,443,192 | 0.43x | +57.0% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 16,374,073,620 | 7,039,259,060 | 0.43x | +57.0% (Better) |
| L1 dcache misses | 20,902,509 | 100,562,198 | 4.81x | -381.1% (Worse) |
| L1 miss rate (%) | 0.13 | 1.43 | 11.00x | -1000.0% (Worse) |
| LLC loads | 2,984,757 | 2,572,695 | 0.86x | +13.8% (Better) |
| LLC misses | 2,238,367 | 1,846,426 | 0.82x | +17.5% (Better) |
| LLC miss rate (%) | 74.99 | 71.77 | 0.96x | +4.3% (Better) |
| Branches | 2,339,436,240 | 248,511,139 | 0.11x | +89.4% (Better) |
| Branch misses | 839,899 | 74,966 | 0.09x | +91.1% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
