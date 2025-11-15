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

// Versão OTIMIZADA: Struct of Arrays (SoA), cache-friendly, prefetching

// Calcula distância euclidiana ao quadrado - versão SoA otimizada e inline
static inline float euclidean_distance_soa_fast(
    const float * restrict f0, const float * restrict f1,
    const float * restrict f2, const float * restrict f3,
    const float * restrict f4, const float * restrict f5,
    const float * restrict f6, size_t idx,
    const float c0, const float c1, const float c2, const float c3,
    const float c4, const float c5, const float c6) {

    // Carregar valores e calcular diferenças
    const float diff0 = f0[idx] - c0;
    const float diff1 = f1[idx] - c1;
    const float diff2 = f2[idx] - c2;
    const float diff3 = f3[idx] - c3;
    const float diff4 = f4[idx] - c4;
    const float diff5 = f5[idx] - c5;
    const float diff6 = f6[idx] - c6;

    // FMA optimization
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

// Encontra cluster mais próximo - OTIMIZADO com unroll para k=5
static inline int find_nearest_cluster_k5(
    const float * restrict f0, const float * restrict f1,
    const float * restrict f2, const float * restrict f3,
    const float * restrict f4, const float * restrict f5,
    const float * restrict f6, size_t idx,
    const float centroids[][NUM_FEATURES]) {

    // Unroll manual para k=5
    float dist0 = euclidean_distance_soa_fast(f0, f1, f2, f3, f4, f5, f6, idx,
        centroids[0][0], centroids[0][1], centroids[0][2], centroids[0][3],
        centroids[0][4], centroids[0][5], centroids[0][6]);

    float dist1 = euclidean_distance_soa_fast(f0, f1, f2, f3, f4, f5, f6, idx,
        centroids[1][0], centroids[1][1], centroids[1][2], centroids[1][3],
        centroids[1][4], centroids[1][5], centroids[1][6]);

    float dist2 = euclidean_distance_soa_fast(f0, f1, f2, f3, f4, f5, f6, idx,
        centroids[2][0], centroids[2][1], centroids[2][2], centroids[2][3],
        centroids[2][4], centroids[2][5], centroids[2][6]);

    float dist3 = euclidean_distance_soa_fast(f0, f1, f2, f3, f4, f5, f6, idx,
        centroids[3][0], centroids[3][1], centroids[3][2], centroids[3][3],
        centroids[3][4], centroids[3][5], centroids[3][6]);

    float dist4 = euclidean_distance_soa_fast(f0, f1, f2, f3, f4, f5, f6, idx,
        centroids[4][0], centroids[4][1], centroids[4][2], centroids[4][3],
        centroids[4][4], centroids[4][5], centroids[4][6]);

    // Encontrar mínimo - versão branchless
    int nearest = 0;
    float min_dist = dist0;

    // Usar aritmética para evitar branches
    int update = dist1 < min_dist;
    nearest = update ? 1 : nearest;
    min_dist = update ? dist1 : min_dist;

    update = dist2 < min_dist;
    nearest = update ? 2 : nearest;
    min_dist = update ? dist2 : min_dist;

    update = dist3 < min_dist;
    nearest = update ? 3 : nearest;
    min_dist = update ? dist3 : min_dist;

    update = dist4 < min_dist;
    nearest = update ? 4 : nearest;

    return nearest;
}

// Encontra cluster mais próximo - versão genérica para qualquer K
static inline int find_nearest_cluster_generic(
    const float * restrict f0, const float * restrict f1,
    const float * restrict f2, const float * restrict f3,
    const float * restrict f4, const float * restrict f5,
    const float * restrict f6, size_t idx,
    const float centroids[][NUM_FEATURES], int k) {

    int nearest = 0;
    float min_dist = euclidean_distance_soa_fast(f0, f1, f2, f3, f4, f5, f6, idx,
        centroids[0][0], centroids[0][1], centroids[0][2], centroids[0][3],
        centroids[0][4], centroids[0][5], centroids[0][6]);

    for (int c = 1; c < k; c++) {
        float dist = euclidean_distance_soa_fast(f0, f1, f2, f3, f4, f5, f6, idx,
            centroids[c][0], centroids[c][1], centroids[c][2], centroids[c][3],
            centroids[c][4], centroids[c][5], centroids[c][6]);

        if (dist < min_dist) {
            min_dist = dist;
            nearest = c;
        }
    }

    return nearest;
}

// Atualiza centroids - versão otimizada (1 ÚNICA passada!)
static void update_centroids_soa(float centroids[][NUM_FEATURES],
                                  const DataSetSoA * restrict dataset, int k) {
    // Alocar tudo de uma vez alinhado para melhor cache
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

    // Ponteiros aos arrays de features (carregar uma vez)
    const float * restrict f0 = dataset->global_active_power;
    const float * restrict f1 = dataset->global_reactive_power;
    const float * restrict f2 = dataset->voltage;
    const float * restrict f3 = dataset->global_intensity;
    const float * restrict f4 = dataset->sub_metering_1;
    const float * restrict f5 = dataset->sub_metering_2;
    const float * restrict f6 = dataset->sub_metering_3;

    // UMA ÚNICA passada - acumula todas features ao mesmo tempo
    for (size_t i = 0; i < n; i++) {
        const int cluster = cluster_ids[i];

        // Acumular todas as features para este cluster
        sums0[cluster] += f0[i];
        sums1[cluster] += f1[i];
        sums2[cluster] += f2[i];
        sums3[cluster] += f3[i];
        sums4[cluster] += f4[i];
        sums5[cluster] += f5[i];
        sums6[cluster] += f6[i];
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

    free(buffer);
}

// K-means OTIMIZADO - versão especializada para k=5
void kmeans_optimized(DataSetSoA * restrict dataset,
                      float centroids[][NUM_FEATURES],
                      int k, int max_iterations) {

    // Inicializar centroids
    initialize_centroids_soa(centroids, dataset, k);

    const size_t n = dataset->num_points;
    int * restrict cluster_ids = dataset->cluster_ids;

    // Carregar ponteiros aos arrays uma vez
    const float * restrict f0 = dataset->global_active_power;
    const float * restrict f1 = dataset->global_reactive_power;
    const float * restrict f2 = dataset->voltage;
    const float * restrict f3 = dataset->global_intensity;
    const float * restrict f4 = dataset->sub_metering_1;
    const float * restrict f5 = dataset->sub_metering_2;
    const float * restrict f6 = dataset->sub_metering_3;

    // Iterar até convergência ou max_iterations
    for (int iter = 0; iter < max_iterations; iter++) {
        int changes = 0;

        // Usar versão especializada para k=5, genérica para outros
        if (k == 5) {
            // Loop principal otimizado para k=5 com unrolling
            for (size_t i = 0; i < n; i++) {
                const int old_cluster = cluster_ids[i];
                const int new_cluster = find_nearest_cluster_k5(f0, f1, f2, f3, f4, f5, f6, i, centroids);

                cluster_ids[i] = new_cluster;
                changes += (old_cluster != new_cluster);
            }
        } else {
            // Loop genérico para qualquer K
            for (size_t i = 0; i < n; i++) {
                const int old_cluster = cluster_ids[i];
                const int new_cluster = find_nearest_cluster_generic(f0, f1, f2, f3, f4, f5, f6, i, centroids, k);

                cluster_ids[i] = new_cluster;
                changes += (old_cluster != new_cluster);
            }
        }

        DEBUG_PRINT("Iteration %d: %d points changed cluster\n", iter, changes);

        // Convergência - parar se nada mudou
        if (changes == 0) {
            DEBUG_PRINT("Converged after %d iterations\n", iter + 1);
            break;
        }

        // Atualizar centroids
        update_centroids_soa(centroids, dataset, k);
    }
}
