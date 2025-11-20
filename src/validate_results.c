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
    printf("  K-means Validation (3 Versions)\n");
    printf("========================================\n");
    printf("K=%d, Max iterations=%d\n", k, max_iter);
    printf("Dataset: %s\n\n", dataset_path);

    // Seed fixa para resultados reproduzíveis
    seed_random(42);

    // ========================================
    // 1. Carregar dados para versão NAIVE
    // ========================================
    printf("[1/9] Loading dataset for NAIVE version...\n");
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
    printf("[2/9] Running NAIVE K-means...\n");
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
    // 2. Carregar dados para versão OPTIMIZED NO-UNROLL
    // ========================================
    printf("[3/9] Loading dataset for OPTIMIZED NO-UNROLL version...\n");

    // Resetar seed para mesma inicialização
    seed_random(42);

    size_t n_opt_no_unroll;
    DataSetSoA *opt_no_unroll_dataset = load_dataset_soa(dataset_path, &n_opt_no_unroll);
    if (!opt_no_unroll_dataset) {
        fprintf(stderr, "Failed to load dataset (SoA) for no-unroll\n");
        free(naive_points);
        return 1;
    }
    printf("  Loaded %zu points\n", n_opt_no_unroll);

    if (n_naive != n_opt_no_unroll) {
        fprintf(stderr, "ERROR: Dataset sizes don't match! (%zu vs %zu)\n", n_naive, n_opt_no_unroll);
        free(naive_points);
        free_dataset_soa(opt_no_unroll_dataset);
        return 1;
    }

    // Alocar centroids
    float opt_no_unroll_centroids[k][NUM_FEATURES];

    // Rodar K-means optimized no-unroll
    printf("[4/9] Running OPTIMIZED NO-UNROLL K-means...\n");
    kmeans_optimized_no_unroll(opt_no_unroll_dataset, opt_no_unroll_centroids, k, max_iter);

    // Calcular inércia optimized no-unroll
    DataPoint *opt_no_unroll_points_aos = malloc(n_opt_no_unroll * sizeof(DataPoint));
    for (size_t i = 0; i < n_opt_no_unroll; i++) {
        opt_no_unroll_points_aos[i].features[0] = opt_no_unroll_dataset->global_active_power[i];
        opt_no_unroll_points_aos[i].features[1] = opt_no_unroll_dataset->global_reactive_power[i];
        opt_no_unroll_points_aos[i].features[2] = opt_no_unroll_dataset->voltage[i];
        opt_no_unroll_points_aos[i].features[3] = opt_no_unroll_dataset->global_intensity[i];
        opt_no_unroll_points_aos[i].features[4] = opt_no_unroll_dataset->sub_metering_1[i];
        opt_no_unroll_points_aos[i].features[5] = opt_no_unroll_dataset->sub_metering_2[i];
        opt_no_unroll_points_aos[i].features[6] = opt_no_unroll_dataset->sub_metering_3[i];
        opt_no_unroll_points_aos[i].cluster_id = opt_no_unroll_dataset->cluster_ids[i];
    }
    float opt_no_unroll_inertia = calculate_inertia(opt_no_unroll_points_aos, n_opt_no_unroll, opt_no_unroll_centroids);
    printf("  Optimized no-unroll inertia: %.2f\n", opt_no_unroll_inertia);

    // ========================================
    // 3. Carregar dados para versão OPTIMIZED WITH-UNROLL
    // ========================================
    printf("[5/9] Loading dataset for OPTIMIZED WITH-UNROLL version...\n");

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

    // Rodar K-means optimized with-unroll
    printf("[6/9] Running OPTIMIZED WITH-UNROLL K-means...\n");
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

    // Calcular inércia optimized with-unroll
    float opt_inertia = calculate_inertia(opt_points_aos, n_opt, opt_centroids);
    printf("  Optimized with-unroll inertia: %.2f\n", opt_inertia);

    // ========================================
    // 4. Comparar resultados
    // ========================================
    printf("[7/9] Comparing results...\n");

    // Comparar Naive vs No-Unroll
    printf("\n--- NAIVE vs NO-UNROLL ---\n");
    int naive_vs_no_unroll = compare_centroids(naive_centroids, opt_no_unroll_centroids, k);

    // Comparar Naive vs With-Unroll
    printf("\n--- NAIVE vs WITH-UNROLL ---\n");
    int naive_vs_with_unroll = compare_centroids(naive_centroids, opt_centroids, k);

    // Comparar No-Unroll vs With-Unroll
    printf("\n--- NO-UNROLL vs WITH-UNROLL ---\n");
    int no_unroll_vs_with_unroll = compare_centroids(opt_no_unroll_centroids, opt_centroids, k);

    // Comparar distribuição
    printf("\n[8/9] Comparing cluster distributions...\n");

    int *naive_cluster_ids = malloc(n_naive * sizeof(int));
    for (size_t i = 0; i < n_naive; i++) {
        naive_cluster_ids[i] = naive_points[i].cluster_id;
    }

    printf("\n--- Naive vs No-Unroll Distribution ---\n");
    compare_distribution(naive_cluster_ids, opt_no_unroll_dataset->cluster_ids, n_naive, k);

    printf("\n--- Naive vs With-Unroll Distribution ---\n");
    compare_distribution(naive_cluster_ids, opt_dataset->cluster_ids, n_naive, k);

    printf("\n--- No-Unroll vs With-Unroll Distribution ---\n");
    compare_distribution(opt_no_unroll_dataset->cluster_ids, opt_dataset->cluster_ids, n_naive, k);

    // Comparar inércia
    printf("\n=== Comparing Inertia ===\n");
    float inertia_diff_naive_no_unroll = fabsf(naive_inertia - opt_no_unroll_inertia);
    float inertia_diff_naive_with_unroll = fabsf(naive_inertia - opt_inertia);
    float inertia_diff_no_unroll_with_unroll = fabsf(opt_no_unroll_inertia - opt_inertia);

    float inertia_diff_pct_1 = (inertia_diff_naive_no_unroll / naive_inertia) * 100.0f;
    float inertia_diff_pct_2 = (inertia_diff_naive_with_unroll / naive_inertia) * 100.0f;
    float inertia_diff_pct_3 = (inertia_diff_no_unroll_with_unroll / opt_no_unroll_inertia) * 100.0f;

    printf("  Naive inertia:              %.2f\n", naive_inertia);
    printf("  Optimized no-unroll inertia: %.2f\n", opt_no_unroll_inertia);
    printf("  Optimized with-unroll inertia: %.2f\n", opt_inertia);
    printf("\n");
    printf("  Naive vs No-Unroll diff:    %.2f (%.3f%%)\n", inertia_diff_naive_no_unroll, inertia_diff_pct_1);
    printf("  Naive vs With-Unroll diff:  %.2f (%.3f%%)\n", inertia_diff_naive_with_unroll, inertia_diff_pct_2);
    printf("  No-Unroll vs With-Unroll:   %.2f (%.3f%%)\n", inertia_diff_no_unroll_with_unroll, inertia_diff_pct_3);

    // ========================================
    // 5. Resultado final
    // ========================================
    printf("\n[9/9] Final validation result:\n");
    printf("========================================\n");

    int all_match = naive_vs_no_unroll && naive_vs_with_unroll && no_unroll_vs_with_unroll;
    int all_inertia_ok = (inertia_diff_pct_1 < 0.1f) && (inertia_diff_pct_2 < 0.1f) && (inertia_diff_pct_3 < 0.1f);

    if (all_match && all_inertia_ok) {
        printf("✓ VALIDATION PASSED\n");
        printf("  All 3 implementations produce equivalent results!\n");
        printf("  - Naive vs No-Unroll: ✓\n");
        printf("  - Naive vs With-Unroll: ✓\n");
        printf("  - No-Unroll vs With-Unroll: ✓\n");
    } else {
        printf("✗ VALIDATION FAILED\n");
        if (!naive_vs_no_unroll) {
            printf("  Naive vs No-Unroll: Centroids don't match!\n");
        }
        if (!naive_vs_with_unroll) {
            printf("  Naive vs With-Unroll: Centroids don't match!\n");
        }
        if (!no_unroll_vs_with_unroll) {
            printf("  No-Unroll vs With-Unroll: Centroids don't match!\n");
        }
        if (!all_inertia_ok) {
            printf("  Inertia differences too large!\n");
        }
    }
    printf("========================================\n");

    // Cleanup
    free(naive_points);
    free(naive_cluster_ids);
    free(opt_no_unroll_points_aos);
    free(opt_points_aos);
    free_dataset_soa(opt_no_unroll_dataset);
    free_dataset_soa(opt_dataset);

    return all_match && all_inertia_ok ? 0 : 1;
}
