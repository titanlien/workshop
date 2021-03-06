# Overview

We have a fleet of about 700 servers in a number of datacentres worldwide.
Occasionally, we see increased error rates for some services - the services are
failing to query DNS. The failures don't seem correlated to any particular
datacentre or pattern of machines.

We'd like to set up a service on each machine that periodically makes a test
query and records the results.

# The Question

What we'd like from you is the following:

* A script that performs occasional test queries to the hostname "google.com"
  to each of the DNS servers configured in /etc/resolv.conf.
* Each test query should test exactly one DNS server. Nameservers can be
  queried in any order.
* All DNS servers in /etc/resolv.conf must be tested at least once every hour.
* The script should write exactly one comma-delimited line for each test to
  standard output, per _Output format_ below. No other data should be written
  to standard output.
* The script should log terse human-readable diagnostic information to
  standard error.
* The script should run forever, and exit cleanly when it receives SIGINT.
* *The script must be written in Ruby or Bash-compatible shell scripting.*

Note that the script will be started simultaneously on 700 machines by our
service management daemon. We have six different DNS servers.

**You should ensure that test traffic generated by your script has no impact on
the production DNS infrastructure, and be prepared to justify your design
decisions with reference to the throughput of a typical BIND nameserver.**

## Output format

The script should write exactly one line of output to standard out for each
test run. The line should contain exactly four fields, separated by commas:

* The time the test was performed, in seconds since the UNIX epoch
* The IP address of the DNS server tested
* If the test query returned the correct response, the string "succeeded"; in
  all other cases, the string "failed"
* The time taken to perform the test query in milliseconds. This value should
  be empty if the test query times out, but should be set if the query response is
  invalid.

Each line should be terminated by \n, and should contain no other whitespace.

For example, the following three lines describe three tests performed to DNS
servers 208.67.222.222 and 208.67.220.220:

~~~~
  1489675672,208.67.222.222,succeeded,10
  1489675681,208.67.222.222,failed,
  1489675729,208.67.220.220,succeeded,7
~~~~

The first test to 208.67.222.222 succeeds in 10 milliseconds, the second test
to 208.67.222.222 times out, and the third test to 208.67.220.220 succeeds in 7
milliseconds.

During the on-site interviews we'll discuss your answer so remember to take
notes as you go.  Some people find it helpful to log their terminal and review
it later to remember what they did along the way.

# FAQ

## How do I get started?

* 208.67.220.220 and 208.67.220.222 are publicly-accessible DNS servers (run by
  OpenDNS). You can use them to test DNS queries.
* Try running a DNS query manually to 208.67.220.220 for google.com, and
  thinking about how you might process the DNS tool's output.

## What are all the files?

* This question has no associated files, aside from this README.md.
