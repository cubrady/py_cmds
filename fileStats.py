import os
import sys
import progressbar
import argparse

KB = 1024
MB = KB * 1024
GB = MB * 1024

SORT_BY_NAME = 0
SORT_BY_FILE_COUNT = 1
SORT_BY_FILE_SIZE = 2


def __progressbar_pos(code):
    '''
    https://stackoverflow.com/questions/23113494/double-progress-bar-in-python
    '''
    sys.stdout.write(code)
    sys.stdout.flush()

def up_progressbar():
    __progressbar_pos('\x1b[1A')

def down_progressbar():
    __progressbar_pos('\n')

def formatNumber(num):
    return "{:,}".format(num)

def getFileSize(path):
    if os.path.exists(path):
        return float(os.stat(path).st_size)
    return 0.0

def formatSize(size):
    for unit, unitName in [(GB, "GB"), (MB, "MB"), (KB, "KB")]:
        if int(size) / unit > 0:
            return "%.2f %s" % (size / float(unit), unitName)
    return "%d Bytes" % size

def getFolderInfo(path):
    size = 0
    count = 0
    for dirPath, dirNames, fileNames in os.walk(path):
        up_progressbar()
        bar = progressbar.ProgressBar()
        for f in bar(fileNames):
            size += getFileSize(os.path.join(dirPath, f))
            count += 1

    return (count, size)

def getFileStatas(sort_key, path):
    rootFileCount, rootFileSize = 0, 0
    sumSize, sumCount = 0, 0
    lstResult = []
    maxLen = 0

    file_list = []
    if not path:
        file_list = os.listdir(".")
    elif os.path.isfile(path):
        file_list = [path]
    else:
        file_list = os.listdir(path)

    down_progressbar()
    bar = progressbar.ProgressBar()
    for p in bar(file_list):
        full_path = os.path.join(path, p)
        if os.path.isdir(full_path):
            if len(full_path) > maxLen:
                maxLen = len(full_path)
            c, s = getFolderInfo(full_path)
            lstResult.append((full_path, c, s))
            sumSize += s
            sumCount += c
        else:
            rootFileSize += getFileSize(full_path)
            rootFileCount += 1

    lstResult.insert(0, ("..", rootFileCount, rootFileSize))

    sumSize += rootFileSize
    sumCount += rootFileCount

    lstResult = sorted(lstResult, key = lambda x : x[sort_key])

    strFormat = "%%%ds" % maxLen
    for folder, c, s in lstResult:
        sizePercent = 0 if sumSize == 0.0 else 100 * s / sumSize
        print "%s  %8s files  %10s %10.2f %%" % ((strFormat % folder), formatNumber(c), formatSize(s), sizePercent)
    print "=" * 20 + " Summary " + "=" * 20
    print "File count:%s, size:%s" % (formatNumber(sumCount), formatSize(sumSize))

def parseKey(sort_by):
    try:
        key = int(sort_by)
    except:
        print "[Warning] Invalid argument : %s" % cmd_args.sort_by
        key = SORT_BY_NAME

    if key > SORT_BY_FILE_SIZE or key < SORT_BY_NAME:
        print "[Warning] Unsupported sort key : %d" % key
        key = SORT_BY_NAME
    
    return key

if __name__ == '__main__':
    cmd_arg_parser = argparse.ArgumentParser()

    cmd_arg_parser.add_argument(
        '-s', action='store', dest='sort_by', default="0",
        help='Sort shown files by {0:name , 1:file counts ,2:fils size}'
    )

    cmd_arg_parser.add_argument(
        '-p', action='store', dest='path', default="",
        help='Show the file status of specified path instead of current directory'
    )

    cmd_args = cmd_arg_parser.parse_args()

    getFileStatas(parseKey(cmd_args.sort_by), path = cmd_args.path)
