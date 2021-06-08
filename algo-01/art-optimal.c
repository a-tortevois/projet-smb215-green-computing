/*
root@raspberrypi:~/projet-smb215# gcc -w -Wall algo-01/art-optimal.c -o algo-01/art-optimal.o
root@raspberrypi:~/projet-smb215# chmod +x algo-01/art-optimal.o
root@raspberrypi:~/projet-smb215# perf stat ./algo-01/art-optimal.o
*/

#include <errno.h>
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LONG_MAX     2147483647L
#define LONG_MIN (-LONG_MAX - 1L)

#define INPUT_FILE  "./algo-01/input.txt"
#define OUTPUT_FILE "./algo-01/solution.txt"

int parseInt(char *str, int *value) {
    char *endptr;
    errno = 0; // to distinguish success/failure after call
    long int lvalue = strtol(str, &endptr, 10);
    if ((errno == ERANGE && (lvalue == LONG_MAX || lvalue == LONG_MIN)) || (errno != 0 && lvalue == 0)) {
        printf("Conversion Error !\n");
        return -1;
    }
    *value = (int) lvalue;
    return 0;
}

int parseFirstLine(FILE *inFp, int *baseX, int *baseY) {
    int rc = 0;
    char line[32] = {0};
    if (fgets(line, sizeof(line), inFp) == NULL) {
        rc = -1;
        printf("Unable to get the first line: %s\n", strerror(errno));
        goto __error;
    }
    char *baseX_str = strtok(line, ",");
    char *baseY_str = strtok(NULL, ",");
    if ((rc = parseInt(baseX_str, baseX)) < 0) {
        goto __error;
    }
    if ((rc = parseInt(baseY_str, baseY)) < 0) {
        goto __error;
    }
    __error:
    return rc;
}

int computeBaseGrid(FILE *inFp, char *baseGrid, int lineLength) {
    char *pos0 = baseGrid;
    int len = lineLength + 4; // add 4 bytes for the end of the line and end of the string
    char line[len];
    memset(line, 0, sizeof(line));
    // Lines are placed one after the other in the memory
    // baseGrid[0][0] is pos0
    // baseGrid[1][0] is pos0 + lineLength
    // To know the position of baseGrid[x][y], baseGrid = pos0 + x * lineLength + y
    while (fgets(line, len, inFp) != NULL) {
        memcpy(baseGrid, line, lineLength);
        memset(line, 0, sizeof(line));
        baseGrid += lineLength; // move the pointer
    }
    // Back to position 0
    *baseGrid = *pos0;
    return 0;
}

int main() {
    int rc = 0;
    FILE *inFptr = NULL;
    FILE *outFptr = NULL;
    int baseX; // num of rows
    int baseY; // num of cols (line length)

    if ((inFptr = fopen(INPUT_FILE, "r")) == NULL) {
        rc = -1;
        printf("Unable to open the file %s: %s\n", INPUT_FILE, strerror(errno));
        goto __error;
    }

    if ((outFptr = fopen(OUTPUT_FILE, "w")) == NULL) {
        rc = -1;
        printf("Unable to open the file %s: %s\n", OUTPUT_FILE, strerror(errno));
        goto __error;
    }

    if ((rc = parseFirstLine(inFptr, &baseX, &baseY)) < 0) {
        goto __error;
    }

    // printf("BaseX: %d, BaseY: %d\n", baseX, baseY);

    int result = 0;
    int gridLen = baseX * baseY + 1;
    char *baseGrid = malloc(sizeof(char) * gridLen);
    char *pos0 = baseGrid;
    memset(baseGrid, 0, gridLen);
    computeBaseGrid(inFptr, baseGrid, baseX);

    char buffer[20] = {0};
    for (int y = 0; y < baseY; y++) {
        for (int x = 0; x < baseX; x++) {
            // baseGrid = pos0 + x * baseY + y;
            if (*baseGrid == '\043') { // #
                result++;
                sprintf(buffer, "FILL,%d,%d,1\n", x, y);
                fwrite(buffer, 1, strlen(buffer), outFptr);
                memset(buffer, 0, sizeof(buffer));
            }
            baseGrid++;
        }
    }

    printf("Res: %d\n", result);

    // Back pointer to position 0 and free memory
    baseGrid = pos0;
    free(baseGrid);

    __error:
    if (inFptr) {
        if (fclose(inFptr) != 0) {
            rc = -1;
            printf("Unable to close the file %s: %s\n", INPUT_FILE, strerror(errno));
        }
    }

    if (outFptr) {
        if (fclose(outFptr) != 0) {
            rc = -1;
            printf("Unable to close the file %s: %s\n", OUTPUT_FILE, strerror(errno));
        }
    }

    return rc;
}
