import sys

sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/10.in').read()
part_1, part_2, cycle, x = 0, [], 0, 1
for line in puzzle.splitlines():
    for _ in range(1 if line == 'noop' else 2):
        cycle += 1
        part_2.append('#' if abs((len(part_2) % 40) - x) < 2 else '.')
        if (cycle - 20) % 40 == 0:
            part_1 += x * cycle
    if line != 'noop':
        x += int(line.split()[-1])

time_print(part_1)
time_print('\n' + '\n'.join(''.join(line) for line in chunked(part_2, 40)))
