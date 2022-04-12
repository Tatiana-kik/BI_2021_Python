# HW6:  Decorators

## 1. Overview

HW6 requests to solve 5 tasks:
1. create decorator that replaces `return-function-value`
   to `time-of-function-execution`;
1. create decorator that logs function calls;
1. create decorator that changes `return-function-value` with requested
   probability;
1. implement `staticmethod` decorator;
1. implement `dataclass` decorator.


All 5 tasks are in main.py python script.

## 2. Requirements

Code was tested on Ubuntu 20.04, Python 3.8.10.
Necessary modules are listed in requirements.txt file.
To install them you need to run `pip install -r requirements.txt`.

## 3. Task 1 - Measure Time Decorator

I created a decorator that replaces return function value to time
of function execution.<br>
Test function is `task_1_test()`.

## 4. Task 2 - Func Loger Decorator

I created a decorator that output next info:
* list of incoming function parameters before the function call;
* type of return value after function call.

Test function is `task_2_test()`.

## 5. Task 3 - Russian Roulette Decorator

I created a decorator that changing the return value with
requested probabilitie.<br>
Test function is `task_3_test()`.

## 6. Task 4 - StaticMethod Decorator

I created a decorator that works as standart `staticmethod` decorator -
allows to call decorated function with and without object.<br>
Test function is `task_4_test()`.

## 7. Task 8 - DataClass Decorator

I created a decorator that works as standart `dataclass` decorator:
* create class data fields according to class annotation;
* create methods `__init__()` and `__repr__`.

Test function is `task_5_test()`.

## 8. Execution

To execute you need to run script `main.py` as a single file application
`python main.py`:

* To run demonstration of work task1 - uncomment line `task1_test()` at the bottom of file.
* To run demonstration of work task2 - uncomment line `task2_test()` at the bottom of file.
* To run demonstration of work task3 - uncomment line `task3_test()` at the bottom of file.
* To run demonstration of work task4 - uncomment line `task4_test()` at the bottom of file.
* To run demonstration of work task5 - uncomment line `task5_test()` at the bottom of file.