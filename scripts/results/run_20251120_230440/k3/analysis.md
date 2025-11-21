# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:04:50

## Executive Summary

**Overall Speedup**: 1.39x

The optimized version is **1.39x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 0.164s | ±0.001s |
| Optimized | 0.118s | ±0.004s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 615,280,816 | 468,239,736 | 0.76x | +23.9% (Better) |
| Instructions | 1,818,708,066 | 1,216,865,691 | 0.67x | +33.1% (Better) |
| IPC | 2.96 | 2.60 | 0.88x | -12.1% (Worse) |
| Cache references | 15,930,092 | 16,360,227 | 1.03x | -2.7% (Worse) |
| Cache misses | 11,869,967 | 6,928,994 | 0.58x | +41.6% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 557,147,064 | 481,375,668 | 0.86x | +13.6% (Better) |
| L1 dcache misses | 1,145,441 | 6,216,738 | 5.43x | -442.7% (Worse) |
| L1 miss rate (%) | 0.21 | 1.29 | 6.14x | -514.3% (Worse) |
| LLC loads | 791,216 | 902,790 | 1.14x | -14.1% (Worse) |
| LLC misses | 739,836 | 709,546 | 0.96x | +4.1% (Better) |
| LLC miss rate (%) | 93.51 | 78.59 | 0.84x | +16.0% (Better) |
| Branches | 177,703,121 | 102,960,818 | 0.58x | +42.1% (Better) |
| Branch misses | 73,962 | 271,388 | 3.67x | -266.9% (Worse) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
