#!/usr/bin/env python3.5

import numpy as np
import matplotlib.pyplot as plt

from geolite2 import geolite2

import processlog as plog

import pprint
import pickle
import sys
import json

def mapplot():
    
    directoryToSave = '/home/andre/edgetrace/server/generated/'
    
    with open('/tmp/edgetracetmp/logdata' + '.pkl', 'rb') as printfile:
        data = pickle.load(printfile)
    
    reader = geolite2.reader()
    
    lats = []
    lons = []
    
    for token in data:
        ip = next(iter(data[token].values()))[0]['host']
        
        match = reader.get(ip)
        
        if match is not None:
            lats.append(match['location']['latitude'])
            lons.append(match['location']['longitude'])
    
    coordinates = {'latitude':lats, 'longitude':lons}
    
    with open(directoryToSave + 'coordinates.json', 'w') as outfile:
        outfile.write('var coordinates = ' + json.dumps(coordinates))
    
    plt.close('all')
    geolite2.close()

if __name__ == "__main__":
    
    mapplot()
