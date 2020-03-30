#!/usr/bin/python

from bs4 import BeautifulSoup as bs
from os import listdir
from os import path

from tools import getLink

import sys
import link_chaotic as lc
import link_distance as ld
import cluster_link as cl
import cluster_metric as cm
import numpy as np
import traceback as tb

#run clustering
#   input:  data set 'dataDir'
#           cluster method 'clmd'
#           'para' is the parameter of 'clmd'
def run(dataDir, clmd, para):
    htmlList = listdir(dataDir)
    htmlList = [html for html in htmlList if html.split('.')[-1] == 'html']
    ariList = []
    amiList = []
    for html in htmlList:
        try:
            dom = bs(open(path.join(dataDir, html)))
            linkClusterList = clmd(dom, para)
        except:
            print(tb.format_exc())
            print(dataDir)
            print(html)
            break
        try:
            ariList.append(cm.ari(linkClusterList))
            amiList.append(cm.ami(linkClusterList))
        except:
            continue
    return [ariList, amiList]

#run clustering with 'k'
#   input:  data set 'dataDir'
#           cluster method 'clmd'
#   output: the 'ariList'
def runK(dataDir, clmd):
    kMin = 1
    kMax = 100
    htmlList = listdir(dataDir)
    htmlList = [html for html in htmlList if html.split('.')[-1] == 'html']
    ariList = []
    amiList = []
    for html in htmlList:
        dom = bs(open(path.join(dataDir, html)))
        linkList = getLink(dom)
        tmpSet = set()
        for link in linkList:
            if 'clusterindex' in link.attrs:
                tmpSet.add(link['clusterindex'])
        try:
            linkClusterList = clmd(dom, len(tmpSet))
        except:
            print(tb.format_exc())
            continue
        ariList.append(cm.ari(linkClusterList))
        amiList.append(cm.ami(linkClusterList))
    return [ariList, amiList]

def main():
    dataBase = '../../data'
    dataDirList = []
#    dataDirList = listdir(path.join(dataBase, 'Big5_labeled'))
#    dataDirList = ['Big5_labeled/'+dataDir for dataDir in dataDirList if dataDir.split('.')[-1] == 'com']
#    dataDirList.append('cleanEval_labeled')
    dataDirList.append('myriad40_labeled')
    print(dataDirList)
    #'''
    #clustering based gap
    clmdList = [cl.chd, cl.chdLD]
#    clmdList = [cl.chd, cl.chdLD, cl.clusterLinkDB, cl.clusterLinkAgg]
    #clmdList = [cl.clusterLinkDB, cl.clusterLinkAgg]
    for clmd in clmdList:
        for dataDir in dataDirList:
            tmp = run(path.join(dataBase, dataDir), clmd, 1)
            ariList = tmp[0]
            amiList = tmp[1]
            '''
            ariPer = []
            amiPer = []
            for i in range(0, 11):
                tmp = 0
                for ari in ariList:
                    if ari <= (i/10.0):
                        tmp += 1
                ariPer.append(float(tmp)/len(ariList))
            for i in range(0, 11):
                tmp = 0
                for ami in amiList:
                    if ami <= (i/10.0):
                        tmp += 1
                amiPer.append(float(tmp)/len(amiList))
            print(ariPer)
            print(amiPer)
            '''
            print('Data set: %s, method: %s' ) % (dataDir, str(clmd).split()[1])
            print('Mean of ari: %s' % (float(sum(ariList))/len(ariList)))
            print('Mean of ami: %s' % (float(sum(amiList))/len(amiList)))
        print('*'*20)
    '''
    #clustering based 'k'
    clmdList = [cl.clusterLinkKM, cl.clusterLinkSC]
    #clmdList = [cl.clusterLinkSC]
    for clmd in clmdList:
        for dataDir in dataDirList:
            tmp = runK(path.join(dataBase, dataDir), clmd)
            ariList = tmp[0]
            amiList = tmp[1]
            ariPer = []
            amiPer = []
            for i in range(0, 11):
                tmp = 0
                for ari in ariList:
                    if ari <= (i/10.0):
                        tmp += 1
                ariPer.append(float(tmp)/len(ariList))
            for i in range(0, 11):
                tmp = 0
                for ami in amiList:
                    if ami <= (i/10.0):
                        tmp += 1
                amiPer.append(float(tmp)/len(amiList))
            print(ariPer)
            print(amiPer)
            #print('For the data set %s on method %s') % (dataDir, str(clmd))
            #print('Mean of ari:')
            #print(float(sum(ariList))/len(ariList))
            #print('Mean of ami:')
            #print(float(sum(amiList))/len(amiList))
        print('*'*20)

    '''

if __name__ == '__main__':
    main()
