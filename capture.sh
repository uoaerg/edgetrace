#!/bin/sh

sudo tcpdump -w '/home/tom/mnt/capture/trace_%Y-%m-%d_%H:%M:%S.pcap' \
	-G 3600 \
	-i re0 \
	"(tcp and port 80) or (udp and port 60606)"

