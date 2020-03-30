#get metrics for the classification results
#   input:  the classification results "result"
#           the ground truth "ground"
#   output: the metrice (precision, recall, accuracy,f1-score):
#   hit:    1 in result represents "is navi" and 0 "is not navi"
def metric(result, ground):
    tpNum = 0
    tnNum = 0
    fpNum = 0
    fnNum = 0
    for i in range(0, len(result)):
        if result[i] == 1 and ground[i] == 1:
            tpNum += 1.0
        if result[i] == 0 and ground[i] == 0:
            tnNum += 1.0
        if result[i] == 1 and ground[i] == 0:
            fpNum += 1.0
        if result[i] == 0 and ground[i] == 1:
            fnNum += 1.0
    if tpNum+fpNum == 0:
        precision = 1.0
    else:
        precision = tpNum/(tpNum + fpNum)
    if tpNum+fnNum == 0:
        recall = 1.0
    else:
        recall = tpNum/(tpNum + fnNum)
    if tpNum+tnNum+fpNum+fnNum == 0:
        accuracy = 1.0
    else:
        accuracy = (tpNum + tnNum)/(tpNum + tnNum + fpNum + fnNum)
    if precision+recall == 0:
        f1_score = 0
    else:
        f1_score = 2*precision*recall/(precision+recall)
    return (precision, recall, f1_score, accuracy)
