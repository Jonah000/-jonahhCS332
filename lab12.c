#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

typedef struct {
    double *a;
    double sum;
    int N;
    int size;
    long tid;
} ThreadData;

void *compute(void *arg) {
    ThreadData *data = (ThreadData *)arg;
    int myStart, myEnd, myN, i;

    myN = data->N / data->size;
    myStart = data->tid * myN;
    myEnd = myStart + myN;
    if (data->tid == (data->size - 1)) myEnd = data->N;

    double mysum = 0.0;
    for (i = myStart; i < myEnd; i++)
        mysum += data->a[i];

    pthread_mutex_lock(&mutex);
    data->sum += mysum;
    pthread_mutex_unlock(&mutex);

    return NULL;
}

int main(int argc, char **argv) {
    long i;
    pthread_t *threads;
    ThreadData *threadData;
    double *a;
    int N, size;
    double totalSum = 0.0;

    if (argc != 3) {
        printf("Usage: %s <# of elements> <# of threads>\n", argv[0]);
        exit(-1);
    }

    N = atoi(argv[1]);
    size = atoi(argv[2]);

    threads = (pthread_t *)malloc(sizeof(pthread_t) * size);
    threadData = (ThreadData *)malloc(sizeof(ThreadData) * size);
    a = (double *)malloc(sizeof(double) * N);

    for (i = 0; i < N; i++)
        a[i] = (double)(i + 1);

    for (i = 0; i < size; i++) {
        threadData[i].a = a;
        threadData[i].sum = 0.0;
        threadData[i].N = N;
        threadData[i].size = size;
        threadData[i].tid = i;
        pthread_create(&threads[i], NULL, compute, (void *)&threadData[i]);
    }

    for (i = 0; i < size; i++) {
        pthread_join(threads[i], NULL);
        totalSum += threadData[i].sum;
    }

    printf("The total is %g, it should be equal to %g\n",
           totalSum, ((double)N * (N + 1)) / 2);

    free(threads);
    free(threadData);
    free(a);

    return 0;
}