###############################################################################
#
# Homework #5 - Iterators and Generators.
#
###############################################################################

import random


# -----------------------------------------------------------------------------
# Task 1 - Generator to read fasta file.
# -----------------------------------------------------------------------------

def fasta_reader(file_path):

    f = open(file_path)
    prev_id = None              # storage id-line between sequences reading
    while True:
        # looking for ID string '>...'
        if not prev_id:
            str1 = f.readline()
        else:
            str1 = prev_id
            prev_id = None
        if not str1:
            break
        if str1[0] != '>':
            continue
        str1 = str1.strip()
        # get next strings with sequence, seq can be several lines
        str2 = ''
        while True:
            s = f.readline()
            if not s:
                break
            s = s.strip()
            if s[0] != '>':
                str2 += s    # add line to sequence
            else:
                prev_id = s     # store id-line for the next sequence reading
                break
        if not str2:
            break
        yield str1, str2


def task1_test():

    reader = fasta_reader('sequences.fasta')
    print(type(reader))

    for id_, seq in reader:
        print(id_, seq[:50])


# -----------------------------------------------------------------------------
# Task 2 - Class for reading sequences with small changes.
# -----------------------------------------------------------------------------

class FasteChangingReader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.gen = fasta_reader(file_path)

    def __iter__(self):
        return self

    def _make_deletion(self, seq):
        # delete part of sequence in random place with random length
        start = random.randrange(len(seq))
        length = random.randint(1, 10)
        # print(f'start={start}, len={length}')
        return seq[:start] + seq[start + length:]

    def _make_insertion(self, seq):
        # insert random sequence in random place
        # to avoid mistakes with the letters - get them from current string
        iseq = ''
        for i in range(random.randint(1, 10)):
            iseq += seq[random.randrange(len(seq))]
        # print(iseq)
        place = random.randrange(len(seq))
        return seq[:place] + iseq + seq[place:]

    def _make_replacement(self, seq):
        # choosing 2 seq in random places with random
        # length 1-10 and swap them
        place1 = random.randrange(len(seq))
        place2 = random.randrange(len(seq))
        length = random.randint(1, 10)
        # print(f'p1={place1}, p2={place2}, l={length}')
        iseq1 = seq[place1: place1 + length]
        iseq2 = seq[place2: place2 + length]
        seq = seq[: place1] + iseq2 + seq[place1 + length:]
        seq = seq[: place2] + iseq1 + seq[place2 + length:]
        return seq

    def _random_change(self, seq):
        # print('org:', seq)
        operation = random.randint(1, 4)
        if operation == 1:
            seq = self._make_deletion(seq)
        elif operation == 2:
            seq = self._make_insertion(seq)
        elif operation == 3:
            seq = self._make_replacement(seq)
        else:
            pass  # no changes
        # print(f'ch{operation}:', seq)
        return seq

    def __next__(self):
        try:
            # try to get next sequence
            idx, seq = next(self.gen)
        except StopIteration:
            # restart generator
            self.gen = fasta_reader(self.file_path)
            idx, seq = next(self.gen)
        return idx, self._random_change(seq)


def task2_test():

    reader = FasteChangingReader('sequences.fasta')
    print(type(reader))

    count = 0
    for id_, seq in reader:
        print(id_, seq[:50])
        count += 1
        if count > 170:
            break


# -----------------------------------------------------------------------------
# Task 3 - Generator iter_append.
# -----------------------------------------------------------------------------
'''
def iter_append(iterable, item):

    it = iter(iterable)
    yield next(it)
    it

def task3_test():

    # test 1
    generator = iter_append([1, 2, 3, 4], 'ABCD')
    print(type(generator))
    for i in generator:
        print(i)

    # test 2
    filt = filter(lambda x: x % 2 == 0, [1, 2, 3, 4])
    generator = iter_append(filt, [5, 6, 7, 8])
    print(type(generator))
    for i in generator:
        print(i)
'''

if __name__ == "__main__":

    task1_test()
    # task2_test()
    # task3_test()
