#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void insertionSort(char *arr[], int n) {
    for (int i = 1; i < n; i++) {
        char *key = arr[i];
        int j = i - 1;

        while (j >= 0 && strcmp(arr[j], key) > 0) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

void printArray(char *arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%s ", arr[i]);
    }
    printf("\n");
}

int main() {
    int n;
    
    printf("Enter the number of strings: ");
    scanf("%d", &n);

    char **arr = (char **)malloc(n * sizeof(char *));
    if (arr == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    char buffer[100];
    printf("Enter the strings:\n");
    for (int i = 0; i < n; i++) {
        scanf("%s", buffer);
        arr[i] = (char *)malloc((strlen(buffer) + 1) * sizeof(char));
        if (arr[i] == NULL) {
            printf("Memory allocation failed.\n");
            return 1;
        }
        strcpy(arr[i], buffer);
    }

    printf("Original array: \n");
    printArray(arr, n);

    insertionSort(arr, n);


    printf("Sorted array: \n");
    printArray(arr, n);

    for (int i = 0; i < n; i++) {
        free(arr[i]);
    }
    free(arr);

    return 0;
}