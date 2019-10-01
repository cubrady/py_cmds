import os
import sys
import progressbar
import argparse
from natsort import natsorted

KB = 1024
MB = KB * 1024
GB = MB * 1024

SORT_BY_NAME = 0
SORT_BY_FILE_COUNT = 1
SORT_BY_FILE_SIZE = 2
SORT_BY_AVG_FILE_SIZE = 3
__KEYS = [SORT_BY_NAME, SORT_BY_FILE_COUNT, SORT_BY_FILE_SIZE, SORT_BY_AVG_FILE_SIZE]


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

def format_number(num):
    return "{:,}".format(num)

def get_file_size(path):
    if os.path.exists(path):
        return float(os.stat(path).st_size)
    return 0.0

def format_size(size):
    for unit, unitName in [(GB, "GB"), (MB, "MB"), (KB, "KB")]:
        if int(size) / unit > 0:
            size_unit = size / float(unit)
            formatter = "%.1f %s" if size_unit > 100. else "%.2f %s"
            return formatter % (size_unit, unitName)
    return "%d Bytes" % size

def get_folder_info(path):
    size = 0
    count = 0
    for dir_path, _, file_names in os.walk(path):
        up_progressbar()
        bar = progressbar.ProgressBar()
        for f in bar(file_names):
            size += get_file_size(os.path.join(dir_path, f))
            count += 1

    return (count, size)

def get_file_statas(sort_key, path):
    root_file_count, root_file_size = 0, 0
    sum_size, sum_count = 0, 0
    lst_result = []
    maxLen = 0

    file_list = []
    if not path:
        file_list = os.listdir(".")
    elif os.path.isfile(path):
        file_list = [path]
    else:
        file_list = os.listdir(path)

    def __add_folder_info(full_path, file_count, file_size, insert_idx = -1):
        info = [full_path, file_count, file_size]
        info.append(file_size / float(file_count) if file_count != 0 else 0.)
        if insert_idx != -1:
            lst_result.insert(insert_idx, info)
        else:
            lst_result.append(info)

    down_progressbar()
    bar = progressbar.ProgressBar()
    for p in bar(file_list):
        full_path = os.path.join(path, p)
        if os.path.isdir(full_path):
            if len(full_path) > maxLen:
                maxLen = len(full_path)
            file_count, file_size = get_folder_info(full_path)
            __add_folder_info(full_path, file_count, file_size)
            sum_size += file_size
            sum_count += file_count
        else:
            root_file_size += get_file_size(full_path)
            root_file_count += 1

    __add_folder_info("..", root_file_count, root_file_size, insert_idx = 0)

    sum_size += root_file_size
    sum_count += root_file_count

    lst_result = natsorted(lst_result, key = lambda x : x[sort_key])

    strFormat = "%%%ds" % maxLen
    print ("%s %14s %13s %13s %12s" % (strFormat % "Folder", "File Count", "Files Size", "Averege", "Ratio"))
    for folder, c, s, avg_size in lst_result:
        sizePercent = 0 if sum_size == 0.0 else 100 * s / sum_size
        print ("%s  %8s files  %13s %13s %10.2f %%" % ((strFormat % folder), format_number(c), format_size(s), format_size(avg_size), sizePercent))
    avg_size = sum_size / sum_count if sum_count > 0. else 0.
    print ("=" * 40 + " Summary " + "=" * 40)
    print ("File count:%s, size:%s, avg:%s" % (format_number(sum_count), format_size(sum_size), format_size(avg_size)))

def parseKey(sort_by):
    try:
        key = int(sort_by)
    except:
        print ("[Warning] Invalid argument : %s" % cmd_args.sort_by)
        key = SORT_BY_NAME

    if key not in __KEYS:
        print ("[Warning] Unsupported sort key : %d" % key)
        key = SORT_BY_NAME
    
    return key

if __name__ == '__main__':
    cmd_arg_parser = argparse.ArgumentParser()

    cmd_arg_parser.add_argument(
        '-s', action='store', dest='sort_by', default="0",
        help='Sort shown files by {0:name, 1:file counts, 2:fils size, 3:average file size}'
    )

    cmd_arg_parser.add_argument(
        '-p', action='store', dest='path', default="",
        help='Show the file status of specified path instead of current directory'
    )

    cmd_args = cmd_arg_parser.parse_args()

    get_file_statas(parseKey(cmd_args.sort_by), path = cmd_args.path)
