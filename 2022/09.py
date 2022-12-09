import sys
from typing import Generator

sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/09.in').read()
lines = puzzle.splitlines()
dir_to_delta = {
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
    'U': (-1, 0),
}
Cord = tuple[int, int]


def get_delta(cord_a: Cord, cord_b: Cord) -> Cord:
    y_dist, x_dist = psub(cord_b, cord_a)
    if abs(y_dist) > 1 or abs(x_dist) > 1:
        if y_dist == 0:
            return 0, 1 if x_dist > 0 else -1
        elif x_dist == 0:
            return 1 if y_dist > 0 else -1, 0
        return 1 if y_dist > 0 else -1, 1 if x_dist > 0 else -1
    return 0, 0


def yield_tail_path(length: int) -> Generator[Cord, None, None]:
    snake: list[Cord] = [(0, 0) for _ in range(length)]
    for line in lines:
        direction, steps = line.split()
        head_delta = dir_to_delta[direction]
        for _ in range(int(steps)):
            snake[-1] = padd(snake[-1], head_delta)
            for idx in range(len(snake)-1):
                delta = get_delta(snake[~idx-1], snake[~idx])
                snake[~idx-1] = padd(snake[~idx-1], delta)
            yield snake[0]


time_print(len(set(yield_tail_path(2))))
time_print(len(set(yield_tail_path(10))))
