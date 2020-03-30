from bs4 import BeautifulSoup as bs
from label_navi import calLinkChaotic as clc
from label_navi import calLinkRatio as clr
import scipy as sp
import numpy as np
import sys
import matplotlib.pyplot as plt


fileName = sys.argv[1]
dom = bs(open('../data/en-original/' + fileName))

nodeList = []
for des in dom.descendants:
    try:
        if des.name != None and des.find_all('a'):
            if ~np.isnan(clc(des)) and clc(des) >= 0:
                nodeList.append([clc(des), clr(des), len(des.find_all('a')), des.name])
    except:
        print(des.name)
        break
dataList = []
for node in nodeList:
    if node[2] > 1:
        dataList.append( [node[0], node[1] ])
dataList = np.array(dataList)

print(len(dataList))

k = len(dataList)
x = dataList[:,0]
y = dataList[:,1]
#n, bins, patches = P.hist(x, 10, histtype='step', stacked=True, fill=True)

plt.scatter( range( 1, (k+1)), x )

plt.grid()
plt.show()
