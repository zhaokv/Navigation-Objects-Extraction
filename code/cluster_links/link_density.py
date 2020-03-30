import numpy as np

from tools import getLink

class linkDensity:
    #dt is the threshold to decide whether the domTree(sub-tree) belongs to one cluster
    dt = 0
    #init the linkDensity
    def __init__(self, domTree, alpha = 1, beta = 1):
        self.alpha = alpha
        self.beta = beta
        self.dt = self.denThres(domTree)


    #get the density threshold for judging whether this dom-node is one cluster
    #bigger value means higher possibility to be one cluster
    #   input:  dom-tree 
    #   output: the density threshold
    def denThres(self, domTree):
        linkList = getLink(domTree)
        linkStrList = []
        for link in linkList:
            linkStrList.append(link.text)
            imgList = link.find_all('img')
            if not imgList:
                linkStrList.append('string')
            for img in link.find_all('img'):
                if 'alt' in img.attrs:
                    linkStrList.append(img['alt'])
                else:
                    linkStrList.append('string')
        linkStrLen = sum([len(linkStr.split()) for linkStr in linkStrList])
        dt = self.alpha*(linkStrLen+self.beta)/(float(len(domTree.text.split()))+linkStrLen+self.beta)
        return dt

    #get the link density in a dom-tree
    #   input: one dom-tree
    #   output: the link density value, if any error return None
    def getLinkDen(self, subDomList):
        linkList = []
        for subDom in subDomList:
            linkList += getLink(subDom)
        linkStrList = []
        for link in linkList:
            linkStrList.append(link.text)
            imgList = link.find_all('img')
            if not imgList:
                linkStrList.append('string')
            for img in link.find_all('img'):
                if 'alt' in img.attrs:
                    linkStrList.append(img['alt'])
                else:
                    linkStrList.append('string')
        linkStrLen = sum([len(linkStr.split()) for linkStr in linkStrList])
        ld = (linkStrLen+self.beta)/(float(len(subDom.text.split()))+linkStrLen+self.beta)
        return ld

    #decide whether links in a sub Dom-tree are in one block
    def isOneCluster(self, subDom):
        if self.alpha == 0:
            return True
        return self.getLinkDen(subDom)>self.dt
