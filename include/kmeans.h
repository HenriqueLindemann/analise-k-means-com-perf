#ifndef KMEANS_H
#define KMEANS_H

#include <stddef.h>

// Número de features do dataset (excluindo date e time)
#define NUM_FEATURES 7

// Estrutura para representar um ponto de dados (Array of Structs - AoS)
typedef struct {
    float features[NUM_FEATURES];
    int cluster_id;
} DataPoint;

// Estrutura para centroids
typedef struct {
    float features[NUM_FEATURES];
    int count;  // número de pontos neste cluster
} Centroid;

// Estrutura para dados em formato SoA (Struct of Arrays) - cache-friendly
typedef struct {
    float *global_active_power;
    float *global_reactive_power;
    float *voltage;
    float *global_intensity;
    float *sub_metering_1;
    float *sub_metering_2;
    float *sub_metering_3;
    int *cluster_ids;
    size_t num_points;
} DataSetSoA;

// K-means naive (AoS, sem otimizações)
void kmeans_naive(DataPoint *points, size_t num_points,
                  Centroid *centroids, int k, int max_iterations);

// K-means otimizado (SoA, cache-friendly)
void kmeans_optimized(DataSetSoA *dataset,
                      float centroids[][NUM_FEATURES],
                      int k, int max_iterations);

// Funções auxiliares
float euclidean_distance_aos(const DataPoint *p, const Centroid *c);
float euclidean_distance_soa(const DataSetSoA *dataset, size_t point_idx,
                              const float centroid[NUM_FEATURES]);

void initialize_centroids_random(Centroid *centroids, const DataPoint *points,
                                  int k, size_t num_points);
void initialize_centroids_soa(float centroids[][NUM_FEATURES],
                              const DataSetSoA *dataset, int k);

#endif // KMEANS_H
