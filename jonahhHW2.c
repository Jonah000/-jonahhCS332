#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <unistd.h>

typedef struct {
    char name[256];
    unsigned char type;
} FileInfo;

int compareFileNames(const void *a, const void *b) {
    FileInfo *fileA = (FileInfo *)a;
    FileInfo *fileB = (FileInfo *)b;
    return strcmp(fileA->name, fileB->name);
}

char *filetype(unsigned char type) {
    switch(type) {
        case DT_BLK: return "block device";
        case DT_CHR: return "character device";
        case DT_DIR: return "directory";
        case DT_FIFO: return "FIFO/pipe";
        case DT_LNK: return "symlink";
        case DT_REG: return "regular file";
        case DT_SOCK: return "socket";
        case DT_UNKNOWN: return "unknown";
        default: return "unknown";
    }
}

void traverseDirectory(const char *dirName, int filterType) {
    DIR *dir;
    struct dirent *entry;
    FileInfo files[1024];
    int fileCount = 0;

    dir = opendir(dirName);
    if (dir == NULL) {
        perror("Unable to open directory");
        return;
    }

    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }

        strcpy(files[fileCount].name, entry->d_name);
        files[fileCount].type = entry->d_type;
        fileCount++;

        if (entry->d_type == DT_DIR) {
            char path[1024];
            snprintf(path, sizeof(path), "%s/%s", dirName, entry->d_name);
            printf("Directory: %s\n", path);
            traverseDirectory(path, filterType);
        }
    }

    qsort(files, fileCount, sizeof(FileInfo), compareFileNames);

    for (int i = 0; i < fileCount; i++) {
        if (filterType == 0 || files[i].type == filterType) {
            printf("%s (%s)\n", files[i].name, filetype(files[i].type));
        }
    }

    closedir(dir);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <directory_name> [file_type]\n", argv[0]);
        printf("File types: 1=regular file, 2=directory, 3=symlink\n");
        exit(EXIT_FAILURE);
    }

    char *dirName = argv[1];

    int filterType = 0;
    if (argc == 3) {
        if (strcmp(argv[2], "regular") == 0) {
            filterType = DT_REG;
        } else if (strcmp(argv[2], "directory") == 0) {
            filterType = DT_DIR;
        } else if (strcmp(argv[2], "symlink") == 0) {
            filterType = DT_LNK;
        } else {
            printf("Unknown file type for filtering\n");
            exit(EXIT_FAILURE);
        }
    }

    traverseDirectory(dirName, filterType);

    return 0;
}