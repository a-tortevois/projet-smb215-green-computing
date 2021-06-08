<?php
/*
root@raspberrypi:~/projet-smb215# php -f algo-02/art-optimal.php
root@raspberrypi:~/projet-smb215# perf stat php -f algo-02/art-optimal.php
*/

define("INPUT_FILE", __DIR__ . "/input.txt");
define("OUTPUT_FILE", __DIR__ . "/solution.txt");


class DrawableArea {
    public $x;
    public $y;
    public $d;
    public $w;

    function __construct($x, $y, $d, $w) {
        $this->x = $x;
        $this->y = $y;
        $this->d = $d;
        $this->w = $w;
    }
}

function getArrayIndex($x, $y) {
    global $baseX;
    return $y * $baseX + $x;
}

function isBetween($value, $min, $max) {
    return $value > $min && $value < $max;
}

function inDrawableArea($x, $y, $d) {
    global $baseX, $baseY;
    return $x + $d < $baseX && $y + $d < $baseY;
}


function isDrawable($x, $y, $d) {
    global $baseGrid;
    if( $baseGrid[$y + $d][$x + $d] === "*" ) {
        return false;
    }
    for( $i = 0; $i < $d; $i++ ) {
        if( $baseGrid[$y + $i][$x + $d] === "*" || $baseGrid[$y + $d][$x + $i] === "*" ) {
            return false;
        }
    }
    return true;
}

function sortByValueReversed($a, $b) {
    if( $a[1] === $b[1] ) {
        if( $a[0]->d === $b[0]->d ) {
            if( $a[0]->y === $b[0]->y ) {
                return ($a[0]->x < $b[0]->x) ? -1 : 1;
            }
            return ($a[0]->y < $b[0]->y) ? -1 : 1;
        }
        return ($b[0]->d < $a[0]->d) ? -1 : 1;
    }
    return ($b[1] < $a[1]) ? -1 : 1;
}

function getDrawableArea() {
    global $baseX, $baseY, $baseGrid, $isolationIndex, $indexValues;
    $drawableArea = [];
    for( $y = 0; $y < $baseY; $y++ ) {
        for( $x = 0; $x < $baseX; $x++ ) {
            if( $baseGrid[$y][$x] === "#" ) {
                $d = 1;
                while( inDrawableArea($x, $y, $d) && isDrawable($x, $y, $d) ) {
                    $d++;
                }
                $yxIndex = getArrayIndex($x, $y);
                $drawableArea[$yxIndex] = new DrawableArea($x, $y, $d, $d ** 2);
            }
        }
    }
    return $drawableArea;
}

function isInArea($x, $y, $elem) {
    return isBetween($x, $elem->x - 1, $elem->x + $elem->d) && isBetween($y, $elem->y - 1, $elem->y + $elem->d);
}

function computeWeightArea($elem) {
    global $baseGrid;
    $weight = 0;
    for( $j = 0; $j < $elem->d; $j++ ) {
        for( $i = 0; $i < $elem->d; $i++ ) {
            if( $baseGrid[$elem->y + $j][$elem->x + $i] === "#" ) {
                $weight++;
            }
        }
    }
    return $weight;
}

function fillHeaviestArea($x, $y) {
    global $drawableArea;
    $found = [];
    foreach( $drawableArea as $elem ) {
        if( isInArea($x, $y, $elem) ) {
            $weight = computeWeightArea($elem);
            if( $weight === 0 ) {
                unset($drawableArea[getArrayIndex($x, $y)]);
            } else {
                $found[] = [$elem, $weight];
            }
        }
    }
    if( count($found) > 0 ) {
        usort($found, 'sortByValueReversed');
        $elem = $found[0][0];
        addToResult($elem);
        unset($drawableArea[getArrayIndex($elem->x, $elem->y)]);
    }
}

function fillGrid($elem) {
    global $baseGrid;
    for( $j = 0; $j < $elem->d;
         $j++ ) {
        for( $i = 0; $i < $elem->d;
             $i++ ) {
            if( $baseGrid[$elem->y + $j][$elem->x + $i] === "#" ) {
                $baseGrid[$elem->y + $j][$elem->x + $i] = "+";
            }
        }
    }
}

function addToResult($elem) {
    global $result;
    // printf("FILL,%d,%d,%d\n", $elem->x, $elem->y, $elem->d);
    $result[] = 'FILL,' . $elem->x . ',' . $elem->y . ',' . $elem->d;
    fillGrid($elem);
}

$fpIn = fopen(INPUT_FILE, "r");
if( !$fpIn ) {
    printf("Unable to open the file %s\n", INPUT_FILE);
    exit;
}

if( ($buffer = fgets($fpIn, 4096)) === false ) {
    printf("Unable to get the first line\n");
    exit;
}

$result = [];
$base = explode(",", $buffer);
$baseX = intval(trim($base[0]));
$baseY = intval(trim($base[1]));
// printf("baseX: %s baseY: %s\n", $baseX, $baseY);
$baseGrid = [];
while( ($buffer = fgets($fpIn, 4096)) !== false ) {
    $baseGrid[] .= trim($buffer);
}
if( !feof($fpIn) ) {
    printf("Error: unexpected fgets() fail\n");
}
fclose($fpIn);

$drawableArea = getDrawableArea();

// Fill in with the heaviest area
for( $y = 0; $y < $baseY; $y++ ) {
    for( $x = 0; $x < $baseX; $x++ ) {
        if( $baseGrid[$y][$x] === "#" ) {
            fillHeaviestArea($x, $y);
        }
    }
}

$fpOut = fopen(OUTPUT_FILE, "w");
if( !$fpOut ) {
    printf("Unable to open the file %s\n", OUTPUT_FILE);
    exit;
}
fwrite($fpOut, implode("\n", $result));
fclose($fpOut);

printf("Res: %s\n", count($result));
?>