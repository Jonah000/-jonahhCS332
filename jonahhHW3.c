#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>
#include <errno.h>

int count_words_in_file(const char *filepath) {
    FILE *file = fopen(filepath, "r");
    if (!file) {
        perror("Error opening file");
        return -1;
    }

    int words = 0;
    char ch, prev = ' ';
    while ((ch = fgetc(file)) != EOF) {
        if (ch == ' ' || ch == '\n' || ch == '\t') {
            if (prev != ' ' && prev != '\n' && prev != '\t') {
                words++;
            }
        }
        prev = ch;
    }

    if (prev != ' ' && prev != '\n' && prev != '\t') {
        words++;
    }

    fclose(file);
    return words;
}

void process_file(const char *filepath, const char *filename) {
    struct stat file_stat;

    if (stat(filepath, &file_stat) == -1) {
        perror("Error retrieving file information");
        exit(EXIT_FAILURE);
    }

    printf("File: %s\n", filename);
    printf("Size: %ld bytes\n", file_stat.st_size);

    if (strstr(filename, ".txt") != NULL) {
        int word_count = count_words_in_file(filepath);
        if (word_count != -1) {
            printf("Word Count: %d\n", word_count);
        }
    } else {
        printf("Word Count: Not applicable (not a .txt file)\n");
    }
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <directory>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *directory_path = argv[1];
    DIR *dir = opendir(directory_path);
    if (!dir) {
        perror("Error opening directory");
        return EXIT_FAILURE;
    }

    struct dirent *entry;
    int child_pid;
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_DIR || entry->d_name[0] == '.') {
            continue;
        }

        char filepath[PATH_MAX];
        snprintf(filepath, sizeof(filepath), "%s/%s", directory_path, entry->d_name);

        if ((child_pid = fork()) == -1) {
            perror("Error creating child process");
            closedir(dir);
            return EXIT_FAILURE;
        }

        if (child_pid == 0) {
            process_file(filepath, entry->d_name);
            exit(EXIT_SUCCESS);
        }
    }

    closedir(dir);

    while (wait(NULL) > 0);
    
    printf("All child processes have completed.\n");
    return EXIT_SUCCESS;
}