#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int i;
    pid_t pids[3];

    for (i = 0; i < 3; i++) {
        pids[i] = fork();
        if (pids[i] == 0) {
            printf("Child %d (PID %d): sleeping 30s...\n", i+1, getpid());
            sleep(60);
            exit(0);
        }
    }

    printf("Parent (PID %d): created 3 children. Check ps --forest now!\n", getpid());
    for (i = 0; i < 3; i++) wait(NULL);
    printf("Parent: all children done.\n");
    return 0;
}
