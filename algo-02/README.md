# Algo

Here we pre-compute each pixel to get the maximum square area available from this pixel.
We fill in next the heaviest area from each drawable pixel.
Result is 3146 output instructions to draw the picture.

# C

```
root@raspberrypi:~/projet-smb215# perf stat -d -- taskset -c 0 ./algo-02/art-optimal.o
Res: 3146

 Performance counter stats for 'taskset -c 0 ./algo-02/art-optimal.o':

      16012.611194      task-clock (msec)         #    0.999 CPUs utilized
                88      context-switches          #    0.005 K/sec
                 0      cpu-migrations            #    0.000 K/sec
               878      page-faults               #    0.055 K/sec
    22,348,340,281      cycles                    #    1.396 GHz                      (87.46%)
    20,241,028,251      instructions              #    0.91  insn per cycle           (87.51%)
     2,446,686,210      branches                  #  152.797 M/sec                    (87.51%)
         7,442,185      branch-misses             #    0.30% of all branches          (87.52%)
     9,562,605,232      L1-dcache-loads           #  597.192 M/sec                    (87.51%)
         4,767,171      L1-dcache-load-misses     #    0.05% of all L1-dcache hits    (87.52%)
       272,477,606      LLC-loads                 #   17.016 M/sec                    (87.51%)
       134,588,402      LLC-load-misses           #   49.39% of all LL-cache hits     (74.91%)

      16.028550571 seconds time elapsed
```

```
root@raspberrypi:~/projet-smb215# /usr/bin/time -v taskset -c 0 ./algo-02/art-optimal.o
Res: 3146
        Command being timed: "taskset -c 0 ./algo-02/art-optimal.o"
        User time (seconds): 15.98
        System time (seconds): 0.00
        Percent of CPU this job got: 99%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:16.00
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 4024
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 909
        Voluntary context switches: 1
        Involuntary context switches: 65
        Swaps: 0
        File system inputs: 0
        File system outputs: 96
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

# Python3

```
root@raspberrypi:~/projet-smb215# perf stat -d -- taskset -c 0 python3 algo-02/art-optimal.py
Res: 3146

 Performance counter stats for 'taskset -c 0 python3 algo-02/art-optimal.py':

     469213.780749      task-clock (msec)         #    1.000 CPUs utilized
             1,382      context-switches          #    0.003 K/sec
                 0      cpu-migrations            #    0.000 K/sec
             4,530      page-faults               #    0.010 K/sec
   655,747,093,993      cycles                    #    1.398 GHz                      (87.50%)
   445,776,871,580      instructions              #    0.68  insn per cycle           (87.50%)
    22,585,690,108      branches                  #   48.135 M/sec                    (87.50%)
     7,608,223,389      branch-misses             #   33.69% of all branches          (87.50%)
   226,522,149,079      L1-dcache-loads           #  482.770 M/sec                    (87.50%)
       266,185,873      L1-dcache-load-misses     #    0.12% of all L1-dcache hits    (87.50%)
     2,027,918,351      LLC-loads                 #    4.322 M/sec                    (87.50%)
       631,629,997      LLC-load-misses           #   31.15% of all LL-cache hits     (75.00%)

     469.331920186 seconds time elapsed
```

```
root@raspberrypi:~/projet-smb215# /usr/bin/time -v taskset -c 0 python3 algo-02/art-optimal.py
Res: 3146
        Command being timed: "taskset -c 0 python3 algo-02/art-optimal-origin.py"
        User time (seconds): 465.50
        System time (seconds): 0.60
        Percent of CPU this job got: 99%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 7:46.20
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 15224
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 4561
        Voluntary context switches: 1
        Involuntary context switches: 1277
        Swaps: 0
        File system inputs: 0
        File system outputs: 96
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

# Javascript

```
root@raspberrypi:~/projet-smb215# perf stat -d -- taskset -c 0 node algo-02/art-optimal.js
stdout: Res: 3146

 Performance counter stats for 'taskset -c 0 node algo-02/art-optimal.js':

      32976.778322      task-clock (msec)         #    1.000 CPUs utilized
               908      context-switches          #    0.028 K/sec
                 0      cpu-migrations            #    0.000 K/sec
             5,005      page-faults               #    0.152 K/sec
    46,000,947,672      cycles                    #    1.395 GHz                      (87.51%)
    45,985,889,081      instructions              #    1.00  insn per cycle           (87.49%)
     2,354,742,829      branches                  #   71.406 M/sec                    (87.51%)
        78,365,887      branch-misses             #    3.33% of all branches          (87.48%)
    20,824,494,589      L1-dcache-loads           #  631.490 M/sec                    (87.51%)
        23,695,341      L1-dcache-load-misses     #    0.11% of all L1-dcache hits    (87.48%)
       474,852,436      LLC-loads                 #   14.400 M/sec                    (87.51%)
       218,695,248      LLC-load-misses           #   46.06% of all LL-cache hits     (75.02%)

      32.992130955 seconds time elapsed
```

