#!/bin/bash

# Script de validação para verificar equivalência entre versões naive e optimized

set -e

K=${1:-5}
ITER=${2:-100}
DATASET=${3:-data/dataset.bin}

echo "========================================"
echo "  K-means Validation Script"
echo "========================================"
echo "K=$K, Iterations=$ITER"
echo "Dataset: $DATASET"
echo ""

# Verificar se binário existe
if [ ! -f "bin/validate_results" ]; then
    echo "Building validation binary..."
    make release
fi

# Verificar se dataset existe
if [ ! -f "$DATASET" ]; then
    echo "Error: Dataset not found at $DATASET"
    echo "Run: bin/preprocessor 0"
    exit 1
fi

# Rodar validação
bin/validate_results $K $ITER $DATASET

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "All validations passed successfully!"
    echo "The optimized version produces the same"
    echo "results as the naive implementation."
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "VALIDATION FAILED!"
    echo "Check the output above for details."
    echo "=========================================="
fi

exit $exit_code
