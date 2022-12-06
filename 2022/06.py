import sys

sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/06.in').read()

part_1 = False
for idx in range(4, len(puzzle)):
    if not part_1 and len(set(puzzle[idx-4: idx])) == 4:
        part_1 = True
        time_print(idx)
    if idx > 13 and len(set(puzzle[idx-14: idx])) == 14:
        time_print(idx)
        break
