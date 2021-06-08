/*
root@raspberrypi:~/projet-smb215# gcc -w -Wall algo-03/art-optimal.c -o algo-03/art-optimal.o
root@raspberrypi:~/projet-smb215# chmod +x algo-03/art-optimal.o
root@raspberrypi:~/projet-smb215# perf stat ./algo-03/art-optimal.o
*/

#include <errno.h>
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define LONG_MAX     2147483647L
#define LONG_MIN (-LONG_MAX - 1L)

#define INPUT_FILE  "./algo-03/input.txt"
#define OUTPUT_FILE "./algo-03/solution.txt"

#define HASH '\043'
#define STAR '\052'
#define PLUS '\053'

typedef struct drawableElem {
    int x; // coord X
    int y; // coord Y
    int d; // deep max
    int i; // isolationIndex
    int w; // weight
} drawableElem;

static FILE *inFptr = NULL;
static FILE *outFptr = NULL;
static int result = 0;
static int baseX = 0; // num of rows
static int baseY = 0; // num of cols (line length)
static int gridLen = 0;
static char *baseGrid;
static drawableElem *drawableArea;
//static int *isolationIndex;

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

int parseFirstLine(FILE *inFp) {
    int rc = 0;
    char line[32] = {0};
    if (fgets(line, sizeof(line), inFp) == NULL) {
        rc = -1;
        printf("Unable to get the first line: %s\n", strerror(errno));
        goto __error;
    }
    char *baseX_str = strtok(line, ",");
    char *baseY_str = strtok(NULL, ",");
    if ((rc = parseInt(baseX_str, &baseX)) < 0) {
        goto __error;
    }
    if ((rc = parseInt(baseY_str, &baseY)) < 0) {
        goto __error;
    }
    __error:
    return rc;
}

int computeBaseGrid(FILE *inFp) {
    char *baseGrid_pos0 = baseGrid;
    int len = baseX + 4; // add 4 bytes for the end of the line and end of the string
    char line[len];
    memset(line, 0, sizeof(line));
    // Lines are placed one after the other in the memory
    // baseGrid[0][0] is pos0
    // baseGrid[1][0] is pos0 + lineLength
    // To know the position of baseGrid[x][y], baseGrid = pos0 + y * baseX + x
    while (fgets(line, len, inFp) != NULL) {
        memcpy(baseGrid, line, baseX);
        memset(line, 0, sizeof(line));
        baseGrid += baseX; // move the pointer
    }
    // Back to position 0
    baseGrid = baseGrid_pos0;
    return 0;
}

int getArrayIndex(int x, int y) {
    return y * baseX + x;
}

char getBaseGrid(int x, int y) {
    return *(baseGrid + getArrayIndex(x, y));
}

bool isBetween(int value, int min, int max) {
    return value > min && value < max;
}

bool inDrawableArea(int x, int y, int d) {
    return x + d < baseX && y + d < baseY;
}

bool isDrawable(int x, int y, int d) {
    if (getBaseGrid(x + d, y + d) == STAR) {
        return false;
    }
    for (int i = 0; i < d; i++) {
        if (getBaseGrid(x + d, y + i) == STAR || getBaseGrid(x + i, y + d) == STAR) {
            return false;
        }
    }
    return true;
}

int compareElem(drawableElem a, drawableElem b) {
    if (a.w == b.w) {
        if (a.d == b.d) {
            if (a.y == b.y) {
                return a.x - b.x;
            }
            return a.y - b.y;
        }
        return b.d - a.d;
    }
    return b.w - a.w;
}

int getIsolationIndex(int x, int y) {
    int index = 0;
    for (int j = -1; j < 2; j++) {
        int yj = y + j;
        if (yj < 0 || yj > baseY - 1) {
            continue;
        }
        for (int i = -1; i < 2; i++) {
            int xi = x + i;
            if (xi < 0 || xi > baseX - 1) {
                continue;
            }
            if (getBaseGrid(xi, yj) == STAR) {
                index++;
            }
        }
    }
    switch (index) {
        case 3: {
            if (isBetween(y, 0, baseY - 2)) {
                if (isBetween(x, 0, baseX - 2)) {
                    if (getBaseGrid(x, y - 1) == STAR && getBaseGrid(x - 1, y - 1) == STAR && getBaseGrid(x + 1, y - 1) == STAR) {
                        return 0;
                    }
                    if (getBaseGrid(x, y + 1) == STAR && getBaseGrid(x - 1, y + 1) == STAR && getBaseGrid(x + 1, y + 1) == STAR) {
                        return 0;
                    }
                    if (getBaseGrid(x - 1, y) == STAR && getBaseGrid(x - 1, y - 1) == STAR && getBaseGrid(x - 1, y + 1) == STAR) {
                        return 0;
                    }
                    if (getBaseGrid(x + 1, y) == STAR && getBaseGrid(x + 1, y - 1) == STAR && getBaseGrid(x + 1, y + 1) == STAR) {
                        return 0;
                    }
                    return index;
                }
            }
            break;
        }
        case 2: {
            if (isBetween(y, 0, baseY - 2)) {
                if (isBetween(x, 0, baseX - 2)) {
                    if (getBaseGrid(x, y - 1) == STAR && (getBaseGrid(x - 1, y - 1) == STAR || getBaseGrid(x + 1, y - 1) == STAR)) {
                        return 0;
                    }
                    if (getBaseGrid(x, y + 1) == STAR && (getBaseGrid(x - 1, y + 1) == STAR || getBaseGrid(x + 1, y + 1) == STAR)) {
                        return 0;
                    }
                    if (getBaseGrid(x - 1, y) == STAR && (getBaseGrid(x - 1, y - 1) == STAR || getBaseGrid(x - 1, y + 1) == STAR)) {
                        return 0;
                    }
                    if (getBaseGrid(x + 1, y) == STAR && (getBaseGrid(x + 1, y - 1) == STAR || getBaseGrid(x + 1, y + 1) == STAR)) {
                        return 0;
                    }
                    return index;
                }
            }
            break;
        }
        default:
            break;
    }
    return index;
}

