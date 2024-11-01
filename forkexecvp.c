/* Simple program to illustrate the use of fork-exec-wait pattern.
* This version uses execvp and command-line arguments to create a new process.
* To Compile: gcc -Wall forkexecvp.c
* To Run: ./a.out <command> [args]
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>

pid_t child_pid;

void handle_signal(int sig) {
    if (sig == SIGINT || sig == SIGTSTP) {
        if (child_pid > 0) {
            kill(child_pid, sig);
        }
    } else if (sig == SIGQUIT) {
        printf("Parent received SIGQUIT. Exiting...\n");
        if (child_pid > 0) {
            kill(child_pid, SIGKILL);
        }
        exit(0);
    }
}

int main(int argc, char **argv) {
    int status;

    if (argc < 2) {
        printf("Usage: %s <command> [args]\n", argv[0]);
        exit(-1);
    }

    signal(SIGINT, handle_signal);
    signal(SIGTSTP, handle_signal);
    signal(SIGQUIT, handle_signal);

    child_pid = fork();
    if (child_pid == 0) {
        execvp(argv[1], &argv[1]);
        printf("If you see this statement then execvp failed ;-(\n");
        perror("execvp");
        exit(-1);
    } else if (child_pid > 0) {
        printf("Wait for the child process to terminate or send signals (Ctrl-C, Ctrl-Z, Ctrl-\\)\n");
        
        waitpid(child_pid, &status, 0);
        if (WIFEXITED(status)) {
            printf("Child process exited with status = %d\n", WEXITSTATUS(status));
        } else if (WIFSIGNALED(status)) {
            printf("Child process terminated by signal %d\n", WTERMSIG(status));
        } else {
            printf("Child process did not terminate normally!\n");
        }
    } else {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    printf("[%ld]: Exiting program .....\n", (long)getpid());
    return 0;
}