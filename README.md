# K-means: Naive vs Optimized (SoA) vs Optimized + Loop Unrolling

Implementação de K-means em C comparando **três versões** para isolar e medir o impacto de diferentes otimizações no desempenho.

## Implementações

### 1. Naive (Array of Structs - AoS)

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

### 2. Optimized No-Unroll (Struct of Arrays - SoA)

Organização onde cada feature é armazenada em um array separado, **sem loop unrolling manual**:

```c
typedef struct {
    float *global_active_power;
    float *global_reactive_power;
    float *voltage;
    // ... 7 arrays separados (um por feature)
    int *cluster_ids;
    size_t num_points;
} DataSetSoA;

// Layout: [all_f0][all_f1]...[all_f6][cluster_ids]
```

**Características:**
- Features separadas em arrays contíguos
- Excelente localidade espacial e temporal ao processar uma feature
- Cache lines são utilizadas de forma mais eficiente
- Permite vetorização automática pelo compilador

**Otimizações implementadas:**

1. **Single-pass centroid updates**: Acumula todas features em uma única passada
2. **Branchless distance calculation**: Calcula distâncias sem branches
3. **Restrict pointers**: Permite ao compilador assumir não-aliasing
4. **Aggressive compilation**: -O3 -march=native -ffast-math -flto -funroll-loops

### 3. Optimized With-Unroll (SoA + Manual Loop Unrolling)

Versão SoA com **loop unrolling manual especializado** para K=2 até K=10:

**Otimizações implementadas:**

1. **Single-pass centroid updates**: Acumula todas features em uma única passada
2. **Branchless distance calculation**: Calcula distâncias sem branches
3. **Manual loop unrolling**: Loop desenrolado manualmente para K=2 até K=10
4. **Restrict pointers**: Permite ao compilador assumir não-aliasing
5. **Aggressive compilation**: -O3 -march=native -ffast-math -flto -funroll-loops

**Exemplo de unrolling para K=5:**
```c
// Em vez de loop genérico:
for (int c = 0; c < k; c++) { /* calcular distância */ }

// Código desenrolado fixo para K=5:
dist0 = euclidean_distance_soa_fast(..., centroids[0]);
dist1 = euclidean_distance_soa_fast(..., centroids[1]);
dist2 = euclidean_distance_soa_fast(..., centroids[2]);
dist3 = euclidean_distance_soa_fast(..., centroids[3]);
dist4 = euclidean_distance_soa_fast(..., centroids[4]);
nearest = find_min_of_5(dist0, dist1, dist2, dist3, dist4);
```

Isso permite ao compilador eliminar branches, melhorar pipeline de instruções e aumentar IPC.

## Quick Start

### Análise para um único K

```bash
# Pipeline completo para K=5 (100 iterações, 15 execuções)
./run_full_analysis.sh "5" 100 15

# Resultados em:
# scripts/results/run_TIMESTAMP/k5/
# scripts/results/latest/  (symlink para última execução)
```

### Análise comparativa com múltiplos K

```bash
# Comparar K=2,3,4,5,6,7 (100 iterações, 10 execuções por K)
./run_full_analysis.sh "2 3 4 5 6 7" 100 10

# Análise completa K=2 a K=10
./run_full_analysis.sh "2 3 4 5 6 7 8 9 10" 100 15

# Formato: <K_values> <iterations> <runs_per_K>
```

**Ver resultados:**
```bash
# Para um único K
cat scripts/results/latest/k5/analysis.txt
cat scripts/results/latest/k5/validation.txt
xdg-open scripts/results/latest/k5/graphs/

# Para múltiplos K (análise comparativa)
cat scripts/results/latest/k_comparison/k_analysis.txt
xdg-open scripts/results/latest/k_comparison/graphs/
```

## Pipeline Automatizado

O script `run_full_analysis.sh` executa o workflow completo em 5 etapas:

### Etapa 1: Compilação
Verifica e compila os binários necessários:
- `bin/kmeans_benchmark` - Executa as **3 versões** (naive, optimized_no_unroll, optimized)
- `bin/validate_results` - Valida equivalência entre as **3 versões**
- `bin/preprocessor` - Converte dataset para binário
- `bin/cluster_save` - Salva clusters para visualização

### Etapa 2: Processamento de Dataset
Converte o CSV original (~2M amostras) para formato binário eficiente:
- Input: `household_power_consumption.txt`
- Output: `data/dataset.bin`

