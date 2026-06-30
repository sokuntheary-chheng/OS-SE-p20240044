#include <stdio.h>
#include <unistd.h>

int main(void) {
    printf("Real UID: %d\n", getuid());
    printf("Effective UID: %d\n", geteuid());
    return 0;
}
