#include "kmeans.h"
#include "utils.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <float.h>

#ifdef DEBUG
#define DEBUG_PRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DEBUG_PRINT(...) do {} while(0)
#endif

// Versão OTIMIZADA: Struct of Arrays (SoA), cache-friendly, loop blocking

// Calcula distância euclidiana ao quadrado - versão SoA otimizada
static inline float euclidean_distance_soa(const DataSetSoA * restrict dataset, size_t point_idx,
                                           const float * restrict centroid) {
    // Acesso sequencial à memória para melhor uso de cache
    // Usar restrict ajuda o compilador a otimizar
    const float diff0 = dataset->global_active_power[point_idx] - centroid[0];
    const float diff1 = dataset->global_reactive_power[point_idx] - centroid[1];
    const float diff2 = dataset->voltage[point_idx] - centroid[2];
    const float diff3 = dataset->global_intensity[point_idx] - centroid[3];
    const float diff4 = dataset->sub_metering_1[point_idx] - centroid[4];
    const float diff5 = dataset->sub_metering_2[point_idx] - centroid[5];
    const float diff6 = dataset->sub_metering_3[point_idx] - centroid[6];

    // FMA (fused multiply-add) pode ser usado pelo compilador aqui
    return diff0 * diff0 + diff1 * diff1 + diff2 * diff2 + diff3 * diff3 +
           diff4 * diff4 + diff5 * diff5 + diff6 * diff6;
}

// Inicializa centroids aleatoriamente
void initialize_centroids_soa(float centroids[][NUM_FEATURES],
                              const DataSetSoA *dataset, int k) {
    int *selected = malloc(k * sizeof(int));

    for (int i = 0; i < k; i++) {
        int idx;
        int is_unique;

        do {
            idx = random_int(dataset->num_points);
            is_unique = 1;

            for (int j = 0; j < i; j++) {
                if (selected[j] == idx) {
                    is_unique = 0;
                    break;
                }
            }
        } while (!is_unique);

        selected[i] = idx;

        // Copiar features - acesso direto aos arrays
        centroids[i][0] = dataset->global_active_power[idx];
        centroids[i][1] = dataset->global_reactive_power[idx];
        centroids[i][2] = dataset->voltage[idx];
        centroids[i][3] = dataset->global_intensity[idx];
        centroids[i][4] = dataset->sub_metering_1[idx];
        centroids[i][5] = dataset->sub_metering_2[idx];
        centroids[i][6] = dataset->sub_metering_3[idx];
    }

    free(selected);
}

// Encontra cluster mais próximo - otimizado
static inline int find_nearest_cluster_soa(const DataSetSoA *dataset, size_t point_idx,
                                            const float centroids[][NUM_FEATURES], int k) {
    int nearest = 0;
    float min_dist = euclidean_distance_soa(dataset, point_idx, centroids[0]);

    // Loop unrolling manual para k pequeno pode ajudar
    for (int i = 1; i < k; i++) {
        float dist = euclidean_distance_soa(dataset, point_idx, centroids[i]);
        if (dist < min_dist) {
            min_dist = dist;
            nearest = i;
        }
    }

    return nearest;
}

// Atualiza centroids - versão otimizada (1 ÚNICA passada!)
static void update_centroids_soa(float centroids[][NUM_FEATURES],
                                  const DataSetSoA * restrict dataset, int k) {
    // Alocar tudo de uma vez em bloco contíguo para melhor cache
    // Layout: [sums_feature0][sums_feature1]...[sums_feature6][counts]
    const size_t total_size = NUM_FEATURES * k * sizeof(float) + k * sizeof(int);
    void *buffer = calloc(1, total_size);

    float *sums_base = (float *)buffer;
    int *counts = (int *)(sums_base + NUM_FEATURES * k);

    // Ponteiros para cada feature
    float * restrict sums0 = sums_base + 0 * k;
    float * restrict sums1 = sums_base + 1 * k;
    float * restrict sums2 = sums_base + 2 * k;
    float * restrict sums3 = sums_base + 3 * k;
    float * restrict sums4 = sums_base + 4 * k;
    float * restrict sums5 = sums_base + 5 * k;
    float * restrict sums6 = sums_base + 6 * k;

    const size_t n = dataset->num_points;
    const int * restrict cluster_ids = dataset->cluster_ids;

    // UMA ÚNICA passada - acumula todas features ao mesmo tempo
    // Usar restrict ajuda o compilador a otimizar
    for (size_t i = 0; i < n; i++) {
        const int cluster = cluster_ids[i];

        // Acumular todas as features para este cluster
        sums0[cluster] += dataset->global_active_power[i];
        sums1[cluster] += dataset->global_reactive_power[i];
        sums2[cluster] += dataset->voltage[i];
        sums3[cluster] += dataset->global_intensity[i];
        sums4[cluster] += dataset->sub_metering_1[i];
        sums5[cluster] += dataset->sub_metering_2[i];
        sums6[cluster] += dataset->sub_metering_3[i];
        counts[cluster]++;
    }

    // Calcular médias
    for (int i = 0; i < k; i++) {
        if (counts[i] > 0) {
            const float inv_count = 1.0f / counts[i];
            centroids[i][0] = sums0[i] * inv_count;
            centroids[i][1] = sums1[i] * inv_count;
            centroids[i][2] = sums2[i] * inv_count;
            centroids[i][3] = sums3[i] * inv_count;
            centroids[i][4] = sums4[i] * inv_count;
            centroids[i][5] = sums5[i] * inv_count;
            centroids[i][6] = sums6[i] * inv_count;
        }
    }

    // Limpar memória (uma única free!)
    free(buffer);
}

// K-means OTIMIZADO
void kmeans_optimized(DataSetSoA * restrict dataset,
                      float centroids[][NUM_FEATURES],
                      int k, int max_iterations) {

    // Inicializar centroids
    initialize_centroids_soa(centroids, dataset, k);

    const size_t n = dataset->num_points;
    int * restrict cluster_ids = dataset->cluster_ids;

    // Iterar até convergência ou max_iterations
    for (int iter = 0; iter < max_iterations; iter++) {
        int changes = 0;

        // Processar todos os pontos sequencialmente
        // Loop simples para melhor vetorização do compilador
        for (size_t i = 0; i < n; i++) {
            const int new_cluster = find_nearest_cluster_soa(dataset, i, centroids, k);

            if (cluster_ids[i] != new_cluster) {
                changes++;
                cluster_ids[i] = new_cluster;
            }
        }

        DEBUG_PRINT("Iteration %d: %d points changed cluster\n", iter, changes);

        // Convergência
        if (changes == 0) {
            DEBUG_PRINT("Converged after %d iterations\n", iter + 1);
            break;
        }

        // Atualizar centroids
        update_centroids_soa(centroids, dataset, k);
    }
}
