#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) { perror("fork"); exit(1); }

    if (pid == 0) {
        printf("Child (PID %d): Exiting now.\n", getpid());
        exit(0);
    }

    /* Parent sleeps 10 seconds, THEN calls wait() */
    printf("Parent (PID %d): Child is %d. Sleeping 10s before wait()...\n", getpid(), pid);
    sleep(10);
    wait(NULL);
    printf("Parent: Called wait(). Zombie should be gone now.\n");
    sleep(5);
    return 0;
}
