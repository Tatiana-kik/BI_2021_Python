import functional as fu
import numpy as np

# tests for task 1 and 1*
if 1:
    print(fu.sequential_map(np.square,
                            np.sqrt,
                            lambda x: x**3,
                            [1, 2, 3, 4, 5]))

    print(fu.sequential_map_2(np.square,
                              np.sqrt,
                              lambda x: x**3,
                              [1, 2, 3, 4, 5]))

# tests for task 2
if 0:
    print(fu.consensus_filter(lambda x: x > 0,
                              lambda x: x > 5,
                              lambda x: x < 10,
                              [-2, 0, 4, 6, 11]))

# tests for task 3
if 0:
    print(fu.conditional_reduce(lambda x: x < 5,
                                lambda x, y: x + y,
                                [1, 3, 5, 10]))

    print(fu.conditional_reduce(lambda x: x.isalpha(),
                                lambda x, y: x + y,
                                ['a', '3', 'b', '10', 'c']))

    print(fu.conditional_reduce(lambda x: x.isalpha(),
                                lambda x, y: x + y,
                                []))

    print(fu.conditional_reduce(lambda x: len(x) < 4,
                                lambda x, y: x + y,
                                [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10]]))

# tests for task 4
if 0:
    my_chain = fu.func_chain(lambda x: x + 2, np.square)
    print(my_chain(4))

    my_chain = fu.func_chain(lambda x: x + 2,
                             lambda x: (x/4, x//4))
    print(my_chain(37))

    my_chain = fu.func_chain(lambda x: x + 'b cd',
                             lambda x: x.split())
    print(my_chain('a'))

# tests for task 5
if 0:
    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(arr)
    print(f'orig mean():        {np.mean(arr)}')
    print(f'orig mean(axis=1):  {np.mean(arr, axis=1)}')
    print(f'orig max(axis=1):   {np.max(arr, axis=1)}')
    print(f'orig sum(axis=1):   {np.sum(arr, axis=1)}')

    ax1_mean, ax1_max, ax1_sum = \
        fu.multiple_partial(np.mean, np.max, np.sum, axis=1)
    print(f'ax1_mean():         {ax1_mean(arr)}')
    print(f'ax1_max():          {ax1_max(arr)}')
    print(f'ax1_sum():          {ax1_sum(arr)}')

    res_arr = np.array([0, 0, 0])
    ax1_out_mean, ax1_out_max, ax1_out_sum = \
        fu.multiple_partial(np.mean, np.max, np.sum, axis=1, out=res_arr)
    ax1_out_mean(arr)
    print(f'ax1_mean():         {res_arr}')
    ax1_out_max(arr)
    print(f'ax1_max():          {res_arr}')
    ax1_out_sum(arr)
    print(f'ax1_sum():          {res_arr}')
