import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = list(map(int, open('puzzle/01.in').read().splitlines()))


def f(x):
    return x // 3 - 2


def f2(x):
    x = f(x)
    if x <= 0:
        return 0
    return x + f2(x)


time_print(sum(map(f, puzzle)))
time_print(sum(map(f2, puzzle)))
