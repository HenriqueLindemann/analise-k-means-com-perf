# K-means: Naive vs Cache-Optimized

Implementação de K-means em C comparando duas abordagens:
- **Naive (AoS)**: Array of Structs - implementação direta
- **Optimized (SoA)**: Struct of Arrays - otimizada para cache

## Quick Start

```bash
# Análise completa automática (compila, processa, benchmarks, análise)
./run_full_analysis.sh 5 100 15

# OU passo a passo:

# 1. Compilar
make

# 2. Processar dataset completo (~2M amostras)
bin/preprocessor 0

# 3. Rodar benchmark com perf (gera análise automaticamente)
./scripts/perf_benchmark.sh 5 100 15

# 4. Visualizar clusters
bin/cluster_save optimized 5 data/dataset.bin clusters
python3 scripts/plot_clusters.py clusters_optimized.csv
```

## Estrutura do Projeto

```
.
├── bin/              # Binários compilados
│   ├── kmeans_benchmark
│   ├── cluster_save
│   └── preprocessor
├── src/              # Implementações C (7 arquivos)
├── include/          # Headers (3 arquivos)
├── scripts/          # Benchmarks e análise
│   ├── perf_benchmark.sh
│   ├── analyze_perf.py
│   ├── benchmark_csv.sh
│   └── plot_clusters.py
├── data/             # Datasets binários
└── Makefile
```

## Instalação do perf

```bash
# Instalar linux-tools para o kernel
sudo apt-get install linux-tools-$(uname -r) linux-tools-generic

# Verificar
perf --version

# Configurar permissões (opcional)
echo -1 | sudo tee /proc/sys/kernel/perf_event_paranoid
```

## Otimizações Implementadas (SoA)

1. **Struct of Arrays**: Features separadas em arrays contíguos
   ```c
   // Naive (AoS): [p0_f0,f1,...,f6][p1_f0,f1,...,f6]
   // Optimized (SoA): [all_f0][all_f1]...[all_f6]
   ```

2. **Update centroids em 1 passada**: Reduz acessos a cluster_ids de 7x para 1x

3. **Loop blocking**: Processamento em blocos de 1024 pontos

4. **Compilação**: `-O3 -march=native`

## Comandos Úteis

```bash
# Compilar
make release              # Release (otimizado)
make debug                # Debug (com prints)
make clean                # Limpar

# Preparar dados
bin/preprocessor 0        # Dataset completo
bin/preprocessor 100000   # 100k amostras
make test                 # Teste rápido

# Benchmarks
./scripts/perf_benchmark.sh <k> <iter> <runs>
./scripts/benchmark_csv.sh <k> <iter> <runs>

# Clusters e visualização
bin/cluster_save <naive|optimized> <k> data/dataset.bin clusters
python3 scripts/plot_clusters.py clusters_*.csv
```

## Dataset

**Individual Household Electric Power Consumption**

Ver `info_data_set.md` para detalhes.

**Download do Dataset:**
Baixe manualmente em:
https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption
Coloque o arquivo `household_power_consumption.txt` na pasta principal do projeto.

## Arquivos de Análise Gerados

Após rodar benchmarks, os seguintes arquivos são gerados automaticamente:

- `scripts/results/perf_TIMESTAMP.txt` - Log completo do perf
- `scripts/results/analysis_TIMESTAMP.txt` - Análise em texto
- `scripts/results/ANALYSIS_TIMESTAMP.md` - Relatório em markdown
- `scripts/results/*.png` - Gráficos de comparação (5 gráficos):
  - `execution_time.png` - Comparação de tempo de execução
  - `cache_misses.png` - Comparação de cache misses
  - `ipc.png` - Comparação de IPC
  - `metrics_comparison.png` - Comparação de múltiplas métricas
  - `improvements.png` - Melhorias percentuais
