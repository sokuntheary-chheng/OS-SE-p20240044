#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

volatile sig_atomic_t keep_running = 1;
volatile sig_atomic_t caught_signal = 0;

void handle_signal(int sig) {
    caught_signal = sig;
    keep_running = 0;
}

int main(void) {
    struct sigaction sa;
    sa.sa_handler = handle_signal;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;

    sigaction(SIGINT, &sa, NULL);
    sigaction(SIGTERM, &sa, NULL);

    printf("signal_demo running, pid=%d. Send SIGINT (Ctrl+C) or SIGTERM to stop.\n", getpid());

    while (keep_running) {
        printf("looping... (pid=%d)\n", getpid());
        sleep(1);
    }

    printf("Caught signal %d. Cleaning up gracefully...\n", caught_signal);
    printf("Cleanup complete. Exiting now.\n");
    return 0;
}
