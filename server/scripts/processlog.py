#!/usr/bin/env python3.5

import plt #python-libtrace
import time
import sys
import json
import pprint
import csv

import random

def processpcap(filelist):
    
    TTLbyOS = {'linux':64,
                'darwin':64,
                'freebsd':64,
                'windows':128,
                'Unavailable':64}

    sessions = {}

    for filename in filelist:
        trace = plt.trace('pcapfile:{}'.format(filename))
        trace.start()

        try:
            for pkt in trace:
                ip = pkt.ip

                if ip.proto != 17:
                    continue

                protonum = ip.proto
                recvdscpvalue = ip.traffic_class >> 2
                ttl = ip.ttl

                jsonstr = str(ip.udp_payload.data, "utf-8")
                session = json.loads(jsonstr)
                session['recv_dscp'] = recvdscpvalue
                session['recv_ttl'] = ttl
                session['OS'] = session.get('OS', 'Unavailable')
                session['ttl'] = session.get('ttl', TTLbyOS[session['OS']])

                session['path_length'] = session['ttl'] - session['recv_ttl'] + 1 #number of hop to routers + hop to the server

                token = session['token']
                dscpvalue = session['dscp']
                if token not in sessions:
                    sessions[token] = {dscpvalue:[session]}
                    #print(token)
                else:
                    if dscpvalue not in sessions[token]:
                        sessions[token][dscpvalue] = [session]
                    else:
                        sessions[token][dscpvalue].append(session)

        except KeyboardInterrupt:
            trace.close()
            sys.exit()

    #pprint.pprint(sessions)

    return sessions

if __name__ == "__main__":

    processpcap([])
