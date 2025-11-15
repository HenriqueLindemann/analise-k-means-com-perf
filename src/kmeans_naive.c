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

// Versão NAIVE: Array of Structs (AoS), sem otimizações de cache

// Calcula distância euclidiana ao quadrado entre ponto e centroid
float euclidean_distance_aos(const DataPoint *p, const Centroid *c) {
    float dist = 0.0f;
    for (int i = 0; i < NUM_FEATURES; i++) {
        float diff = p->features[i] - c->features[i];
        dist += diff * diff;
    }
    return dist;
}

// Inicializa centroids aleatoriamente (k-means++)
void initialize_centroids_random(Centroid *centroids, const DataPoint *points,
                                  int k, size_t num_points) {
    // Selecionar k pontos aleatórios únicos
    int *selected = malloc(k * sizeof(int));

    for (int i = 0; i < k; i++) {
        int idx;
        int is_unique;

        do {
            idx = random_int(num_points);
            is_unique = 1;

            // Verificar se já foi selecionado
            for (int j = 0; j < i; j++) {
                if (selected[j] == idx) {
                    is_unique = 0;
                    break;
                }
            }
        } while (!is_unique);

        selected[i] = idx;

        // Copiar features do ponto selecionado
        memcpy(centroids[i].features, points[idx].features,
               NUM_FEATURES * sizeof(float));
        centroids[i].count = 0;
    }

    free(selected);
}

// Encontra o cluster mais próximo para um ponto
static int find_nearest_cluster(const DataPoint *point, const Centroid *centroids, int k) {
    int nearest = 0;
    float min_dist = euclidean_distance_aos(point, &centroids[0]);

    for (int i = 1; i < k; i++) {
        float dist = euclidean_distance_aos(point, &centroids[i]);
        if (dist < min_dist) {
            min_dist = dist;
            nearest = i;
        }
    }

    return nearest;
}

// Atualiza centroids baseado nos pontos atribuídos
static void update_centroids(Centroid *centroids, const DataPoint *points,
                             size_t num_points, int k) {
    // Resetar centroids
    for (int i = 0; i < k; i++) {
        memset(centroids[i].features, 0, NUM_FEATURES * sizeof(float));
        centroids[i].count = 0;
    }

    // Somar features de todos os pontos em cada cluster
    for (size_t i = 0; i < num_points; i++) {
        int cluster = points[i].cluster_id;
        if (cluster >= 0 && cluster < k) {
            for (int j = 0; j < NUM_FEATURES; j++) {
                centroids[cluster].features[j] += points[i].features[j];
            }
            centroids[cluster].count++;
        }
    }

    // Calcular média
    for (int i = 0; i < k; i++) {
        if (centroids[i].count > 0) {
            for (int j = 0; j < NUM_FEATURES; j++) {
                centroids[i].features[j] /= centroids[i].count;
            }
        }
    }
}

// K-means NAIVE
void kmeans_naive(DataPoint *points, size_t num_points,
                  Centroid *centroids, int k, int max_iterations) {

    // Inicializar centroids
    initialize_centroids_random(centroids, points, k, num_points);

    // Iterar até convergência ou max_iterations
    for (int iter = 0; iter < max_iterations; iter++) {
        int changes = 0;

        // Atribuir cada ponto ao cluster mais próximo
        for (size_t i = 0; i < num_points; i++) {
            int new_cluster = find_nearest_cluster(&points[i], centroids, k);

            if (points[i].cluster_id != new_cluster) {
                changes++;
                points[i].cluster_id = new_cluster;
            }
        }

        DEBUG_PRINT("Iteration %d: %d points changed cluster\n", iter, changes);

        // Se não houve mudanças, convergiu
        if (changes == 0) {
            DEBUG_PRINT("Converged after %d iterations\n", iter + 1);
            break;
        }

        // Atualizar centroids
        update_centroids(centroids, points, num_points, k);
    }
}
