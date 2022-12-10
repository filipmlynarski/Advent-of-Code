import sys

sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/10.in').read()
lines = puzzle.splitlines()

cycle = 0
part_1 = 0
x = 1
grid = []
for line in lines:
    noop = line == 'noop'
    for _ in range(1 if noop else 2):
        cycle += 1
        if abs((len(grid) % 40) - x) < 2:
            grid.append('#')
        else:
            grid.append('.')
        if (cycle - 20) % 40 == 0:
            part_1 += x * cycle
    if noop:
        continue
    val = int(line.split()[-1])
    x += val

time_print(part_1)
part_2 = []
for idx, i in enumerate(grid):
    if idx % 40 == 0:
        part_2.append([])
    part_2[-1].append(i)
time_print('\n' + '\n'.join(''.join(line) for line in part_2))
