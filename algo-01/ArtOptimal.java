/*
root@raspberrypi:~/projet-smb215# javac algo-01/art-optimal.java
root@raspberrypi:~/projet-smb215# java -cp algo-01 ArtOptimal
*/

import java.io.*;


class ArtOptimal {
    private static String DIR = "algo-01";
    private static String INPUT_FILE = DIR + "/input.txt";
    private static String OUTPUT_FILE = DIR + "/solution.txt";

    private static String baseGrid[];
    private static int baseX, baseY;

    public static void main(String[] args) {
        readInputFile();
        // System.out.println("BaseX: " + baseX + ", BaseY: " + baseY);
        int i = 0, res = 0;
        StringBuilder stringBuilder = new StringBuilder();
        for (int y = 0; y < baseY; y++) {
            for (int x = 0; x < baseX; x++) {
                if (baseGrid[i].charAt(x) == '#') {
                    stringBuilder.append("FILL," + x + "," + y + ",1\n");
                    res++;
                }
            }
            i += baseX;
        }
        writeOutputFile(stringBuilder.toString());
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

    private static void writeOutputFile(String str) {
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(OUTPUT_FILE));
            writer.write(str);
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