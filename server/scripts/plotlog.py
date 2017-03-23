#!/usr/bin/env python3.5

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as mticker

import processlog as plog

import pprint
import sys
import json

def plotchangedscp(dataSet):
    
    directoryToSave = '/home/andre/edgetrace/server/generated/'
    
    if dataSet is None:
        data = np.loadtxt("/tmp/edgetracetmp/Edge_Connectivity_Information.csv", delimiter=',', skiprows=1)
    else:
        data = dataSet
            
    listOfMeaning = {
        0:"BE", 2:"LE",
        8:"CS1",10:"AF11",12:"AF12",14:"AF13",
        16:"CS2",18:"AF21",20:"AF22",22:"AF23",
        24:"CS3",26:"AF31",28:"AF32",30:"AF33",
        32:"CS4",34:"AF41",36:"AF42",38:"AF43",
        40:"CS5",44:"VA",46:"EF",
        48:"CS6",
        56:"CS7"
    }

    listOfDSCP = []
    for row in data:
        if row[0] not in listOfDSCP:
            listOfDSCP.append(int(row[0]))
    listOfDSCP = np.array(listOfDSCP)

    listOfUnassignedDSCP = listOfDSCP[(listOfDSCP[:] >= 1) & (listOfDSCP[:] <= 7)]
    
    
    #
    #Plot for all DSCPs
    #
    
    width = 0.2
    
    xdata = np.arange(0,len(listOfDSCP))

    ydataunchanged = []
    ydatachanged = []
    for dscp in listOfDSCP:
        somedata = data[(data[:,0]==dscp)]
        unchanged = 0
        changed = 0
        
        for index, value in np.ndenumerate(somedata[:,1]):
            if value == somedata[index,0]:
                unchanged = somedata[index,3]
            else:
                changed += somedata[index,3]
                
        ydataunchanged.append(unchanged)
        ydatachanged.append(changed)
    
    xaxisticks = xdata + width/2
    
    xaxislabels = []
    for labeldscp in listOfDSCP:
        if labeldscp in listOfMeaning:
            xaxislabels.append('%d\n(%s)' % (labeldscp, listOfMeaning[labeldscp]))
        else:
            xaxislabels.append('%d' % labeldscp)
    yaxisticks = np.arange(0,101,20)

    yaxislabels = []
    for number in yaxisticks:
        yaxislabels.append("{}%".format(number))
    
    rectsunchanged = plt.bar(xdata, ydataunchanged, width, color='blue', edgecolor='none')
    rectschanged = plt.bar(xdata+width, ydatachanged, width, color='red', edgecolor='none')
    
    fig = plt.gcf()
    defaultsize = fig.get_size_inches()
    fig.set_size_inches(15,3)
    
    ax = plt.gca()
    ax.tick_params(direction='out', top='off', right='off')
    ax.yaxis.set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
            
    ax.legend((rectsunchanged[0], rectschanged[0]), ('Unchanged', 'Changed'), loc=9, bbox_to_anchor=(0.5, 1.1), ncol=2)

    plt.xlim(0 - width / 3,len(xaxisticks))
    plt.ylim(0,100)
    
    plt.xticks(xaxisticks + width / 2, xaxislabels, fontsize=12)
    
    plt.axhline(y=25, color='black', linestyle='--', linewidth=1)
    plt.axhline(y=50, color='black', linestyle='--', linewidth=1)
    plt.axhline(y=75, color='black', linestyle='--', linewidth=1)
    
    plt.tight_layout()
    plt.savefig(directoryToSave+"plots/Path_Information_Summary.png", transparent=True, bbox_inches="tight")
    #plt.show()
    plt.clf()

    
    #
    #Plots for each DSCPs
    #

    width = 0.75
        
    fig.set_size_inches(defaultsize)
    
    for DSCP in listOfDSCP:
        averageNumberOfHopsTotal = 0
        averageNumberOfHops = 0
    
        someOfTheDSCP = data[(data[:,0]==DSCP)]

        averagepathlength = someOfTheDSCP[0,4]
        numberofpaths = someOfTheDSCP[0,5]
    
        xSomeOfTheDSCP = np.arange(0,len(someOfTheDSCP[:,1]))

        ySomeOfTheDSCP = []
        for index, value in np.ndenumerate(someOfTheDSCP[:,1]):
            #unchanged
            if value == someOfTheDSCP[index,0]:
                ySomeOfTheDSCP.insert(0,someOfTheDSCP[index,3])
            #ToS bleach
            elif value in listOfUnassignedDSCP:
                ySomeOfTheDSCP.insert(1,someOfTheDSCP[index,3])
            else:
                ySomeOfTheDSCP.append(someOfTheDSCP[index,3])

        xaxisticks = xSomeOfTheDSCP

        xaxislabels = []
        for labeldscp in someOfTheDSCP[:,1]:
            #unchanged
            if labeldscp == DSCP:
                xaxislabels.insert(0,'Unchanged')
            #ToS bleach
            elif labeldscp in listOfUnassignedDSCP:
                xaxislabels.insert(1,'ToS\nBleach')
            else:
                if labeldscp in listOfMeaning:
                    xaxislabels.append('%d\n(%s)' % (labeldscp, listOfMeaning[labeldscp]))
                else:
                    xaxislabels.append('%d' % labeldscp)

        yaxisticks = np.arange(0,101,20)

        yaxislabels = []
        for number in yaxisticks:
            yaxislabels.append("{}%".format(number))

        colormap = cm.jet(1.*np.arange(0,len(xaxisticks))/len(xaxisticks))

        rects = plt.bar(xaxisticks, ySomeOfTheDSCP, width, color=colormap, edgecolor='none')

        ax = plt.gca()
        ax.tick_params(direction='out', top='off', right='off')
        ax.yaxis.set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        plt.xlim(0 - width / 3,len(xaxisticks))
        plt.ylim(0,100)

        #if DSCP in listOfMeaning:
        #    plt.title('Initial DSCP %d (%s)\nObserved DSCP at end of path' % (DSCP, listOfMeaning[DSCP]), fontsize=14)
        #else:
        #    plt.title('Initial DSCP %d\nObserved DSCP at end of path' % DSCP, fontsize=14)

        #plt.text(len(xaxisticks),92,'Number of paths : %d\nAverage number of hops per path : %0.1f' % 
        #        (numberofpaths, averagepathlength), horizontalalignment='right', verticalalignment='center', fontsize=12)
        #plt.xlabel('DSCP')
        plt.xticks(xaxisticks, xaxislabels, fontsize=16)
        #plt.yticks(yaxisticks, yaxislabels)

        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width()/2., height+0.65, '%d' % height + '%', ha='center', va='bottom', fontsize=16)

        plt.tight_layout()
        plt.savefig(directoryToSave+"plots/Path_Information_DSCP%d.png" % DSCP, transparent=True)
        #plt.show()
        plt.clf()
    

    plt.close('all')
    
    with open(directoryToSave + 'path_information.json', 'w') as printfile:
        printfile.write('var listOfMeaning = ' + json.dumps(listOfMeaning) + "\n")
        printfile.write('var listofdscp = ' + json.dumps(listOfDSCP.tolist()) + "\n")
        printfile.write('var numberofpaths = ' + json.dumps(numberofpaths) + "\n")
        printfile.write('var averagepathlength = ' + json.dumps(averagepathlength))

if __name__ == "__main__":
    
    plotchangedscp(None)
