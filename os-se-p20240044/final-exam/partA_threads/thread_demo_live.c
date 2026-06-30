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
    sleep(3);
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
        pthread_create(&threads[i], NULL, worker, &data[i]);
    }
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
        sum += data[i].result;
    }
    printf("Summary: all %d workers joined. Total = %d\n", NUM_THREADS, sum);

    // CURVEBALL A: 1 extra worker, starts only after originals joined
    printf("Spawning 1 extra worker AFTER originals joined...\n");
    pthread_t extra;
    thread_data_t extra_data = { .id = 99 };
    pthread_create(&extra, NULL, worker, &extra_data);
    printf("Extra worker spawned, pid=%d (check /proc/%d/task NOW)\n", getpid(), getpid());
    pthread_join(extra, NULL);
    printf("Extra worker joined. Final extra result=%d\n", extra_data.result);

    return 0;
}
