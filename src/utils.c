#include "utils.h"
#include "kmeans.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef DEBUG
#define DEBUG_PRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DEBUG_PRINT(...) do {} while(0)
#endif

void timer_start(Timer *t) {
    clock_gettime(CLOCK_MONOTONIC, &t->start);
}

void timer_stop(Timer *t) {
    clock_gettime(CLOCK_MONOTONIC, &t->end);
    t->elapsed_ms = (t->end.tv_sec - t->start.tv_sec) * 1000.0 +
                    (t->end.tv_nsec - t->start.tv_nsec) / 1000000.0;
}

double timer_elapsed_ms(const Timer *t) {
    return t->elapsed_ms;
}

void seed_random(unsigned int seed) {
    srand(seed);
}

int random_int(int max) {
    return rand() % max;
}

void print_centroids(const float centroids[][NUM_FEATURES], int k) {
#ifdef DEBUG
    DEBUG_PRINT("\n=== Centroids ===\n");
    for (int i = 0; i < k; i++) {
        DEBUG_PRINT("Cluster %d: [", i);
        for (int j = 0; j < NUM_FEATURES; j++) {
            DEBUG_PRINT("%.4f%s", centroids[i][j], j < NUM_FEATURES - 1 ? ", " : "");
        }
        DEBUG_PRINT("]\n");
    }
#else
    (void)centroids;
    (void)k;
#endif
}

void save_results(const char *filename, const int *cluster_ids,
                  size_t num_points, int k) {
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        fprintf(stderr, "Error: cannot open %s for writing\n", filename);
        return;
    }

    // Contar pontos por cluster
    int *counts = calloc(k, sizeof(int));
    for (size_t i = 0; i < num_points; i++) {
        if (cluster_ids[i] >= 0 && cluster_ids[i] < k) {
            counts[cluster_ids[i]]++;
        }
    }

    fprintf(fp, "k=%d, total_points=%zu\n", k, num_points);
    for (int i = 0; i < k; i++) {
        fprintf(fp, "cluster_%d: %d points (%.2f%%)\n",
                i, counts[i], 100.0 * counts[i] / num_points);
    }

    free(counts);
    fclose(fp);
}

int validate_clustering(const int *cluster_ids1, const int *cluster_ids2,
                        size_t num_points) {
    int differences = 0;
    for (size_t i = 0; i < num_points; i++) {
        if (cluster_ids1[i] != cluster_ids2[i]) {
            differences++;
        }
    }
    return differences;
}
