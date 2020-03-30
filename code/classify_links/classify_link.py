import sys
sys.path.append('../cluster_links')
sys.path.append('../libsvm-3.20/tools')
import cluster_link as cl
import link_distance as ld
import link_chaotic as lc

import numpy as np
import random
import traceback as tb

from tools import getLink
from metric import metric
from bs4 import BeautifulSoup as bs
from os import path

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.cluster import KMeans
from sklearn.metrics.cluster import adjusted_rand_score as ari

labelDic = {'nav': 0, 'list': 1, 'content': 2, 'other': 3, 'none': 4, 'others': 5}
#get the classification result and ground truth
#   input:  domTree List "domList"
#   output: the link representation list and ground truth list
def genMatrix(domList):
    linkMatrix = []
    groundList = []
    clusterIndex = []
    for dom in domList:
        linkChaotic = lc.linkChaotic(dom, 2)
        #linkClusterList = cl.chd(dom, 1)
        linkClusterList = cl.chdLD(dom, 1)
        for linkCluster in linkClusterList:
            clusterSize = len(linkCluster)
            clusterChaotic = linkChaotic.getChaotic(linkCluster)
            textNumList = [link['wordNum'] for link in linkCluster]
            textNum = reduce(lambda x, y: x+y, textNumList)
            textNumAvg = float(textNum)/clusterSize
            for link in linkCluster:
                if 'cluster' in link.attrs:
                    linkMatrix.append([clusterSize, textNumAvg, clusterChaotic])
                    label = labelDic[link['cluster']]
                    groundList.append(int(label <= 1))
                #clusterIndex.append(int(link['clusterindex']))
    return (linkMatrix, groundList, clusterIndex)

def main():
    htmlFileDir = '../../data/cleanEval'
    htmlFileDir = '../../data/SSD/Big5/techweb.com'
    #htmlFileDir = '../../data/SSD/myriad40'
    '''
    for num in range(0, 10):
        htmlFilePath = path.join(htmlFileDir, str(num+1)+'.html')
        try:
            (oLinkMatrix, oGroundList, oClusterIndex) = genMatrix([bs(open(htmlFilePath))])
            scaler = MinMaxScaler()
            linkMatrix = scaler.fit_transform(oLinkMatrix)
            est = KMeans(n_clusters=2)
            y = est.fit_predict(linkMatrix)
            print metric(y, oGroundList)
        except:
            print(tb.format_exc())
            continue
    '''
    domList = []
    total = 0
    testRatio = 0.5
    search = False
    for num in range(0, 100):
        htmlFilePath = path.join(htmlFileDir, str(num+1)+'.html')
        try:
            domList.append(bs(open(htmlFilePath)))
            total += len(getLink(domList[-1]))
        except:
            continue
    print(total)
    (oLinkMatrix, oGroundList, oClusterIndex) = genMatrix(domList)
    
    dataList = [[oLinkMatrix[i], oGroundList[i]] for i in range(0, len(oGroundList))]
    job_n = 16
    trainRatioList = [float(i)/100 for i in range(1, 11)+range(10, 101,10)]
    for trainRatio in trainRatioList:
        turnNum = 100
        turn = 0
        precision = recall = f1_score = accuracy = 0
        while turn < turnNum:
            try:
                random.shuffle(dataList)
                linkMatrix = [dataList[i][0] for i in range(0, len(dataList))]
                groundList = [dataList[i][1] for i in range(0, len(dataList))]
                testBound = int(testRatio*len(groundList))
                upperBound = int(trainRatio*(1-testRatio)*len(groundList))
                scaler = StandardScaler()
                linkMatrix = scaler.fit_transform(linkMatrix)
                grid=None
                if search:
                    C_range = np.logspace(-2, 10, 13)
                    gamma_range = np.logspace(-9, 3, 13)
                    param_grid = dict(gamma = gamma_range, C = C_range)
                    cv = StratifiedShuffleSplit(groundList[0:upperBound], n_iter = 5, test_size = 0.2, random_state = 42)
                    grid = GridSearchCV(SVC(), param_grid = param_grid,  cv = cv, n_jobs = job_n)
                    grid.fit(linkMatrix[0:upperBound], groundList[0:upperBound])
                    clf = SVC(C = grid.best_params_['C'], gamma = grid.best_params_['gamma'])
                else:
                    C = float(upperBound/sum(groundList[0:upperBound]))
                    clf = SVC(C = 1, gamma = 0.10, kernel='rbf')
                clf.fit(linkMatrix[0:upperBound], groundList[0:upperBound])
                predict = clf.predict(linkMatrix[testBound+1:])
                tmp = metric(predict, groundList[testBound+1:])
                precision += tmp[0]
                recall += tmp[1]
                f1_score += tmp[2]
                accuracy += tmp[3]
                turn += 1
            except:
                continue
        print "%s, %s, %s, %s" % (precision/turnNum, recall/turnNum, f1_score/turnNum, accuracy/turnNum)

if __name__ == '__main__':
    main()
