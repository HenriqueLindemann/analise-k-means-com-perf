#!/bin/bash

# Script completo: validação -> benchmark -> análise para múltiplos valores de K
# Organiza resultados em pastas estruturadas por K

set -e

# Argumentos
K_VALUES=${1:-"5"}
ITER=${2:-100}
RUNS=${3:-15}

# Criar pasta de resultados com timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="scripts/results/run_${TIMESTAMP}"
mkdir -p "$RESULTS_DIR"

echo "========================================"
echo "  K-means Complete Analysis Pipeline"
echo "========================================"
echo "K values: $K_VALUES"
echo "Iterations: $ITER, Runs per K: $RUNS"
echo "Results directory: $RESULTS_DIR"
echo ""

# 1. Verificar compilação
if [ ! -f "bin/kmeans_benchmark" ] || [ ! -f "bin/validate_results" ]; then
    echo "[1/3] Compiling..."
    make clean && make release
else
    echo "[1/3] Binaries already compiled"
fi

# 2. Verificar dataset
if [ ! -f "data/dataset.bin" ]; then
    echo "[2/3] Processing dataset..."
    bin/preprocessor 0
else
    echo "[2/3] Dataset already processed"
fi

echo ""
echo "[3/3] Running analysis for each K value..."
echo ""

# Converter K_VALUES em array
K_ARRAY=($K_VALUES)
DATASET="data/dataset.bin"
P_CORES="0-7"

# Função para rodar workflow completo para um K
run_k_workflow() {
    local K=$1
    local K_DIR="$RESULTS_DIR/k${K}"

    echo "========================================"
    echo "  Processing K=$K"
    echo "========================================"

    # Criar diretórios
    mkdir -p "$K_DIR"
    mkdir -p "$K_DIR/graphs/performance"
    mkdir -p "$K_DIR/graphs/clusters"

    # [A] Validação
    echo "  [A] Validating correctness..."
    bin/validate_results $K $ITER "$DATASET" > "$K_DIR/validation.txt" 2>&1

    if [ $? -eq 0 ]; then
        echo "      ✓ Validation passed for K=$K"
    else
        echo "      ✗ Validation FAILED for K=$K!"
        echo "      Check $K_DIR/validation.txt"
        return 1
    fi

    # [B] Benchmark com perf
    echo "  [B] Running benchmark with perf..."

    export LC_NUMERIC=C
    PERF_FILE="$K_DIR/perf_raw.txt"

    {
        echo "=== K-means Perf Analysis ==="
        echo "Date: $(date)"
        echo "K=$K, Max iterations=$ITER, Runs=$RUNS"
        echo "P-cores: $P_CORES"
        echo ""
    } > "$PERF_FILE"

    # Rodar naive
    echo "      Running naive..."
    {
        echo ""
        echo "========================================"
        echo "  naive VERSION"
        echo "========================================"
        echo ""

        taskset -c "$P_CORES" perf stat -r $RUNS \
            -e cpu_core/cycles/,cpu_core/instructions/,cpu_core/cache-references/,cpu_core/cache-misses/,cpu_core/L1-dcache-loads/,cpu_core/L1-dcache-load-misses/,cpu_core/LLC-loads/,cpu_core/LLC-load-misses/,cpu_core/branches/,cpu_core/branch-misses/ \
            bin/kmeans_benchmark naive $K $ITER "$DATASET" 2>&1

    } >> "$PERF_FILE"

    # Rodar optimized
    echo "      Running optimized..."
    {
        echo ""
        echo "========================================"
        echo "  optimized VERSION"
        echo "========================================"
        echo ""

        taskset -c "$P_CORES" perf stat -r $RUNS \
            -e cpu_core/cycles/,cpu_core/instructions/,cpu_core/cache-references/,cpu_core/cache-misses/,cpu_core/L1-dcache-loads/,cpu_core/L1-dcache-load-misses/,cpu_core/LLC-loads/,cpu_core/LLC-load-misses/,cpu_core/branches/,cpu_core/branch-misses/ \
            bin/kmeans_benchmark optimized $K $ITER "$DATASET" 2>&1

    } >> "$PERF_FILE"

    # [C] Análise e visualizações
    echo "  [C] Generating analysis and visualizations..."

    ANALYSIS_TXT="$K_DIR/analysis.txt"
    ANALYSIS_MD="$K_DIR/analysis.md"

    # Análise em texto
    python3 scripts/analyze_perf.py "$PERF_FILE" > "$ANALYSIS_TXT"

    # Análise em markdown + gráficos (já salvos nas pastas corretas)
    python3 scripts/analyze_perf.py "$PERF_FILE" "$ANALYSIS_MD" "$K" "$DATASET" 2>&1 | grep -v "Warning:" || true

    # Mover arquivos de clusters para o diretório K
    mv scripts/results/clusters_naive.csv "$K_DIR/" 2>/dev/null || true
    mv scripts/results/clusters_naive.bin "$K_DIR/" 2>/dev/null || true
    mv scripts/results/clusters_optimized.csv "$K_DIR/" 2>/dev/null || true
    mv scripts/results/clusters_optimized.bin "$K_DIR/" 2>/dev/null || true

    echo "      ✓ K=$K complete"
    echo ""
}

# Executar workflow para cada K
for K in ${K_ARRAY[@]}; do
    run_k_workflow $K
done

# Se houver múltiplos K, gerar análise comparativa
if [ ${#K_ARRAY[@]} -gt 1 ]; then
    echo "========================================"
    echo "  Generating K Comparison Analysis"
    echo "========================================"

    COMP_DIR="$RESULTS_DIR/k_comparison"
    mkdir -p "$COMP_DIR/graphs"

    # Criar lista de K values para o script Python
    K_LIST=""
    for K in ${K_ARRAY[@]}; do
        K_LIST="$K_LIST $K"
    done

    # Gerar análise comparativa
    python3 scripts/analyze_k_comparison.py "$RESULTS_DIR" "$K_LIST" 2>&1 | grep -v "Warning:" || true

    echo "  ✓ Comparison analysis complete"
    echo ""
fi

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

if [ ${#K_ARRAY[@]} -eq 1 ]; then
    K=${K_ARRAY[0]}
    echo "Generated files (K=$K):"
    echo "  - Validation:         $RESULTS_DIR/k${K}/validation.txt"
    echo "  - Perf raw data:      $RESULTS_DIR/k${K}/perf_raw.txt"
    echo "  - Analysis (txt):     $RESULTS_DIR/k${K}/analysis.txt"
    echo "  - Analysis (md):      $RESULTS_DIR/k${K}/analysis.md"
    echo "  - Performance graphs: $RESULTS_DIR/k${K}/graphs/performance/"
    echo "  - Cluster graphs:     $RESULTS_DIR/k${K}/graphs/clusters/"
    echo ""
    echo "Quick view:"
    echo "  cat $RESULTS_DIR/k${K}/analysis.txt"
else
    echo "Generated files:"
    for K in ${K_ARRAY[@]}; do
        echo "  - K=$K results:       $RESULTS_DIR/k${K}/"
    done
    echo "  - K comparison:       $RESULTS_DIR/k_comparison/"
    echo ""
    echo "Quick view:"
    echo "  cat $RESULTS_DIR/k_comparison/k_analysis.txt"
fi

echo ""
echo "Latest results always at:"
echo "  scripts/results/latest/"
echo ""
