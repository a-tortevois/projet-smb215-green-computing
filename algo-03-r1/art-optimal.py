'''
root@raspberrypi:~/projet-smb215# python3 algo-03-r1/art-optimal.py
root@raspberrypi:~/projet-smb215# perf stat python3 algo-03-r1/art-optimal.py
'''

import os


DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = DIR + "/input.txt"
OUTPUT_FILE = DIR + "/solution.txt"


class DrawableArea:
    def __init__(self, x, y, d, w):
        self.x = x
        self.y = y
        self.d = d
        self.w = w


def inDrawableArea(x, y, d):
    return x + d < baseX and y + d < baseY


def isDrawable(x, y, d):
    if baseGrid[y + d][x + d] == "*":
        return False
    for i in range(d):
        if baseGrid[y + i][x + d] == "*" or baseGrid[y + d][x + i] == "*":
            return False
    return True


def compareElem(a, b):
    if a[1] == b[1]:
        if a[0][2] == b[0][2]:
            if a[0][1] == b[0][1]:
                return a[0][0] - b[0][0]
            return a[0][1] - b[0][1]
        return b[0][2] - a[0][2]
    return b[1] - a[1]


def getIsolationIndex(x, y):
    index = 0
    for j in [-1, 0, 1]:
        yj = y + j
        if yj < 0 or yj > baseY - 1:
            continue
        for i in [-1, 0, 1]:
            xi = x + i
            if xi < 0 or xi > baseX - 1:
                continue
            if baseGrid[yj][xi] == "*":
                index += 1
    if index == 3:
        if 0 < y < baseY - 2:
            if 0 < x < baseX - 2:
                if baseGrid[y - 1][x] == "*" and baseGrid[y - 1][x - 1] == "*" and baseGrid[y - 1][x + 1] == "*":
                    return 0
                if baseGrid[y + 1][x] == "*" and baseGrid[y + 1][x - 1] == "*" and baseGrid[y + 1][x + 1] == "*":
                    return 0
                if baseGrid[y][x - 1] == "*" and baseGrid[y - 1][x - 1] == "*" and baseGrid[y + 1][x - 1] == "*":
                    return 0
                if baseGrid[y][x + 1] == "*" and baseGrid[y - 1][x + 1] == "*" and baseGrid[y + 1][x + 1] == "*":
                    return 0
                return index
    if index == 2:
        if 0 < y < baseY - 2:
            if 0 < x < baseX - 2:
                if baseGrid[y - 1][x] == "*" and (baseGrid[y - 1][x - 1] == "*" or baseGrid[y - 1][x + 1] == "*"):
                    return 0
                if baseGrid[y + 1][x] == "*" and (baseGrid[y + 1][x - 1] == "*" or baseGrid[y + 1][x + 1] == "*"):
                    return 0
                if baseGrid[y][x - 1] == "*" and (baseGrid[y - 1][x - 1] == "*" or baseGrid[y + 1][x - 1] == "*"):
                    return 0
                if baseGrid[y][x + 1] == "*" and (baseGrid[y - 1][x + 1] == "*" or baseGrid[y + 1][x + 1] == "*"):
                    return 0
                return index
    return index


def getDrawableArea():
    global maxSize
    drawableArea = {}
    for y in range(baseY):
        for x in range(baseX):
            if baseGrid[y][x] == "#":
                d = 1
                while True:
                    if not inDrawableArea(x, y, d) or not isDrawable(x, y, d):
                        break
                    d += 1
                drawableArea[(x, y)] = DrawableArea(x,y,d,d ** 2)
                isolationIndex[y][x] = getIsolationIndex(x, y)
                maxSize = max(maxSize, d)
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
    found = [(0, 0, 0), 0]
    yMin = y - maxSize if y - maxSize > 0 else 0
    xMin = x - maxSize if x - maxSize > 0 else 0
    for j in range(yMin,y+1,1):
        for i in range(xMin,x+1,1):
            if baseGrid[j][i] !="*" and (i,j) in drawableArea:
                obj = drawableArea[(i, j)]
                elem = (obj.x, obj.y, obj.d)
                if isInArea(x, y, elem):
                    weight = computeWeightArea(*elem)
                    if weight == 0:
                        del drawableArea[(i, j)]
                    elif compareElem([elem, weight], found) < 0:
                        found = [elem, weight]
    if found[1] > 0:
        elem = found[0]
        addToResult(*elem)
        del drawableArea[(elem[0],elem[1])]


def fillGrid(x, y, d):
    for j in range(d):
        for i in range(d):
            if baseGrid[y + j][x + i] == "#":
                baseGrid[y + j][x + i] = "+"
                isolationIndex[y + j][x + i] = 0


def addToResult(x, y, d):
    # print(f'FILL,{x},{y},{d}')
    result.append(f'FILL,{x},{y},{d}')
    return fillGrid(x, y, d)


result = []
baseX = 0
baseY = 0
baseGrid = []
maxSize = 0
isolationIndex = []
drawableArea = []

with open(INPUT_FILE) as f:
    baseX, baseY = map(int, f.readline().strip().split(','))
    for line in f:
        pixels = list(line.strip())
        baseGrid.append(pixels)
        isolationIndex.append([0] * baseX)

# print(f'BaseX: {baseX}, BaseY: {baseY}')
drawableArea = getDrawableArea()

# Fill in the most isolated pixels by heaviest area
for index in range(8, 1, -1):
    if index > 1:
        for y in range(baseY):
            for x in range(baseX):
                if baseGrid[y][x] == "#" and index == int(isolationIndex[y][x]):
                    fillHeaviestArea(x, y)

# Fill in the remaining pixels from the end line
for y in range(baseY - 1, -1, -1):
    for x in range(baseX):
        if baseGrid[y][x] == "#":
            fillHeaviestArea(x, y)

with open(OUTPUT_FILE, 'w') as f:
    f.write('\n'.join(result))
print('Res:', len(result))
