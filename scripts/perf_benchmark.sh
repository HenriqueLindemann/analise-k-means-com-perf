#!/bin/bash

# Benchmark completo com perf
# Coleta métricas detalhadas: cycles, IPC, cache misses, branch misses

set -e
export LC_NUMERIC=C

BENCHMARK="bin/kmeans_benchmark"
DATASET="data/dataset.bin"
K=${1:-5}
MAX_ITER=${2:-100}
RUNS=${3:-10}
P_CORES="0-7"

# Eventos a coletar
EVENTS="cycles,instructions,cache-references,cache-misses,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,branches,branch-misses"

echo "========================================"
echo "  K-means Perf Benchmark"
echo "========================================"
echo "Dataset: $DATASET"
echo "K=$K, Iterations=$MAX_ITER, Runs=$RUNS"
echo "P-cores: $P_CORES"
echo ""

# Verificar perf
if ! command -v perf &> /dev/null; then
    echo "Error: perf not found"
    exit 1
fi

# Verificar dataset
if [ ! -f "$DATASET" ]; then
    echo "Error: dataset not found at $DATASET"
    exit 1
fi

# Criar diretório de resultados
mkdir -p scripts/results
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULT_FILE="scripts/results/perf_${TIMESTAMP}.txt"

{
    echo "=== K-means Perf Analysis ==="
    echo "Date: $(date)"
    echo "K=$K, Max iterations=$MAX_ITER, Runs=$RUNS"
    echo "P-cores: $P_CORES"
    echo ""
} > "$RESULT_FILE"

# Função para rodar perf stat
run_perf() {
    local mode=$1
    echo ""
    echo "========================================" | tee -a "$RESULT_FILE"
    echo "  $mode VERSION" | tee -a "$RESULT_FILE"
    echo "========================================" | tee -a "$RESULT_FILE"
    echo ""

    # Executar com perf stat
    taskset -c "$P_CORES" perf stat -e $EVENTS -r $RUNS \
        $BENCHMARK "$mode" $K $MAX_ITER "$DATASET" \
        2>&1 | tee -a "$RESULT_FILE"

    echo "" | tee -a "$RESULT_FILE"
}

# Executar benchmarks
echo "[1/3] Running NAIVE version..."
run_perf "naive"

echo "[2/3] Running OPTIMIZED NO-UNROLL version..."
run_perf "optimized_no_unroll"

echo "[3/3] Running OPTIMIZED WITH-UNROLL version..."
run_perf "optimized"

echo "========================================"
echo "Results saved to: $RESULT_FILE"
echo ""

# Gerar análise automática com Python
if command -v python3 &> /dev/null; then
    echo "Generating analysis..."
    python3 scripts/analyze_perf.py "$RESULT_FILE" > "scripts/results/analysis_${TIMESTAMP}.txt"
    echo ""
    echo "Analysis saved to: scripts/results/analysis_${TIMESTAMP}.txt"
    echo ""
    echo "Quick summary:"
    cat "scripts/results/analysis_${TIMESTAMP}.txt"
else
    echo "Python3 not found. Skipping automatic analysis."
    echo "Run manually: python3 scripts/analyze_perf.py $RESULT_FILE"
fi
