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
float euclidean_distance_soa(const DataSetSoA *dataset, size_t point_idx,
                              const float centroid[NUM_FEATURES]) {
    // Acesso sequencial à memória para melhor uso de cache
    float diff0 = dataset->global_active_power[point_idx] - centroid[0];
    float diff1 = dataset->global_reactive_power[point_idx] - centroid[1];
    float diff2 = dataset->voltage[point_idx] - centroid[2];
    float diff3 = dataset->global_intensity[point_idx] - centroid[3];
    float diff4 = dataset->sub_metering_1[point_idx] - centroid[4];
    float diff5 = dataset->sub_metering_2[point_idx] - centroid[5];
    float diff6 = dataset->sub_metering_3[point_idx] - centroid[6];

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
                                  const DataSetSoA *dataset, int k) {
    // Arrays temporários para acumulação - layout SoA para melhor cache
    float *sums[NUM_FEATURES];
    int *counts = calloc(k, sizeof(int));

    for (int f = 0; f < NUM_FEATURES; f++) {
        sums[f] = calloc(k, sizeof(float));
    }

    size_t n = dataset->num_points;

    // UMA ÚNICA passada - acumula todas features ao mesmo tempo
    // Mantém cluster_ids na cache L1
    for (size_t i = 0; i < n; i++) {
        int cluster = dataset->cluster_ids[i];

        // Acumular todas as features para este cluster
        sums[0][cluster] += dataset->global_active_power[i];
        sums[1][cluster] += dataset->global_reactive_power[i];
        sums[2][cluster] += dataset->voltage[i];
        sums[3][cluster] += dataset->global_intensity[i];
        sums[4][cluster] += dataset->sub_metering_1[i];
        sums[5][cluster] += dataset->sub_metering_2[i];
        sums[6][cluster] += dataset->sub_metering_3[i];
        counts[cluster]++;
    }

    // Calcular médias
    for (int i = 0; i < k; i++) {
        if (counts[i] > 0) {
            float inv_count = 1.0f / counts[i];
            for (int f = 0; f < NUM_FEATURES; f++) {
                centroids[i][f] = sums[f][i] * inv_count;
            }
        }
    }

    // Limpar memória temporária
    for (int f = 0; f < NUM_FEATURES; f++) {
        free(sums[f]);
    }
    free(counts);
}

// K-means OTIMIZADO
void kmeans_optimized(DataSetSoA *dataset,
                      float centroids[][NUM_FEATURES],
                      int k, int max_iterations) {

    // Inicializar centroids
    initialize_centroids_soa(centroids, dataset, k);

    // Blocking size para melhor cache locality
    const size_t BLOCK_SIZE = 1024;

    // Iterar até convergência ou max_iterations
    for (int iter = 0; iter < max_iterations; iter++) {
        int changes = 0;

        // Processar pontos em blocos (cache blocking)
        for (size_t block_start = 0; block_start < dataset->num_points; block_start += BLOCK_SIZE) {
            size_t block_end = block_start + BLOCK_SIZE;
            if (block_end > dataset->num_points) {
                block_end = dataset->num_points;
            }

            // Atribuir pontos neste bloco aos clusters mais próximos
            for (size_t i = block_start; i < block_end; i++) {
                int new_cluster = find_nearest_cluster_soa(dataset, i, centroids, k);

                if (dataset->cluster_ids[i] != new_cluster) {
                    changes++;
                    dataset->cluster_ids[i] = new_cluster;
                }
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
