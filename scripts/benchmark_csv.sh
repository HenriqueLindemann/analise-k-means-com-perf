#!/bin/bash

# Script para rodar benchmarks e salvar resultados em CSV
# Para uso com perf (se disponível) ou apenas tempo

set -e

# Forçar locale com ponto decimal
export LC_NUMERIC=C

BENCHMARK="bin/kmeans_benchmark"
DATASET="data/dataset.bin"
K=${1:-5}
MAX_ITER=${2:-100}
RUNS=${3:-20}
P_CORES="0-7"

# Criar diretório de resultados
mkdir -p scripts/results
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CSV_FILE="scripts/results/benchmark_${TIMESTAMP}.csv"

echo "========================================"
echo "  K-means Benchmark with CSV output"
echo "========================================"
echo "Dataset: $DATASET"
echo "K=$K, Max iterations=$MAX_ITER, Runs=$RUNS"
echo "P-cores: $P_CORES"
echo "Output: $CSV_FILE"
echo ""

# Verificar se dataset existe
if [ ! -f "$DATASET" ]; then
    echo "Error: dataset not found at $DATASET"
    exit 1
fi

# Verificar tamanho do dataset
SAMPLES=$(./preprocessor 0 2>&1 | grep "Total samples" | awk '{print $3}')
echo "Dataset size: $SAMPLES samples"
echo ""

# Criar header do CSV
echo "version,run,k,max_iter,samples,time_ms" > "$CSV_FILE"

# Função para rodar benchmark de uma versão
run_version() {
    local version=$1
    echo "[$version] Running $RUNS iterations..."

    for run in $(seq 1 $RUNS); do
        # Executar benchmark
        time_ms=$(taskset -c "$P_CORES" $BENCHMARK "$version" $K $MAX_ITER "$DATASET")

        # Salvar no CSV
        echo "$version,$run,$K,$MAX_ITER,$SAMPLES,$time_ms" >> "$CSV_FILE"

        printf "  Run %2d/%2d: %.3f ms\n" $run $RUNS $time_ms
    done
    echo ""
}

# Executar benchmarks para as 3 versões
run_version "naive"
run_version "optimized_no_unroll"
run_version "optimized"

echo "========================================"
echo "Results saved to: $CSV_FILE"
echo ""

# Calcular estatísticas básicas
echo "=== Quick Statistics ==="
echo ""

# Naive stats
naive_times=$(grep "^naive," "$CSV_FILE" | cut -d, -f6)
naive_avg=$(echo "$naive_times" | awk '{sum+=$1; count++} END {printf "%.3f", sum/count}')
naive_min=$(echo "$naive_times" | sort -n | head -1)
naive_max=$(echo "$naive_times" | sort -n | tail -1)

echo "Naive (AoS):"
echo "  Min: $naive_min ms"
echo "  Max: $naive_max ms"
echo "  Avg: $naive_avg ms"
echo ""

# Optimized no-unroll stats
opt_no_unroll_times=$(grep "^optimized_no_unroll," "$CSV_FILE" | cut -d, -f6)
opt_no_unroll_avg=$(echo "$opt_no_unroll_times" | awk '{sum+=$1; count++} END {printf "%.3f", sum/count}')
opt_no_unroll_min=$(echo "$opt_no_unroll_times" | sort -n | head -1)
opt_no_unroll_max=$(echo "$opt_no_unroll_times" | sort -n | tail -1)

echo "Optimized (SoA, No-Unroll):"
echo "  Min: $opt_no_unroll_min ms"
echo "  Max: $opt_no_unroll_max ms"
echo "  Avg: $opt_no_unroll_avg ms"
echo ""

# Optimized with-unroll stats
opt_times=$(grep "^optimized," "$CSV_FILE" | cut -d, -f6)
opt_avg=$(echo "$opt_times" | awk '{sum+=$1; count++} END {printf "%.3f", sum/count}')
opt_min=$(echo "$opt_times" | sort -n | head -1)
opt_max=$(echo "$opt_times" | sort -n | tail -1)

echo "Optimized (SoA, With-Unroll):"
echo "  Min: $opt_min ms"
echo "  Max: $opt_max ms"
echo "  Avg: $opt_avg ms"
echo ""

# Speedups
echo "=== Speedups ==="
speedup_naive_to_with_unroll=$(echo "scale=3; $naive_avg / $opt_avg" | bc)
speedup_no_unroll_to_with_unroll=$(echo "scale=3; $opt_no_unroll_avg / $opt_avg" | bc)

echo "Naive → With-Unroll:     ${speedup_naive_to_with_unroll}x"
echo "No-Unroll → With-Unroll: ${speedup_no_unroll_to_with_unroll}x (unroll effect)"
echo ""
