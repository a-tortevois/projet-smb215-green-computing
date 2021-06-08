# Algo

For the first algorithm, we put the input image file in memory, then we check one by one pixel and add a line to the output file if the pixel is '#', which symbolizes a painted pixel. The result
should be 84784 output lines.

# C

```
root@raspberrypi:~/projet-smb215# perf stat -d -- taskset -c 0 ./algo-01/art-optimal.o
Res: 84784

 Performance counter stats for 'taskset -c 0 ./algo-01/art-optimal.o':

        109.843648      task-clock (msec)         #    0.954 CPUs utilized
                 5      context-switches          #    0.046 K/sec
                 0      cpu-migrations            #    0.000 K/sec
               211      page-faults               #    0.002 M/sec
         153455923      cycles                    #    1.397 GHz                      (81.82%)
         134223889      instructions              #    0.87  insn per cycle           (84.76%)
          15214998      branches                  #  138.515 M/sec                    (90.90%)
            887946      branch-misses             #    5.84% of all branches          (90.90%)
          55757711      L1-dcache-loads           #  507.610 M/sec                    (90.89%)
             65561      L1-dcache-load-misses     #    0.12% of all L1-dcache hits    (90.90%)
            595133      LLC-loads                 #    5.418 M/sec                    (90.90%)
             21010      LLC-load-misses           #    3.53% of all LL-cache hits     (60.75%)

       0.115118041 seconds time elapsed
```

```
root@raspberrypi:~/projet-smb215# /usr/bin/time -v taskset -c 0 ./algo-01/art-optimal.o
Res: 84784

        Command being timed: "taskset -c 0 ./algo-01/art-optimal.o"
        User time (seconds): 0.13
        System time (seconds): 0.02
        Percent of CPU this job got: 98%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.15
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 1392
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 243
        Voluntary context switches: 2
        Involuntary context switches: 8
        Swaps: 0
        File system inputs: 0
        File system outputs: 2424
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

# Python3

```
root@raspberrypi:~/projet-smb215# perf stat -d -- taskset -c 0 python3 algo-01/art-optimal.py
stdout: Res: 84784

 Performance counter stats for 'taskset -c 0 python3 algo-01/art-optimal.py':

        861.370315      task-clock (msec)         #    0.998 CPUs utilized
                 8      context-switches          #    0.009 K/sec
                 0      cpu-migrations            #    0.000 K/sec
              2330      page-faults               #    0.003 M/sec
        1203754542      cycles                    #    1.397 GHz                      (87.23%)
         848161393      instructions              #    0.70  insn per cycle           (87.23%)
          54504859      branches                  #   63.277 M/sec                    (87.23%)
           9708286      branch-misses             #   17.81% of all branches          (87.27%)
         378386371      L1-dcache-loads           #  439.284 M/sec                    (87.23%)
            872218      L1-dcache-load-misses     #    0.23% of all L1-dcache hits    (87.92%)
           7463801      LLC-loads                 #    8.665 M/sec                    (88.39%)
            702096      LLC-load-misses           #    9.41% of all LL-cache hits     (74.73%)

       0.863516578 seconds time elapsed
```

```
root@raspberrypi:~/projet-smb215# /usr/bin/time -v taskset -c 0 python3 algo-01/art-optimal.py
Res: 84784

        Command being timed: "taskset -c 0 python3 algo-01/art-optimal.py"
        User time (seconds): 0.85
        System time (seconds): 0.05
        Percent of CPU this job got: 99%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.90
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 13028
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 2361
        Voluntary context switches: 1
        Involuntary context switches: 10
        Swaps: 0
        File system inputs: 0
        File system outputs: 2424
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

# Javascript

```
root@raspberrypi:~/projet-smb215# perf stat -d -- taskset -c 0 node algo-01/art-optimal.js
Res: 84784

 Performance counter stats for 'taskset -c 0 node algo-01/art-optimal.js':

        664.456825      task-clock (msec)         #    0.987 CPUs utilized
               234      context-switches          #    0.352 K/sec
                 0      cpu-migrations            #    0.000 K/sec
              4912      page-faults               #    0.007 M/sec
         909386695      cycles                    #    1.369 GHz                      (87.96%)
         573348930      instructions              #    0.63  insn per cycle           (85.77%)
          67293322      branches                  #  101.276 M/sec                    (86.66%)
           6203569      branch-misses             #    9.22% of all branches          (87.96%)
         243934629      L1-dcache-loads           #  367.119 M/sec                    (87.50%)
           1848265      L1-dcache-load-misses     #    0.76% of all L1-dcache hits    (88.00%)
          13679296      LLC-loads                 #   20.587 M/sec                    (87.96%)
           1899006      LLC-load-misses           #   13.88% of all LL-cache hits     (76.16%)

       0.673049147 seconds time elapsed
```

