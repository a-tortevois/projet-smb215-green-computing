<?php
/*
root@raspberrypi:~/projet-smb215# php -f algo-01/art-optimal.php
root@raspberrypi:~/projet-smb215# perf stat php -f algo-01/art-optimal.php
*/

define("INPUT_FILE", __DIR__ . "/input.txt");
define("OUTPUT_FILE", __DIR__ . "/solution.txt");

$fpIn = fopen(INPUT_FILE, "r");
if (!$fpIn) {
    printf("Unable to open the file %s\n", INPUT_FILE);
    exit;
}

if (($buffer = fgets($fpIn, 4096)) === false) {
    printf("Unable to get the first line\n");
    exit;
}
$base = explode(",", $buffer);
$baseX = intval(trim($base[0]));
$baseY = intval(trim($base[1]));
// printf("baseX: %s baseY: %s\n", $baseX, $baseY);
$baseGrid = [];
while (($buffer = fgets($fpIn, 4096)) !== false) {
    $baseGrid[] .= trim($buffer);
}
if (!feof($fpIn)) {
    printf("Error: unexpected fgets() fail\n");
}
fclose($fpIn);

$result = [];
for ($y = 0; $y < $baseY; $y++) {
    for ($x = 0; $x < $baseX; $x++) {
        if ($baseGrid[$y][$x] === "#") {
            $result[] .= "FILL," . $x . "," . $y . ",1";
        }
    }
}

$fpOut = fopen(OUTPUT_FILE, "w");
if (!$fpOut) {
    printf("Unable to open the file %s\n", OUTPUT_FILE);
    exit;
}
fwrite($fpOut, implode("\n", $result));
fclose($fpOut);

printf("Res: %s\n", count($result));
?>