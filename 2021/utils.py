import collections
import copy
import functools
import heapq
import itertools
import math
import operator
import re
import sys
import typing
from collections import Counter, defaultdict, deque
from copy import deepcopy
from functools import reduce
from pprint import pprint

# thanks mcpower
sys.setrecursionlimit(100000)
T = typing.TypeVar("T")

def lmap(func, *iterables):
    return list(map(func, *iterables))

def flatten(l):
    return [i for x in l for i in x]


def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"(?:(?<!\d)-)?\d+", s))  # thanks mserrano!

def positive_ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!

def floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))

def positive_floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))

def words(s: str) -> typing.List[str]:
    return re.findall(r"[a-zA-Z]+", s)


def make_hashable(l):
    if isinstance(l, list):
        return tuple(map(make_hashable, l))
    if isinstance(l, dict):
        l = set(l.items())
    if isinstance(l, set):
        return frozenset(map(make_hashable, l))
    return l

def invert_dict(d, single=True):
    out = {}
    if single:
        for k, v in d.items():
            v = make_hashable(v)
            if v in out:
                print("[invert_dict] WARNING WARNING: duplicate key", v)
            out[v] = k
    else:
        for k, v in d.items():
            v = make_hashable(v)
            out.setdefault(v, []).append(k)
    return out


def bisect(f, lo=0, hi=None, eps=1e-9):
    """
    Returns a value x such that f(x) is true.
    Based on the values of f at lo and hi.
    Assert that f(lo) != f(hi).
    """
    lo_bool = f(lo)
    if hi is None:
        offset = 1
        while f(lo+offset) == lo_bool:
            offset *= 2
        hi = lo + offset
    else:
        assert f(hi) != lo_bool
    while hi - lo > eps:
        mid = (hi + lo) / 2
        if f(mid) == lo_bool:
            lo = mid
        else:
            hi = mid
    if lo_bool:
        return lo
    else:
        return hi

def binary_search(f, lo=0, hi=None):
    """
    Returns a value x such that f(x) is true.
    Based on the values of f at lo and hi.
    Assert that f(lo) != f(hi).
    """
    lo_bool = f(lo)
    if hi is None:
        offset = 1
        while f(lo+offset) == lo_bool:
            offset *= 2
        hi = lo + offset
    else:
        assert f(hi) != lo_bool
    best_so_far = lo if lo_bool else hi
    while lo <= hi:
        mid = (hi + lo) // 2
        result = f(mid)
        if result:
            best_so_far = mid
        if result == lo_bool:
            lo = mid + 1
        else:
            hi = mid - 1
    return best_so_far


GRID_DELTA = [[-1, 0], [1, 0], [0, -1], [0, 1]]
OCT_DELTA = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + GRID_DELTA
CHAR_TO_DELTA = {
    "U": [-1, 0],
    "R": [0, 1],
    "D": [1, 0],
    "L": [0, -1],
    "N": [-1, 0],
    "E": [0, 1],
    "S": [1, 0],
    "W": [0, -1],
}
DELTA_TO_UDLR = {
    (-1, 0): "U",
    (0, 1): "R",
    (1, 0): "D",
    (0, -1): "L",
}
DELTA_TO_NESW = {
    (-1, 0): "N",
    (0, 1): "E",
    (1, 0): "S",
    (0, -1): "W",
}


def print_grid(grid):
    for line in grid:
        print(*line, sep="")
def get_neighbours(grid, row, col, deltas, fill=None):
    n, m = len(grid), len(grid[0])
    out = []
    for i, j in deltas:
        p_row, p_col = row+i, col+j
        if 0 <= p_row < n and 0 <= p_col < m:
            out.append(grid[p_row][p_col])
        elif fill is not None:
            out.append(fill)
    return out
def lget(l, i):
    if len(l) == 2: return l[i[0]][i[1]]
    for index in i: l = l[index]
    return l
def lset(l, i, v):
    if len(l) == 2:
        l[i[0]][i[1]] = v
        return
    for index in i[:-1]: l = l[index]
    l[i[-1]] = v

def padd(x, y):
    if len(x) == 2: return [x[0] + y[0], x[1] + y[1]]
    return [a+b for a, b in zip(x, y)]
def pneg(v):
    if len(v) == 2: return [-v[0], -v[1]]
    return [-i for i in v]
def psub(x, y):
    if len(x) == 2: return [x[0] - y[0], x[1] - y[1]]
    return [a-b for a, b in zip(x, y)]
def pmul(m: int, v):
    if len(v) == 2: return [m * v[0], m * v[1]]
    return [m * i for i in v]
def pdot(x, y):
    if len(x) == 2: return x[0] * y[0] + x[1] * y[1]
    return sum(a*b for a, b in zip(x, y))
def pdist1(x, y=None):
    if y is not None: x = psub(x, y)
    if len(x) == 2: return abs(x[0]) + abs(x[1])
    return sum(map(abs, x))
def pdist2sq(x, y=None):
    if y is not None: x = psub(x, y)
    if len(x) == 2: return (x[0] * x[0]) + (x[1] * x[1])
    return sum(i*i for i in x)
def pdist2(v):
    return math.sqrt(pdist2sq(v))

def decor(f):
    import time
    def inner(*args, **kwargs):
        return f(time.time(), *args, **kwargs)
    return inner
time_print = decor(print)

