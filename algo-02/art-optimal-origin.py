'''
root@raspberrypi:~/projet-smb215# python3 algo-02/art-optimal.py
root@raspberrypi:~/projet-smb215# perf stat python3 algo-02/art-optimal.py
'''

import os
from functools import cmp_to_key


DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = DIR + "/input.txt"
OUTPUT_FILE = DIR + "/solution.txt"


def inDrawableArea(x, y, d):
    return x + d < baseX and y + d < baseY


def isDrawable(x, y, d):
    if baseGrid[y + d][x + d] == "*":
        return False
    for i in range(d):
        if baseGrid[y + i][x + d] == "*" or baseGrid[y + d][x + i] == "*":
            return False
    return True


def sortByValueReversed(dictionary, reverse=True):
    def comparator(a, b):
        if a[1] == b[1]:
            if a[0][2] == b[0][2]:
                if a[0][1] == b[0][1]:
                    return a[0][0] - b[0][0]
                return a[0][1] - b[0][1]
            return b[0][2] - a[0][2]
        return b[1] - a[1]

    return dict(sorted(dictionary.items(), key=cmp_to_key(comparator)))


def getDrawableArea():
    drawableArea = {}
    for y in range(baseY):
        for x in range(baseX):
            if baseGrid[y][x] == "#":
                d = 1
                while True:
                    if not inDrawableArea(x, y, d) or not isDrawable(x, y, d):
                        break
                    d += 1
                drawableArea[(x, y, d)] = d ** 2
    return drawableArea


def isInArea(x, y, s):
    return s[0] <= x < s[0] + s[2] and s[1] <= y < s[1] + s[2]


def computeWeightArea(x, y, d):
    weight = 0
    for j in range(d):
        for i in range(d):
            if baseGrid[y + j][x + i] == "#":
                weight += 1
    return weight


def fillHeaviestArea(x, y):
    found = {}
    listElem = list(drawableArea)
    for elem in listElem:
        if isInArea(x, y, elem):
            weight = computeWeightArea(*elem)
            if weight == 0:
                del drawableArea[elem]
            else:
                found[elem] = weight
    if len(found) > 0:
        elem = list(sortByValueReversed(found))[0]
        addToResult(*elem)
        del drawableArea[elem]


def fillGrid(x, y, d):
    for j in range(d):
        for i in range(d):
            if baseGrid[y + j][x + i] == "#":
                baseGrid[y + j][x + i] = "+"


def addToResult(x, y, d):
    # print(f'FILL,{x},{y},{d}')
    result.append(f'FILL,{x},{y},{d}')
    return fillGrid(x, y, d)


result = []
baseX = 0
baseY = 0
baseGrid = []
drawableArea = []

with open(INPUT_FILE) as f:
    baseX, baseY = map(int, f.readline().strip().split(','))
    for line in f:
        pixels = list(line.strip())
        baseGrid.append(pixels)

# print(f'BaseX: {baseX}, BaseY: {baseY}')
drawableArea = getDrawableArea()


# Fill in with the heaviest area
for y in range(baseY):
    for x in range(baseX):
        if baseGrid[y][x] == "#":
            fillHeaviestArea(x, y)

with open(OUTPUT_FILE, 'w') as f:
    f.write('\n'.join(result))
print('Res:', len(result))
