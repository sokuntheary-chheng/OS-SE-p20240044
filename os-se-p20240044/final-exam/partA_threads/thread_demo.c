#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/types.h>

#define NUM_THREADS 4

typedef struct {
    int id;
    int result;
} thread_data_t;

void *worker(void *arg) {
    thread_data_t *data = (thread_data_t *)arg;
    pid_t tid = (pid_t) syscall(SYS_gettid);
    data->result = (data->id + 1) * (data->id + 1); // computed value
    printf("Worker %d: pid=%d tid(LWP)=%d computed_value=%d\n",
           data->id, getpid(), tid, data->result);
    return NULL;
}

int main(void) {
    pthread_t threads[NUM_THREADS];
    thread_data_t data[NUM_THREADS];
    int sum = 0;

    printf("Main: starting %d worker threads, main pid=%d\n", NUM_THREADS, getpid());

    for (int i = 0; i < NUM_THREADS; i++) {
        data[i].id = i;
        if (pthread_create(&threads[i], NULL, worker, &data[i]) != 0) {
            perror("pthread_create failed");
            exit(1);
        }
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
        sum += data[i].result;
    }

    printf("Summary: all %d workers joined. Total of computed values = %d\n",
           NUM_THREADS, sum);

    return 0;
}
