import sys
sys.dont_write_bytecode = True
from utils import *


puzzle = open('puzzle/04.in').read().splitlines()
guards = defaultdict(lambda: defaultdict(int))

current = None
falls = None
for line in sorted(puzzle):
    *_, value = ints(line)
    if 'Guard' in line:
        current = value
    elif 'falls' in line:
        falls = value
    else:
        for minute in range(falls, value + 1):
            guards[current][minute] += 1

guard = max(guards, key=lambda id_: sum(guards[id_].values()))
print(guard * max(guards[guard], key=guards[guard].__getitem__))
guard = max(guards, key=lambda id_: max(guards[id_].values()))
print(guard * max(guards[guard], key=guards[guard].__getitem__))
