from bs4 import BeautifulSoup as bs
from tools import getLink

import sys
import numpy as np
import link_chaotic as lc
import link_distance as ld
import cluster_link as cl

def gaussianSmooth(  dataset, sigma ):
    
    count = int(np.ceil(sigma))
    
    jj = np.array(range(-count,count+1))
    jj = jj**2;
    ki = np.exp(-jj/float(sigma*sigma))
    kis = np.sum(ki)
    kii = np.copy(ki)
    kii = ki/float(kis)
    
    lenth = len(dataset)
    TT = range(0,lenth+2*count+1)
    TT[count:] = np.array(dataset)
    head = dataset[1:count+1]
    tail = dataset[lenth-count-1:lenth-1]
    head.reverse()
    tail.reverse()
    TT[0:count] = head
    TT[lenth+count:lenth+count*2] = tail
    
    result = range(0,lenth)
    for i in range(0,lenth):
        result[i] = np.sum(kii*TT[i:i+count*2+1])
    return result;

#please smooth the domTree at first
def smoothTree( tree, sigma = 2 ):
    
    linkSet = tree.find_all('a')
    wordNumList = []
    for item in linkSet:
        wordNumList.append( len(item.text.split()) )
    lenth = len(wordNumList)

    if sigma and sigma < len(linkSet):
        smoothedList = gaussianSmooth(wordNumList, sigma)
    else:
        smoothedList = wordNumList
    for ind in range(0,lenth):
        linkSet[ind]['wordNum'] = smoothedList[ind]

class linkChaotic:
    #ct is the threshold to decide whether the domTree(sub-tree) in a list belong to one cluster
    ct = 0
    #init the linkChaotic, this will smooth the domTree
    def __init__(self, domTree, sigma = 2):
        smoothTree(domTree, sigma)
#        self.ct = self.chaoticThres(domTree)

    #get the chaotic threshold for judging whether this dom-node is one cluster
    #small value means high possibility to be one cluster
    #   input: dom-tree smoothed
    #   output: the chaotic threshold
    def chaoticThres(self, domTree):
        chaoticList = []
        for des in domTree.descendants:
            chaotic = self.getChaotic(des)
            if chaotic:
                chaoticList.append(chaotic)
        chaoticList.sort()
        ct = chaoticList[0]
        maxInc = 0
        for i in range(1, len(chaoticList)):
            if chaoticList[i]-chaoticList[i-1] > maxInc:
                ct = chaoticList[i]
                maxInc = chaoticList[i]-chaoticList[i-1]
        return ct

    #get the chaotic of dom-tree(maybe a sub-tree) list
    #   input: dom-tree smoothed
    #   output: the chaotic value, if no link return None
    def getChaotic(self, domTreeList):
        linkList = []
        for domTree in domTreeList:
            try:
                linkList += getLink(domTree)
            except:
                continue
        if linkList:
            wordNumList = [float(link['wordNum']) for link in linkList]
            return np.var(np.array(wordNumList))
        else:
            return None

    #decide whether the domTree in a list belong to one cluster
    #   input: dom-tree list
    #   output: True or False
    def isOneCluster(self, domTreeList):
        return self.getChaotic([domTreeList]) < self.ct

    #cluster the same floor links according to the word number in links
    def clusterSameFloor(self, childList):
        avgNumList = []
        for child in childList:
            numList = [link['wordNum'] for link in getLink(child)]
            avgNumList.append(sum(numList)/len(numList))
        sumList = [0]
        for i in range(1, len(avgNumList)+1):
            sumList.append(sumList[i-1]+avgNumList[i-1])
        gapList = [0]
        for i in range(0, len(avgNumList)-1):
            for j in range(i+1, len(avgNumList)):
                gapList.append(abs(avgNumList[j]-(sumList[j]-sumList[i]+0.0)/(j-i)))
        gapList.sort(reverse = True)
        for gap in gapList:
            nodeClusterList = []
            start = 0
            for i in range(1, len(avgNumList)):
                if abs(avgNumList[i]-(sumList[i]-sumList[start]+0.0)/(i-start)) >= gap:
                    nodeClusterList.append(childList[start:i])
                    start = i
            nodeClusterList.append(childList[start:])
            if all([self.getChaotic(cluster) < self.ct for cluster in nodeClusterList]):
                clusterList = []
                for cluster in nodeClusterList:
                    oneCluster = []
                    for node in cluster:
                        oneCluster += [link['href'] for link in getLink(node)]
                    clusterList.append(oneCluster)
                return clusterList
        return None

def main():
    dom = bs(open('../../data/clean_eval/'+sys.argv[1]+'.html'))
    linkList = getLink(dom)
    linkLenList = [len(link.text.split()) for link in linkList]
    print(linkLenList)
    lc = linkChaotic(dom)
    linkLenList = [link['wordNum'] for link in linkList]
    print(linkLenList)

if __name__ == '__main__':
    main()
