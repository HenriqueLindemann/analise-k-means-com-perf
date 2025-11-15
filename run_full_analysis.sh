#!/bin/bash

# Script completo: validação -> benchmark -> análise
# Organiza resultados em pastas estruturadas

set -e

K=${1:-5}
ITER=${2:-100}
RUNS=${3:-15}

# Criar pasta de resultados com timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="scripts/results/run_${TIMESTAMP}"
mkdir -p "$RESULTS_DIR"/{graphs/performance,graphs/clusters}

echo "========================================"
echo "  K-means Complete Analysis Pipeline"
echo "========================================"
echo "K=$K, Iterations=$ITER, Runs=$RUNS"
echo "Results directory: $RESULTS_DIR"
echo ""

# 1. Verificar compilação
if [ ! -f "bin/kmeans_benchmark" ] || [ ! -f "bin/validate_results" ]; then
    echo "[1/5] Compiling..."
    make clean && make release
else
    echo "[1/5] Binaries already compiled"
fi

# 2. Verificar dataset
if [ ! -f "data/dataset.bin" ]; then
    echo "[2/5] Processing dataset..."
    bin/preprocessor 0
else
    echo "[2/5] Dataset already processed"
fi

# 3. Validar equivalência entre versões
echo "[3/5] Validating algorithm correctness..."
bin/validate_results $K $ITER data/dataset.bin > "$RESULTS_DIR/validation.txt" 2>&1

if [ $? -eq 0 ]; then
    echo "  ✓ Validation passed"
    tail -8 "$RESULTS_DIR/validation.txt"
else
    echo "  ✗ Validation FAILED! Check $RESULTS_DIR/validation.txt"
    exit 1
fi

# 4. Rodar benchmark com perf
echo "[4/5] Running benchmark with perf..."
export LC_NUMERIC=C

BENCHMARK="bin/kmeans_benchmark"
DATASET="data/dataset.bin"
P_CORES="0-7"
EVENTS="cycles,instructions,cache-references,cache-misses,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,branches,branch-misses"

PERF_FILE="$RESULTS_DIR/perf_raw.txt"

{
    echo "=== K-means Perf Analysis ==="
    echo "Date: $(date)"
    echo "K=$K, Max iterations=$ITER, Runs=$RUNS"
    echo "P-cores: $P_CORES"
    echo ""
} > "$PERF_FILE"

# Função para rodar perf stat
run_perf() {
    local mode=$1
    echo ""
    echo "========================================" | tee -a "$PERF_FILE"
    echo "  $mode VERSION" | tee -a "$PERF_FILE"
    echo "========================================" | tee -a "$PERF_FILE"
    echo ""

    # Executar com perf stat
    taskset -c "$P_CORES" perf stat -e $EVENTS -r $RUNS \
        $BENCHMARK "$mode" $K $ITER "$DATASET" \
        2>&1 | tee -a "$PERF_FILE"

    echo "" | tee -a "$PERF_FILE"
}

echo "  Running NAIVE version..."
run_perf "naive"

echo "  Running OPTIMIZED version..."
run_perf "optimized"

echo "  ✓ Benchmark complete"

# 5. Gerar análise e visualizações
echo "[5/5] Generating analysis and visualizations..."

ANALYSIS_TXT="$RESULTS_DIR/analysis.txt"
ANALYSIS_MD="$RESULTS_DIR/analysis.md"

# Gerar análise em texto
echo "  [5.1] Generating text analysis..."
python3 scripts/analyze_perf.py "$PERF_FILE" > "$ANALYSIS_TXT"
if [ $? -ne 0 ]; then
    echo "  ✗ Failed to generate text analysis"
    exit 1
fi

# Gerar análise em markdown com gráficos de performance
echo "  [5.2] Generating markdown and performance graphs..."
python3 scripts/analyze_perf.py "$PERF_FILE" "$ANALYSIS_MD" "$K" "$DATASET"
if [ $? -ne 0 ]; then
    echo "  ✗ Failed to generate markdown analysis"
    exit 1
fi

# Verificar se gráficos de performance foram gerados
echo "  [5.3] Organizing performance graphs..."
# Small delay to ensure all files are flushed to disk
sleep 1
graph_count=0
for graph in execution_time cache_misses ipc metrics_comparison improvements; do
    if [ -f "$RESULTS_DIR/${graph}.png" ]; then
        mv "$RESULTS_DIR/${graph}.png" "$RESULTS_DIR/graphs/performance/"
        graph_count=$((graph_count + 1))
    fi
done
echo "      ✓ $graph_count performance graphs organized"

# Verificar se gráficos de clusters foram gerados
echo "  [5.4] Organizing cluster graphs..."
cluster_count=0
for graph in clusters_comparison cluster_distribution cluster_centroids_heatmap; do
    if [ -f "$RESULTS_DIR/${graph}.png" ]; then
        mv "$RESULTS_DIR/${graph}.png" "$RESULTS_DIR/graphs/clusters/"
        cluster_count=$((cluster_count + 1))
    fi
done
echo "      ✓ $cluster_count cluster graphs organized"

# Limpar arquivos temporários apenas se existirem
echo "  [5.5] Cleaning up temporary files..."
removed=0
if [ -f scripts/results/clusters_naive.csv ] || [ -f scripts/results/clusters_optimized.csv ]; then
    rm -f scripts/results/clusters_*.csv scripts/results/clusters_*.bin 2>/dev/null
    removed=1
fi
if [ $removed -eq 1 ]; then
    echo "      ✓ Temporary files removed"
else
    echo "      ✓ No temporary files to remove"
fi

echo "  ✓ Analysis and visualizations complete"

# Criar symlink para latest
rm -f scripts/results/latest
ln -sf "run_${TIMESTAMP}" scripts/results/latest

echo ""
echo "========================================"
echo "  Pipeline Complete!"
echo "========================================"
echo ""
echo "Results saved to: $RESULTS_DIR"
echo ""
echo "Generated files:"
echo "  - Validation:    $RESULTS_DIR/validation.txt"
echo "  - Perf raw data: $RESULTS_DIR/perf_raw.txt"
echo "  - Analysis (txt): $RESULTS_DIR/analysis.txt"
echo "  - Analysis (md):  $RESULTS_DIR/analysis.md"
echo "  - Performance graphs: $RESULTS_DIR/graphs/performance/"
echo "  - Cluster graphs:     $RESULTS_DIR/graphs/clusters/"
echo ""
echo "Quick view:"
echo "  cat $RESULTS_DIR/analysis.txt"
echo ""
echo "Latest results always at:"
echo "  scripts/results/latest/"
echo ""
