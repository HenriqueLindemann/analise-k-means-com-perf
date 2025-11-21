# K-means Performance Analysis Report

**Generated**: 2025-11-20 23:07:09

## Executive Summary

**Overall Speedup**: 3.35x

The optimized version is **3.35x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 3.775s | ±0.138s |
| Optimized | 1.126s | ±0.003s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 15,268,664,110 | 4,768,363,195 | 0.31x | +68.8% (Better) |
| Instructions | 50,889,806,395 | 16,528,106,051 | 0.32x | +67.5% (Better) |
| IPC | 3.33 | 3.47 | 1.04x | +4.0% (Better) |
| Cache references | 208,068,674 | 199,597,095 | 0.96x | +4.1% (Better) |
| Cache misses | 121,189,890 | 55,426,352 | 0.46x | +54.3% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 16,372,108,063 | 7,032,154,082 | 0.43x | +57.0% (Better) |
| L1 dcache misses | 15,534,779 | 73,271,526 | 4.72x | -371.7% (Worse) |
| L1 miss rate (%) | 0.09 | 1.04 | 11.56x | -1055.6% (Worse) |
| LLC loads | 2,705,538 | 2,118,797 | 0.78x | +21.7% (Better) |
| LLC misses | 2,036,255 | 1,472,791 | 0.72x | +27.7% (Better) |
| LLC miss rate (%) | 75.26 | 69.51 | 0.92x | +7.6% (Better) |
| Branches | 2,340,429,216 | 251,163,287 | 0.11x | +89.3% (Better) |
| Branch misses | 880,201 | 92,494 | 0.11x | +89.5% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
