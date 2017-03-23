import os

KB = 1024
MB = KB * 1024
GB = MB * 1024

def formatNumber(num):
    return "{:,}".format(num)

def getFileSize(path):
    return os.stat(path).st_size

def formatSize(size):
    for unit, unitName in [(GB, "GB"), (MB, "MB"), (KB, "KB")]:
        if size / unit > 0:
            return "%.2f %s" % (size / float(unit), unitName)
    return "%d Bytes" % size

def getFolderInfo(path):
    size = 0
    count = 0
    for dirPath, dirNames, fileNames in os.walk(path):
        #print dirPath
        for f in fileNames:
            size += getFileSize(os.path.join(dirPath, f))
            count += 1

    return (count, size)

if __name__ == '__main__':
    rootFileCount, rootFileSize = 0, 0
    sumSize, sumCount = 0, 0
    lstResult = []
    maxLen = 0
    lst = os.listdir(".")

    for p in lst:
        if os.path.isdir(p):
            if len(p) > maxLen:
                maxLen = len(p)
            c, s = getFolderInfo(p)
            lstResult.append((p, c, s))
            sumSize += s
            sumCount += c
        else:
            rootFileSize += getFileSize(p)
            rootFileCount += 1

    lstResult.insert(0, ("..", rootFileCount, rootFileSize))

    sumSize += rootFileSize
    sumCount += rootFileCount

    strFormat = "%%%ds" % maxLen
    for folder, c, s in lstResult:
        print "%s  %8s files  %10s" % ((strFormat % folder), formatNumber(c), formatSize(s))
    print "=" * 20 + " Summary " + "=" * 20
    print "File count:%s, size:%s" % (formatNumber(sumCount), formatSize(sumSize))
