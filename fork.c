#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include <time.h>

char** parse_command(char *line, int *argc) {
    int buffer_size = 64;
    char **args = malloc(buffer_size * sizeof(char*));
    char *arg;
    int count = 0;

    arg = strtok(line, " \n");
    while (arg != NULL) {
        args[count++] = arg;

        if (count >= buffer_size) {
            buffer_size += 64;
            args = realloc(args, buffer_size * sizeof(char*));
        }

        arg = strtok(NULL, " \n");
    }
    args[count] = NULL;
    *argc = count;
    return args;
}

void log_details(const char *command, const char *start_time, const char *end_time) {
    FILE *log_file = fopen("output.log", "a");
    if (log_file == NULL) {
        perror("Failed to open log file");
        exit(EXIT_FAILURE);
    }
    fprintf(log_file, "%s\t%s\t%s\n", command, start_time, end_time);
    fclose(log_file);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <input_filename>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    FILE *input_file = fopen(argv[1], "r");
    if (input_file == NULL) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    char line[256];
    while (fgets(line, sizeof(line), input_file) != NULL) {
        int arg_count;
        char **args = parse_command(line, &arg_count);

        if (arg_count == 0) {
            continue;
        }

        time_t start_time_t = time(NULL);
        char *start_time_str = ctime(&start_time_t);

        pid_t pid = fork();

        if (pid == -1) {
            perror("fork failed");
            exit(EXIT_FAILURE);
        } else if (pid == 0) {

            if (execvp(args[0], args) == -1) {
                perror("execvp failed");
                exit(EXIT_FAILURE);
            }
        } else {
            int status;
            waitpid(pid, &status, 0);

            time_t end_time_t = time(NULL);
            char *end_time_str = ctime(&end_time_t);

            log_details(line, start_time_str, end_time_str);
        }

        free(args);
    }

    fclose(input_file);

    return 0;
}