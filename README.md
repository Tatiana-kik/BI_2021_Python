# Homework modules os and sys

## Overview
This repo contains 4 utilites (ls.py, wc.py, sort.py, rm.py) that are similar in their fuctionality to the coreutils.<br>
All these utilities cover the basic functionality of analogous coreutils.<br>
Each utilite has embedded help info that you can see by executing programm with key "-h" or "--help".

## ls.py

### Installation
The program is written and tested in Python 3.8.10.<br>
To use the programm it is enough to clone this repo:<br>
`git clone -b modules git@github.com:Tatiana-kik/BI_2021_Python.git`<br>
`cd BI_2021_Python`

### Functionality
List information about the FILEs (the current directory by default).<br>
Sort entries alphabetically.

### Usage and examples

#### Usage:
`ls.py [OPTION]... [FILE]...`

#### Positional arguments
* FILE - input files

#### Optional arguments
* -h, --help  show this help message and exit
* -a, --all   do not ignore entries starting with .

#### Examples
* List files in current directory 
`/ls.py` or `./ls.py .`

* List all files (including started from dot) in parent directory
`./ls.py -a ..`

* List all python files in current directory
`./ls.py *.py`


## wc.py

### Installation
The program is written and tested in Python 3.8.10.<br>
To use the programm it is enough to clone this repo:<br>
`git clone -b modules git@github.com:Tatiana-kik/BI_2021_Python.git`<br>
`cd BI_2021_Python`

### Functionality
Print newline, word, and byte counts for each FILE, and a total line if more than one FILE is specified. A word is a non-zero-length sequence of characters delimited by white space.

### Usage and examples

#### Usage
`wc.py [OPTION]... [FILE]...`

With no FILE, or when FILE is -, read standard input.

The options below may be used to select which counts are printed, always in the following order: newline, word, byte.

#### Positional arguments
* FILE - input files

#### Optional arguments
* -h, --help   show this help message and exit
* -l, --lines  print the newline counts
* -w, --words  print the word counts
* -c, --bytes  print the byte counts

#### Examples
* Show all counters for the file example.txt
`./wc.py example.txt` or `cat example.txt | ./wc.py`

* Show line counters for all python files in current directory
`./wc.py -l *.py`

* Show character and word counters for the stdin stream
`./wc.py -c -l -`


## sort.py

### Installation
The program is written and tested in Python 3.8.10.<br>
To use the programm it is enough to clone this repo:<br>
`git clone -b modules git@github.com:Tatiana-kik/BI_2021_Python.git`<br>
`cd BI_2021_Python`

### Functionality
Write sorted concatenation of all FILE(s) to standard output.

With no FILE, or when FILE is -, read standard input.

*** WARNING ***
The locale specified by the environment affects sort order.
Set LC_ALL=C to get the traditional sort order that uses
native byte values.

### Usage and examples

#### Usage:
`sort.py [FILE]...`

#### Positional arguments
  FILE        input files

#### Optional arguments
  -h, --help  show this help message and exit

#### Examples

* Sort the lines of the file example.txt
`./sort.py example.txt` or `cat example.txt | ./sort.py `

* Sort the lines of all python files in current directory
`./sort.py *.py`

* Sort the lines of the stdin stream
`./sort.py -`


## rm.py

### Installation
The program is written and tested in Python 3.8.10.<br>
To use the programm it is enough to clone this repo:<br>
`git clone -b modules git@github.com:Tatiana-kik/BI_2021_Python.git`<br>
`cd BI_2021_Python`

### Functionality
Remove (unlink) the FILE(s).

### Usage and examples

#### Usage
`rm.py [OPTION]... [FILE]...`

#### Positional arguments
* FILE - input files

#### Optional arguments
* -h, --help - show this help message and exit
* -r, --recursive -- remove directories and their contents recursively

Note that if you use rm to remove a file, it might be possible to recover
some of its contents, given sufficient expertise and/or time. For greater
assurance that the contents are truly unrecoverable, consider using shred.

#### Examples

* Remove fire example.txt
`./rm.py example.txt`

* Remove directory Example and with all content
`./rm.py -r Example`

* Remove all python files in home directory
`./rm.py ~/*.py`

