#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define NUM_THREADS_PARENT 3
#define NUM_THREADS_CHILD 10
#define NUM_NUMBERS 500
#define NUM_READ_PER_THREAD 150
#define RANDOM_RANGE 1000

int pipe_fd[2];
pthread_mutex_t pipe_mutex;

void* parent_thread_func(void* arg) {
    int thread_id = *(int*)arg;
    free(arg);

    for (int i = 0; i < NUM_NUMBERS; i++) {
        int random_num = rand() % (RANDOM_RANGE + 1);

        pthread_mutex_lock(&pipe_mutex);
        write(pipe_fd[1], &random_num, sizeof(random_num));
        pthread_mutex_unlock(&pipe_mutex);
    }

    printf("Parent thread %d completed.\n", thread_id);
    pthread_exit(NULL);
}

void* child_thread_func(void* arg) {
    int thread_id = *(int*)arg;
    free(arg);

    int sum = 0;
    int number;
    for (int i = 0; i < NUM_READ_PER_THREAD; i++) {
        pthread_mutex_lock(&pipe_mutex);
        read(pipe_fd[0], &number, sizeof(number));
        pthread_mutex_unlock(&pipe_mutex);

        sum += number;
    }

    int* result = malloc(sizeof(int));
    *result = sum;
    printf("Child thread %d computed sum: %d\n", thread_id, sum);
    pthread_exit(result);
}

int main() {
    if (pipe(pipe_fd) == -1) {
        perror("Pipe creation failed");
        return 1;
    }

    pthread_mutex_init(&pipe_mutex, NULL);

    pthread_t parent_threads[NUM_THREADS_PARENT];
    for (int i = 0; i < NUM_THREADS_PARENT; i++) {
        int* thread_id = malloc(sizeof(int));
        *thread_id = i + 1;
        if (pthread_create(&parent_threads[i], NULL, parent_thread_func, thread_id) != 0) {
            perror("Parent thread creation failed");
            return 1;
        }
    }

    for (int i = 0; i < NUM_THREADS_PARENT; i++) {
        pthread_join(parent_threads[i], NULL);
    }

    printf("Parent process threads completed. Creating child process...\n");

    pid_t pid = fork();
    if (pid < 0) {
        perror("Fork failed");
        return 1;
    } else if (pid == 0) {
        pthread_t child_threads[NUM_THREADS_CHILD];
        int* thread_results[NUM_THREADS_CHILD] = {0};

        for (int i = 0; i < NUM_THREADS_CHILD; i++) {
            int* thread_id = malloc(sizeof(int));
            *thread_id = i + 1;
            if (pthread_create(&child_threads[i], NULL, child_thread_func, thread_id) != 0) {
                perror("Child thread creation failed");
                return 1;
            }
        }

        int total_sum = 0;
        for (int i = 0; i < NUM_THREADS_CHILD; i++) {
            int* result;
            pthread_join(child_threads[i], (void**)&result);
            total_sum += *result;
            free(result);
        }

        double average = (double)total_sum / NUM_THREADS_CHILD;
        freopen("output.txt", "w", stdout);
        printf("Average of sums: %.2f\n", average);
        fclose(stdout);

        exit(0);
    } else {
        wait(NULL);
        printf("Child process completed. Check 'output.txt' for the result.\n");
    }

    close(pipe_fd[0]);
    close(pipe_fd[1]);
    pthread_mutex_destroy(&pipe_mutex);

    return 0;
}