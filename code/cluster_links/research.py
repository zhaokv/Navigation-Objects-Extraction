#!/usr/bin/python

from bs4 import BeautifulSoup as bs
from tools import getLink

import sys
import link_chaotic as lc
import link_distance as ldi
import link_density as lde
import cluster_link as cl
import cluster_metric as cm

def main():
    dom = bs(open('../../data/Big5_labeled/techweb.com/'+sys.argv[2]+'.html'))
    #md = lc.linkChaotic(dom)
    if sys.argv[1] == '1':
        output = True
    else:
        output = False
    linkClusterList = cl.chd(dom)
    print('CHD: ARI, %s; AMI, %s' %(cm.ari(linkClusterList),cm.ami(linkClusterList)))
    linkClusterList = cl.chdLD(dom)
    print('CHD-LD: ARI, %s; AMI, %s' %(cm.ari(linkClusterList),cm.ami(linkClusterList)))
    if output:
        for linkCluster in linkClusterList:
            print(linkCluster)
            print(len(linkCluster))
            print('-'*50)
        print(len(linkClusterList))
        print('#'*100)

if __name__ == '__main__':
    main()
