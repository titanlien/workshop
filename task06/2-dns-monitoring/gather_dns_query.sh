#!/usr/bin/env bash

set -e

DNS_SERVERS=`awk -F " " '/nameserver/{print $2}' /etc/resolv.conf`

function print_query {
for dns in $DNS_SERVERS; do
  #echo $dns
  time=`dig +time=3 +tries=1 @$dns google.com |grep "Query time:"|awk {'print $4'}`
  if [ ! -z "$time" ]
  then
    result="succeeded"
  else
    result="failed"
  fi
  now=`date +"%s"`
  echo -e "$now,$dns,$result,$time"
done
}

while true
do
  print_query
  sleep 3600
done
