#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LISTINGS 1000
#define MAX_STR_LEN 100

typedef struct {
    char host_name[MAX_STR_LEN];
    double price;
} Listing;

int compareHostName(const void *a, const void *b) {
    Listing *listingA = (Listing *)a;
    Listing *listingB = (Listing *)b;
    return strcmp(listingA->host_name, listingB->host_name);
}

int comparePrice(const void *a, const void *b) {
    Listing *listingA = (Listing *)a;
    Listing *listingB = (Listing *)b;
    if (listingA->price < listingB->price) return -1;
    if (listingA->price > listingB->price) return 1;
    return 0;
}

int readCSV(const char *filename, Listing listings[], int maxListings) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        return -1;
    }

    char line[1024];
    int count = 0;

    fgets(line, sizeof(line), file);

    while (fgets(line, sizeof(line), file)) {
        if (count >= maxListings) {
            printf("Reached maximum number of listings\n");
            break;
        }

        char *token = strtok(line, ",");
        strcpy(listings[count].host_name, token);

        token = strtok(NULL, ",");
        listings[count].price = atof(token);


        count++;
    }

    fclose(file);
    return count;
}

void printListings(Listing listings[], int count) {
    for (int i = 0; i < count; i++) {
        printf("Host: %s, Price: %.2f\n", listings[i].host_name, listings[i].price);
    }
}

void writeCSV(const char *filename, Listing listings[], int count) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error opening file for writing");
        return;
    }

    fprintf(file, "host_name,price\n");

    for (int i = 0; i < count; i++) {
        fprintf(file, "%s,%.2f\n", listings[i].host_name, listings[i].price);
    }

    fclose(file);
}

int main() {
    Listing listings[MAX_LISTINGS];
    int listingCount;

    listingCount = readCSV("listings.csv", listings, MAX_LISTINGS);
    if (listingCount == -1) {
        return 1;
    }

    printf("\nSorting by host_name:\n");
    qsort(listings, listingCount, sizeof(Listing), compareHostName);
    printListings(listings, listingCount);

    writeCSV("sorted_by_host_name.csv", listings, listingCount);

    printf("\nSorting by price:\n");
    qsort(listings, listingCount, sizeof(Listing), comparePrice);
    printListings(listings, listingCount);

    writeCSV("sorted_by_price.csv", listings, listingCount);

    return 0;
}