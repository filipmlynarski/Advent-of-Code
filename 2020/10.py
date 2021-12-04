import sys
sys.dont_write_bytecode = True
from utils import *

from functools import lru_cache

puzzle = sorted(list(map(int, open('puzzle/10.in').read().splitlines())))
puzzle = [0] + puzzle + [puzzle[-1] + 3]

diff = {1: 0, 3: 0}
for num_1, num_2 in zip(puzzle, puzzle[1:]):
    diff[num_2 - num_1] += 1
time_print(diff[1] * diff[3])


@lru_cache(maxsize=len(puzzle))
def explore(num):
    if num == puzzle[-1]:
        return 1
    return sum(explore(num + i) for i in range(1, 4) if num + i in puzzle)


time_print(explore(puzzle[0]))
