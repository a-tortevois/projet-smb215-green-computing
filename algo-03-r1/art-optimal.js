/*
root@raspberrypi:~/projet-smb215# node algo-03-r1/art-optimal.js
root@raspberrypi:~/projet-smb215# perf stat node algo-03-r1/art-optimal.js
*/

const fs = require('fs');

INPUT_FILE = __dirname + "/input.txt";
OUTPUT_FILE = __dirname + "/solution.txt";

// Hack, in JavaScript, strings are immutable
String.prototype.replaceAt = function (index, replacement) {
    return this.substr(0, index) + replacement + this.substr(index + replacement.length);
}

fs.readFile(INPUT_FILE, 'utf8', (err, data) => {
    if (err) {
        return console.error(`Unable to open the file: ${err}\n`);
    }

    const getArrayIndex = (x, y) => {
        return y * baseX + x;
    }

    const isBetween = (value, min, max) => {
        return value > min && value < max;
    }

    const inDrawableArea = (x, y, d) => {
        return x + d < baseX && y + d < baseY;
    }

    const isDrawable = (x, y, d) => {
        if (baseGrid[y + d][x + d] === "*") {
            return false;
        }
        for (let i = 0; i < d; i++) {
            if (baseGrid[y + i][x + d] === "*" || baseGrid[y + d][x + i] === "*") {
                return false;
            }
        }
        return true;
    }

    const compareElem = (a, b) => {
        if (a[1] === b[1]) {
            if (a[0].d === b[0].d) {
                if (a[0].y === b[0].y) {
                    return a[0].x - b[0].x;
                }
                return a[0].y - b[0].y;
            }
            return b[0].d - a[0].d;
        }
        return b[1] - a[1];
    }

    const getIsolationIndex = (x, y) => {
        let index = 0;
        for (let j = -1; j < 2; j++) {
            const yj = y + j;
            if (yj < 0 || yj > baseY - 1) {
                continue;
            }
            for (let i = -1; i < 2; i++) {
                const xi = x + i;
                if (xi < 0 || xi > baseX - 1) {
                    continue;
                }
                if (baseGrid[yj][xi] === "*") {
                    index++;
                }
            }
        }
        switch (index) {
            case 3: {
                if (isBetween(y, 0, baseY - 2)) {
                    if (isBetween(x, 0, baseX - 2)) {
                        if (baseGrid[y - 1][x] === "*" && baseGrid[y - 1][x - 1] === "*" && baseGrid[y - 1][x + 1] === "*") {
                            return 0;
                        }
                        if (baseGrid[y + 1][x] === "*" && baseGrid[y + 1][x - 1] === "*" && baseGrid[y + 1][x + 1] === "*") {
                            return 0;
                        }
                        if (baseGrid[y][x - 1] === "*" && baseGrid[y - 1][x - 1] === "*" && baseGrid[y + 1][x - 1] === "*") {
                            return 0;
                        }
                        if (baseGrid[y][x + 1] === "*" && baseGrid[y - 1][x + 1] === "*" && baseGrid[y + 1][x + 1] === "*") {
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
                        if (baseGrid[y - 1][x] === "*" && (baseGrid[y - 1][x - 1] === "*" || baseGrid[y - 1][x + 1] === "*")) {
                            return 0;
                        }
                        if (baseGrid[y + 1][x] === "*" && (baseGrid[y + 1][x - 1] === "*" || baseGrid[y + 1][x + 1] === "*")) {
                            return 0;
                        }
                        if (baseGrid[y][x - 1] === "*" && (baseGrid[y - 1][x - 1] === "*" || baseGrid[y + 1][x - 1] === "*")) {
                            return 0;
                        }
                        if (baseGrid[y][x + 1] === "*" && (baseGrid[y - 1][x + 1] === "*" || baseGrid[y + 1][x + 1] === "*")) {
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

    const getDrawableArea = () => {
        const drawableArea = new Array(baseX * baseY);
        for (let y = 0; y < baseY; y++) {
            for (let x = 0; x < baseX; x++) {
                if (baseGrid[y][x] === "#") {
                    let d = 1;
                    while (inDrawableArea(x, y, d) && isDrawable(x, y, d)) {
                        d++;
                    }
                    const yxIndex = getArrayIndex(x, y);
                    drawableArea[yxIndex] = {
                        x: x,
                        y: y,
                        d: d,
                        w: d ** 2
                    }
                    isolationIndex[yxIndex] = getIsolationIndex(x, y);
                    maxSize = Math.max(maxSize, d);
                }
            }
        }
        return drawableArea;
    }

    const isInArea = (x, y, elem) => {
        return isBetween(x, elem.x - 1, elem.x + elem.d) && isBetween(y, elem.y - 1, elem.y + elem.d);
    }

    const computeWeightArea = (elem) => {
        let weight = 0;
        for (let j = 0; j < elem.d; j++) {
            for (let i = 0; i < elem.d; i++) {
                if (baseGrid[elem.y + j][elem.x + i] === "#") {
                    weight++;
                }
            }
        }
        return weight;
    }

    const fillHeaviestArea = (x, y) => {
        let found = [{x: 0, y: 0, d: 0, w: 0}, 0];
        const yMin = (y - maxSize > 0) ? y - maxSize : 0;
        const xMin = (x - maxSize > 0) ? x - maxSize : 0;
        for (let j = yMin; j <= y; j++) {
            for (let i = xMin; i <= x; i++) {
                if (baseGrid[j][i] !== "*") {
                    const elem = drawableArea[getArrayIndex(i, j)];
                    if (elem && isInArea(x, y, elem)) {
                        const weight = computeWeightArea(elem);
                        if (weight === 0) {
                            drawableArea[getArrayIndex(x, y)] = undefined;
                        } else if (compareElem([elem, weight], found) < 0) {
                            found = [elem, weight];
                        }
                    }
                }
            }
        }
        if (found[1] > 0) {
            const elem = found[0];
            addToResult(elem);
            drawableArea[getArrayIndex(elem.x, elem.y)] = undefined;
        }
    }

    const fillGrid = (elem) => {
        for (let j = 0; j < elem.d; j++) {
            for (let i = 0; i < elem.d; i++) {
                if (baseGrid[elem.y + j][elem.x + i] === "#") {
                    baseGrid[elem.y + j] = baseGrid[elem.y + j].replaceAt(elem.x + i, "+");
                    isolationIndex[getArrayIndex(elem.x + i, elem.y + j)] = 0;
                }
            }
        }
    }

    const addToResult = (elem) => {
        // console.log(`FILL,${elem.x},${elem.y},${elem.d}`);
        result.push(`FILL,${elem.x},${elem.y},${elem.d}`);
        fillGrid(elem);
    }

    const result = [];
    data = data.split('\r\n');
    const [baseX, baseY] = data[0].split(',').map(value => parseInt(value));
    const baseGrid = data.slice(1);
    // console.log(`BaseX: ${baseX}, BaseY: ${baseY}`);
    let maxSize = 0;
    const isolationIndex = new Array(baseX * baseY);
    const drawableArea = getDrawableArea();

    // Fill in the most isolated pixels by heaviest area
    for (let index = 8; index > 1; index--) {
        for (let y = 0; y < baseY; y++) {
            for (let x = 0; x < baseX; x++) {
                if (index === isolationIndex[getArrayIndex(x, y)] && baseGrid[y][x] === "#") {
                    fillHeaviestArea(x, y);
                }
            }
        }
    }

    // Fill in the remaining pixels from the end line
    for (let y = baseY - 1; y > -1; y--) {
        for (let x = 0; x < baseX; x++) {
            if (baseGrid[y][x] === "#") {
                fillHeaviestArea(x, y);
            }
        }
    }

    // Write the output
    fs.writeFile(OUTPUT_FILE, result.join('\n'), {flag: 'w+'}, (err) => {
        if (err) {
            return console.error(`Unable to write the file: ${err}\n`);
        }
        console.log(`Res: ${result.length}`);
    });
});
