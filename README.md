# Subject

https://primers.xyz/0

https://titouant.github.io/artOptimisation/

# Requirement

### perf

https://man7.org/linux/man-pages/man1/perf-stat.1.html

```
root@raspberrypi:~# apt install linux-perf
```

```
root@raspberrypi:~# apt-cache search linux-tools
linux-perf-4.18 - Performance analysis tools for Linux 4.18
linux-perf-4.9 - Performance analysis tools for Linux 4.9
linux-tools - Performance analysis tools for Linux (dummy package)
linux-tools-3.6 - Performance analysis tools for Linux 3.6
```

Edit the version number:

```
root@raspberrypi:~# nano /usr/bin/perf
exec "perf_4.9" "$@"
exit 0
```

https://raspberrypi.stackexchange.com/questions/43218/how-to-use-the-perf-utility-on-raspbian

### time

https://man7.org/linux/man-pages/man1/time.1.html

```
root@raspberrypi:~# apt install time
```

### GCC

```
root@raspberrypi:~# gcc --version gcc (Raspbian 8.3.0-6+rpi1) 8.3.0 Copyright (C) 2018 Free Software Foundation, Inc. This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

### Python3

```
root@raspberrypi:~# python3 --version Python 3.7.3
```

### node.js

```
root@raspberrypi:~# sudo curl -sL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
root@raspberrypi:~# sudo apt install nodejs
root@raspberrypi:~# npm install npm@latest -g
```

```
root@raspberrypi:~# node --version v14.16.0
```

### PHP

```
root@raspberrypi:~# apt install php
```

```
root@raspberrypi:~# php --version PHP 7.3.27-1~deb10u1 (cli) (built: Feb 13 2021 16:31:40) ( NTS )
Copyright (c) 1997-2018 The PHP Group Zend Engine v3.3.27, Copyright (c) 1998-2018 Zend Technologies with Zend OPcache v7.3.27-1~deb10u1, Copyright (c) 1999-2018, by Zend Technologies
```

### Java

```
root@raspberrypi:~# apt install openjdk-11-jre openjdk-11-jdk
```

```
root@raspberrypi:~# javac --version
javac 11.0.9.1
root@raspberrypi:~# java --version
openjdk 11.0.9.1 2020-11-04
OpenJDK Runtime Environment (build 11.0.9.1+1-post-Raspbian-1deb10u2)
OpenJDK Server VM (build 11.0.9.1+1-post-Raspbian-1deb10u2, mixed mode)
```

### Custom

```
root@raspberrypi:~# sudo nano /boot/config.txt

dtparam=audio=off
dtoverlay=disable-bt dtoverlay=disable-wifi

root@raspberrypi:~# sudo systemctl disable hciuart
```