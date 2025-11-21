#include "kmeans.h"
#include "utils.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <float.h>
#include <immintrin.h>  // AVX intrinsics

#ifdef DEBUG
#define DEBUG_PRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DEBUG_PRINT(...) do {} while(0)
#endif

// Versão OTIMIZADA SEM UNROLL: Struct of Arrays (SoA) + SIMD/AVX

// Calcula distância euclidiana ao quadrado - versão escalar otimizada
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

// SIMD: Processa 8 pontos simultaneamente para um centroid
static inline void compute_distances_8_points(
    const float * restrict f0, const float * restrict f1,
    const float * restrict f2, const float * restrict f3,
    const float * restrict f4, const float * restrict f5,
    const float * restrict f6, size_t start_idx,
    const float c0, const float c1, const float c2, const float c3,
    const float c4, const float c5, const float c6,
    float * restrict distances) {

    // Carregar centroid values como vetores broadcast
    __m256 vc0 = _mm256_set1_ps(c0);
    __m256 vc1 = _mm256_set1_ps(c1);
    __m256 vc2 = _mm256_set1_ps(c2);
    __m256 vc3 = _mm256_set1_ps(c3);
    __m256 vc4 = _mm256_set1_ps(c4);
    __m256 vc5 = _mm256_set1_ps(c5);
    __m256 vc6 = _mm256_set1_ps(c6);

    // Carregar 8 pontos de cada feature
    __m256 vf0 = _mm256_loadu_ps(&f0[start_idx]);
    __m256 vf1 = _mm256_loadu_ps(&f1[start_idx]);
    __m256 vf2 = _mm256_loadu_ps(&f2[start_idx]);
    __m256 vf3 = _mm256_loadu_ps(&f3[start_idx]);
    __m256 vf4 = _mm256_loadu_ps(&f4[start_idx]);
    __m256 vf5 = _mm256_loadu_ps(&f5[start_idx]);
    __m256 vf6 = _mm256_loadu_ps(&f6[start_idx]);

    // Calcular diferenças
    __m256 d0 = _mm256_sub_ps(vf0, vc0);
    __m256 d1 = _mm256_sub_ps(vf1, vc1);
    __m256 d2 = _mm256_sub_ps(vf2, vc2);
    __m256 d3 = _mm256_sub_ps(vf3, vc3);
    __m256 d4 = _mm256_sub_ps(vf4, vc4);
    __m256 d5 = _mm256_sub_ps(vf5, vc5);
    __m256 d6 = _mm256_sub_ps(vf6, vc6);

    // Calcular quadrados e acumular
    __m256 sum = _mm256_mul_ps(d0, d0);
    sum = _mm256_fmadd_ps(d1, d1, sum);  // sum += d1²
    sum = _mm256_fmadd_ps(d2, d2, sum);
    sum = _mm256_fmadd_ps(d3, d3, sum);
    sum = _mm256_fmadd_ps(d4, d4, sum);
    sum = _mm256_fmadd_ps(d5, d5, sum);
    sum = _mm256_fmadd_ps(d6, d6, sum);

    // Armazenar resultados
    _mm256_storeu_ps(distances, sum);
}

// Inicializa centroids aleatoriamente
static void initialize_centroids_soa_no_unroll(float centroids[][NUM_FEATURES],
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

// Encontra cluster mais próximo - versão escalar
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

// Processa 8 pontos e encontra clusters mais próximos (SIMD)
static inline void find_nearest_clusters_8(
    const float * restrict f0, const float * restrict f1,
    const float * restrict f2, const float * restrict f3,
    const float * restrict f4, const float * restrict f5,
    const float * restrict f6, size_t start_idx,
    const float centroids[][NUM_FEATURES], int k,
    int * restrict results) {

    float distances[8] __attribute__((aligned(32)));
    float min_distances[8];

    // Inicializar com distâncias ao primeiro centroid
    compute_distances_8_points(f0, f1, f2, f3, f4, f5, f6, start_idx,
        centroids[0][0], centroids[0][1], centroids[0][2], centroids[0][3],
        centroids[0][4], centroids[0][5], centroids[0][6], min_distances);

    for (int i = 0; i < 8; i++) {
        results[i] = 0;
    }

    // Comparar com outros centroids
    for (int c = 1; c < k; c++) {
        compute_distances_8_points(f0, f1, f2, f3, f4, f5, f6, start_idx,
            centroids[c][0], centroids[c][1], centroids[c][2], centroids[c][3],
            centroids[c][4], centroids[c][5], centroids[c][6], distances);

        for (int i = 0; i < 8; i++) {
            if (distances[i] < min_distances[i]) {
                min_distances[i] = distances[i];
                results[i] = c;
            }
        }
    }
}

// Atualiza centroids - versão otimizada (1 ÚNICA passada!)
static void update_centroids_soa_no_unroll(float centroids[][NUM_FEATURES],
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

// K-means OTIMIZADO SEM UNROLL - com SIMD processando 8 pontos por vez
void kmeans_optimized_no_unroll(DataSetSoA * restrict dataset,
                                float centroids[][NUM_FEATURES],
                                int k, int max_iterations) {

    // Inicializar centroids
    initialize_centroids_soa_no_unroll(centroids, dataset, k);

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

        // Processar em blocos de 8 pontos com SIMD
        const size_t n_simd = (n / 8) * 8;  // Múltiplo de 8
        int results[8];

        for (size_t i = 0; i < n_simd; i += 8) {
            // Processar 8 pontos de uma vez
            find_nearest_clusters_8(f0, f1, f2, f3, f4, f5, f6, i, centroids, k, results);

            // Atualizar cluster_ids e contar mudanças
            for (int j = 0; j < 8; j++) {
                const int old_cluster = cluster_ids[i + j];
                cluster_ids[i + j] = results[j];
                changes += (old_cluster != results[j]);
            }
        }

        // Processar pontos restantes (cleanup)
        for (size_t i = n_simd; i < n; i++) {
            const int old_cluster = cluster_ids[i];
            const int new_cluster = find_nearest_cluster_generic(f0, f1, f2, f3, f4, f5, f6, i, centroids, k);

            cluster_ids[i] = new_cluster;
            changes += (old_cluster != new_cluster);
        }

        DEBUG_PRINT("Iteration %d: %d points changed cluster\n", iter, changes);

        // Convergência - parar se nada mudou
        if (changes == 0) {
            DEBUG_PRINT("Converged after %d iterations\n", iter + 1);
            break;
        }

        // Atualizar centroids
        update_centroids_soa_no_unroll(centroids, dataset, k);
    }
}
