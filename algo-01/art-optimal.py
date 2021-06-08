'''
root@raspberrypi:~/projet-smb215# python3 algo-01/art-optimal.py
root@raspberrypi:~/projet-smb215# perf stat python3 algo-01/art-optimal.py
'''

import os
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = DIR + "/input.txt"
OUTPUT_FILE = DIR + "/solution.txt"

with open(INPUT_FILE) as f:
    baseX, baseY = map(int, f.readline().strip().split(','))
    baseGrid = []
    for line in f:
        baseGrid.append(line.strip())
#print(f'BaseX: {baseX}, BaseY: {baseY}')
result = []
for y in range(baseY):
    for x in range(baseX):
        if baseGrid[y][x] == "#":
            result.append(f'FILL,{x},{y},1')
with open(OUTPUT_FILE, 'w') as f:
    f.write('\n'.join(result))
print('Res:', len(result))