#!/usr/bin/python

import sqlite3
import codecs

from os import path
from os import mkdir

def selectMyriad(dataDir):
    dbFilePath = path.join(dataDir, 'myriad.db')
    conn = sqlite3.connect(dbFilePath)
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT Source FROM Pages')
    sourceList = cur.fetchall()
    for i in range(0, len(sourceList)):
        source = "'%s'" % sourceList[i]
        cur.execute('SELECT HTML FROM Pages WHERE Source = %s limit 1' % source)
        page = cur.fetchall()[0][0]
        with codecs.open(path.join(dataDir, str(i)+'.html'), 'w', 'utf-8') as htmlFile:
            htmlFile.write(page)

def selectBig5(dataDir):
    dbFilePath = path.join(dataDir, 'ate.db')
    conn = sqlite3.connect(dbFilePath)
    cur = conn.cursor()
    sourceList = ['suntimes.com', 'techweb.com', 'nypost.com', 'freep.com', 'chicagotribune.com']
    for i in range(0, len(sourceList)):
        outDir = path.join(dataDir, sourceList[i])
        if not path.exists(outDir):
            mkdir(path.join(dataDir, sourceList[i]))
        source = "'%s'" % sourceList[i]
        begin = 1
        end = 11
        cur.execute('SELECT HTML FROM Pages WHERE Source = %s limit %s,%s' % (source, begin, end))
        results = cur.fetchall()
        for j in range(begin, end):
            page = results[j][0]
            with codecs.open(path.join(outDir, str(j)+'.html'), 'w', 'utf-8') as htmlFile:
                htmlFile.write(page)
    

def main():
    dataDir = '../../data/MSS/Myriad'
    selectMyriad(dataDir)
    
    dataDir = '../../data/MSS/Big5'
    selectBig5(dataDir)

if __name__ == '__main__':
    main()
