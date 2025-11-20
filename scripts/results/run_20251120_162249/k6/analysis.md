# K-means Performance Analysis Report

**Generated**: 2025-11-20 16:25:59

## Executive Summary

**Overall Speedup**: 2.52x

The optimized version is **2.52x faster** than naive.

## Execution Time

| Version | Time | Std Dev |
|---------|------|----------|
| Naive | 1.109s | ±0.013s |
| Optimized | 0.439s | ±0.006s |

## Performance Metrics

| Metric | Naive | Optimized | Ratio | Improvement |
|--------|-------|-----------|-------|-------------|
| Cycles | 4,837,952,663 | 1,884,842,025 | 0.39x | +61.0% (Better) |
| Instructions | 15,309,257,428 | 5,235,154,400 | 0.34x | +65.8% (Better) |
| IPC | 3.16 | 2.78 | 0.88x | -12.2% (Worse) |
| Cache references | 93,041,174 | 90,929,853 | 0.98x | +2.3% (Better) |
| Cache misses | 55,092,160 | 27,186,091 | 0.49x | +50.7% (Better) |
| Cache miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
| L1 dcache loads | 4,876,757,245 | 2,635,463,543 | 0.54x | +46.0% (Better) |
| L1 dcache misses | 39,052,764 | 65,582,402 | 1.68x | -67.9% (Worse) |
| L1 miss rate (%) | 0.80 | 2.49 | 3.11x | -211.3% (Worse) |
| LLC loads | 5,022,009 | 2,234,906 | 0.45x | +55.5% (Better) |
| LLC misses | 4,668,825 | 1,841,840 | 0.39x | +60.6% (Better) |
| LLC miss rate (%) | 92.97 | 82.41 | 0.89x | +11.4% (Better) |
| Branches | 909,718,188 | 132,698,402 | 0.15x | +85.4% (Better) |
| Branch misses | 835,475 | 73,312 | 0.09x | +91.2% (Better) |
| Branch miss rate (%) | 0 | 0 | 0.00x | +0.0% (Better) |
