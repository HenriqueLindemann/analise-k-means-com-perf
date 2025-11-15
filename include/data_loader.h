#ifndef DATA_LOADER_H
#define DATA_LOADER_H

#include <stddef.h>
#include "kmeans.h"

// Carrega dataset do arquivo texto original e converte para binário
int convert_dataset_to_binary(const char *input_txt, const char *output_bin,
                               size_t max_samples);

// Carrega dataset binário em formato AoS
DataPoint* load_dataset_aos(const char *binary_file, size_t *num_points);

// Carrega dataset binário em formato SoA
DataSetSoA* load_dataset_soa(const char *binary_file, size_t *num_points);

// Libera memória do dataset SoA
void free_dataset_soa(DataSetSoA *dataset);

// Obtém informações sobre o dataset binário
int get_dataset_info(const char *binary_file, size_t *num_points);

#endif // DATA_LOADER_H
