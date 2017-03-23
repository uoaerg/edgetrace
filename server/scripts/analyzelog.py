#!/usr/bin/env python3.5

import plt #python-libtrace
import pickle
import time
import sys
import os
import json
import pprint
import csv

import processlog as plog

def analyzedata():

    numberofdscp = 64

    filelist = []
    capturedirectory = '/home/andre/mnt/capture/'
    
    for files in os.listdir(capturedirectory):
        if files.endswith('.pcap'):
            filelist.append(os.path.join(capturedirectory,files))
    
    data = plog.processpcap(filelist)

    numberofdscpatendofpath = {}
    
    for token in data:
        for dscp in data[token]:
            recv_dscp = []
            path_length = []
            for packet in data[token][dscp]:
                if packet['recv_dscp'] not in recv_dscp:
                    recv_dscp.append(packet['recv_dscp'])
                if packet['path_length'] not in path_length:
                    path_length.append(packet['path_length'])

            path_length = sum(path_length)/len(path_length)

            for eachdscp in recv_dscp:
                if dscp not in numberofdscpatendofpath:
                    numberofdscpatendofpath[dscp] = {'recv_dscp':{eachdscp:1}, 'path_lengths':path_length}
                else:
                    if eachdscp not in numberofdscpatendofpath[dscp]['recv_dscp']:
                        numberofdscpatendofpath[dscp]['recv_dscp'][eachdscp] = 1
                    else:
                        
                        numberofdscpatendofpath[dscp]['recv_dscp'][eachdscp] += 1

    sortednumberofdscpatendofpath = []

    with open('/tmp/edgetracetmp/Edge_Connectivity_Information.csv', 'w') as printfile:
        wtr = csv.writer(printfile)

        for dscp in numberofdscpatendofpath:

            numberofpaths = sum(numberofdscpatendofpath[dscp]['recv_dscp'].values())
            averagepathlength = numberofdscpatendofpath[dscp]['path_lengths']

            for recvdscp in numberofdscpatendofpath[dscp]['recv_dscp']:
                number = numberofdscpatendofpath[dscp]['recv_dscp'][recvdscp]
                relativenumber = number / numberofpaths * 100
                sortednumberofdscpatendofpath.append([dscp,recvdscp,number,relativenumber,averagepathlength,numberofpaths])

        sortednumberofdscpatendofpath = sorted(sortednumberofdscpatendofpath)
        
        wtr.writerow(['Initial DSCP','DSCP at end of path','Number of times at end of path','Perncetage of times at end of path relative to number path',
                'Average number of hops before end of path','Number of paths'])
        wtr.writerows(sortednumberofdscpatendofpath)
        
    with open('/tmp/edgetracetmp/logdata' + '.pkl', 'wb') as printfile:
        pickle.dump(data, printfile, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    analyzedata()
