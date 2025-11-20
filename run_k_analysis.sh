#!/bin/bash

# Script para análise de K-means variando o valor de K
# Testa diferentes valores de K e gera gráficos comparativos

set -e

ITER=${1:-100}
RUNS=${2:-5}
K_VALUES=${3:-"2 3 4 5 6 7 8"}

# Criar pasta de resultados com timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="scripts/results/k_analysis_${TIMESTAMP}"
mkdir -p "$RESULTS_DIR"

echo "========================================"
echo "  K-means K-Value Analysis Pipeline"
echo "========================================"
echo "Iterations=$ITER, Runs per K=$RUNS"
echo "K values: $K_VALUES"
echo "Results directory: $RESULTS_DIR"
echo ""

# 1. Verificar compilação
if [ ! -f "bin/kmeans_benchmark" ]; then
    echo "[1/4] Compiling..."
    make release
else
    echo "[1/4] Binaries already compiled"
fi

# 2. Verificar dataset
if [ ! -f "data/dataset.bin" ]; then
    echo "[2/4] Processing dataset..."
    bin/preprocessor 0
else
    echo "[2/4] Dataset already processed"
fi

echo ""
echo "[3/4] Running benchmarks for different K values..."

# Loop sobre diferentes valores de K
for K in $K_VALUES; do
    echo ""
    echo "  Testing K=$K..."

    K_DIR="$RESULTS_DIR/k${K}"
    mkdir -p "$K_DIR"

    PERF_FILE="$K_DIR/perf_raw.txt"

    # Rodar naive
    echo "    Running naive..."
    {
        echo "========================================"
        echo "  naive VERSION (K=$K)"
        echo "========================================"
        echo ""

        for run in $(seq 1 $RUNS); do
            taskset -c 0-7 bin/kmeans_benchmark naive $K $ITER data/dataset.bin
        done

        echo ""
        taskset -c 0-7 perf stat -r $RUNS -e cpu_core/cycles/,cpu_core/instructions/,cpu_core/cache-references/,cpu_core/cache-misses/,cpu_core/L1-dcache-loads/,cpu_core/L1-dcache-load-misses/,cpu_core/LLC-loads/,cpu_core/LLC-load-misses/,cpu_core/branches/,cpu_core/branch-misses/ bin/kmeans_benchmark naive $K $ITER data/dataset.bin 2>&1

    } > "$PERF_FILE"

    # Rodar optimized no-unroll
    echo "    Running optimized no-unroll..."
    {
        echo ""
        echo "========================================"
        echo "  optimized_no_unroll VERSION (K=$K)"
        echo "========================================"
        echo ""

        for run in $(seq 1 $RUNS); do
            taskset -c 0-7 bin/kmeans_benchmark optimized_no_unroll $K $ITER data/dataset.bin
        done

        echo ""
        taskset -c 0-7 perf stat -r $RUNS -e cpu_core/cycles/,cpu_core/instructions/,cpu_core/cache-references/,cpu_core/cache-misses/,cpu_core/L1-dcache-loads/,cpu_core/L1-dcache-load-misses/,cpu_core/LLC-loads/,cpu_core/LLC-load-misses/,cpu_core/branches/,cpu_core/branch-misses/ bin/kmeans_benchmark optimized_no_unroll $K $ITER data/dataset.bin 2>&1

    } >> "$PERF_FILE"

    # Rodar optimized with-unroll
    echo "    Running optimized with-unroll..."
    {
        echo ""
        echo "========================================"
        echo "  optimized VERSION (K=$K)"
        echo "========================================"
        echo ""

        for run in $(seq 1 $RUNS); do
            taskset -c 0-7 bin/kmeans_benchmark optimized $K $ITER data/dataset.bin
        done

        echo ""
        taskset -c 0-7 perf stat -r $RUNS -e cpu_core/cycles/,cpu_core/instructions/,cpu_core/cache-references/,cpu_core/cache-misses/,cpu_core/L1-dcache-loads/,cpu_core/L1-dcache-load-misses/,cpu_core/LLC-loads/,cpu_core/LLC-load-misses/,cpu_core/branches/,cpu_core/branch-misses/ bin/kmeans_benchmark optimized $K $ITER data/dataset.bin 2>&1

    } >> "$PERF_FILE"

    echo "    Done K=$K"
done

echo ""
echo "[4/4] Generating analysis and visualizations..."

# Gerar análise comparativa de K
python3 scripts/analyze_k_values.py "$RESULTS_DIR" "$K_VALUES"

echo ""
echo "========================================"
echo "  Analysis Complete!"
echo "========================================"
echo ""
echo "Results saved to: $RESULTS_DIR"
echo ""
echo "Generated files:"
echo "  - $RESULTS_DIR/k_analysis.txt"
echo "  - $RESULTS_DIR/k_analysis.md"
echo "  - $RESULTS_DIR/graphs/*.png"
echo ""
echo "Quick view:"
echo "  cat $RESULTS_DIR/k_analysis.txt"
echo ""

# Criar symlink
ln -sf "k_analysis_${TIMESTAMP}" scripts/results/latest_k_analysis
echo "Latest results also at: scripts/results/latest_k_analysis/"