void getDrawableArea(drawableElem *_drawableArea) {
    for (int y = 0; y < baseY; y++) {
        for (int x = 0; x < baseX; x++) {
            if (getBaseGrid(x, y) == HASH) {
                int d = 1;
                while (inDrawableArea(x, y, d) && isDrawable(x, y, d)) {
                    d++;
                }
                int yxIndex = getArrayIndex(x, y);
                drawableElem elem = {
                    .x =  x,
                    .y = y,
                    .d = d,
                    .i = getIsolationIndex(x, y),
                    .w = d * d
                };
                _drawableArea[yxIndex] = elem;
                // isolationIndex[yxIndex] = getIsolationIndex(x, y);
            }
        }
    }
}

bool isInArea(int x, int y, drawableElem elem) {
    return isBetween(x, elem.x - 1, elem.x + elem.d) && isBetween(y, elem.y - 1, elem.y + elem.d);
}

int computeWeightArea(drawableElem elem) {
    int weight = 0;
    for (int j = 0; j < elem.d; j++) {
        for (int i = 0; i < elem.d; i++) {
            if (getBaseGrid(elem.x + i, elem.y + j) == HASH) {
                weight++;
            }
        }
    }
    return weight;
}

void fillGrid(drawableElem elem) {
    for (int j = 0; j < elem.d; j++) {
        for (int i = 0; i < elem.d; i++) {
            if (getBaseGrid(elem.x + i, elem.y + j) == HASH) {
                int yxIndex = getArrayIndex(elem.x + i, elem.y + j);
                baseGrid[yxIndex] = PLUS;
                drawableArea[yxIndex].i = 0;
                // isolationIndex[yxIndex] = 0;
            }
        }
    }
}

void addToResult(drawableElem elem) {
    // console.log(`FILL,${elem.x},${elem.y},${elem.d}`);
    fillGrid(elem);
    result++;
    char buffer[20] = {0};
    sprintf(buffer, "FILL,%d,%d,%d\n", elem.x, elem.y, elem.d);
    fwrite(buffer, 1, strlen(buffer), outFptr);
}

void fillHeaviestArea(int x, int y) {
    drawableElem found = {0, 0, 0, 0 /*, 0 */};
    for (int i = 0; i < gridLen; i++) {
        if (drawableArea[i].w == 0) {
            continue;
        }
        if (isInArea(x, y, drawableArea[i])) {
            drawableArea[i].w = computeWeightArea(drawableArea[i]);
            if (drawableArea[i].w == 0) {
                continue;
            }
            if (compareElem(drawableArea[i], found) < 0) {
                found = drawableArea[i];
            }
        }
    }
    if (found.w != 0) {
        addToResult(found);
        drawableArea[getArrayIndex(found.x, found.y)].w = 0;
    }
}

int main() {
    int rc = 0;
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

    if ((rc = parseFirstLine(inFptr)) < 0) {
        goto __error;
    }

    // printf("BaseX: %d, BaseY: %d\n", baseX, baseY);
    gridLen = baseX * baseY + 1;
    baseGrid = malloc(sizeof(char) * gridLen);
    memset(baseGrid, 0, gridLen);
    computeBaseGrid(inFptr);

    // isolationIndex = malloc(sizeof(isolationIndex) * gridLen);
    // memset(isolationIndex, 0, sizeof(isolationIndex) * gridLen);

    drawableArea = malloc(sizeof(drawableElem) * gridLen);
    memset(drawableArea, 0, sizeof(drawableElem) * gridLen);
    getDrawableArea(drawableArea);

    // Fill in the most isolated pixels by heaviest area
    for (int index = 8; index > 1; index--) {
        for (int y = 0; y < baseY; y++) {
            for (int x = 0; x < baseX; x++) {
                if (getBaseGrid(x, y) == HASH && index == /*isolationIndex[getArrayIndex(x, y)] */ drawableArea[getArrayIndex(x, y)].i) {
                    fillHeaviestArea(x, y);
                }
            }
        }
    }

    // Fill in the remaining pixels from the end line
    for (int y = baseY - 1; y > -1; y--) {
        for (int x = 0; x < baseX; x++) {
            if (getBaseGrid(x, y) == HASH) {
                fillHeaviestArea(x, y);
            }
        }
    }

    printf("Res: %d\n", result);

    // Free memory
    free(baseGrid);
    // free(isolationIndex);
    free(drawableArea);

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