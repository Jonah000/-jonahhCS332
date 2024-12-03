#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <sys/stat.h>

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

void listDirectory(const char *dirname, int level) {
    struct dirent *dirent;
    DIR *dir = opendir(dirname);

    if (dir == NULL) {
        perror("Error opening directory");
        return;
    }

    printf("%*sDirectory: %s\n", level * 2, "", dirname);
    int count = 1;

    while ((dirent = readdir(dir)) != NULL) {

        if (strcmp(dirent->d_name, ".") == 0 || strcmp(dirent->d_name, "..") == 0) {
            continue;
        }

        char path[1024];
        snprintf(path, sizeof(path), "%s/%s", dirname, dirent->d_name);

        printf("%*s[%d] %s (%s)\n", level * 2, "", count, dirent->d_name, filetype(dirent->d_type));
        count++;

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
    listDirectory(argv[1], 0);

    return 0;
}