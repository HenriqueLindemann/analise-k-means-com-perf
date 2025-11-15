#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "kmeans.h"
#include "data_loader.h"
#include "utils.h"

#define MAX_DIFF_THRESHOLD 1e-3  // Threshold para diferenças nos centroids

// Calcula distância euclidiana entre dois centroids
float centroid_distance(const float c1[NUM_FEATURES], const float c2[NUM_FEATURES]) {
    float sum = 0.0f;
    for (int i = 0; i < NUM_FEATURES; i++) {
        float diff = c1[i] - c2[i];
        sum += diff * diff;
    }
    return sqrtf(sum);
}

// Compara centroids entre duas versões
int compare_centroids(const float naive_centroids[][NUM_FEATURES],
                      const float opt_centroids[][NUM_FEATURES],
                      int k) {
    printf("\n=== Comparing Centroids ===\n");

    int matches = 0;
    int used[k];
    memset(used, 0, sizeof(used));

    // Para cada centroid naive, encontrar o mais próximo no optimized
    for (int i = 0; i < k; i++) {
        float min_dist = 1e10f;
        int best_match = -1;

        for (int j = 0; j < k; j++) {
            if (used[j]) continue;

            float dist = centroid_distance(naive_centroids[i], opt_centroids[j]);
            if (dist < min_dist) {
                min_dist = dist;
                best_match = j;
            }
        }

        used[best_match] = 1;

        printf("  Naive cluster %d <-> Optimized cluster %d: distance = %.6f",
               i, best_match, min_dist);

        if (min_dist < MAX_DIFF_THRESHOLD) {
            printf(" ✓\n");
            matches++;
        } else {
            printf(" ✗ (MISMATCH!)\n");
        }
    }

    printf("\nMatches: %d/%d\n", matches, k);
    return matches == k;
}

// Compara distribuição de clusters
void compare_distribution(const int *naive_ids, const int *opt_ids,
                          size_t n, int k) {
    printf("\n=== Comparing Cluster Distribution ===\n");

    int naive_counts[k];
    int opt_counts[k];
    memset(naive_counts, 0, sizeof(naive_counts));
    memset(opt_counts, 0, sizeof(opt_counts));

    for (size_t i = 0; i < n; i++) {
        naive_counts[naive_ids[i]]++;
        opt_counts[opt_ids[i]]++;
    }

    printf("Cluster | Naive Count | Optimized Count | Difference\n");
    printf("--------|-------------|-----------------|------------\n");

    for (int i = 0; i < k; i++) {
        int diff = abs(naive_counts[i] - opt_counts[i]);
        float diff_pct = (diff * 100.0f) / n;
        printf("   %d    | %11d | %15d | %d (%.3f%%)\n",
               i, naive_counts[i], opt_counts[i], diff, diff_pct);
    }
}

