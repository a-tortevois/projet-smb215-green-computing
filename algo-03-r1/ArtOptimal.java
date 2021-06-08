/*
root@raspberrypi:~/projet-smb215# javac algo-03-r1/art-optimal.java
root@raspberrypi:~/projet-smb215# java -cp algo-03-r1 ArtOptimal
*/

import java.io.*;

class ArtOptimal {
    private static final String DIR = "algo-03-r1";
    private static final String INPUT_FILE = DIR + "/input.txt";
    private static final String OUTPUT_FILE = DIR + "/solution.txt";

    private static String[] baseGrid;
    private static int baseX, baseY;
    private static final StringBuilder result = new StringBuilder();
    private static int res = 0;
    private static int maxSize = 0;
    private static int[] isolationIndex;
    private static DrawableArea[] drawableArea;

    public static void main(String[] args) {
        readInputFile();
        // System.out.println("BaseX: " + baseX + ", BaseY: " + baseY);
        drawableArea = getDrawableArea();

        // Fill in the most isolated pixels by heaviest area
        for (int index = 8; index > 1; index--) {
            for (int y = 0; y < baseY; y++) {
                for (int x = 0; x < baseX; x++) {
                    if (getBaseGridCharAt(x, y) == '#' && index == isolationIndex[getArrayIndex(x, y)]) {
                        fillHeaviestArea(x, y);
                    }
                }
            }
        }

        // Fill in the remaining pixels from the end line
        for (int y = baseY - 1; y > -1; y--) {
            for (int x = 0; x < baseX; x++) {
                if (getBaseGridCharAt(x, y) == '#') {
                    fillHeaviestArea(x, y);

                }
            }
        }

        writeOutputFile();
        System.out.println("Res: " + res);
    }

