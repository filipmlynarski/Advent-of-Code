import sys

sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/07.in').read()
lines = puzzle.splitlines()

pwd = ()
sizes = defaultdict(int)
for line in lines[1:]:
    if line.startswith('$ cd '):
        if (destination := line.split()[-1]) == '..':
            pwd = pwd[:-1]
        else:
            pwd = (*pwd, destination)
    elif line != '$ ls':
        size, name = line.split()
        if size != 'dir':
            for idx in range(len(pwd)+1):
                sizes[pwd[:idx]] += int(size)

time_print(sum(filter(lambda x: x <= 100_000, sizes.values())))
for size in sorted(sizes.values()):
    if 70_000_000 - sizes[()] + size > 30_000_000:
        time_print(size)
        break