// Calcula inércia (soma das distâncias quadradas ao centroid)
float calculate_inertia(const DataPoint *points, size_t n,
                        const float centroids[][NUM_FEATURES]) {
    float inertia = 0.0f;

    for (size_t i = 0; i < n; i++) {
        int cluster = points[i].cluster_id;
        for (int f = 0; f < NUM_FEATURES; f++) {
            float diff = points[i].features[f] - centroids[cluster][f];
            inertia += diff * diff;
        }
    }

    return inertia;
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s <k> <max_iter> <dataset.bin>\n", argv[0]);
        return 1;
    }

    int k = atoi(argv[1]);
    int max_iter = atoi(argv[2]);
    const char *dataset_path = argv[3];

    printf("========================================\n");
    printf("  K-means Validation\n");
    printf("========================================\n");
    printf("K=%d, Max iterations=%d\n", k, max_iter);
    printf("Dataset: %s\n\n", dataset_path);

    // Seed fixa para resultados reproduzíveis
    seed_random(42);

    // ========================================
    // 1. Carregar dados para versão NAIVE
    // ========================================
    printf("[1/6] Loading dataset for NAIVE version...\n");
    size_t n_naive;
    DataPoint *naive_points = load_dataset_aos(dataset_path, &n_naive);
    if (!naive_points) {
        fprintf(stderr, "Failed to load dataset (AoS)\n");
        return 1;
    }
    printf("  Loaded %zu points\n", n_naive);

    // Alocar centroids
    float naive_centroids[k][NUM_FEATURES];

    // Rodar K-means naive
    printf("[2/6] Running NAIVE K-means...\n");
    Centroid centroids_aos[k];
    for (int i = 0; i < k; i++) {
        memset(&centroids_aos[i], 0, sizeof(Centroid));
    }

    kmeans_naive(naive_points, n_naive, centroids_aos, k, max_iter);

    // Copiar centroids
    for (int i = 0; i < k; i++) {
        memcpy(naive_centroids[i], centroids_aos[i].features, NUM_FEATURES * sizeof(float));
    }

    // Calcular inércia naive
    float naive_inertia = calculate_inertia(naive_points, n_naive, naive_centroids);
    printf("  Naive inertia: %.2f\n", naive_inertia);

    // ========================================
    // 2. Carregar dados para versão OPTIMIZED
    // ========================================
    printf("[3/6] Loading dataset for OPTIMIZED version...\n");

    // Resetar seed para mesma inicialização
    seed_random(42);

    size_t n_opt;
    DataSetSoA *opt_dataset = load_dataset_soa(dataset_path, &n_opt);
    if (!opt_dataset) {
        fprintf(stderr, "Failed to load dataset (SoA)\n");
        free(naive_points);
        return 1;
    }
    printf("  Loaded %zu points\n", n_opt);

    if (n_naive != n_opt) {
        fprintf(stderr, "ERROR: Dataset sizes don't match! (%zu vs %zu)\n", n_naive, n_opt);
        free(naive_points);
        free_dataset_soa(opt_dataset);
        return 1;
    }

    // Alocar centroids
    float opt_centroids[k][NUM_FEATURES];

    // Rodar K-means optimized
    printf("[4/6] Running OPTIMIZED K-means...\n");
    kmeans_optimized(opt_dataset, opt_centroids, k, max_iter);

    // Copiar cluster_ids para array AoS para comparação
    DataPoint *opt_points_aos = malloc(n_opt * sizeof(DataPoint));
    for (size_t i = 0; i < n_opt; i++) {
        opt_points_aos[i].features[0] = opt_dataset->global_active_power[i];
        opt_points_aos[i].features[1] = opt_dataset->global_reactive_power[i];
        opt_points_aos[i].features[2] = opt_dataset->voltage[i];
        opt_points_aos[i].features[3] = opt_dataset->global_intensity[i];
        opt_points_aos[i].features[4] = opt_dataset->sub_metering_1[i];
        opt_points_aos[i].features[5] = opt_dataset->sub_metering_2[i];
        opt_points_aos[i].features[6] = opt_dataset->sub_metering_3[i];
        opt_points_aos[i].cluster_id = opt_dataset->cluster_ids[i];
    }

    // Calcular inércia optimized
    float opt_inertia = calculate_inertia(opt_points_aos, n_opt, opt_centroids);
    printf("  Optimized inertia: %.2f\n", opt_inertia);

    // ========================================
    // 3. Comparar resultados
    // ========================================
    printf("[5/6] Comparing results...\n");

    int centroids_match = compare_centroids(naive_centroids, opt_centroids, k);

    // Comparar distribuição
    int *naive_cluster_ids = malloc(n_naive * sizeof(int));
    for (size_t i = 0; i < n_naive; i++) {
        naive_cluster_ids[i] = naive_points[i].cluster_id;
    }

    compare_distribution(naive_cluster_ids, opt_dataset->cluster_ids, n_naive, k);

    // Comparar inércia
    printf("\n=== Comparing Inertia ===\n");
    float inertia_diff = fabsf(naive_inertia - opt_inertia);
    float inertia_diff_pct = (inertia_diff / naive_inertia) * 100.0f;
    printf("  Naive inertia:     %.2f\n", naive_inertia);
    printf("  Optimized inertia: %.2f\n", opt_inertia);
    printf("  Difference:        %.2f (%.3f%%)\n", inertia_diff, inertia_diff_pct);

    // ========================================
    // 4. Resultado final
    // ========================================
    printf("\n[6/6] Final validation result:\n");
    printf("========================================\n");

    if (centroids_match && inertia_diff_pct < 0.1f) {
        printf("✓ VALIDATION PASSED\n");
        printf("  Both implementations produce equivalent results!\n");
    } else {
        printf("✗ VALIDATION FAILED\n");
        if (!centroids_match) {
            printf("  Centroids don't match!\n");
        }
        if (inertia_diff_pct >= 0.1f) {
            printf("  Inertia difference too large (%.3f%%)\n", inertia_diff_pct);
        }
    }
    printf("========================================\n");

    // Cleanup
    free(naive_points);
    free(naive_cluster_ids);
    free(opt_points_aos);
    free_dataset_soa(opt_dataset);

    return centroids_match && inertia_diff_pct < 0.1f ? 0 : 1;
}
