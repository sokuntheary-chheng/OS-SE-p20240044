#include <stdio.h>

int main(int argc, char *argv[]) {

    if (argc != 2) {

        printf("Usage: sign_book 'se-chheng-sokuntheary'\n");

        return 1;

    }

    FILE *file = fopen("/home/se-chheng-sokuntheary/guestbook.txt", "a");

    if (file == NULL) {

        printf("Error opening guestbook.\n");

        return 1;

    }

    fprintf(file, "Visitor signed: %s\n", argv[1]);

    fclose(file);

    printf("Successfully signed the VIP guestbook!\n");

    return 0;

}
