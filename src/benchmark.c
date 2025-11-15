// Programa principal para benchmark de K-means
#include "kmeans.h"
#include "data_loader.h"
#include "utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_usage(const char *prog) {
    fprintf(stderr, "Usage: %s <mode> <k> <max_iter> <dataset.bin>\n", prog);
    fprintf(stderr, "  mode:      'naive' ou 'optimized'\n");
    fprintf(stderr, "  k:         número de clusters\n");
    fprintf(stderr, "  max_iter:  número máximo de iterações\n");
    fprintf(stderr, "  dataset:   arquivo binário de dados\n");
    fprintf(stderr, "\nExemplo: %s optimized 5 100 data/dataset.bin\n", prog);
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        print_usage(argv[0]);
        return 1;
    }

    const char *mode = argv[1];
    int k = atoi(argv[2]);
    int max_iterations = atoi(argv[3]);
    const char *dataset_file = argv[4];

    if (k <= 0 || max_iterations <= 0) {
        fprintf(stderr, "Error: k and max_iterations must be positive\n");
        return 1;
    }

    // Seed para reprodutibilidade
    seed_random(42);

    Timer timer;

    if (strcmp(mode, "naive") == 0) {
        // ===== VERSÃO NAIVE =====
        size_t num_points;
        DataPoint *points = load_dataset_aos(dataset_file, &num_points);
        if (!points) {
            fprintf(stderr, "Error loading dataset\n");
            return 1;
        }

        Centroid *centroids = malloc(k * sizeof(Centroid));
        if (!centroids) {
            fprintf(stderr, "Error allocating centroids\n");
            free(points);
            return 1;
        }

        // Executar K-means naive
        timer_start(&timer);
        kmeans_naive(points, num_points, centroids, k, max_iterations);
        timer_stop(&timer);

        // Output apenas o tempo (para parsing fácil pelo script)
        printf("%.3f\n", timer_elapsed_ms(&timer));

        // Salvar resultados
        int *cluster_ids = malloc(num_points * sizeof(int));
        for (size_t i = 0; i < num_points; i++) {
            cluster_ids[i] = points[i].cluster_id;
        }
        save_results("results_naive.txt", cluster_ids, num_points, k);

        free(cluster_ids);
        free(centroids);
        free(points);

    } else if (strcmp(mode, "optimized") == 0) {
        // ===== VERSÃO OTIMIZADA =====
        size_t num_points;
        DataSetSoA *dataset = load_dataset_soa(dataset_file, &num_points);
        if (!dataset) {
            fprintf(stderr, "Error loading dataset\n");
            return 1;
        }

        // Alocar centroids
        float (*centroids)[NUM_FEATURES] = malloc(k * NUM_FEATURES * sizeof(float));
        if (!centroids) {
            fprintf(stderr, "Error allocating centroids\n");
            free_dataset_soa(dataset);
            return 1;
        }

        // Executar K-means otimizado
        timer_start(&timer);
        kmeans_optimized(dataset, centroids, k, max_iterations);
        timer_stop(&timer);

        // Output apenas o tempo
        printf("%.3f\n", timer_elapsed_ms(&timer));

        // Salvar resultados
        save_results("results_optimized.txt", dataset->cluster_ids, num_points, k);

        free(centroids);
        free_dataset_soa(dataset);

    } else {
        fprintf(stderr, "Error: mode must be 'naive' or 'optimized'\n");
        print_usage(argv[0]);
        return 1;
    }

    return 0;
}
