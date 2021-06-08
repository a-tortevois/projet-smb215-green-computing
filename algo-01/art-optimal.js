/*
root@raspberrypi:~/projet-smb215# node algo-01/art-optimal.js
root@raspberrypi:~/projet-smb215# perf stat node algo-01/art-optimal.js
*/

const fs = require('fs');

INPUT_FILE = __dirname + "/input.txt";
OUTPUT_FILE = __dirname + "/solution.txt";

fs.readFile(INPUT_FILE, 'utf8', (err, data) => {
    if (err) {
        return console.error(`Unable to open the file: ${err}\n`);
    }

    data = data.split('\r\n');
    const [baseX, baseY] = data[0].split(',').map(value => parseInt(value));

    // console.log(`BaseX: ${baseX}, BaseY: ${baseY}`);

    let result = [];
    const baseGrid = data.slice(1);
    for (let y = 0; y < baseY; y++) {
        for (let x = 0; x < baseX; x++) {
            if (baseGrid[y][x] === "#") {
                result.push(`FILL,${x},${y},1`);
            }
        }
    }

    fs.writeFile(OUTPUT_FILE, result.join('\n'), {flag: 'w+'}, (err) => {
        if (err) {
            return console.error(`Unable to write the file: ${err}\n`);
        }
        console.log(`Res: ${result.length}`);
    });
});