import codecs
import os
import sqlite3

sq = sqlite3.connect('../data/myriad.db')
cu = sq.cursor()
cu.execute('select * from Pages')
dataList = cu.fetchall()
for data in dataList:
    documentId = data[0]
    html = data[4]
    htmlFilePath = os.path.join('../data/output/html', str(documentId)+'.html')
    with codecs.open(htmlFilePath, 'w', 'utf-8') as htmlFile:
        htmlFile.write(html)
    cu.execute('select * from Extractions where DocumentID = %s and Quality = 1' %documentId)
    extrInfoList = cu.fetchall()
    extrFilePath = os.path.join('../data/output/extr', str(documentId)+'.txt')
    with codecs.open(extrFilePath, 'w', 'utf-8') as extrFile:
        for extrInfo in extrInfoList:
            extrData = html[extrInfo[3]:extrInfo[3]+extrInfo[2]]
            extrFile.write(extrData)
            extrFile.write('\n\n')
