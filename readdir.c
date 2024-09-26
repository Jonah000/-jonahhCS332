#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <sys/stat.h>

// Function to get file type as a string
char *filetype(unsigned char type) {
    switch (type) {
        case DT_BLK: return "block device";
        case DT_CHR: return "character device";
        case DT_DIR: return "directory";
        case DT_FIFO: return "named pipe (FIFO)";
        case DT_LNK: return "symbolic link";
        case DT_REG: return "regular file";
        case DT_SOCK: return "UNIX domain socket";
        case DT_UNKNOWN: return "unknown file type";
        default: return "UNKNOWN";
    }
}

// Function to list contents of a directory recursively
void listDirectory(const char *dirname, int level) {
    struct dirent *dirent;
    DIR *dir = opendir(dirname);

    if (dir == NULL) {
        perror("Error opening directory");
        return;
    }

    // Print the current directory
    printf("%*sDirectory: %s\n", level * 2, "", dirname);
    int count = 1;

    while ((dirent = readdir(dir)) != NULL) {
        // Skip the current directory (.) and the parent directory (..)
        if (strcmp(dirent->d_name, ".") == 0 || strcmp(dirent->d_name, "..") == 0) {
            continue;
        }

        // Create the full path for each entry
        char path[1024];
        snprintf(path, sizeof(path), "%s/%s", dirname, dirent->d_name);

        // Print the file or directory with its type
        printf("%*s[%d] %s (%s)\n", level * 2, "", count, dirent->d_name, filetype(dirent->d_type));
        count++;

        // If the entry is a directory, call the function recursively
        if (dirent->d_type == DT_DIR) {
            listDirectory(path, level + 1);
        }
    }

    closedir(dir);
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <dirname>\n", argv[0]);
        return 1;
    }

    // Start recursive directory listing from the given directory
    listDirectory(argv[1], 0);

    return 0;
}