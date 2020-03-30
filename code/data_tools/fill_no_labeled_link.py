from bs4 import BeautifulSoup
import sys
import os

def filterHtml(item):
    return item.endswith('html')

filePath = '../groundTruth/'
fileList = os.listdir(filePath)

fileList = filter(filterHtml, fileList)


for item in fileList:
    with open(filePath + item,'r+') as data:
        dom = BeautifulSoup(data)
        links = dom.find_all('a')
        for link in links:
            try:
                if not link.has_attr('cluster'):
                    print(link)
                    link['cluster'] = 'none'
            except:
                continue
        linkSet = dom.find_all('a')
        for link in linkSet:
            try:
                if not link.has_attr('cluster'):
                   print(link)
            except:
                continue
        
        # write back to file
        html = dom.prettify("utf-8")
        with open(filePath + item, "wb") as file:
            file.write(html)

print('write done')