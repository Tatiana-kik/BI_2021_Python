'''
Homework #5 - Iterators and Generators.
'''

import random


# -----------------------------------------------------------------------------
# Task 1 - Generator to read fasta file.
# -----------------------------------------------------------------------------

def fasta_reader(file_path: str):
    '''
    This function is a generator to read FASTA file.
    Parameter:
        file_path - path to FASTA file.
    Yield values:
        idx - sequence ID
        seq - sequence body
    '''
    f = open(file_path)
    prev_id = None              # storage id-line between sequences reading
    while True:
        # looking for ID string '>...'
        if not prev_id:
            idx = f.readline()
        else:
            idx = prev_id
            prev_id = None
        if not idx:
            break
        if idx[0] != '>':
            continue
        idx = idx.strip()
        # get next strings with sequence, seq can be several lines
        seq = ''
        while True:
            s = f.readline()
            if not s:
                break
            s = s.strip()
            if s[0] != '>':
                seq += s        # add line to sequence
            else:
                prev_id = s     # store id-line for the next sequence reading
                break
        if not seq:
            break
        yield idx, seq


def task1_test():

    reader = fasta_reader('sequences.fasta')
    print(type(reader))

    for id_, seq in reader:
        print(id_, seq[:50])


# -----------------------------------------------------------------------------
# Task 2 - Class for reading sequences with small changes.
# -----------------------------------------------------------------------------

class FastaChangingReader:
    '''
    This class is iterator that every call reads the next sequence
    from file, makes small random changes of sequence and returns
    two values: id and seq.
    '''
    def __init__(self, file_path: str):
        '''
        Parameter:
            file_path - path to FASTE file.
        '''
        self.file_path = file_path
        self.gen = fasta_reader(file_path)

    def __iter__(self):
        return self

    def _make_deletion(self, seq: str) -> str:
        '''
        Delete part of sequence in random place with random length.
        '''
        start = random.randrange(len(seq))
        length = random.randint(1, 10)
        # print(f'start={start}, len={length}')
        return seq[:start] + seq[start + length:]

    def _make_insertion(self, seq: str) -> str:
        '''
        Insert random sub-sequence in random place.
        To don't make mistake with the letter - get them from current
        string.
        '''
        iseq = ''
        for i in range(random.randint(1, 10)):
            iseq += seq[random.randrange(len(seq))]
        # print(iseq)
        place = random.randrange(len(seq))
        return seq[:place] + iseq + seq[place:]

    def _make_replacement(self, seq: str) -> str:
        '''
        Replace some sun-sequence with random length in random place
        with another one sub-sequences with the same length in anothe
        random place.
        '''
        place1 = random.randrange(len(seq))
        place2 = random.randrange(len(seq))
        length = random.randint(1, 10)
        # print(f'p1={place1}, p2={place2}, l={length}')
        iseq1 = seq[place1: place1 + length]
        iseq2 = seq[place2: place2 + length]
        seq = seq[: place1] + iseq2 + seq[place1 + length:]
        seq = seq[: place2] + iseq1 + seq[place2 + length:]
        return seq

    def _random_change(self, seq: str) -> str:
        '''
        Do small random changing of sequence.
        '''
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
        '''
        Implementation of Iterator Protocol - access to the next item.
        Return value:
            idx - sequence ID
            seq - sequence body
        '''
        try:
            # try to get next sequence
            idx, seq = next(self.gen)
        except StopIteration:
            # restart generator
            self.gen = fasta_reader(self.file_path)
            idx, seq = next(self.gen)
        return idx, self._random_change(seq)


def task2_test():

    reader = FastaChangingReader('sequences.fasta')
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

def iter_append(iterable, item):
    '''
    This function is a generator to iterate in some iterable object and
    append the item after the last iteration in iterable
    Parameter:
        iterable - some iterable object.
    Yield value:
        item from iterable, or
        appended item
    '''
    yield from iterable  # to don't use cycles use 'yield from'
    yield item


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


# -----------------------------------------------------------------------------
# Task 4 - Nested list unpacker.
# -----------------------------------------------------------------------------

# generator to unpack nested list recursively
def unpack_nested_list(lst: list):
    '''
    This function is a generator that unpacks nested list.
    Parameter:
        lst - nested list to unpack
    Yield values:
        list item or nested list item
    '''
    for i in lst:
        if type(i) is list:
            yield from unpack_nested_list(i)
        else:
            yield i


# target function to make list by using generator
def nested_list_unpacker(lst: list) -> list:
    '''
    This function is just a wrapper to transform result of generator
    to a list.
    '''
    return list(unpack_nested_list(lst))


# test of task 4
def task4_test():

    lst = [1, 2, 3, [1, 2, [3, 4, []], [1], [], 12, 3], [1, [5, 6]]]
    print(nested_list_unpacker(lst))


if __name__ == "__main__":

    # help(fasta_reader)
    task1_test()
    # task2_test()
    # task3_test()
    # task4_test()