    private static void readInputFile() {
        try {
            BufferedReader file = new BufferedReader(new FileReader(INPUT_FILE));
            String line = file.readLine();
            String[] data = line.split(",");
            baseX = Integer.parseInt(data[0]);
            baseY = Integer.parseInt(data[1]);
            baseGrid = new String[baseX * baseY];
            isolationIndex = new int[baseX * baseY];
            int i = 0;
            while ((line = file.readLine()) != null) {
                baseGrid[i] = line.trim();
                i += baseX;
            }
            file.close();
        } catch (FileNotFoundException e) {
            System.out.println("Unable to open the file " + INPUT_FILE + ": " + e.getMessage());
            e.printStackTrace();
        } catch (IOException e) {
            System.out.println("Unable to read the file " + INPUT_FILE + ": " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static char getBaseGridCharAt(int x, int y) {
        return baseGrid[y * baseX].charAt(x);
    }

    private static int getArrayIndex(int x, int y) {
        return y * baseX + x;
    }

    private static boolean isBetween(int value, int min, int max) {
        return value > min && value < max;
    }

    private static boolean inDrawableArea(int x, int y, int d) {
        return x + d < baseX && y + d < baseY;
    }

    private static boolean isDrawable(int x, int y, int d) {
        if (getBaseGridCharAt(x + d, y + d) == '*') {
            return false;
        }
        for (int i = 0; i < d; i++) {
            if (getBaseGridCharAt(x + d, y + i) == '*' || getBaseGridCharAt(x + i, y + d) == '*') {
                return false;
            }
        }
        return true;
    }

    private static int compareElem(DrawableArea a, int wa, DrawableArea b, int wb) {
        if (wa == wb) {
            if (a.d == b.d) {
                if (a.y == b.y) {
                    return a.x - b.x;
                }
                return a.y - b.y;
            }
            return b.d - a.d;
        }
        return wb - wa;
    }

    private static int getIsolationIndex(int x, int y) {
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
                if (getBaseGridCharAt(xi, yj) == '*') {
                    index++;
                }
            }
        }
        switch (index) {
            case 3: {
                if (isBetween(y, 0, baseY - 2)) {
                    if (isBetween(x, 0, baseX - 2)) {
                        if (getBaseGridCharAt(x, y - 1) == '*' && getBaseGridCharAt(x - 1, y - 1) == '*' && getBaseGridCharAt(x + 1, y - 1) == '*') {
                            return 0;
                        }
                        if (getBaseGridCharAt(x, y + 1) == '*' && getBaseGridCharAt(x - 1, y + 1) == '*' && getBaseGridCharAt(x + 1, y + 1) == '*') {
                            return 0;
                        }
                        if (getBaseGridCharAt(x - 1, y) == '*' && getBaseGridCharAt(x - 1, y - 1) == '*' && getBaseGridCharAt(x - 1, y + 1) == '*') {
                            return 0;
                        }
                        if (getBaseGridCharAt(x + 1, y) == '*' && getBaseGridCharAt(x + 1, y - 1) == '*' && getBaseGridCharAt(x + 1, y + 1) == '*') {
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
                        if (getBaseGridCharAt(x, y - 1) == '*' && (getBaseGridCharAt(x - 1, y - 1) == '*' || getBaseGridCharAt(x + 1, y - 1) == '*')) {
                            return 0;
                        }
                        if (getBaseGridCharAt(x, y + 1) == '*' && (getBaseGridCharAt(x - 1, y + 1) == '*' || getBaseGridCharAt(x + 1, y + 1) == '*')) {
                            return 0;
                        }
                        if (getBaseGridCharAt(x - 1, y) == '*' && (getBaseGridCharAt(x - 1, y - 1) == '*' || getBaseGridCharAt(x - 1, y + 1) == '*')) {
                            return 0;
                        }
                        if (getBaseGridCharAt(x + 1, y) == '*' && (getBaseGridCharAt(x + 1, y - 1) == '*' || getBaseGridCharAt(x + 1, y + 1) == '*')) {
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

    private static DrawableArea[] getDrawableArea() {
        DrawableArea[] drawableArea = new DrawableArea[baseX * baseY];
        for (int y = 0; y < baseY; y++) {
            for (int x = 0; x < baseX; x++) {
                if (getBaseGridCharAt(x, y) == '#') {
                    int d = 1;
                    while (inDrawableArea(x, y, d) && isDrawable(x, y, d)) {
                        d++;
                    }
                    int yxIndex = getArrayIndex(x, y);
                    drawableArea[yxIndex] = new DrawableArea(x, y, d, d ^ 2);
                    isolationIndex[yxIndex] = getIsolationIndex(x, y);
                    maxSize = Math.max(maxSize, d);
                }
            }
        }
        return drawableArea;
    }

    private static boolean isInArea(int x, int y, DrawableArea elem) {
        return isBetween(x, elem.x - 1, elem.x + elem.d) && isBetween(y, elem.y - 1, elem.y + elem.d);
    }

    private static int computeWeightArea(DrawableArea elem) {
        int weight = 0;
        for (int j = 0; j < elem.d; j++) {
            for (int i = 0; i < elem.d; i++) {
                if (getBaseGridCharAt(elem.x + i, elem.y + j) == '#') {
                    weight++;
                }
            }
        }
        return weight;
    }

    private static void fillHeaviestArea(int x, int y) {
        DrawableArea foundDrawableArea = new DrawableArea(0, 0, 0, 0);
        int foundWeight = 0;
        int yMin = (y - maxSize > 0) ? y - maxSize : 0;
        int xMin = (x - maxSize > 0) ? x - maxSize : 0;
        for (int j = yMin; j <= y; j++) {
            for (int i = xMin; i <= x; i++) {
                if (getBaseGridCharAt(i, j) != '*') {
                    int yxIndex = getArrayIndex(x, y);
                    DrawableArea elem = drawableArea[yxIndex];
                    if (elem != null && isInArea(x, y, elem)) {
                        int weight = computeWeightArea(elem);
                        if (weight == 0) {
                            drawableArea[getArrayIndex(x, y)] = null;
                        } else if (compareElem(elem, weight, foundDrawableArea, foundWeight) < 0) {
                            foundDrawableArea = elem;
                            foundWeight = weight;
                        }
                    }
                }
            }
        }
        if (foundWeight > 0) {
            addToResult(foundDrawableArea);
        }
    }

    private static String replaceAt(int pos, String s, char c) {
        return s.substring(0, pos) + c + s.substring(pos + 1);
    }

    private static void fillGrid(DrawableArea elem) {
        for (int j = 0; j < elem.d; j++) {
            for (int i = 0; i < elem.d; i++) {
                if (getBaseGridCharAt(elem.x + i, elem.y + j) == '#') {
                    int p = (elem.y + j) * baseX;
                    baseGrid[p] = replaceAt(elem.x + i, baseGrid[p], '+');
                    isolationIndex[getArrayIndex(elem.x + i, elem.y + j)] = 0;
                }
            }
        }
    }

    private static void addToResult(DrawableArea elem) {
        // System.out.println("FILL," + elem.x + "," + elem.y + "," + elem.d +"\n");
        result.append("FILL," + elem.x + "," + elem.y + "," + elem.d + "\n");
        fillGrid(elem);
        res++;
    }

    private static void writeOutputFile() {
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(OUTPUT_FILE));
            writer.write(result.toString());
            writer.close();
        } catch (FileNotFoundException e) {
            System.out.println("Unable to open the file " + OUTPUT_FILE + ": " + e.getMessage());
            e.printStackTrace();
        } catch (IOException e) {
            System.out.println("Unable to write the file " + OUTPUT_FILE + ": " + e.getMessage());
            e.printStackTrace();
        }
    }
}