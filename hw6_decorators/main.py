'''
Homework #6 - Decorators
'''

import time
import requests
import random


# #############################################################################
# Task 1:  Measure time decorator.
# #############################################################################

def measure_time(func):
    '''
    A simple decorator replacing the func-return-value by
    duration-of-func-execution.
    '''
    def inner_func(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        return t2 - t1
    return inner_func


@measure_time
def some_function(a, b, c, d, e=0, f=2, g='3'):
    '''
    Example of using of decorator according to Example_1.
    '''
    time.sleep(a)
    time.sleep(b)
    time.sleep(c)
    time.sleep(d)
    time.sleep(e)
    time.sleep(f)
    return g


def task_1_test():
    '''
    Task 1 test function according to Example_1.
    Expected output is around 21 (1 + 2 + 3 + 4 + 5 + 6).
    '''
    res = some_function(1, 2, 3, 4, e=5, f=6, g='99999')
    print(res)


# #############################################################################
# Task 2:  Function logging.
# #############################################################################

def function_logging(func):
    '''
    A decorator logging function call.
    '''
    def inner_func(*args, **kwargs):
        # print info about incomming arguments
        fname = func.__name__
        kwargs_str = ', '.join(['{}={!r}'.format(k, v)
                                for k, v in kwargs.items()])
        if not args and not kwargs:
            print(f'Function {fname} is called with no arguments.')
        elif args and not kwargs:
            print(f'Function {fname} is called with positional '
                  f'arguments: {args}.')
        elif not args and kwargs:
            print(f'Function {fname} is called with keyword '
                  f'arguments: {kwargs_str}.')
        elif args and kwargs:
            print(f'Function {fname} is called with positional '
                  f'arguments: {args} and keyword arguments: {kwargs_str}.')
        # call the function
        res = func(*args, **kwargs)
        # print info about incoming result value
        res_type = type(res).__name__
        print(f'Function {fname} returned output of type {res_type}.')
        return res
    return inner_func


@function_logging
def func1():
    return set()


@function_logging
def func2(a, b, c):
    return (a + b) / c


@function_logging
def func3(a, b, c, d):
    return [a + b * c] * d


@function_logging
def func4(a=None, b=None):
    return {a: b}


def task_2_test():
    '''
    Task 2 test function according to Example_2.
    '''
    print(func1(), end='\n\n')
    print(func2(1, 2, 3), end='\n\n')
    print(func3(1, 2, c=3, d=2), end='\n\n')
    print(func4(a=None, b=float('-inf')), end='\n\n')


# #############################################################################
# Task 3:  Russian roulette.
# #############################################################################

def russian_roulette_decorator(probability, return_value):
    '''
    Decorator specification.
    '''
    def decorator(func):
        '''
        Decorator function.
        '''
        def inner_func(*args, **kwargs):
            '''
            Replace output value with probability.
            '''
            if random.random() < probability:
                return return_value
            return func(*args, **kwargs)
        return inner_func
    return decorator


@russian_roulette_decorator(probability=0.2,
                            return_value='Ooops, your output has been stolen!')
def make_request(url):
    '''
    Decorated function.
    '''
    return requests.get(url)


def task_3_test():
    '''
    Task 3 test function according to Examples_3.pdf.
    '''
    for _ in range(10):
        print(make_request('https://google.com'))


# #############################################################################
# Task 4 (additional):  staticmethod implementation.
# #############################################################################

class MyStaticMethod:
    '''
    Decorator to make member method as static method.
    Using the non-data descriptor protocol.
    https://docs.python.org/3/howto/descriptor.html#static-methods
    '''
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, objtype=None):
        return self.f

    def __call__(self, *args, **kwds):
        return self.f(*args, **kwds)


def task_4_test():
    '''
    Task 4 test function.
    '''
    class Math:
        '''
        Example of a claass with method, that decorated by MyStaticMethod.
        '''
        @MyStaticMethod
        def mul10(x):
            return x * 10

    # check that we can call function mul10() from class and from object
    print(Math.mul10(3))    # without creating a object
    print(Math().mul10(3))  # with creating a object


