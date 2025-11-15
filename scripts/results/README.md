# Results Directory Structure

This directory contains organized benchmark results from automated analysis runs.

## Directory Structure

```
scripts/results/
├── run_YYYYMMDD_HHMMSS/          # Each run gets a timestamped folder
│   ├── validation.txt             # Validation output (naive vs optimized)
│   ├── perf_raw.txt              # Raw perf stat output
│   ├── analysis.txt              # Text analysis summary
│   ├── analysis.md               # Markdown detailed report
│   ├── clusters_naive.csv        # Cluster assignments (naive)
│   ├── clusters_optimized.csv    # Cluster assignments (optimized)
│   └── graphs/
│       ├── performance/          # Performance comparison graphs
│       │   ├── execution_time.png
│       │   ├── cache_misses.png
│       │   ├── ipc.png
│       │   ├── metrics_comparison.png
│       │   └── improvements.png
│       └── clusters/              # Cluster visualization graphs
│           ├── clusters_comparison.png
│           ├── cluster_distribution.png
│           └── cluster_centroids_heatmap.png
└── latest -> run_YYYYMMDD_HHMMSS  # Symlink to most recent run
```

## Files Description

### validation.txt
Contains the output of correctness validation comparing naive and optimized implementations:
- Centroid comparison (distance between corresponding centroids)
- Cluster distribution (number of points per cluster)
- Inertia comparison (sum of squared distances)
- Final validation result (PASSED/FAILED)

### perf_raw.txt
Raw output from `perf stat` containing:
- Execution times for both versions
- Hardware performance counters (cycles, instructions, cache events, branches)
- Statistical data across multiple runs

### analysis.txt
Human-readable summary including:
- Execution time comparison
- Speedup calculation
- Detailed metrics comparison
- Key insights

### analysis.md
Markdown report with:
- Executive summary
- Performance metrics tables
- Comparison ratios and improvements

### Performance Graphs
Visual comparisons of key metrics:
- **execution_time.png**: Bar chart comparing execution time
- **cache_misses.png**: Cache miss comparison
- **ipc.png**: Instructions per cycle comparison
- **metrics_comparison.png**: Side-by-side metric comparison
- **improvements.png**: Percentage improvements visualization

### Cluster Graphs
Clustering result visualizations:
- **clusters_comparison.png**: Scatter plot of clusters (naive vs optimized)
- **cluster_distribution.png**: Bar charts showing point distribution per cluster
- **cluster_centroids_heatmap.png**: Heatmap of normalized centroid values

## Accessing Results

### Latest Results
```bash
# View latest analysis
cat scripts/results/latest/analysis.txt

# View latest validation
cat scripts/results/latest/validation.txt

# Open latest performance graphs
xdg-open scripts/results/latest/graphs/performance/
```

### Specific Run
```bash
# List all runs
ls -lt scripts/results/

# View specific run
cat scripts/results/run_20251115_120000/analysis.txt
```

## Cleanup

To clean up old results:
```bash
# Remove all results except latest
find scripts/results -name "run_*" -not -path "$(readlink scripts/results/latest)" -exec rm -rf {} +

# Remove all results
rm -rf scripts/results/run_*
```

## Reproducibility

Each run is self-contained with:
- Exact parameters (K, iterations, runs)
- Validation results
- Raw performance data
- All generated visualizations

This allows comparing different optimization attempts or parameter configurations.
