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

## Acessando Resultados

### Última Execução
```bash
# Análise completa
cat scripts/results/latest/analysis.txt

# Validação
cat scripts/results/latest/validation.txt

# Relatório markdown
cat scripts/results/latest/analysis.md

# Visualizar gráficos
xdg-open scripts/results/latest/graphs/performance/
xdg-open scripts/results/latest/graphs/clusters/
```

### Execução Específica
```bash
# Listar todas execuções
ls -lt scripts/results/

# Acessar execução específica
cat scripts/results/run_20251115_113809/analysis.txt
```

## Comandos Individuais

### 1. Apenas Validação
```bash
./scripts/validate.sh 5 100 data/dataset.bin
```

### 2. Apenas Benchmark
```bash
./scripts/perf_benchmark.sh 5 100 15
```

### 3. Gerar Clusters e Visualizar
```bash
# Gerar CSVs
bin/cluster_save naive 5 data/dataset.bin output
bin/cluster_save optimized 5 data/dataset.bin output

# Visualizar
python3 scripts/plot_clusters.py output_naive.csv
```

## Interpretando Resultados

### validation.txt
```
✓ VALIDATION PASSED
Both implementations produce equivalent results!
```
- **Centroids**: Distância < 0.001 ✓
- **Distribuição**: Diferença < 0.001% ✓
- **Inércia**: Diferença < 0.001% ✓

### analysis.txt
```
Speedup:   1.70x ✓ FASTER

KEY INSIGHTS:
✓ Cache misses reduced by 38.7%
✗ L1 misses increased by 498.5%
✓ Overall speedup: 1.70x faster
```

### Métricas Importantes

**Melhores (✓):**
- ↓ Execution time (menor é melhor)
- ↓ Cycles (menos ciclos CPU)
- ↓ Instructions (menos instruções)
- ↓ Cache misses (menos faltas de cache)
- ↓ Branches (menos branches)
- ↑ IPC (mais instruções por ciclo)

**Trade-offs (aceitáveis):**
- ↑ L1 misses - Compensado pela redução em LLC misses

## Otimizações Implementadas

1. **Struct of Arrays (SoA)** - Layout cache-friendly
2. **Manual loop unrolling** - Para K=5 especificamente
3. **Branchless min-finding** - Redução de branch mispredictions
4. **Single-pass centroid update** - Uma iteração sobre dados
5. **Restrict pointers** - Ajuda compilador com aliasing
6. **Aggressive compiler flags** - `-O3 -march=native -flto -ffast-math`

## Troubleshooting

### Pipeline falha na validação
```
✗ VALIDATION FAILED!
Check scripts/results/run_TIMESTAMP/validation.txt
```
**Solução**: Verificar se há bugs recentes no código

### Perf não encontrado
```
Error: perf not found
```
**Solução**: `sudo apt-get install linux-tools-$(uname -r)`

### Dataset não encontrado
```
Error: Dataset not found
```
**Solução**:
1. Baixar `household_power_consumption.txt`
2. Rodar `bin/preprocessor 0`

### Gráficos não gerados
```
Warning: Failed to generate cluster visualizations
```
**Causa**: Falta matplotlib ou scikit-learn
**Solução**: `pip3 install --break-system-packages matplotlib pandas scikit-learn`

## Reprodutibilidade

Cada run contém:
- Parâmetros exatos (K, iterações, runs)
- Validação completa
- Raw data do perf
- Análises geradas
- Todas visualizações

Permite comparar:
- Diferentes otimizações
- Diferentes parâmetros (K, iterações)
- Performance em diferentes máquinas
