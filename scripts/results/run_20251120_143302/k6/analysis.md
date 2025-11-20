# K-means Performance Analysis Report

**Generated**: 2025-11-20 14:35:09

## Executive Summary

**Overall Speedup**: 2.54x

The optimized version is **2.54x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.078s | ±0.009s |
| Optimized | 0.425s | ±0.002s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 4,640,935,396 | 1,798,442,204 | 0.39x | +61.2% (Better) |
| Instructions | 15,317,367,665 | 5,237,637,514 | 0.34x | +65.8% (Better) |
| IPC | 3.30 | 2.91 | 0.88x | -11.8% (Worse) |
| Cache references | 93,196,717 | 90,618,099 | 0.97x | +2.8% (Better) |
| Cache misses | 61,133,077 | 29,684,178 | 0.49x | +51.4% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 4,877,209,118 | 2,640,885,556 | 0.54x | +45.9% (Better) |
| L1 dcache misses | 13,670,057 | 32,296,035 | 2.36x | -136.3% (Worse) |
| L1 miss rate (%) | 0.28 | 1.22 | 4.36x | -335.7% (Worse) |
| LLC loads | 2,231,332 | 1,384,056 | 0.62x | +38.0% (Better) |
| LLC misses | 1,973,544 | 1,089,686 | 0.55x | +44.8% (Better) |
| LLC miss rate (%) | 88.45 | 78.73 | 0.89x | +11.0% (Better) |
| Branches | 909,739,689 | 132,658,150 | 0.15x | +85.4% (Better) |
| Branch misses | 857,492 | 65,597 | 0.08x | +92.4% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
