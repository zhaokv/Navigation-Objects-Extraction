#This program is used to remove the text tag from dataSet

import os


def main():
    dataDir = '../data/clean_eval'
    dataOutDir = '../data/clean_eval'
    fileNumBegin = 1
    fileNumEnd = 797
    for dataFileNum in range(fileNumBegin, fileNumEnd+1):
        with open(os.path.join(dataDir, str(dataFileNum)+'.html')) as dataFile:
            fileLines = dataFile.readlines()
            with open(os.path.join(dataOutDir, str(dataFileNum)+'.html'), 'w') as outputFile:
                for lineNum in range(1, len(fileLines)-2):
                    outputFile.write(fileLines[lineNum])

if __name__ == '__main__':
    main()
