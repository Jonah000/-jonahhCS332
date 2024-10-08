#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void printFileContents(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        return;
    }

    char ch;
    while ((ch = fgetc(file)) != EOF) {
        putchar(ch);
    }

    fclose(file);
}

int main(int argc, char *argv[]) {

    if (argc != 3) {
        fprintf(stderr, "Usage: %s <first_file> <second_file>\n", argv[0]);
        return 1;
    }

    char *firstFileName = argv[1];
    char *secondFileName = argv[2];

    if (strcmp(firstFileName, secondFileName) == 0) {
        fprintf(stderr, "Error: Filenames are the same. Cannot concatenate.\n");
        return 1;
    }

    FILE *firstFile = fopen(firstFileName, "a");
    if (firstFile == NULL) {
        perror("Error opening first file");
        return 1;
    }

    FILE *secondFile = fopen(secondFileName, "r");
    if (secondFile == NULL) {
        perror("Error opening second file");
        fclose(firstFile);
        return 1;
    }

    char buffer[1024];
    size_t bytesRead;
    while ((bytesRead = fread(buffer, 1, sizeof(buffer), secondFile)) > 0) {
        fwrite(buffer, 1, bytesRead, firstFile);
    }

    fclose(firstFile);
    fclose(secondFile);

    printf("Files concatenated successfully.\n");

    printf("\nContents of the first file (%s) after concatenation:\n", firstFileName);
    printFileContents(firstFileName);

    printf("\nContents of the second file (%s):\n", secondFileName);
    printFileContents(secondFileName);

    return 0;
}