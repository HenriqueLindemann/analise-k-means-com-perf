# K-means: Naive vs Cache-Optimized

Implementação de K-means em C comparando duas abordagens de organização de memória para medir impacto no desempenho.

## Implementações

### Naive (Array of Structs - AoS)

Implementação direta onde cada ponto é representado como uma estrutura contígua:

```c
typedef struct {
    float features[NUM_FEATURES];  // 7 features
    int cluster_id;
} DataPoint;

DataPoint points[N];  // [p0: f0,f1,...,f6][p1: f0,f1,...,f6]...
```

**Características:**
- Dados de um ponto ficam próximos na memória
- Boa localidade espacial ao acessar todas features de um ponto
- Má localidade ao processar uma feature específica de múltiplos pontos

### Optimized (Struct of Arrays - SoA)

Organização onde cada feature é armazenada em um array separado:

```c
typedef struct {
    float *feature_arrays[NUM_FEATURES];  // 7 arrays separados
    int *cluster_ids;
    size_t size;
} DataSetSoA;

// Layout: [all_f0][all_f1]...[all_f6][cluster_ids]
```

**Características:**
- Features separadas em arrays contíguos
- Excelente localidade espacial e temporal ao processar uma feature
- Cache lines são utilizadas de forma mais eficiente
- Permite vetorização automática pelo compilador

**Otimizações implementadas:**

1. **Single-pass centroid updates**: Acumula todas features em uma única passada sobre cluster_ids (reduz de 7 passadas para 1)

2. **Branchless distance calculation**: Calcula distâncias sem branches para reduzir mispredictions

3. **Manual loop unrolling**: Loop desenrolado manualmente para K=5

4. **Restrict pointers**: Permite ao compilador assumir não-aliasing

5. **Prefetching**: __builtin_prefetch para carregar dados antecipadamente

6. **Aggressive compilation**: -O3 -march=native -ffast-math -flto -funroll-loops

## Quick Start

```bash
# Pipeline completo automático (recomendado)
./run_full_analysis.sh 5 100 15

# Resultados em:
# scripts/results/run_TIMESTAMP/
# scripts/results/latest/  (symlink para última execução)
```

**Ver resultados:**
```bash
cat scripts/results/latest/analysis.txt        # Análise completa
cat scripts/results/latest/validation.txt      # Validação de corretude
xdg-open scripts/results/latest/graphs/        # Visualizações
```

## Pipeline Automatizado

O script `run_full_analysis.sh` executa o workflow completo em 5 etapas:

### Etapa 1: Compilação
Verifica e compila os binários necessários:
- `bin/kmeans_benchmark` - Executa ambas as versões
- `bin/validate_results` - Valida equivalência
- `bin/preprocessor` - Converte dataset para binário
- `bin/cluster_save` - Salva clusters para visualização

### Etapa 2: Processamento de Dataset
Converte o CSV original (~2M amostras) para formato binário eficiente:
- Input: `household_power_consumption.txt`
- Output: `data/dataset.bin`

### Etapa 3: Validação de Corretude
Executa naive e optimized com mesma seed e compara:
- Centroids finais (threshold < 0.001)
- Distribuição de clusters (pontos por cluster)
- Inércia total (qualidade do clustering)

**Pipeline para se a validação falhar.**

### Etapa 4: Benchmarks com perf
Executa ambas as versões com `perf stat` para coletar métricas hardware:
- Cycles, instructions, IPC
- Cache references/misses
- L1 dcache loads/misses
- LLC loads/misses
- Branches/branch-misses

Usa taskset para fixar em P-cores (0-7) e realiza múltiplas execuções para estabilidade.

### Etapa 5: Análise e Visualizações
Gera automaticamente:
- Análise em texto (analysis.txt)
- Relatório markdown (analysis.md)
- 5 gráficos de performance
- 3 gráficos de clustering
- Organiza tudo em estrutura de pastas

## Estrutura de Resultados

Cada execução cria uma pasta com timestamp:

```
scripts/results/
├── run_20251115_120000/
│   ├── validation.txt              # Resultado da validação
│   ├── perf_raw.txt                # Raw output do perf stat
│   ├── analysis.txt                # Análise em texto
│   ├── analysis.md                 # Relatório markdown
│   ├── clusters_naive.csv          # Clusters (naive)
│   ├── clusters_optimized.csv      # Clusters (optimized)
│   └── graphs/
│       ├── performance/
│       │   ├── execution_time.png
│       │   ├── cache_misses.png
│       │   ├── ipc.png
│       │   ├── metrics_comparison.png
│       │   └── improvements.png
│       └── clusters/
│           ├── clusters_comparison.png
│           ├── cluster_distribution.png
│           └── cluster_centroids_heatmap.png
└── latest -> run_20251115_120000   # Symlink para última execução
```

## Estrutura do Projeto

```
.
├── bin/                        # Binários compilados
├── src/                        # Implementações C
│   ├── kmeans_naive.c         # Versão AoS
│   ├── kmeans_optimized.c     # Versão SoA
│   ├── data_loader.c          # Carregamento de datasets
│   └── ...
├── include/                    # Headers
├── scripts/                    # Automação e análise
│   ├── run_full_analysis.sh   # Pipeline completo
│   ├── analyze_perf.py        # Análise de métricas
│   └── ...
├── data/                       # Datasets binários
└── Makefile
```

## Executar Passos Manualmente

Se preferir executar cada etapa separadamente:

```bash
# Compilação
make release              # Versão otimizada
make debug                # Versão com prints de debug
make clean                # Limpar binários

# Processamento de dados
bin/preprocessor 0        # Dataset completo (~2M amostras)
bin/preprocessor 100000   # Subset (100k amostras)

# Validação manual
./scripts/validate.sh 5 100 data/dataset.bin

# Benchmark manual
./scripts/perf_benchmark.sh 5 100 15

# Visualização de clusters
bin/cluster_save naive 5 data/dataset.bin clusters
bin/cluster_save optimized 5 data/dataset.bin clusters
python3 scripts/plot_clusters.py clusters_*.csv
```

## Requisitos

### Dataset

Individual Household Electric Power Consumption (~2M amostras, 7 features)

Download: https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption

Coloque o arquivo `household_power_consumption.txt` na raiz do projeto.

Ver `info_data_set.md` para detalhes sobre o dataset.

### perf (Linux Performance Counters)

Necessário para benchmarks de hardware:

```bash
# Instalar
sudo apt-get install linux-tools-$(uname -r) linux-tools-generic

# Verificar instalação
perf --version

# Configurar permissões (opcional, para rodar sem sudo)
echo -1 | sudo tee /proc/sys/kernel/perf_event_paranoid
```

### Python (para análise e visualizações)

```bash
pip install matplotlib numpy scikit-learn
```

## Metodologia de Validação

Para garantir que as otimizações preservam a corretude do algoritmo, o pipeline executa validação automática comparando:

1. **Centroids finais**: Distância euclidiana < 0.001
2. **Distribuição de clusters**: Contagem de pontos por cluster
3. **Inércia total**: Soma das distâncias quadradas (métrica de qualidade)

Ambas as versões executam com mesma seed para garantir inicialização idêntica.
