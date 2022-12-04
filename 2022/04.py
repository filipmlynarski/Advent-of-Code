import sys

sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/04.in').read()
lines = puzzle.splitlines()
try:
    ints = get_ints(puzzle)
except:
    ints = []
try:
    words = get_words(puzzle)
except:
    words = []

# print(f'lines = {format_list(lines)}')
# print(f'ints = {format_list(ints)}')
# print(f'words = {format_list(words)}')

part_1 = part_2 = 0
for line in lines:
    a1, a2, b1, b2 = get_ints(line)
    a = set(range(a1, a2+1))
    b = set(range(b1, b2+1))
    part_1 += a.issubset(b) or b.issubset(a)
    part_2 += bool(a & b)

time_print(part_1)
time_print(part_2)
