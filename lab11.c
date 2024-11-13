#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    FILE *fp;
    char command[BUFSIZ];
    char output[BUFSIZ];

    while (1) {
        printf("Enter a UNIX command (or type 'quit' to exit): ");
        if (fgets(command, BUFSIZ, stdin) == NULL) {
            printf("Error reading input.\n");
            continue;
        }

        command[strcspn(command, "\n")] = '\0';

        if (strcmp(command, "quit") == 0) {
            printf("Exiting program...\n");
            break;
        }

        if ((fp = popen(command, "r")) == NULL) {
            perror("popen");
            continue;
        }

        printf("Output:\n");
        while (fgets(output, BUFSIZ, fp) != NULL) {
            fputs(output, stdout);
        }

        if (pclose(fp) == -1) {
            perror("pclose");
        }

        printf("\n");
    }

    return 0;
}