### Etapa 3: Validação de Corretude (3-way)
Executa **as 3 versões** com mesma seed e compara todas entre si:
- **Naive vs No-Unroll**: Verifica se SoA produz mesmos resultados
- **Naive vs With-Unroll**: Verifica se unrolling preserva corretude
- **No-Unroll vs With-Unroll**: Isola impacto do unrolling

**Comparações:**
- Centroids finais (threshold < 0.001)
- Distribuição de clusters (pontos por cluster)
- Inércia total (qualidade do clustering)

**Pipeline para se qualquer validação falhar.**

### Etapa 4: Benchmarks com perf
Executa **as 3 versões** com `perf stat` para coletar métricas hardware:
- Cycles, instructions, IPC
- Cache references/misses
- L1 dcache loads/misses
- LLC loads/misses
- Branches/branch-misses

Usa taskset para fixar em P-cores (0-7) e realiza múltiplas execuções para estabilidade.

### Etapa 5: Análise e Visualizações
Gera automaticamente:
- Análise em texto (analysis.txt) com **3 colunas**
- Relatório markdown (analysis.md)
- **6 gráficos de performance** (3 barras cada: Naive, No-Unroll, With-Unroll)
- Gráfico de "Unroll Effect" (isolando ganho do unrolling)
- 3 gráficos de clustering
- Organiza tudo em estrutura de pastas

Se múltiplos K forem especificados, gera também análise comparativa com **13+ gráficos** mostrando métricas em função de K (3 linhas cada: Naive, No-Unroll, With-Unroll).

## Estrutura de Resultados

### Para um único K

```
scripts/results/
├── run_TIMESTAMP/
│   └── k5/                         # Resultados para K=5
│       ├── validation.txt          # Validação de corretude (3-way)
│       ├── perf_raw.txt            # Raw output do perf stat (3 versões)
│       ├── analysis.txt            # Análise em texto (3 colunas)
│       ├── analysis.md             # Relatório markdown
│       ├── clusters_naive.csv
│       ├── clusters_optimized.csv
│       └── graphs/
│           ├── performance/        # 6 gráficos de performance (3 barras cada)
│           │   ├── execution_time.png       # Naive, No-Unroll, With-Unroll
│           │   ├── cache_misses.png         # Comparação cache
│           │   ├── ipc.png                  # Comparação IPC
│           │   ├── metrics_comparison.png   # Multi-métrica (log scale)
│           │   ├── improvements.png         # Melhorias relativas
│           │   └── unroll_effect.png        # Ganho específico do unrolling
│           └── clusters/           # 3 gráficos de clustering
│               ├── clusters_comparison.png
│               ├── cluster_distribution.png
│               └── cluster_centroids_heatmap.png
└── latest -> run_TIMESTAMP
```

### Para múltiplos K (análise comparativa)

```
scripts/results/
├── run_TIMESTAMP/
│   ├── k2/                         # Resultados individuais K=2
│   │   └── (mesma estrutura acima)
│   ├── k4/                         # Resultados individuais K=4
│   ├── k5/                         # Resultados individuais K=5
│   ├── k6/                         # Resultados individuais K=6
│   ├── k7/                         # Resultados individuais K=7
│   └── k_comparison/               # Análise comparativa entre K
│       ├── k_analysis.txt          # Comparação detalhada (3 versões)
│       └── graphs/                 # 13+ gráficos comparativos (3 linhas cada)
│           ├── time_vs_k.png       # Tempo vs K (3 linhas + barras de erro)
│           ├── cycles_vs_k.png     # Ciclos vs K
│           ├── instructions_vs_k.png        # Instruções vs K
│           ├── cache_misses_vs_k.png
│           ├── cache_hit_rate_vs_k.png
│           ├── cache_miss_rate_vs_k.png     # L2/L3
│           ├── l1_cache_miss_rate_vs_k.png
│           ├── llc_miss_rate_vs_k.png       # L3
│           ├── all_cache_levels_vs_k.png    # 3 subplots cache
│           ├── ipc_vs_k.png
│           ├── branches_vs_k.png
            ├── speedup_vs_k.png    # 3 linhas: Naive, N→NU e N→WU (relativo ao Naive)
│           ├── instructions_count_vs_k.png
│           └── all_metrics_vs_k.png # Todas métricas (6 subplots, 3 linhas cada)
└── latest -> run_TIMESTAMP
```

## Estrutura do Projeto

