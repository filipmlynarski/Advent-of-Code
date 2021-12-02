import sys
sys.dont_write_bytecode = True
from utils import *


puzzle = open('puzzle/03.in').read().splitlines()
grid = defaultdict(int)
for line in puzzle:
    _, row, col, height, width = ints(line)
    for y in range(row, row+height):
        for x in range(col, col+width):
            grid[(y, x)] += 1
print(sum(val > 1 for val in grid.values()))

for line in puzzle:
    id_, row, col, height, width = ints(line)
    for cord in itertools.product(range(row, row+height), range(col, col+width)):
        if grid[cord] != 1:
            break
    else:
        print(id_)
        break
