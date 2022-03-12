#!/usr/bin/env ruby

options = {
  count: 10
}

lines = `grep '^Swap' /proc/*/smaps 2>/dev/null`.split("\n")
pid2swap = {}

puts "Swap space   PID   Process"
puts "==========  =====  ======="
lines.each do |line|
  if !line.match (/\/proc\/\d+\/smaps\:Swap\:\s*\d+ kB/)
    #puts "Bad line: " + line
    next
  end
  pid, kb = $1, $2
  if kb.to_i > 0
    pid2swap[pid] = pid2swap[pid].to_i + kb.to_i
  end
end

pid2swap.sort {|a,b| -a[1] <=> -b[1] }.slice(0...options[:count]).each do |pid, kb|
  psout = `ps -p #{pid} -o args=`.strip
  if psout.empty?
    printf "%s kB (no longer running)\n", kb
  else
    printf "%s kB %s %s\n", kb, pid, psout
  end
end
