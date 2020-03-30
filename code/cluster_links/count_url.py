import os


def main():
    dataDir = '../data/clean_eval'
    outputFilePath = '../data/output/count_url.txt'
    urlDic = {}
    for dataFileNum in range(60, 800):
        with open(os.path.join(dataDir, str(dataFileNum)+'.html')) as dataFile:
            firstLine = dataFile.readline()
            urlStart = firstLine.find('\"') + 1
            urlEnd = firstLine.find('\"', urlStart)
            url = firstLine[urlStart: urlEnd]
            if url not in urlDic:
                urlDic[url] = []
            urlDic[url].append(dataFileNum)
    with open(outputFilePath, 'w') as outputFile:
        for url in sorted(urlDic):
            outLine = url
            for dataFileNum in urlDic[url]:
                outLine += (' ' + str(dataFileNum))
            outLine += '\n'
            outputFile.write(outLine)

if __name__ == '__main__':
    main()
