# HW5:  Iterators and Generators

HW5 requests to solve 2 tasks:
1. create generator to read fasta file;
1. create class for reading sequences with small changes.

## 1. Overview

Both tasks are in main.py python script.

## 2. Requirements

Code was tested on Ubuntu 20.04, Python 3.8.10.
There are no necessary python modules, except `random`.
To install this module: `pip install random`.

## 3. Task 1 - generator for reading Fasta file

I created generator for reading fasta file. Every call of the generator returns
pair of values (seq\_id, seq\_value).

## 4. Task 2 - iterator for reading Fasta with small changes.

I created iterator class and I re-used result of task 1 - fasta\_reader().
Every call of the iterator reads next sequence, makes some changes, and returns pair of
values (id, seq).
Sequence changes are random:
1. No changes - probability 25%
1. Deletion - probability 25%, removing 1-10 character from sequence
1. Insertion - probability 25%, insertion in random place of the new subsequence with the
length 1-10 characters.
1. Replacement - probability 25%, replace 2 subsequences in random positions
and with random length of 1-20 characters.

## 5. Execution

To execute you need to run script main.py as a single file application
`python main.py`:

* To run demonstration of work task1 - uncomment line `task1_test()` at the bottom of file.
* To run demonstration of work task2 - uncomment line `task2_test()` at the bottom of file.
