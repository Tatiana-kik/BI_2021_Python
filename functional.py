###############################################################################
#
#  Homework for Functional Programming
#
###############################################################################


# -----------------------------------------------------------------------------
# task 1
def sequential_map(*args):

    cont = args[-1]
    funcs = args[:-1]
    for f in funcs:
        cont = list(map(f, cont))
    return cont


# -----------------------------------------------------------------------------
# task 2
def consensus_filter(*args):

    cont = args[-1]
    funcs = args[:-1]
    for f in funcs:
        cont = list(filter(f, cont))
    return cont


# -----------------------------------------------------------------------------
# task 3
def conditional_reduce(func_filter, func_reduce, cont):

    cont = list(filter(func_filter, cont))

    if not len(cont):
        return None

    reduced = cont[0]
    for i in range(1, len(cont)):
        reduced = func_reduce(reduced, cont[i])

    return reduced


# -----------------------------------------------------------------------------
# task 4
def func_chain(*args):

    if not len(args):
        return None

    funcs = args
    res = 0

    # below I solve the task by 2 ways:
    #  1.  by re-using function conditional_reduce() from taske 3
    #  2.  by creating new lambda function
    if 0:
        # WAY #1:
        #   let's re-use function conditional_reduce() from task 3:
        #     filter func - return always True
        #     reduce func - get 2 args A and F and call F(A)
        #     container   - first element is inc param, and next are functions
        return lambda v: conditional_reduce(lambda x: True,
                                            lambda a, f: f(a),
                                            [v] + list(funcs))
    else:
        # WAY #2
        #   let's create new chained lambda function by chain new functions
        #   one by one in cycle

        # to avoid flake8 error
        # "E731 do not assign a lambda expression, use a def"
        # I use workaround - wraper() function just to wrap lambda
        def wraper(x): return x

        res = wraper(lambda a, f=funcs[0]:  f(a))
        for i in range(1, len(funcs)):
            res = wraper(lambda a, f=funcs[i], fn=res: f(fn(a)))

    return res


# -----------------------------------------------------------------------------
# task 1* - additional task for +2 points:  using func_chain()
def sequential_map_2(*args):

    cont = args[-1]
    funcs = args[:-1]

    fn_chain = func_chain(*funcs)
    cont = list(map(fn_chain, cont))
    return cont


# -----------------------------------------------------------------------------
# task 5 - additional task for +5 points
def multiple_partial(*args, **kwargs):

    funcs = args
    params = kwargs

    res = []
    for i in range(len(funcs)):
        res.append(lambda pos_args, f=funcs[i]:  f(pos_args, **params))

    return res
