###############################################################################
#
#  Random homework
#
###############################################################################

import time
import sys
import random
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# show distribution Random-Generating-Time from Numbers-Count
def task_1():

    seq_lengths = [i * 1000 * 1000 for i in range(8)]
    print(seq_lengths)

    sys_rnd_dur = []     # random gen durations for system random()
    np_rnd_dur = []      # random gen durations for numpy random()
    npseq_rnd_dur = []   # random gen durations for numpy random(arr_len)

    rnds = range(seq_lengths[-1])  # trying to allocate big list befor test

    for ln in seq_lengths:

        print(ln)
        rnds = []
        # system random
        t1 = time.time()
        for n in range(ln):
            rnds.append(random.random())
        t2 = time.time()
        # print(rnds)
        sys_rnd_dur.append(t2 - t1)

        # numpy random
        rnds = []
        t1 = time.time()
        for n in range(ln):
            rnds.append(np.random.rand())
        t2 = time.time()
        # print(rnds)
        np_rnd_dur.append(t2 - t1)

        # numpy random sequence
        rnds = []
        t1 = time.time()
        rnds = np.random.random(ln)
        t2 = time.time()
        # print(rnds)
        npseq_rnd_dur.append(t2 - t1)

    # image creation example
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)
    ax.set(title='Dependency random generation duration from sequence length',
           ylabel='Duration of generating one sequence, sec',
           xlabel='Number of randoms in one sequence')
    ax.plot(seq_lengths, sys_rnd_dur, label="for i in range(len):  random()")
    ax.plot(seq_lengths, np_rnd_dur, label='for i in range(len):  np.random()')
    ax.plot(seq_lengths, npseq_rnd_dur, label='np.random.random(len)')

    # ax.set_xticklabels(seq_lengths)
    # print(seq_lengths)

    print(f'sysrnd:    {sys_rnd_dur}')
    print(f'nprnd:     {np_rnd_dur}')
    print(f'npseqrnd:  {npseq_rnd_dur}')

    plt.legend()
    plt.show()

    return rnds  # return list to avoid optimisation


# -----------------------------------------------------------------------------
# Investigation of Monkey Sort
def is_list_sorted(lst):

    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False

    return True


def monkey_sort(lst):

    while not is_list_sorted(lst):
        np.random.shuffle(lst)
        # print(lst)


def task_2():

    max_list_len = 9
    attempts = 100

    dur_by_length = []
    mean_line_x = []
    mean_line_y = []

    # make measurement
    for l in range(1, max_list_len + 1):
        print(f'Measure duration for len={l}/{max_list_len}:  ', end='')
        durs = []  # sort durations for current list length
        for i in range(attempts):
            # create random list
            lst = list(np.random.randint(0, 1000, l))
            #  print(lst)
            t1 = time.time()
            monkey_sort(lst)
            t2 = time.time()
            dur = t2 - t1
            durs.append(dur)
            if not i % 10:
                # print progress
                print('.', end='')
                sys.stdout.flush()
            # print(f'dur:  {dur}')
        dur_by_length.append(durs)
        mean_line_x.append(l)
        mean_line_y.append(sum(durs) / len(durs))
        print('')  # new line
    # print(dur_by_length)
    # print(len(dur_by_length))
    # print(mean_line_x)
    # print(mean_line_y)

    # draw diagram
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)
    ax.set(title='Dependency Monkey Sort duration from sequence length',
           ylabel='Duration of sorting one list, sec',
           xlabel='Length of list')
    # create boxplots
    ax.boxplot(dur_by_length, patch_artist=True, showfliers=False,
               boxprops=dict(facecolor='yellow', alpha=0.7))
    # create mean line
    ax.plot(mean_line_x, mean_line_y)
    plt.show()


# -----------------------------------------------------------------------------
# Random walk visualisation
def task_3():

    # make random walk
    x = [0]
    y = [0]
    steps = 5000
    for i in range(steps):
        dx = 0
        dy = 0
        direction = random.randint(1, 4)
        if direction == 1:
            dx = -1
        elif direction == 2:
            dx = +1
        elif direction == 3:
            dy = -1
        elif direction == 4:
            dy = +1
        # make next step
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)

    # draw diagram
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)
    ax.set(title='Random walk visualisation',
           ylabel='Y-axis',
           xlabel='X-axis')
    plt.scatter(x, y, alpha=0.3)
    plt.show()


