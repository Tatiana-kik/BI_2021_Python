#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import sys
import locale
import functools


# process request
def process(files):

    result = []

    # iterate by files
    for fname in files:
        # work with wile or stdin
        if fname == '-':
            f = sys.stdin
        else:
            try:
                f = open(fname, 'rt')
            except Exception as e:
                print(e)
                return 2

        # collect lines
        for line in f:
            result.append(line[:-1])  # collect without last '\n'

    # do sorting accorsing with current locale
    # NOTE:  I really don't understand this magic, but to sort like
    #        coreutils sort I need:
    #          1) set the same locale like my current locale  # Why? o__O
    #          2) set key=locale.strcoll
    # locale.setlocale(locale.LC_COLLATE, locale.getlocale())

    result.sort(key=functools.cmp_to_key(locale.strcoll))
    print(*result, sep='\n')
    return 0


descr = (
  'Write sorted concatenation of all FILE(s) to standard output.\n\n'
  'With no FILE, or when FILE is -, read standard input.')

epilog = (
  '*** WARNING ***\n'
  'The locale specified by the environment affects sort order.\n'
  'Set LC_ALL=C to get the traditional sort order that uses\n'
  'native byte values.')


# entry point
def main():

    # configure arguments

    usage = "sort.py [FILE]..."

    parser = argparse.ArgumentParser(description=descr, epilog=epilog,
                                     usage=usage,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('files', metavar='FILE', nargs='*',
                        help='input files', default='-')
    args = parser.parse_args()

    # prepare arguments

    # make file list if need
    files = args.files
    if not isinstance(files, list):
        files = [files]

    # process the request
    return process(files)


if __name__ == '__main__':

    ecode = main()
    sys.exit(ecode)
