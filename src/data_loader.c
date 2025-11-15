#include "data_loader.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef DEBUG
#define DEBUG_PRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DEBUG_PRINT(...) do {} while(0)
#endif

// Converte dataset do formato texto para binário
int convert_dataset_to_binary(const char *input_txt, const char *output_bin,
                               size_t max_samples) {
    FILE *fin = fopen(input_txt, "r");
    if (!fin) {
        fprintf(stderr, "Error: cannot open %s\n", input_txt);
        return -1;
    }

    FILE *fout = fopen(output_bin, "wb");
    if (!fout) {
        fprintf(stderr, "Error: cannot create %s\n", output_bin);
        fclose(fin);
        return -1;
    }

    char line[1024];
    size_t count = 0;

    // Pular header
    if (fgets(line, sizeof(line), fin) == NULL) {
        fclose(fin);
        fclose(fout);
        return -1;
    }

    // Escrever placeholder para número de amostras (atualizar depois)
    fwrite(&count, sizeof(size_t), 1, fout);

    // Processar linhas
    while (fgets(line, sizeof(line), fin) && (max_samples == 0 || count < max_samples)) {
        float features[NUM_FEATURES];
        char date[11], time[9];

        // Parse: Date;Time;Global_active_power;Global_reactive_power;Voltage;
        //        Global_intensity;Sub_metering_1;Sub_metering_2;Sub_metering_3
        int parsed = sscanf(line, "%10[^;];%8[^;];%f;%f;%f;%f;%f;%f;%f",
                           date, time,
                           &features[0], &features[1], &features[2],
                           &features[3], &features[4], &features[5], &features[6]);

        if (parsed != 9) {
            continue;  // Pular linhas com valores faltantes
        }

        // Verificar se há valores inválidos
        int valid = 1;
        for (int i = 0; i < NUM_FEATURES; i++) {
            if (features[i] < 0 || features[i] > 1e6) {
                valid = 0;
                break;
            }
        }

        if (valid) {
            fwrite(features, sizeof(float), NUM_FEATURES, fout);
            count++;
        }
    }

    // Atualizar número de amostras no header
    fseek(fout, 0, SEEK_SET);
    fwrite(&count, sizeof(size_t), 1, fout);

    fclose(fin);
    fclose(fout);

    DEBUG_PRINT("Converted %zu samples to %s\n", count, output_bin);
    return 0;
}

int get_dataset_info(const char *binary_file, size_t *num_points) {
    FILE *fp = fopen(binary_file, "rb");
    if (!fp) {
        return -1;
    }

    fread(num_points, sizeof(size_t), 1, fp);
    fclose(fp);
    return 0;
}

// Carrega dataset em formato AoS (Array of Structs)
DataPoint* load_dataset_aos(const char *binary_file, size_t *num_points) {
    FILE *fp = fopen(binary_file, "rb");
    if (!fp) {
        fprintf(stderr, "Error: cannot open %s\n", binary_file);
        return NULL;
    }

    // Ler número de pontos
    fread(num_points, sizeof(size_t), 1, fp);

    // Alocar memória para DataPoints
    DataPoint *points = malloc(*num_points * sizeof(DataPoint));
    if (!points) {
        fprintf(stderr, "Error: cannot allocate memory for %zu points\n", *num_points);
        fclose(fp);
        return NULL;
    }

    // Ler features
    for (size_t i = 0; i < *num_points; i++) {
        fread(points[i].features, sizeof(float), NUM_FEATURES, fp);
        points[i].cluster_id = -1;
    }

    fclose(fp);
    DEBUG_PRINT("Loaded %zu samples (AoS format)\n", *num_points);
    return points;
}

// Carrega dataset em formato SoA (Struct of Arrays) - cache-friendly
DataSetSoA* load_dataset_soa(const char *binary_file, size_t *num_points) {
    FILE *fp = fopen(binary_file, "rb");
    if (!fp) {
        fprintf(stderr, "Error: cannot open %s\n", binary_file);
        return NULL;
    }

    // Ler número de pontos
    fread(num_points, sizeof(size_t), 1, fp);

    // Alocar estrutura SoA
    DataSetSoA *dataset = malloc(sizeof(DataSetSoA));
    if (!dataset) {
        fclose(fp);
        return NULL;
    }

    dataset->num_points = *num_points;

    // Alocar arrays separados para cada feature (melhor para cache)
    dataset->global_active_power = malloc(*num_points * sizeof(float));
    dataset->global_reactive_power = malloc(*num_points * sizeof(float));
    dataset->voltage = malloc(*num_points * sizeof(float));
    dataset->global_intensity = malloc(*num_points * sizeof(float));
    dataset->sub_metering_1 = malloc(*num_points * sizeof(float));
    dataset->sub_metering_2 = malloc(*num_points * sizeof(float));
    dataset->sub_metering_3 = malloc(*num_points * sizeof(float));
    dataset->cluster_ids = malloc(*num_points * sizeof(int));

    if (!dataset->global_active_power || !dataset->global_reactive_power ||
        !dataset->voltage || !dataset->global_intensity ||
        !dataset->sub_metering_1 || !dataset->sub_metering_2 ||
        !dataset->sub_metering_3 || !dataset->cluster_ids) {
        fprintf(stderr, "Error: cannot allocate memory for SoA\n");
        free_dataset_soa(dataset);
        fclose(fp);
        return NULL;
    }

    // Ler dados e reorganizar em SoA
    float features[NUM_FEATURES];
    for (size_t i = 0; i < *num_points; i++) {
        fread(features, sizeof(float), NUM_FEATURES, fp);
        dataset->global_active_power[i] = features[0];
        dataset->global_reactive_power[i] = features[1];
        dataset->voltage[i] = features[2];
        dataset->global_intensity[i] = features[3];
        dataset->sub_metering_1[i] = features[4];
        dataset->sub_metering_2[i] = features[5];
        dataset->sub_metering_3[i] = features[6];
        dataset->cluster_ids[i] = -1;
    }

    fclose(fp);
    DEBUG_PRINT("Loaded %zu samples (SoA format - cache-friendly)\n", *num_points);
    return dataset;
}

void free_dataset_soa(DataSetSoA *dataset) {
    if (!dataset) return;

    free(dataset->global_active_power);
    free(dataset->global_reactive_power);
    free(dataset->voltage);
    free(dataset->global_intensity);
    free(dataset->sub_metering_1);
    free(dataset->sub_metering_2);
    free(dataset->sub_metering_3);
    free(dataset->cluster_ids);
    free(dataset);
}
