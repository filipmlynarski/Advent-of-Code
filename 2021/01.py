import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/01.in').read()
all_ints = ints(puzzle)

part_1 = 0
part_2 = 0
for idx in range(len(all_ints) - 1):
    part_1 += all_ints[idx] < all_ints[idx + 1]
    if idx < len(all_ints) - 2:
        part_2 += sum(all_ints[idx:idx+3]) < sum(all_ints[idx+1:idx+4])

print(part_1)
print(part_2)
