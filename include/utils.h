#ifndef UTILS_H
#define UTILS_H

#include <stddef.h>
#include <time.h>

// Forward declaration
#define NUM_FEATURES 7

// Estrutura para armazenar estatísticas de tempo
typedef struct {
    struct timespec start;
    struct timespec end;
    double elapsed_ms;
} Timer;

// Funções de timing
void timer_start(Timer *t);
void timer_stop(Timer *t);
double timer_elapsed_ms(const Timer *t);

// Funções de random
void seed_random(unsigned int seed);
int random_int(int max);

// Funções de debug/output
void print_centroids(const float centroids[][NUM_FEATURES], int k);
void save_results(const char *filename, const int *cluster_ids,
                  size_t num_points, int k);

// Validação
int validate_clustering(const int *cluster_ids1, const int *cluster_ids2,
                        size_t num_points);

#endif // UTILS_H