```
.
├── bin/                             # Binários compilados
├── src/                             # Implementações C
│   ├── kmeans_naive.c              # Versão 1: AoS
│   ├── kmeans_optimized_no_unroll.c # Versão 2: SoA sem unrolling manual
│   ├── kmeans_optimized.c          # Versão 3: SoA com unrolling (K=2-10)
│   ├── benchmark.c                 # Benchmark runner (3 modos)
│   ├── data_loader.c               # Carregamento de datasets (AoS e SoA)
│   ├── validate_results.c          # Validação 3-way
│   └── ...
├── include/                         # Headers
│   └── kmeans.h                    # Declarações das 3 versões
├── scripts/                         # Automação e análise
│   ├── run_full_analysis.sh        # Pipeline completo (3 versões)
│   ├── analyze_perf.py             # Parsing perf (3 versões)
│   ├── analyze_k_values.py         # Análise vs K (3 linhas)
│   ├── analyze_k_comparison.py     # Comparação K (13+ gráficos)
│   ├── perf_benchmark.sh           # Benchmark perf (3 versões)
│   ├── validate.sh                 # Validação wrapper
│   └── benchmark_csv.sh            # Benchmark CSV (3 versões)
├── data/                            # Datasets binários
└── Makefile                         # Compila as 3 versões
```

## Exemplos de Uso

### Teste rápido (5 execuções)

```bash
# Testar apenas K=5 com 5 execuções rápidas
./run_full_analysis.sh "5" 100 5
```

### Análise completa de K=2 a K=10

```bash
# Análise abrangente com 15 execuções por K
./run_full_analysis.sh "2 3 4 5 6 7 8 9 10" 100 15

# Ver comparação geral
cat scripts/results/latest/k_comparison/k_analysis.txt

# Ver gráfico de speedup vs K
xdg-open scripts/results/latest/k_comparison/graphs/speedup_vs_k.png
```

### Comparar apenas alguns K específicos

```bash
# Testar K=3, K=5 e K=7 (valores ímpares)
./run_full_analysis.sh "3 5 7" 100 10

# Testar K=2, K=4, K=6 (valores pares)
./run_full_analysis.sh "2 4 6" 100 10
```

### Análise detalhada para K específico

```bash
# Rodar apenas K=5 com muitas execuções para alta precisão
./run_full_analysis.sh "5" 100 20

# Ver análise detalhada
cat scripts/results/latest/k5/analysis.txt

# Ver validação
cat scripts/results/latest/k5/validation.txt

# Abrir todos os gráficos
xdg-open scripts/results/latest/k5/graphs/performance/
xdg-open scripts/results/latest/k5/graphs/clusters/
```

## Executar Passos Manualmente

Se preferir executar cada etapa separadamente:

```bash
# Compilação
make release              # Versão otimizada (3 versões)
make debug                # Versão com prints de debug
make clean                # Limpar binários

# Processamento de dados
bin/preprocessor 0        # Dataset completo (~2M amostras)
bin/preprocessor 100000   # Subset (100k amostras)

# Validação manual (3-way)
./scripts/validate.sh 5 100 data/dataset.bin

# Benchmark manual das 3 versões
bin/kmeans_benchmark naive 5 100 data/dataset.bin
bin/kmeans_benchmark optimized_no_unroll 5 100 data/dataset.bin
bin/kmeans_benchmark optimized 5 100 data/dataset.bin

# Benchmark com perf (3 versões)
./scripts/perf_benchmark.sh 5 100 15

# Benchmark CSV (3 versões)
./scripts/benchmark_csv.sh 5 100 20

# Visualização de clusters
bin/cluster_save naive 5 data/dataset.bin clusters
bin/cluster_save optimized_no_unroll 5 data/dataset.bin clusters
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

Para garantir que as otimizações preservam a corretude do algoritmo, o pipeline executa validação automática **3-way** comparando todas as implementações entre si:

### Comparações realizadas:

1. **Naive vs No-Unroll**: Verifica se a mudança de AoS para SoA preserva corretude
2. **Naive vs With-Unroll**: Verifica corretude da versão totalmente otimizada
3. **No-Unroll vs With-Unroll**: Isola e valida o impacto do loop unrolling

### Métricas comparadas:

1. **Centroids finais**: Distância euclidiana entre centroids correspondentes < 0.001
2. **Distribuição de clusters**: Contagem de pontos atribuídos a cada cluster
3. **Inércia total**: Soma das distâncias quadradas (métrica de qualidade do clustering)

**Todas as 3 versões** executam com mesma seed (42) para garantir inicialização idêntica dos centroids.

### Exemplo de saída da validação:

```
[9/9] Final validation result:
========================================
✓ VALIDATION PASSED
  All 3 implementations produce equivalent results!
  - Naive vs No-Unroll: ✓
  - Naive vs With-Unroll: ✓
  - No-Unroll vs With-Unroll: ✓
========================================
```

O pipeline **para** se qualquer uma das validações falhar.
