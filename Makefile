# Makefile for K-means benchmark project

CC = gcc
CFLAGS_BASE = -Iinclude -Wall -Wextra
CFLAGS_DEBUG = $(CFLAGS_BASE) -g -DDEBUG -O0
CFLAGS_RELEASE = $(CFLAGS_BASE) -O3 -march=native -DNDEBUG -ffast-math -funroll-loops -ftree-vectorize -fno-signed-zeros -fno-trapping-math -flto
LDFLAGS = -lm -flto

# Diretórios
SRC_DIR = src
INC_DIR = include
BUILD_DIR = build
DATA_DIR = data
BIN_DIR = bin

# Arquivos fonte
SRCS = $(SRC_DIR)/kmeans_naive.c \
       $(SRC_DIR)/kmeans_optimized.c \
       $(SRC_DIR)/data_loader.c \
       $(SRC_DIR)/utils.c

# Objetos (release)
OBJS_RELEASE = $(BUILD_DIR)/kmeans_naive.o \
               $(BUILD_DIR)/kmeans_optimized.o \
               $(BUILD_DIR)/data_loader.o \
               $(BUILD_DIR)/utils.o

# Objetos (debug)
OBJS_DEBUG = $(BUILD_DIR)/kmeans_naive_debug.o \
             $(BUILD_DIR)/kmeans_optimized_debug.o \
             $(BUILD_DIR)/data_loader_debug.o \
             $(BUILD_DIR)/utils_debug.o

# Binários
BENCHMARK_RELEASE = $(BIN_DIR)/kmeans_benchmark
BENCHMARK_DEBUG = $(BIN_DIR)/kmeans_benchmark_debug
PREPROCESSOR = $(BIN_DIR)/preprocessor
CLUSTER_SAVE = $(BIN_DIR)/cluster_save
VALIDATE = $(BIN_DIR)/validate_results

.PHONY: all clean release debug test prepare

# Build padrão: release
all: release

# Build release (para benchmarks)
release: CFLAGS = $(CFLAGS_RELEASE)
release: $(BUILD_DIR) $(BIN_DIR) $(DATA_DIR) $(BENCHMARK_RELEASE) $(PREPROCESSOR) $(CLUSTER_SAVE) $(VALIDATE)

# Build debug (com prints)
debug: CFLAGS = $(CFLAGS_DEBUG)
debug: $(BUILD_DIR) $(DATA_DIR) $(BENCHMARK_DEBUG) $(PREPROCESSOR)

# Criar diretórios
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(DATA_DIR):
	mkdir -p $(DATA_DIR)

# Compilar benchmark (release)
$(BENCHMARK_RELEASE): $(OBJS_RELEASE) $(BUILD_DIR)/benchmark.o
	$(CC) $(CFLAGS_RELEASE) -o $@ $^ $(LDFLAGS)
	@echo "Built release benchmark (no prints, optimized)"

# Compilar benchmark (debug)
$(BENCHMARK_DEBUG): $(OBJS_DEBUG) $(BUILD_DIR)/benchmark_debug.o
	$(CC) $(CFLAGS_DEBUG) -o $@ $^ $(LDFLAGS)
	@echo "Built debug benchmark (with prints)"

# Compilar preprocessor
$(PREPROCESSOR): $(BUILD_DIR)/preprocessor.o $(BUILD_DIR)/data_loader.o
	$(CC) $(CFLAGS_RELEASE) -o $@ $^ $(LDFLAGS)

# Compilar cluster_save
$(CLUSTER_SAVE): $(BUILD_DIR)/cluster_and_save.o $(OBJS_RELEASE)
	$(CC) $(CFLAGS_RELEASE) -o $@ $^ $(LDFLAGS)

# Compilar validate_results
$(VALIDATE): $(BUILD_DIR)/validate_results.o $(OBJS_RELEASE)
	$(CC) $(CFLAGS_RELEASE) -o $@ $^ $(LDFLAGS)

# Regras de compilação - RELEASE
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS_RELEASE) -c $< -o $@

# Regras de compilação - DEBUG
$(BUILD_DIR)/%_debug.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS_DEBUG) -c $< -o $@

# Preprocessor (sempre release)
$(BUILD_DIR)/preprocessor.o: $(SRC_DIR)/preprocessor.c
	$(CC) $(CFLAGS_RELEASE) -c $< -o $@

# Limpar
clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)
	rm -f results_*.txt perf_*.txt perf.data perf.data.old clusters_*.csv clusters_*.bin
	rm -rf scripts/results

# Preparar dataset (converter para binário)
# Uso: make prepare SAMPLES=100000
SAMPLES ?= 100000
prepare: $(PREPROCESSOR)
	./$(PREPROCESSOR) $(SAMPLES)

# Testes rápidos
test: release
	@echo "\n=== Testing with small dataset (1000 samples) ==="
	./$(PREPROCESSOR) 1000 household_power_consumption.txt data/test_dataset.bin
	@echo "\n--- Naive version ---"
	./$(BENCHMARK_RELEASE) naive 3 50 data/test_dataset.bin
	@echo "\n--- Optimized version ---"
	./$(BENCHMARK_RELEASE) optimized 3 50 data/test_dataset.bin

# Help
help:
	@echo "K-means Benchmark Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  make              - Build release version (default)"
	@echo "  make release      - Build optimized version for benchmarks"
	@echo "  make debug        - Build debug version with prints"
	@echo "  make prepare      - Convert dataset to binary (SAMPLES=N)"
	@echo "  make test         - Quick test with small dataset"
	@echo "  make clean        - Remove build files"
	@echo ""
	@echo "Examples:"
	@echo "  make prepare SAMPLES=50000   - Process 50k samples"
	@echo "  make test                     - Quick functionality test"
