# K-means Performance Analysis Report

**Generated**: 2025-11-15 20:42:15

## Executive Summary

**Overall Speedup**: 2.19x

The optimized version is **2.19x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 2.293s | ±0.016s |
| Optimized | 1.046s | ±0.011s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 6,484,839,828 | 2,894,137,523 | 0.45x | +55.4% (Better) |
| Instructions | 20,241,461,943 | 7,893,419,039 | 0.39x | +61.0% (Better) |
| IPC | 0 | 0 | 0.00x | +0.0% (Worse) |
| Cache references | 143,867,094 | 144,776,730 | 1.01x | -0.6% (Worse) |
| Cache misses | 95,661,025 | 59,971,153 | 0.63x | +37.3% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 6,512,547,078 | 4,213,168,149 | 0.65x | +35.3% (Better) |
| L1 dcache misses | 7,043,452 | 40,793,319 | 5.79x | -479.2% (Worse) |
| L1 miss rate (%) | 0.11 | 0.97 | 8.82x | -781.8% (Worse) |
| Branches | 1,227,539,960 | 167,303,799 | 0.14x | +86.4% (Better) |
| Branch misses | 880,195 | 78,896 | 0.09x | +91.0% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
