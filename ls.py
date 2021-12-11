#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import os
import sys
import math


# print content of one directory
def print_dir_content(content):

    # work with according to termainal length
    terminal_len = os.get_terminal_size()[0]

    # make attempts to place content in 1 line, if not - in 2 lines, ...
    found_lines = 0
    found_column_lengths = []
    for lines in range(1, 1000):

        columns = math.ceil(len(content) / lines)
        column_lengths = []

        # go through each column
        for i in range(columns):
            column_content = content[i * lines: (i+1) * lines]
            ln = len(max(column_content, key=len))
            column_lengths.append(ln)

        if sum(column_lengths) + 2 * columns <= terminal_len:
            found_lines = lines
            found_column_lengths = column_lengths
            break

    # print table with found_lines lines
    found_columns = len(found_column_lengths)
    for i in range(found_lines):
        for j in range(found_columns):
            idx = j * found_lines + i
            if idx >= len(content):
                break
            print("{0:<{1}}  ".format(content[idx],
                  found_column_lengths[j]), end='')
        print()


# print table with column alignment as in original ls
def print_table(list_of_content):

    # go through the files
    for k in range(len(list_of_content)):

        file_name = list_of_content[k][0]
        content = list_of_content[k][1]

        # content could be:
        #   list of files - for directory
        #   None          - for file
        #   error         - for error case
        if content is None:

            print(file_name)

        elif isinstance(content, list):

            if len(list_of_content) > 1:
                print(f'{file_name}:')
            print_dir_content(content)

        else:  # error case

            print(f'{file_name}:  {content}')

        # add empty line if not last iteration
        if k < (len(list_of_content) - 1):
            print()


# make float value for sorting file names like original ls
def get_value(word):

    val = 0.0
    if word[0] == '.':
        word = word[1:]      # skip first dot
    for i in range(len(word)):
        ch = word[i]
        div = 10 ** (4 * i)  # make 4 decimal position for each lette
        if ch.islower():
            val += (ord(ch) * 10) / div
        else:
            val += (ord(ch.lower()) * 10 + 1) / div
    # print('--', word, val)
    return val


# process request
def process(input_files, f_all):

    ecode = 0

    # sorting input files like original ls
    input_files.sort(key=get_value)

    list_of_content = []
    for file_name in input_files:
        try:
            if os.path.isdir(file_name):
                content = os.listdir(file_name)
                # sorting output files like original ls
                content.sort(key=get_value)
                if f_all:
                    # add directories . and ..
                    content.insert(0, '..')
                    content.insert(0, '.')
                else:
                    # remove files started from dot
                    for name in list(content):  # iterating on a copy
                        if name[0] == '.':
                            content.remove(name)
                list_of_content.append((file_name, content))
            elif os.path.exists(file_name):  # isfile
                list_of_content.append((file_name, None))
            else:
                # store error
                ecode = 2
                list_of_content.append((file_name,
                                        '[Error] No such file or directory'))
        except Exception as e:
            # store error
            ecode = 2
            list_of_content.append((file_name, e))

    print_table(list_of_content)
    return ecode


descr = (
  'List information about the FILEs (the current directory by default).\n'
  'Sort entries alphabetically.')


# entry point
def main():

    # configure arguments

    usage = "ls.py [OPTION]... [FILE]..."

    parser = argparse.ArgumentParser(description=descr,
                                     usage=usage,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-a', '--all',
                        action='store_true',
                        help='do not ignore entries starting with .')
    parser.add_argument('files', metavar='FILE', nargs='*',
                        help='input files', default='.')
    args = parser.parse_args()

    # prepare arguments

    # make file list if need
    files = args.files
    if not isinstance(files, list):
        files = [files]

    # process the request
    return process(files, args.all)


if __name__ == '__main__':

    ecode = main()
    sys.exit(ecode)
