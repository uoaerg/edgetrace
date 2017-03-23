#!/bin/sh

cd server
./server | tee -a /home/andre/mnt/log/packetlog.log   
