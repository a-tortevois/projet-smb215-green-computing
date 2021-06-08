'''
root@raspberrypi:~/projet-smb215# python3 algo-03/art-optimal.py
root@raspberrypi:~/projet-smb215# perf stat python3 algo-03/art-optimal.py
'''

import os


DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = DIR + "/input.txt"
OUTPUT_FILE = DIR + "/solution.txt"


class DrawableElem:
    def __init__(self, x, y, d, w, i, prev=None, next=None):
        self.x = x
        self.y = y
        self.d = d
        self.w = w
        self.i = i
        self.prev = prev
        self.next = next


def getArrayIndex(x, y):
    return y * baseX + x


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
    if a.w == b.w:
        if a.d == b.d:
            if a.y == b.y:
                return a.x - b.x
            return a.y - b.y
        return b.d - a.d
    return b.w - a.w


def removeElem(elem):
    prev = elem.prev
    if prev is not None:
        prev.next = elem.next
        if elem.next is not None:
            elem.next.prev = prev
    else:
        drawableArea = elem.next
        drawableArea.prev = None
    return prev


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
    head = None
    prev = None
    for y in range(baseY):
        for x in range(baseX):
            if baseGrid[y][x] == "#":
                d = 1
                while True:
                    if not inDrawableArea(x, y, d) or not isDrawable(x, y, d):
                        break
                    d += 1
                elem = DrawableElem(x, y, d, d ** 2, getIsolationIndex(x, y), prev)
                if prev is None:
                    head = elem
                else:
                    prev.next = elem
                prev = elem
    return head


def isInArea(x, y, elem):
    return elem.x <= x < elem.x + elem.d and elem.y <= y < elem.y + elem.d


def computeWeightArea(x, y, d):
    weight = 0
    for j in range(d):
        for i in range(d):
            if baseGrid[y + j][x + i] == "#":
                weight += 1
    return weight


def fillHeaviestArea(x, y):
    found = None
    elem = drawableArea
    while elem.next is not None:
        if isInArea(x, y, elem):
            elem.w = computeWeightArea(elem.x, elem.y, elem.d)
            if elem.w == 0:
                removeElem(elem)
            else:
                if found is None:
                    found = elem
                elif compareElem(elem, found) < 0:
                    found = elem
        elem = elem.next
    if found is not None and found.w > 0:
        addToResult(found.x, found.y, found.d)
        return removeElem(found)
    return None


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
baseGrid = []
drawableArea = None

with open(INPUT_FILE) as f:
    baseX, baseY = map(int, f.readline().strip().split(','))
    for line in f:
        pixels = list(line.strip())
        baseGrid.append(pixels)
        # isolationIndex.append([0] * baseX)

# print(f'BaseX: {baseX}, BaseY: {baseY}')
drawableArea = getDrawableArea()

# Fill in the most isolated pixels by heaviest area
for index in range(8, 1, -1):
    elem = drawableArea
    while elem.next is not None:
        if baseGrid[elem.y][elem.x] == "#" and index == elem.i:
            elem = fillHeaviestArea(elem.x, elem.y)
        if elem is not None and elem.next is not None:
            elem = elem.next
        else:
            elem = drawableArea

# Fill in the remaining pixels from the end line
for y in range(baseY - 1, -1, -1):
    for x in range(baseX):
        if baseGrid[y][x] == "#":
            fillHeaviestArea(x, y)

with open(OUTPUT_FILE, 'w') as f:
    f.write('\n'.join(result))
print('Res:', len(result))
