import numpy
import os

from bs4 import BeautifulSoup as bs
from cluster_link import getCluster
from tools import getLink

#calculate the link ratio
#   input: a dom-tree, maybe include smooth paramater
#   output: the link ratio of a dom-tree
def calLinkRatio(dom, smooth = 0.0):
    return (len(getLink(dom))+smooth)/(len(dom.text.split())+smooth)

#get the link ratio threshold
#   input: a dom-tree
#   output: the link ratio threshold
def getThres(dom):
    return calLinkRatio(dom)

#find the sub-tree on dom-tree which includes all link in linkSet while it's min
#   input: a dom-tree and a link set
#   output: a sub-tree on dom-tree
def findSubTree(dom, linkSet):
    subTree = dom
    for desc in dom.descendants:
        tmpLinkSet = set([link['href'] for link in getLink(desc)])
        if linkSet.issubset(tmpLinkSet):
            subTree = desc
    return subTree

def main():
    htmlFilePath = '../data/clean_eval/10.html'
    dom = bs(open(htmlFilePath))
    linkRatioThres = getThres(dom)
    linkClusterList = []
    linkClusterList = getCluster(dom)
    for linkCluster in linkClusterList:
        subTree = findSubTree(dom, set(linkCluster))
        print(linkCluster)
        print(calLinkRatio(subTree))
        if calLinkRatio(subTree) > linkRatioThres and len(linkCluster) > 1:
            print('Yes')
        else:
            print('No')

if __name__ == '__main__':
    main()
