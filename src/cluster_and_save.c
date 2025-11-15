// Programa para executar K-means e salvar clusters para visualização
#include "kmeans.h"
#include "data_loader.h"
#include "utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void save_clusters_binary(const char *filename, const int *cluster_ids, size_t num_points) {
    FILE *fp = fopen(filename, "wb");
    if (!fp) {
        fprintf(stderr, "Error: cannot open %s for writing\n", filename);
        return;
    }

    // Escrever número de pontos
    fwrite(&num_points, sizeof(size_t), 1, fp);

    // Escrever cluster_ids
    fwrite(cluster_ids, sizeof(int), num_points, fp);

    fclose(fp);
    printf("Cluster assignments saved to: %s\n", filename);
}

void save_clusters_csv(const char *filename, const float *features,
                       const int *cluster_ids, size_t num_points) {
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        fprintf(stderr, "Error: cannot open %s for writing\n", filename);
        return;
    }

    // Header
    fprintf(fp, "global_active_power,global_reactive_power,voltage,global_intensity,");
    fprintf(fp, "sub_metering_1,sub_metering_2,sub_metering_3,cluster\n");

    // Dados (escrever apenas a cada N pontos para não criar arquivo gigante)
    size_t stride = num_points > 50000 ? num_points / 50000 : 1;

    for (size_t i = 0; i < num_points; i += stride) {
        for (int f = 0; f < NUM_FEATURES; f++) {
            fprintf(fp, "%.4f", features[i * NUM_FEATURES + f]);
            fprintf(fp, f < NUM_FEATURES - 1 ? "," : "");
        }
        fprintf(fp, ",%d\n", cluster_ids[i]);
    }

    fclose(fp);
    printf("Cluster data saved to: %s (sampled %zu/%zu points)\n",
           filename, num_points/stride, num_points);
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s <mode> <k> <dataset.bin> [output_prefix]\n", argv[0]);
        fprintf(stderr, "  mode: 'naive' or 'optimized'\n");
        fprintf(stderr, "  k: number of clusters\n");
        fprintf(stderr, "  dataset.bin: binary dataset file\n");
        fprintf(stderr, "  output_prefix: prefix for output files (default: 'clusters')\n");
        return 1;
    }

    const char *mode = argv[1];
    int k = atoi(argv[2]);
    const char *dataset_file = argv[3];
    const char *output_prefix = argc > 4 ? argv[4] : "clusters";

    if (k <= 0) {
        fprintf(stderr, "Error: k must be positive\n");
        return 1;
    }

    // Seed para reprodutibilidade
    seed_random(42);

    printf("Running K-means clustering...\n");
    printf("  Mode: %s\n", mode);
    printf("  K: %d\n", k);
    printf("  Dataset: %s\n", dataset_file);
    printf("\n");

    if (strcmp(mode, "optimized") == 0) {
        // Versão otimizada (SoA)
        size_t num_points;
        DataSetSoA *dataset = load_dataset_soa(dataset_file, &num_points);
        if (!dataset) {
            fprintf(stderr, "Error loading dataset\n");
            return 1;
        }

        printf("Loaded %zu points\n", num_points);

        float (*centroids)[NUM_FEATURES] = malloc(k * NUM_FEATURES * sizeof(float));
        if (!centroids) {
            fprintf(stderr, "Error allocating centroids\n");
            free_dataset_soa(dataset);
            return 1;
        }

        // Executar K-means
        printf("Running K-means (optimized)...\n");
        kmeans_optimized(dataset, centroids, k, 100);

        // Montar array de features para salvar CSV
        float *features_flat = malloc(num_points * NUM_FEATURES * sizeof(float));
        for (size_t i = 0; i < num_points; i++) {
            features_flat[i * NUM_FEATURES + 0] = dataset->global_active_power[i];
            features_flat[i * NUM_FEATURES + 1] = dataset->global_reactive_power[i];
            features_flat[i * NUM_FEATURES + 2] = dataset->voltage[i];
            features_flat[i * NUM_FEATURES + 3] = dataset->global_intensity[i];
            features_flat[i * NUM_FEATURES + 4] = dataset->sub_metering_1[i];
            features_flat[i * NUM_FEATURES + 5] = dataset->sub_metering_2[i];
            features_flat[i * NUM_FEATURES + 6] = dataset->sub_metering_3[i];
        }

        // Salvar resultados
        char bin_file[256], csv_file[256];
        snprintf(bin_file, sizeof(bin_file), "%s_optimized.bin", output_prefix);
        snprintf(csv_file, sizeof(csv_file), "%s_optimized.csv", output_prefix);

        save_clusters_binary(bin_file, dataset->cluster_ids, num_points);
        save_clusters_csv(csv_file, features_flat, dataset->cluster_ids, num_points);

        // Estatísticas
        int *counts = calloc(k, sizeof(int));
        for (size_t i = 0; i < num_points; i++) {
            counts[dataset->cluster_ids[i]]++;
        }

        printf("\nCluster distribution:\n");
        for (int i = 0; i < k; i++) {
            printf("  Cluster %d: %d points (%.2f%%)\n",
                   i, counts[i], 100.0 * counts[i] / num_points);
        }

        free(counts);
        free(features_flat);
        free(centroids);
        free_dataset_soa(dataset);

    } else if (strcmp(mode, "naive") == 0) {
        // Versão naive (AoS)
        size_t num_points;
        DataPoint *points = load_dataset_aos(dataset_file, &num_points);
        if (!points) {
            fprintf(stderr, "Error loading dataset\n");
            return 1;
        }

        printf("Loaded %zu points\n", num_points);

        Centroid *centroids = malloc(k * sizeof(Centroid));
        if (!centroids) {
            fprintf(stderr, "Error allocating centroids\n");
            free(points);
            return 1;
        }

        // Executar K-means
        printf("Running K-means (naive)...\n");
        kmeans_naive(points, num_points, centroids, k, 100);

        // Extrair cluster_ids e features
        int *cluster_ids = malloc(num_points * sizeof(int));
        float *features_flat = malloc(num_points * NUM_FEATURES * sizeof(float));

        for (size_t i = 0; i < num_points; i++) {
            cluster_ids[i] = points[i].cluster_id;
            for (int f = 0; f < NUM_FEATURES; f++) {
                features_flat[i * NUM_FEATURES + f] = points[i].features[f];
            }
        }

        // Salvar resultados
        char bin_file[256], csv_file[256];
        snprintf(bin_file, sizeof(bin_file), "%s_naive.bin", output_prefix);
        snprintf(csv_file, sizeof(csv_file), "%s_naive.csv", output_prefix);

        save_clusters_binary(bin_file, cluster_ids, num_points);
        save_clusters_csv(csv_file, features_flat, cluster_ids, num_points);

        // Estatísticas
        int *counts = calloc(k, sizeof(int));
        for (size_t i = 0; i < num_points; i++) {
            counts[cluster_ids[i]]++;
        }

        printf("\nCluster distribution:\n");
        for (int i = 0; i < k; i++) {
            printf("  Cluster %d: %d points (%.2f%%)\n",
                   i, counts[i], 100.0 * counts[i] / num_points);
        }

        free(counts);
        free(features_flat);
        free(cluster_ids);
        free(centroids);
        free(points);

    } else {
        fprintf(stderr, "Error: mode must be 'naive' or 'optimized'\n");
        return 1;
    }

    printf("\nDone!\n");
    return 0;
}
