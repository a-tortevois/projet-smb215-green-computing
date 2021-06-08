const canvas = document.querySelector("canvas");
const context = canvas.getContext("2d");
let instructions = [];
let interval = null;
let i = 0;

function draw(x, y, d, color = "black") {
    context.fillStyle = color;
    context.fillRect(x * 2, y * 2, d * 2, d * 2);
}

function drawBackground() {
    for (let i in instructions) {
        const a = instructions[i].split(',');
        draw(a[1], a[2], a[3], "grey");
    }
}

function loadFile(file) {
    const reader = new FileReader();
    reader.onload = () => {
        instructions = reader.result.split('\n').reverse();
        console.log(instructions);
        drawBackground();
    };
    reader.readAsText(file);
}

function reverse() {
    instructions = instructions.reverse();
}

function fillInBlack(i) {
    for (let j = 0; j < i; j++) {
        const a = instructions[j].split(',');
        draw(a[1], a[2], a[3], "black");
    }
}

function drawStart() {
    if (!interval) {
        interval = setInterval(drawNext, 250);
    }
}

function drawPause() {
    if (interval) {
        clearInterval(interval);
        interval = null;
    }
}

function drawPrevious() {
    drawBackground();
    if (i > 0)
        i--;
    fillInBlack(i);
    const a = instructions[i].split(',');
    draw(a[1], a[2], a[3], "rgba(255, 0, 0, 0.5)");
}

function drawNext() {
    if (i > (instructions.length - 1)) {
        drawPause();
        return;
    }
    fillInBlack(i);
    const a = instructions[i].split(',');
    console.log('draw :', i, a[1], a[2], a[3]);
    draw(a[1], a[2], a[3], "rgba(255, 0, 0, 0.5)");
    i++;

}

function goToIndex(index, color) {
    for (let j = i; j < index; j++) {
        const a = instructions[j].split(',');
        draw(a[1], a[2], a[3], color);
    }
    i = index;
}