#!/bin/sh

tcpdump -w '/home/andre/mnt/capture/trace_%Y-%m-%d_%H:%M:%S.pcap' \
	-G 3600 \
	-i re0 \
	"udp and port 60606"

