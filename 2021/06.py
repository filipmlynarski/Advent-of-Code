import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/06.in').read()
counter = defaultdict(int, Counter(ints(puzzle)))

def solve(mapping, days):
    for _ in range(days):
        new_mapping = defaultdict(int)
        for key, value in mapping.copy().items():
            if key == 0:
                new_mapping[6] += value
                new_mapping[8] += value
            else:
                new_mapping[key-1] += value
        mapping = new_mapping
    return sum(mapping.values())

time_print(solve(counter.copy(), 80))
time_print(solve(counter.copy(), 256))
