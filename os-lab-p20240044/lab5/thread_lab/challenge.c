#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>

volatile int keep_running = 1;

void sig_handler(int signo) {
    if (signo == SIGINT) {
        printf("\n[Signal Caught] SIGINT received. Shutting down threads...\n");
        keep_running = 0;
    }
}

void* worker_func(void* arg) {
    long tid = (long)arg;
    while (keep_running) {
        printf("Worker thread %ld is running...\n", tid);
        sleep(1);
    }
    printf("Worker thread %ld exiting cleanly.\n", tid);
    pthread_exit(NULL);
}

int main() {
    pthread_t t1, t2;

    signal(SIGINT, sig_handler);

    pthread_create(&t1, NULL, worker_func, (void*)1);
    pthread_create(&t2, NULL, worker_func, (void*)2);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("All threads cleanly exited. Goodbye.\n");
    return 0;
}