```
root@raspberrypi:~/projet-smb215# /usr/bin/time -v taskset -c 0 node algo-01/art-optimal.js
Res: 84784

        Command being timed: "taskset -c 0 node algo-01/art-optimal.js"
        User time (seconds): 0.58
        System time (seconds): 0.11
        Percent of CPU this job got: 99%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.69
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 40712
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 4941
        Voluntary context switches: 120
        Involuntary context switches: 112
        Swaps: 0
        File system inputs: 0
        File system outputs: 2424
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

# PHP

```
root@raspberrypi:~/projet-smb215# perf stat -d -- taskset -c 0 php -f algo-01/art-optimal.php
Res: 84784

 Performance counter stats for 'taskset -c 0 php -f algo-01/art-optimal.php':

        383.618908      task-clock (msec)         #    0.986 CPUs utilized
                 6      context-switches          #    0.016 K/sec
                 0      cpu-migrations            #    0.000 K/sec
              3036      page-faults               #    0.008 M/sec
         515793022      cycles                    #    1.345 GHz                      (86.97%)
         361556459      instructions              #    0.70  insn per cycle           (86.96%)
          44931997      branches                  #  117.127 M/sec                    (87.67%)
           2302025      branch-misses             #    5.12% of all branches          (86.99%)
         178599414      L1-dcache-loads           #  465.565 M/sec                    (86.97%)
            558021      L1-dcache-load-misses     #    0.31% of all L1-dcache hits    (87.01%)
           3915688      LLC-loads                 #   10.207 M/sec                    (89.52%)
            512344      LLC-load-misses           #   13.08% of all LL-cache hits     (74.87%)

       0.388871020 seconds time elapsed
```

```
root@raspberrypi:~/projet-smb215# /usr/bin/time -v taskset -c 0 php -f algo-01/art-optimal.php
Res: 84784

        Command being timed: "taskset -c 0 php -f algo-01/art-optimal.php"
        User time (seconds): 0.35
        System time (seconds): 0.03
        Percent of CPU this job got: 98%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.40
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 19352
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 3064
        Voluntary context switches: 2
        Involuntary context switches: 8
        Swaps: 0
        File system inputs: 0
        File system outputs: 2424
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

# Java

```
root@raspberrypi:~/projet-smb215# perf stat -d -- taskset -c 0 java -cp algo-01 ArtOptimal
Res: 84784

 Performance counter stats for 'taskset -c 0 java -cp algo-01 ArtOptimal':

       1719.820318      task-clock (msec)         #    0.994 CPUs utilized
               282      context-switches          #    0.164 K/sec
                 0      cpu-migrations            #    0.000 K/sec
              5998      page-faults               #    0.003 M/sec
        2398540585      cycles                    #    1.395 GHz                      (87.12%)
        1201778062      instructions              #    0.50  insn per cycle           (86.84%)
         137265053      branches                  #   79.814 M/sec                    (87.22%)
          38269480      branch-misses             #   27.88% of all branches          (87.14%)
         589751347      L1-dcache-loads           #  342.915 M/sec                    (88.35%)
          11973964      L1-dcache-load-misses     #    2.03% of all L1-dcache hits    (87.75%)
          48020658      LLC-loads                 #   27.922 M/sec                    (88.24%)
           3727628      LLC-load-misses           #    7.76% of all LL-cache hits     (74.46%)

       1.730577934 seconds time elapsed
```

```
root@raspberrypi:~/projet-smb215# /usr/bin/time -v taskset -c 0 java -cp algo-01 ArtOptimal
Res: 84784

        Command being timed: "taskset -c 0 java -cp algo-01 ArtOptimal"
        User time (seconds): 1.61
        System time (seconds): 0.08
        Percent of CPU this job got: 98%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:01.72
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 35076
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 8
        Minor (reclaiming a frame) page faults: 5980
        Voluntary context switches: 115
        Involuntary context switches: 168
        Swaps: 0
        File system inputs: 0
        File system outputs: 2488
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```