# #############################################################################
# Task 5 (additional):  dataclass implementation.
# #############################################################################

class MISSING_VALUE_TYPE:
    '''
    Special type to mark missing value.
    '''
    pass


# missing value marker
MISSING = MISSING_VALUE_TYPE()


class Field:
    '''
    A class that stores class field.
    '''
    def __init__(self, default, name, type):
        self.default = default
        self.name = name
        self.type = type


def create_func(name, args, body, variables, return_type):
    '''
    This function dynamically create python program from text
    according to incommint parameters.
    '''
    # prepare annotation for return value
    return_annotation = ''
    if return_type is not MISSING:
        variables['_return_type'] = return_type
        return_annotation = '->_return_type'

    # prepare args string with comma separation
    args = ','.join(args)

    # prepare function body with new-line separation
    body = '\n'.join(f'  {b}' for b in body)

    # assemble func text
    func_txt = f' def {name}({args}){return_annotation}:\n{body}'

    # prepare variable string
    local_vars = ', '.join(variables.keys())

    # assemble all togethe
    full_txt = f'def __create_fn__({local_vars}):\n{func_txt}\n return {name}'

    # execute python code and return created function object
    ns = {}
    exec(full_txt, None, ns)
    return ns['__create_fn__'](**variables)


def create_init_func(fields):
    '''
    Create func text and func object for class constructor
    according to class fields.
    Return:  func __init__()
    '''

    variables = {f'_type_{f.name}': f.type for f in fields}

    # create func body text
    body_lines = []
    for f in fields:
        if f.default is not MISSING:
            variables[f'_dflt_{f.name}'] = f.default
        line = f'self.{f.name}={f.name}'
        body_lines.append(line)

    # create func parameters line
    init_params_lines = []
    for f in fields:
        defval = '' if f.default is MISSING else f'=_dflt_{f.name}'
        line = f'{f.name}:_type_{f.name}{defval}'
        init_params_lines.append(line)

    # create func object according to text
    return create_func('__init__',
                       ['self'] + init_params_lines,
                       body_lines,
                       variables,
                       return_type=None)


def create_repr_func(fields):
    '''
    Create func text and func object for __repr__() function
    according to class fields.
    Return:  func __repr__()
    '''

    # create func body text
    body_line = ''
    body_line += 'return self.__class__.__qualname__ + f"('
    body_line += ', '.join([f"{f.name}={{self.{f.name}!r}}" for f in fields])
    body_line += ')"'

    # create func object according to text
    fn = create_func('__repr__',
                     ('self',),
                     [body_line],
                     variables={},
                     return_type=MISSING)
    return fn


def mydataclass(cls):
    '''
    A decorator that returns modified class:
        * added data fields according to annotation
        * add constructor
        * add __repr__() method
    '''

    # get class fields from class annotation
    cls_annotations = cls.__dict__.get('__annotations__', {})
    cls_fields = []
    for name, type in cls_annotations.items():
        defval = getattr(cls, name, MISSING)
        f = Field(defval, name, type)
        cls_fields.append(f)

    # add __init__()
    setattr(cls, '__init__', create_init_func(cls_fields))

    # add __repr__
    setattr(cls, '__repr__', create_repr_func(cls_fields))

    return cls


def task_5_test():
    '''
    Task 5 test function.
    '''
    @mydataclass
    class User:
        name: str
        age: int
        iq: int = 100

    # create objects with and without default value of 'iq'
    user1 = User('Иван', 22, iq=99)
    user2 = User('Петр', 33)

    # check printing of object
    print(user1)
    print(user2)
    print(user1 == user2)

    # show annotation for class aud for constructor
    print(User.__annotations__)
    print(User.__init__.__annotations__)


# Examples of using:  uncomment needed function and execute it.
if __name__ == "__main__":

    task_1_test()
    # task_2_test()
    # task_3_test()
    # task_4_test()
    # task_5_test()
