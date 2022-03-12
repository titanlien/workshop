# Overview

Our script to print the top ten processes in swap isn't working. Can you debug it?

# The Question

What we'd like from you is the following:

* A working copy of this script which
  - prints the top ten processes in swap: the swap used, process PID, and process name.
  - sorts output by kilobytes used with the largest first. Zero values should be excluded.
  - aligns formats each field in a vertical column.
* A list of
  - the things wrong with the script and why they don't work, and
  - the changes you needed to make.

Your script output should look the same as the example below.

During the on-site interviews we'll discuss your answer so remember to take notes as you go.
Some people find it helpful to log their terminal and review it later to remember what they did along the way.

### Example output

~~~~
  Swap space   PID   Process
  ==========  =====  =======
    56092 kB  30345  /usr/bin/iperf --server -yc
    10688 kB   4404  (squid) -YC -f /etc/squid3/squid.conf
     4480 kB   1079  /usr/sbin/freeradius
     2236 kB   4356  /usr/sbin/snmpd -Lsd -Lf /dev/null -u snmp -g snmp -I -smux -p /var/run/snmpd.pid
     2196 kB   8038  /bin/sh /etc/init.d/megaclisas-statusd check_megaclisas
     2164 kB   1728  udevd --daemon
     2160 kB   1031  udevd --daemon
     2092 kB   1727  udevd --daemon
     1396 kB   4378  /usr/sbin/squid3 -YC -f /etc/squid3/squid.conf
      844 kB   8414  /usr/sbin/console-kit-daemon --no-daemon
~~~~

# FAQ

## How do I get started?

* Try running the script swaptop.rb. Why doesn't it work?

## What are all the files?

* `swaptop.rb`: a script to print the top processes in swap. It has bugs.
