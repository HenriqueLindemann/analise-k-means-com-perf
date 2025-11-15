# K-means Workflow Completo

## Pipeline Automatizado

### Comando Principal
```bash
./run_full_analysis.sh <k> <max_iter> <runs>

# Exemplo: K=5, 100 iterações, 15 execuções
./run_full_analysis.sh 5 100 15
```

### O que acontece (5 etapas):

1. **[1/5] Compilação** - Verifica e compila binários se necessário
   - `bin/kmeans_benchmark`
   - `bin/validate_results`
   - `bin/preprocessor`
   - `bin/cluster_save`

2. **[2/5] Processamento de Dataset** - Converte CSV para binário se necessário
   - Input: `household_power_consumption.txt` (~2M amostras)
   - Output: `data/dataset.bin` (formato eficiente)

3. **[3/5] Validação de Corretude** ✓
   - Executa naive e optimized com mesma seed
   - Compara centroids (threshold < 0.001)
   - Compara distribuição de clusters
   - Compara inércia (qualidade)
   - **Se falhar, pipeline para**

4. **[4/5] Benchmarks com perf**
   - Executa naive version (15 runs)
   - Executa optimized version (15 runs)
   - Coleta métricas hardware:
     - cycles, instructions, IPC
     - cache references/misses
     - L1 dcache loads/misses
     - LLC loads/misses
     - branches/branch-misses

5. **[5/5] Análise e Visualizações**
   - Gera análise em texto (.txt)
   - Gera relatório markdown (.md)
   - Cria 8 gráficos:
     - 5 de performance
     - 3 de clustering
   - Organiza em estrutura de pastas
   - Cria symlink `latest/`

## Estrutura de Resultados

Cada execução gera uma pasta timestamped:

```
scripts/results/
├── run_20251115_113809/          # Pasta com timestamp
│   ├── validation.txt             # ✓ Resultado da validação
│   ├── perf_raw.txt              # Raw output do perf stat
│   ├── analysis.txt              # Análise em texto
│   ├── analysis.md               # Relatório markdown
│   ├── clusters_naive.csv        # Clusters (naive)
│   ├── clusters_optimized.csv    # Clusters (optimized)
│   └── graphs/
│       ├── performance/          # 5 gráficos de performance
│       │   ├── execution_time.png
│       │   ├── cache_misses.png
│       │   ├── ipc.png
│       │   ├── metrics_comparison.png
│       │   └── improvements.png
│       └── clusters/              # 3 gráficos de clustering
│           ├── clusters_comparison.png
│           ├── cluster_distribution.png
│           └── cluster_centroids_heatmap.png
└── latest -> run_20251115_113809  # Symlink para última execução
```
