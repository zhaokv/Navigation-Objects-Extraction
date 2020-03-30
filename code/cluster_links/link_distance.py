import numpy as np

from tools import getLink

class linkDistance:
    #dt is the threshold to decide whether the domTree(sub-tree) in a list belong to one cluster
    dt = 0
    index = 0
    #init the linkDistance
    def __init__(self, domTree, alpha = 1):
        self.setIndex(domTree)
        self.dt = self.disThres(domTree, alpha)

    #index every node on domTree
    def setIndex(self, domTree):
        for des in domTree.descendants:    
            try:
                des['index'] = self.index
                self.index += 1
            except:
                None
        '''
        for link in getLink(domTree):
            color = int('0000FF', 16)
            fontSize = 0
            hasColor = False
            hasFont = False
            colorMap = {'white': 'FFFFFF', 'navy': '000080', 'gray': '808080', 'black': '000000'}
            for node in link.parents:
                fontInfo = node.find('font')
                if fontInfo:
                    if 'color' in fontInfo.attrs:
                        if fontInfo['color'] in colorMap:
                            color = int (colorMap[fontInfo['color'].lower()], 16)
                        else:
                            color = int(fontInfo['color'][1:], 16)
                        hasColor = True
                    if 'size' in fontInfo.attrs:
                        fontSize = int(fontInfo['size'])
                        hasFont = True
                    if hasColor and hasFont:
                        break
            link['link_color'] = color
            link['link_size'] = fontSize
        '''

    #get the distance threshold for judging whether this dom-node is one cluster
    #small value means high possibility to be one cluster
    #   input:  dom-tree 
    #           balance parameter 'alpha'
    #   output: the distance threshold
    def disThres(self, domTree, alpha = 1):
        disList = []
        disList.append(0)
        linkList = getLink(domTree)
        for i in range(1, len(linkList)):
            dis = self.getDis(linkList[i], linkList[i-1])
            if dis:
                disList.append(dis)
        disList.sort(reverse = True)
        judgeList = [disList[i] * len(disList) * alpha+  i * disList[0] for i in range(0, len(disList))]
        minIndex = 0
        for i in range(0, len(judgeList)):
            if judgeList[i] < judgeList[minIndex]:
                minIndex = i
        dt = disList[minIndex]
        return dt

    #get the distance between two domTree
    #   input: two dom-trees
    #   output: the distance value, if any error return None
    def getDis(self, dom1, dom2):
        dom1Fea = [dom1['index']]
        dom2Fea = [dom2['index']]
#        dom1Fea = [dom1['index'], dom1['link_color'], dom1['link_size']]
#        dom2Fea = [dom2['index'], dom2['link_color'], dom2['link_size']]
#        dom1Fea = [dom1['index'], dom1['link_color'], dom1['link_size'], dom1.parent['index']]
#        dom2Fea = [dom2['index'], dom2['link_color'], dom2['link_size'], dom2.parent['index']]
        return np.linalg.norm(np.array(dom1Fea) - np.array(dom2Fea))
    
    #get the min gap between two domTrees
    #   input: two domTrees
    #   output: the min gap between two domTrees, maybe reture None
    def getMinGap(self, dom1, dom2):
        minGap = None
        linkList1 = getLink(dom1)
        linkList2 = getLink(dom2)
        if linkList1 and linkList2:
            minGap = self.getDis(linkList1[0], linkList2[0])
        for link1 in linkList1:
            for link2 in linkList2:
                minGap = min(self.getDis(link1, link2), minGap)
        return minGap

    #decide whether the domTree in a list belong to one cluster
    #   input: dom-tree list
    #   output: True or False
    def isOneCluster(self, domTree):
        childList = []
        for child in domTree.children:
            try:
                if getLink(child):
                    childList.append(child)
            except:
                continue
        maxGap = 0
        for i in range(1, len(childList)):
            maxGap = max(self.getMinGap(childList[i-1], childList[i]), maxGap)
        return maxGap <= self.dt

    #cluster the same floor links according to the word number in links
    def clusterSameFloor(self, childList, md2):
        clusterList = []
        if not childList:
            return clusterList
        
        oneCluster = getLink(childList[0])
        for i in range(1, len(childList)):
            tmp = list(childList[i-1].next_siblings)
            tmp1 = [childList[i-1]]+tmp[0:tmp.index(childList[i])+1]
            if self.getMinGap(childList[i], childList[i-1]) > self.dt or not md2.isOneCluster(tmp1):
                clusterList.append(oneCluster)
                oneCluster = getLink(childList[i])
            else:
                oneCluster += getLink(childList[i])
        clusterList.append(oneCluster)
        return clusterList
