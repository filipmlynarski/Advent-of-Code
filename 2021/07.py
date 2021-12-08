import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/07.in').read()
crabs = sorted(ints(puzzle))
mid_crab = crabs[len(crabs) // 2]
time_print(sum(abs(mid_crab - crab) for crab in crabs))

def fuel(dist):
    return dist * (dist + 1) // 2

part_2 = sum(fuel(abs(crabs[0] - crab)) for crab in crabs)
for candidate in range(crabs[0]+1, crabs[-1]+1):
    part_2 = min(part_2, sum(fuel(abs(candidate - crab)) for crab in crabs))
time_print(part_2)
