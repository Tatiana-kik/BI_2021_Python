#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import os
import sys
import shutil


# process request
def process(input_files, f_recursive):

    ecode = 0

    for file_name in input_files:
        try:
            if os.path.isdir(file_name):
                if not f_recursive:
                    ecode = 1
                    print(f'[Error] Cannot remove \'{file_name}\':'
                          ' Is a directory')
                    continue
                if file_name == '.' or file_name == '..':
                    ecode = 1
                    print(f'[Error] Refusing to remove \'.\' or \'..\':'
                          f' skipping \'{file_name}\'')
                    continue
                if file_name == '/':
                    ecode = 1
                    print(f'[Error] It is dangerous to operate recursively on'
                          f'\'/\': skipping \'{file_name}\'')
                    continue
                # remove dir
                shutil.rmtree(file_name)
            elif os.path.exists(file_name):  # isfile
                # remove file
                os.remove(file_name)
            else:
                ecode = 1
                print(f'[Error] Cannot remove \'{file_name}\': '
                      'No such file or directory')
        except Exception as e:
            ecode = 1
            print(f'[Error] Cannot remove \'{file_name}\': {e}')

    return ecode


descr = 'Remove (unlink) the FILE(s).'

epilog = (
  'Note that if you use rm to remove a file, it might be possible to recover\n'
  'some of its contents, given sufficient expertise and/or time. For greater\n'
  'assurance that the contents are truly unrecoverable, consider using shred.')


# entry point
def main():

    # configure arguments

    usage = "rm.py [OPTION]... [FILE]..."

    parser = argparse.ArgumentParser(description=descr, epilog=epilog,
                                     usage=usage,
                                     formatter_class=RawTextHelpFormatter)
    hlp = 'remove directories and their contents recursively'
    parser.add_argument('-r', '--recursive',
                        action='store_true',
                        help=hlp)
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='input files', default='.')
    args = parser.parse_args()

    # prepare arguments

    # make file list if need
    files = args.files
    if not isinstance(files, list):
        files = [files]

    # process the request
    return process(files, args.recursive)


if __name__ == '__main__':

    ecode = main()
    sys.exit(ecode)
