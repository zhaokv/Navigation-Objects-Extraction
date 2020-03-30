from tools import getLink
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import DBSCAN
from numpy import * 

import math
import link_distance as ldi
import link_density as lde

#return: if the children in dom-tree are in one cluster, return True
def clusterLink(domTree, clusterList, md1, md2):
    childList = []
    for child in domTree.children:
        try:
            if getLink(child):
                childList.append(child)
        except:
            continue
    if not childList:
        return True
    if not getLink(domTree):
        return True
    isOneClusterList = [clusterLink(child, clusterList, md1, md2) for child in childList]
    if all(isOneClusterList):
        if md1.isOneCluster(domTree) and md2.isOneCluster([domTree]):
            return True
        else:
            clusterList += md1.clusterSameFloor(childList, md2)
            return False
    else:
        tmpChildList = []
        for i in range(0, len(childList)):
            if not isOneClusterList[i]:
                clusterList += md1.clusterSameFloor(tmpChildList, md2)
                tmpChildList = []
            else:
                tmpChildList.append(childList[i])
        clusterList += md1.clusterSameFloor(tmpChildList, md2)
        return False

#cluster samilar links on dom-tree into one cluster
#   input:  dom: domTree
#           md1, md2: the particular method
#   output: link cluster list
def runClusterLink(dom, md1, md2):
    clusterList = []
    if clusterLink(dom, clusterList, md1, md2):
        tmpCluster = getLink(dom)
        if tmpCluster:
            clusterList.append(tmpCluster)
    clusterList = [cluster for cluster in clusterList if cluster]
    return clusterList

#our clustering algorithm withou link density
#   input:   'dom' is the domTree
#           'para' is a parameter for linkDistance
#   output: link clustering list
def chd(dom, para = 1):
    md1 = ldi.linkDistance(dom, para)
    md2 = lde.linkDensity(dom, 0, 0.00001)
    return runClusterLink(dom, md1, md2)

#our clustering algorithm with link density
#   input:   'dom' is the domTree
#           'para' is a parameter for linkDistance
#   output: link clustering list
def chdLD(dom, para = 1):
    md1 = ldi.linkDistance(dom, para)
    md2 = lde.linkDensity(dom, 1, 0.00001)
    return runClusterLink(dom, md1, md2)

#cluster samilar links on dom-tree into one cluster using one-dimension info
#   input:  dom: domTree
#   output: link cluster list
def clusterLink1D(dom, para = 1):
    md = ldi.linkDistance(dom, para)
    linkList = getLink(dom)
    if not linkList:
        return []
    linkClusterList = []
    tmp = [linkList[0]]
    for i in range(1, len(linkList)):
        if md.getDis(linkList[i], linkList[i-1]) > md.dt:
            linkClusterList.append(tmp)
            tmp = []
        else:
            tmp.append(linkList[i])
    if tmp:
        linkClusterList.append(tmp)
    linkClusterList = [linkCluster for linkCluster in linkClusterList if linkCluster]
    return linkClusterList

#get the single-link distance
#   input:  link list 'a' ans 'b', where the link is indexed
#           'md' is the meausre distance
#   output: the single-link distance between 'a' and 'b'
def singleLink(a, b, md):
    if not len(a) or not len(b):
        return None
    result = md.getDis(a[0], b[0])
    for i in range(0, len(a)):
        for j in range(0, len(b)):
            result = min(result, md.getDis(a[i], b[j]))
    return result

#get the single-link distance in 2D-space
#   input:  link list 'a' ans 'b', where the link is indexed
#   output: the single-link distance between 'a' and 'b'
def singleLink2D(a, b, md):
    if not len(a) or not len(b):
        return None
    dis1 = md.getDis(a[0], b[0])
    dis2 = abs(a[0].parent['index'] - b[0].parent['index'])
    result = math.sqrt(dis1 * dis1 + dis2 * dis2)
    for i in range(0, len(a)):
        for j in range(0, len(b)):
            tmp = math.sqrt((a[i]['index']-b[j]['index'])*(a[i]['index']-b[j]['index'])+
                (a[i].parent['index']-b[j].parent['index'])*(a[i].parent['index']-b[j].parent['index']))
            result = min(result, tmp)
    return result

