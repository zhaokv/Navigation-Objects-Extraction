from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import adjusted_mutual_info_score

#transform linkClusterList into two list 'a' and 'b'
#   input:  the result of clustering links 'linkClusterList'
#   output: 'a' is the clustering result, 'b' is the ground truth
def tranResult(linkClusterList):
    a = []
    b = []
    for i in range(0, len(linkClusterList)):
        for link in linkClusterList[i]:
            if 'clusterindex' in link.attrs:
                a.append(i)
                b.append(link['clusterindex'])
    return (a, b)

#the Adjusted Rand index criterion for measuring hyperlink clustering results
#   input:  hyperlink clustering results 'linkClusterList'
#   output: Adjusted Rand Index 'aRandIndex'
def ari(linkClusterList):
    a, b = tranResult(linkClusterList)
    return adjusted_rand_score(a, b)

#the Adjusted Mutual Information criterion for measuring hyperlink clustering results
#   input:  hyperlink clustering results 'linkClusterList'
#   output: Adjusted Rand Index 'aRandIndex'
def ami(linkClusterList):
    a, b = tranResult(linkClusterList)
    return adjusted_mutual_info_score(a, b)

