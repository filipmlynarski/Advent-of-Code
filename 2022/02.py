import sys

sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/02.in').read()
lines = puzzle.splitlines()

part_1 = part_2 = 0
a = ['A', 'B', 'C']
b = ['X', 'Y', 'Z']
for line in lines:
    him, me = line.split()
    a_idx, b_idx = a.index(him), b.index(me)

    part_1 += b_idx + 1
    if a_idx == b_idx:
        part_1 += 3
    elif (a_idx + 1) % 3 == b_idx:
        part_1 += 6

    if b_idx == 0:
        part_2 += (a_idx - 1) % 3 + 1
    elif b_idx == 1:
        part_2 += a_idx + 1 + 3
    elif b_idx == 2:
        part_2 += (a_idx + 1) % 3 + 1 + 6

time_print(part_1)
time_print(part_2)