#cluster samilar links on dom-tree into one cluster using agglomerative
#   input:  dom:    domTree
#           'para' is a parameter for linkDistance
#   output: linkCluster list
def clusterLinkAgg(dom, para = 1):
    md = ldi.linkDistance(dom, para)
    linkList = getLink(dom)
    linkClusterList = []
    for link in linkList:
        linkClusterList.append([link])
    while True:
        if len(linkClusterList) <= 1:
            break
        first = 0
        second = 1
        try:
            minGap = singleLink(linkClusterList[first], linkClusterList[second], md)
            #minGap = singleLink2D(linkClusterList[first], linkClusterList[second], md)
        except:
            print(len(linkClusterList))
            return
        for i in range(0, len(linkClusterList)):
            for j in range(i+1, len(linkClusterList)):
                gap = singleLink(linkClusterList[i], linkClusterList[j], md)
                #gap = singleLink2D(linkClusterList[i], linkClusterList[j], md)
                if gap < minGap:
                    minGap = gap
                    first = i
                    second = j
        if minGap > md.dt:
        #if minGap > md.dt*1.414:
            break
        linkClusterList[first] += linkClusterList[second]
        linkClusterList.pop(second)
    return linkClusterList

#cluster samilar links on dom-tree into one cluster using DBSCAN
#   input:  dom:    domTree
#           'para' is the parameter for DBSCAN
#   output: linkCluster list
def clusterLinkDB(dom, para = 0.5):
    md = ldi.linkDistance(dom, para)
    linkList = getLink(dom)
    a = [[link['index']] for link in linkList]
    #a = [[link['index'], link.parent['index']] for link in linkList]
    #a = [[link['index'], link['link_color'], link['link_size']] for link in linkList]
    #a = [[link['index'], link['link_color'], link['link_size'], link.parent['index']] for link in linkList]
    if not a:
        return []
    if not md.dt:
        return linkList
    #cluster = DBSCAN(md.dt*1.414, min_samples=1)
    cluster = DBSCAN(md.dt, min_samples=1)
    labelList = cluster.fit_predict(array(a))
    tmpSet = set()
    for label in labelList:
        tmpSet.add(label)
    linkClusterList = [[] for i in range(0, len(tmpSet))]
    for i in range(0, len(labelList)):
        linkClusterList[labelList[i]].append(linkList[i])
    linkClusterList = [linkCluster for linkCluster in linkClusterList if linkCluster]
    return linkClusterList

#cluster samilar links on dom-tree into one cluster using k-means
#   input:  dom:    domTree
#           'k' is the number of clusters
#   output: linkCluster list
def clusterLinkKM(dom, k = 2):
    md = ldi.linkDistance(dom, 1)
    linkList = getLink(dom)
    a = [[link['index']] for link in linkList]
    #a = [[link['index'], link.parent['index']] for link in linkList]
    #a = [[link['index'], link['link_color'], link['link_size']] for link in linkList]
    #a = [[link['index'], link['link_color'], link['link_size'], link.parent['index']] for link in linkList]
    if not a:
        return []
    cluster = KMeans(k)
    labelList = cluster.fit_predict(array(a))
    linkClusterList = [[] for i in range(0, k)]
    for i in range(0, len(labelList)):
        linkClusterList[labelList[i]].append(linkList[i])
    return linkClusterList

#cluster samilar links on dom-tree into one cluster using Spectral Clustering
#   input:  dom:    domTree
#           'k' is the number of clusters
#           'gamma' is the parameter for rbf
#   output: linkCluster list
def clusterLinkSC(dom, k = 2, affinity='nearest_neighbors', n_neighbors=1, gamma = 0.021):
    md = ldi.linkDistance(dom, 1)
    linkList = getLink(dom)
    a = [[link['index']] for link in linkList]
    #a = [[link['index'], link.parent['index']] for link in linkList]
    #a = [[link['index'], link['link_color'], link['link_size']] for link in linkList]
    #a = [[link['index'], link['link_color'], link['link_size'], link.parent['index']] for link in linkList]
    if not a:
        return []
    cluster = SpectralClustering(k, gamma = gamma)
    labelList = cluster.fit_predict(array(a))
    linkClusterList = [[] for i in range(0, k)]
    for i in range(0, len(labelList)):
        linkClusterList[labelList[i]].append(linkList[i])
    return linkClusterList