```
root@raspberrypi:~/projet-smb215# /usr/bin/time -v taskset -c 0 node algo-02/art-optimal.js
Res: 3146
        Command being timed: "taskset -c 0 node algo-02/art-optimal.js"
        User time (seconds): 32.77
        System time (seconds): 0.11
        Percent of CPU this job got: 99%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:32.90
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 39588
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 5070
        Voluntary context switches: 357
        Involuntary context switches: 449
        Swaps: 0
        File system inputs: 0
        File system outputs: 96
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

# PHP

```
root@raspberrypi:~/projet-smb215# perf stat -d -- taskset -c 0 php -f algo-02/art-optimal.php
Res: 3146

 Performance counter stats for 'taskset -c 0 php -f algo-02/art-optimal.php':

     285332.015875      task-clock (msec)         #    1.000 CPUs utilized
               807      context-switches          #    0.003 K/sec
                 0      cpu-migrations            #    0.000 K/sec
             4,677      page-faults               #    0.016 K/sec
   398,359,044,072      cycles                    #    1.396 GHz                      (87.50%)
   292,439,823,209      instructions              #    0.73  insn per cycle           (87.50%)
    31,627,946,300      branches                  #  110.846 M/sec                    (87.50%)
       729,596,792      branch-misses             #    2.31% of all branches          (87.50%)
   179,834,460,820      L1-dcache-loads           #  630.264 M/sec                    (87.49%)
       124,755,296      L1-dcache-load-misses     #    0.07% of all L1-dcache hits    (87.50%)
     1,321,140,313      LLC-loads                 #    4.630 M/sec                    (87.50%)
       527,821,059      LLC-load-misses           #   39.95% of all LL-cache hits     (75.00%)

     285.391416017 seconds time elapsed
```

```
root@raspberrypi:~/projet-smb215# /usr/bin/time -v taskset -c 0 php -f algo-02/art-optimal.php
Res: 3146
        Command being timed: "taskset -c 0 php -f algo-02/art-optimal.php"
        User time (seconds): 283.73
        System time (seconds): 0.38
        Percent of CPU this job got: 99%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 4:44.17
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 25800
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 4709
        Voluntary context switches: 1
        Involuntary context switches: 795
        Swaps: 0
        File system inputs: 0
        File system outputs: 96
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

# Java

```
root@raspberrypi:~/projet-smb215# perf stat -d -- taskset -c 0 java -cp algo-02 ArtOptimal
 Res: 3146

 Performance counter stats for 'taskset -c 0 java -cp algo-02 ArtOptimal':

      17073.923384      task-clock (msec)         #    0.997 CPUs utilized
             1,535      context-switches          #    0.090 K/sec
                 0      cpu-migrations            #    0.000 K/sec
             6,120      page-faults               #    0.358 K/sec
    23,785,571,653      cycles                    #    1.393 GHz                      (87.47%)
    23,396,046,454      instructions              #    0.98  insn per cycle           (87.58%)
     2,055,103,613      branches                  #  120.365 M/sec                    (87.47%)
       117,379,036      branch-misses             #    5.71% of all branches          (87.48%)
     6,475,574,827      L1-dcache-loads           #  379.267 M/sec                    (87.45%)
        47,964,856      L1-dcache-load-misses     #    0.74% of all L1-dcache hits    (87.54%)
       523,683,927      LLC-loads                 #   30.672 M/sec                    (87.60%)
       215,490,525      LLC-load-misses           #   41.15% of all LL-cache hits     (74.87%)

      17.116939847 seconds time elapsed
```

```
root@raspberrypi:~/projet-smb215# /usr/bin/time -v taskset -c 0 java -cp algo-02 ArtOptimal
Res: 3146
        Command being timed: "taskset -c 0 java -cp algo-02 ArtOptimal"
        User time (seconds): 17.99
        System time (seconds): 0.16
        Percent of CPU this job got: 99%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:18.18
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 35276
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 12
        Minor (reclaiming a frame) page faults: 6085
        Voluntary context switches: 691
        Involuntary context switches: 908
        Swaps: 0
        File system inputs: 0
        File system outputs: 192
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```