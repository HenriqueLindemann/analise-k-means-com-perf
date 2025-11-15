#!/bin/bash

# Script completo de benchmark e análise
# Roda tudo automaticamente e gera relatórios

set -e

K=${1:-5}
ITER=${2:-100}
RUNS=${3:-15}

echo "========================================"
echo "  K-means Complete Analysis Pipeline"
echo "========================================"
echo "K=$K, Iterations=$ITER, Runs=$RUNS"
echo ""

# 1. Verificar compilação
if [ ! -f "bin/kmeans_benchmark" ]; then
    echo "[1/4] Compiling..."
    make clean && make release
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

# 3. Rodar benchmark com perf
echo "[3/4] Running benchmark with perf..."
./scripts/perf_benchmark.sh $K $ITER $RUNS

# 4. Gerar análise markdown
LATEST_PERF=$(ls -t scripts/results/perf_*.txt | head -1)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ANALYSIS_MD="scripts/results/ANALYSIS_${TIMESTAMP}.md"

echo "[4/4] Generating markdown analysis..."
python3 scripts/analyze_perf.py "$LATEST_PERF" "$ANALYSIS_MD"

echo ""
echo "========================================"
echo "  Analysis Complete!"
echo "========================================"
echo ""
echo "Generated files:"
echo "  - Perf results: $LATEST_PERF"
echo "  - Analysis (MD): $ANALYSIS_MD"
echo ""
echo "View analysis:"
echo "  cat $ANALYSIS_MD"
echo ""
