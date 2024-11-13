#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>

void createarray(char *buf, char **array) {
    int i, count, len;
    len = strlen(buf);
    buf[len - 1] = '\0';
    for (i = 0, array[0] = &buf[0], count = 1; i < len; i++) {
        if (buf[i] == ' ') {
            buf[i] = '\0';
            array[count++] = &buf[i + 1];
        }
    }
    array[count] = NULL;
}

int main(int argc, char **argv) {
    pid_t pid;
    int status;
    char line[BUFSIZ], buf[BUFSIZ], *args[BUFSIZ];
    time_t t1, t2;

    if (argc < 2) {
        printf("Usage: %s <commands file>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    FILE *fp1 = fopen(argv[1], "r");
    if (fp1 == NULL) {
        perror("Error opening input file for reading");
        exit(EXIT_FAILURE);
    }

    FILE *fp2 = fopen("output.log", "w");
    if (fp2 == NULL) {
        perror("Error opening output.log for writing");
        fclose(fp1);
        exit(EXIT_FAILURE);
    }

    while (fgets(line, BUFSIZ, fp1) != NULL) {
        strcpy(buf, line);
        createarray(line, args);

        time(&t1);
        pid = fork();
        if (pid == 0) {
            char out_file[BUFSIZ], err_file[BUFSIZ];
            snprintf(out_file, BUFSIZ, "%d.out", getpid());
            snprintf(err_file, BUFSIZ, "%d.err", getpid());

            int fd_out = open(out_file, O_WRONLY | O_CREAT | O_TRUNC, 0644);
            if (fd_out == -1) {
                perror("Error opening output file for stdout");
                exit(EXIT_FAILURE);
            }
            int fd_err = open(err_file, O_WRONLY | O_CREAT | O_TRUNC, 0644);
            if (fd_err == -1) {
                perror("Error opening output file for stderr");
                close(fd_out);
                exit(EXIT_FAILURE);
            }

            dup2(fd_out, STDOUT_FILENO);
            dup2(fd_err, STDERR_FILENO);

            close(fd_out);
            close(fd_err);

            execvp(args[0], args);
            perror("exec");
            exit(EXIT_FAILURE);
        } else if (pid > 0) {
            printf("Child started at %s", ctime(&t1));
            printf("Waiting for the child process to terminate\n");

            waitpid(pid, &status, 0);
            time(&t2);

            printf("Child ended at %s", ctime(&t2));

            if (WIFEXITED(status)) {
                printf("Child process exited with status = %d\n", WEXITSTATUS(status));
            } else {
                printf("Child process did not terminate normally!\n");
            }

            buf[strlen(buf) - 1] = '\t';
            strcat(buf, ctime(&t1));
            buf[strlen(buf) - 1] = '\t';
            strcat(buf, ctime(&t2));
            fprintf(fp2, "%s", buf);
            fflush(fp2);
        } else {
            perror("fork");
            fclose(fp1);
            fclose(fp2);
            exit(EXIT_FAILURE);
        }
    }

    fclose(fp1);
    fclose(fp2);
    printf("[%ld]: Exiting main program .....\n", (long)getpid());

    return 0;
}