// Preprocessador de dados - converte dataset texto para binário
#include "data_loader.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <max_samples> [input.txt] [output.bin]\n", argv[0]);
        fprintf(stderr, "  max_samples: número máximo de amostras (0 = todas)\n");
        fprintf(stderr, "  input.txt:   arquivo de entrada (padrão: household_power_consumption.txt)\n");
        fprintf(stderr, "  output.bin:  arquivo de saída (padrão: data/dataset.bin)\n");
        return 1;
    }

    size_t max_samples = atoi(argv[1]);
    const char *input = argc > 2 ? argv[2] : "household_power_consumption.txt";
    const char *output = argc > 3 ? argv[3] : "data/dataset.bin";

    printf("Converting dataset...\n");
    printf("  Input:  %s\n", input);
    printf("  Output: %s\n", output);
    printf("  Max samples: %s\n", max_samples == 0 ? "all" : argv[1]);

    int result = convert_dataset_to_binary(input, output, max_samples);

    if (result == 0) {
        // Mostrar informações sobre o dataset gerado
        size_t num_points;
        if (get_dataset_info(output, &num_points) == 0) {
            printf("\nDataset converted successfully!\n");
            printf("  Total samples: %zu\n", num_points);
            printf("  Features: %d\n", NUM_FEATURES);
            printf("  File size: ~%.2f MB\n",
                   (sizeof(size_t) + num_points * NUM_FEATURES * sizeof(float)) / 1048576.0);
        }
    } else {
        fprintf(stderr, "Error converting dataset\n");
        return 1;
    }

    return 0;
}
