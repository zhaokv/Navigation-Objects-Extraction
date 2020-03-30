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

def run(dataDir):
    htmlList = listdir(dataDir)
    htmlList = [html for html in htmlList if html.split('.')[-1] == 'html']
    naviNum = 0
    nNaviNum = 0
    naviDic = {}
    naviDic['navi'] = set()
    naviDic['nNavi'] = set()
    for html in htmlList:
        try:
            dom = bs(open(path.join(dataDir, html)))
        except Exception, e:
            print e
            break
        for link in getLink(dom):
            try:
                if link['cluster'] == 'nav' or link['cluster'] == 'list':
                    naviNum += 1
                    naviDic['navi'].add(link['clusterindex'])
                else:
                    nNaviNum += 1
                    naviDic['nNavi'].add(link['clusterindex'])
            except:
                naviDic['nNavi'].add(-1)
                nNaviNum += 1
    print('Num of nav link is %s, num of non-navi link is %s') % (naviNum, nNaviNum)
    print('Num of nav block is %s, num of non-nav link block is %s') % (len(naviDic['navi']), len(naviDic['nNavi']))


def main():
    dataBase = '../../data'
    dataDirList = []
    dataDirList = listdir(path.join(dataBase, 'Big5_labeled'))
    dataDirList = ['Big5_labeled/'+dataDir for dataDir in dataDirList if dataDir.split('.')[-1] == 'com']
    dataDirList.append('cleanEval_labeled')
    dataDirList.append('myriad40')
    print(dataDirList)
    for dataDir in dataDirList:
        run(path.join(dataBase, dataDir))

if __name__ == '__main__':
    main()