# -----------------------------------------------------------------------------
# Sierpiński triangle
def task_4():

    # make random walk by half-distance-step between current point
    # and random choosed attractor

    # initial state
    max_x = 1000
    max_y = 1000
    angle_num = 3
    shape_x = [random.randint(-max_x, max_x) for i in range(angle_num)]
    shape_y = [random.randint(-max_y, max_y) for i in range(angle_num)]
    init_x = random.randint(-max_x, max_x)
    init_y = random.randint(-max_y, max_y)

    x = [init_x]
    y = [init_y]
    steps = 10 * 1000
    for i in range(steps):
        # make next step
        attractor = random.randint(0, angle_num - 1)
        att_x = shape_x[attractor]
        att_y = shape_y[attractor]
        x.append((x[-1] + att_x) / 2)
        y.append((y[-1] + att_y) / 2)

    # draw diagram
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)
    ax.set(title='Sierpiński N-angel visualisation',
           ylabel='Y-axis',
           xlabel='X-axis')
    plt.scatter(shape_x, shape_y, alpha=1.0)
    plt.scatter(init_x, init_y, alpha=1.0)
    plt.scatter(x, y, alpha=0.1)
    plt.show()


# -----------------------------------------------------------------------------
# Changing order of letter
def task_5():

    text = 'This is a simple text for test task number five. Can you read it?'
    print(f'  original:  {text}')

    # go through text char by char
    char_lst = list(text)           # work with text as list of characters
    inside_word = False             # inside the word flag
    word_pos = 0                    # start pos of the current word
    pos = 0                         # current pos

    while pos < (len(char_lst) - 1):

        # check bigin of new word
        # print(f'pos={pos}, ch={char_lst[pos]}')
        if not inside_word and char_lst[pos].isalpha():
            # print('  inside')
            inside_word = True
            word_pos = pos

        # check end of current word
        if inside_word and (not char_lst[pos + 1].isalpha() or
                            pos == (len(char_lst) - 2)):
            # print('  outside')
            inside_word = False
            chars = char_lst[word_pos + 1: pos]
            # print(chars)
            indexes = np.arange(word_pos + 1, pos)
            # print(indexes)
            np.random.shuffle(indexes)
            # print(indexes)
            for i in range(len(chars)):
                char_lst[indexes[i]] = chars[i]
            # pos += 1

        pos += 1

    text = "".join(char_lst)
    print(f'  shuffled:  {text}')


# -----------------------------------------------------------------------------
# Additional task:  Sierpiński carpet
def task_6():

    # make random walk by half-distance-step between current point
    # and random choosed attractor

    # initial state
    max_x = 1000
    max_y = 1000

    # set 8 points of square carpet
    attr_num = 8
    shape_x = [-max_x, -max_x, -max_x, 0, 0, max_x, max_x, max_x]
    shape_y = [-max_y, 0, max_y, -max_y, max_y, -max_y, 0, max_y]

    init_x = random.randint(-max_x, max_x)
    init_y = random.randint(-max_y, max_y)

    x = [init_x]
    y = [init_y]
    steps = 20 * 1000
    for i in range(steps):
        # make next step
        attractor = random.randint(0, attr_num - 1)
        att_x = shape_x[attractor]
        att_y = shape_y[attractor]
        x.append((x[-1] + 2 * att_x) / 3)
        y.append((y[-1] + 2 * att_y) / 3)

    # draw diagram
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)
    ax.set(title='Sierpiński N-angel visualisation',
           ylabel='Y-axis',
           xlabel='X-axis')
    plt.scatter(shape_x, shape_y, alpha=1.0)
    plt.scatter(init_x, init_y, alpha=1.0)
    plt.scatter(x, y, alpha=0.1)
    plt.show()


# -----------------------------------------------------------------------------
# Additional task:  Sequensing machine simulator
def task_7():

    # TODO
    return


# -----------------------------------------------------------------------------
def main():

    task_1()
    # task_2()
    # task_3()
    # task_4()
    # task_5()
    # task_6()
    # task_7()


if __name__ == "__main__":

    main()
