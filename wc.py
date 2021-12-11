#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import sys


# print table with column alignment
def print_table(list_of_lists):

    # find max lengths to make alignment
    max_num = 0
    for lst in list_of_lists:
        # check that lst contents numbers
        if isinstance(lst[0], int):
            for i in range(len(lst) - 1):
                max_num = max(max_num, lst[i])
        else:
            # if error exist - increase column space as in original `wc`
            max_num = max(max_num, 12345678)

    # print table with column alignment
    max_len = len(str(max_num))
    for lst in list_of_lists:
        # check that lst contents numbers
        if isinstance(lst[0], int):
            # print first column
            print("{0:>{1}}".format(lst[0], max_len), end='')
            # print next columns with 1 space between them
            for i in range(1, len(lst) - 1):
                print("{0:>{1}}".format(lst[i], max_len + 1), end='')
            # print last column with file name with left alignment
            print("", lst[-1])
        else:
            # print stored error message
            print(lst[0])


# process request
def process(files, f_lines, f_words, f_bytes):

    ecode = 0
    result = []
    total_l = 0
    total_w = 0
    total_b = 0

    # iterate by files
    for fname in files:
        res = []
        # work with wile or stdin
        if fname == '-':
            f = sys.stdin
        else:
            try:
                f = open(fname, 'rt')
            except Exception as e:
                # store error
                ecode = 1
                res = [e]
                result.append(res)
                continue

        # count
        num_l = num_w = num_b = 0
        for line in f:
            num_l += 1
            num_b += len(line)
            num_w += len(line.split())

        # store counters according with flags
        if f_lines:
            total_l += num_l
            res.append(num_l)
        if f_words:
            total_w += num_w
            res.append(num_w)
        if f_bytes:
            total_b += num_b
            res.append(num_b)

        # add file name
        if not fname == '-':
            res.append(f.name)
        else:
            res.append('')

        # store counters for the file
        result.append(res)

    # add summury counters if need
    if len(result) > 1:
        total = []
        if f_lines:
            total.append(total_l)
        if f_words:
            total.append(total_w)
        if f_bytes:
            total.append(total_b)
        total.append('total')
        result.append(total)

    print_table(result)
    return ecode


descr = (
  'Print newline, word, and byte counts for each FILE, and a total line if\n'
  'more than one FILE is specified. A word is a non-zero-length sequence of\n'
  'characters delimited by white space.\n\n'
  'With no FILE, or when FILE is -, read standard input.\n\n'
  'The options below may be used to select which counts are printed, always in'
  '\nthe following order: newline, word, byte.\n')


# entry point
def main():

    # configure arguments

    usage = "wc.py [OPTION]... [FILE]..."

    parser = argparse.ArgumentParser(description=descr,
                                     usage=usage,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-l', '--lines',
                        action='store_true',
                        help='print the newline counts')
    parser.add_argument('-w', '--words',
                        action='store_true',
                        help='print the word counts')
    parser.add_argument('-c', '--bytes',
                        action='store_true',
                        help='print the byte counts')
    parser.add_argument('files', metavar='FILE', nargs='*',
                        help='input files', default='-')
    args = parser.parse_args()

    # prepare arguments

    # make file list if need
    files = args.files
    if not isinstance(files, list):
        files = [files]

    # prepare flags
    if not args.lines and not args.words and not args.bytes:
        f_lines = f_words = f_bytes = True
    else:
        f_lines = args.lines
        f_words = args.words
        f_bytes = args.bytes

    # process the request
    return process(files, f_lines, f_words, f_bytes)


if __name__ == '__main__':

    ecode = main()
    sys.exit(ecode)
