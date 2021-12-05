import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/05.in').read()

grid_1 = defaultdict(int)
grid_2 = defaultdict(int)
for line in puzzle.splitlines():
    x1, y1, x2, y2 = ints(line)
    (min_y, max_y), (min_x, max_x) = min_max([y1, y2]), min_max([x1, x2])
    if x1 != x2 and y1 != y2:
        delta = 1 if min_y == y1 else -1, 1 if min_x == x1 else -1
        cord = (y1, x1)
        for _ in range(min_y, max_y + 1):
            grid_2[cord] += 1
            cord = padd(cord, delta)
    else:
        for cord in itertools.product(range(min_y, max_y + 1), range(min_x, max_x + 1)):
            grid_1[cord] += 1
            grid_2[cord] += 1

time_print(sum(1 for val in grid_1.values() if val > 1))
time_print(sum(1 for val in grid_2.values() if val > 1))
