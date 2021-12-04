import sys
sys.dont_write_bytecode = True
from utils import *

part_1 = part_2 = 0
for lines in open('puzzle/06.in').read().split('\n\n'):
    stack = list(map(set, lines.splitlines()))
    part_1 += len(set.union(*stack))
    part_2 += len(set.intersection(*stack))
time_print(part_1)
time_print(part_2)
