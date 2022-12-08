import sys

sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/08.in').read()
lines = [[int(tree) for tree in line] for line in puzzle.splitlines()]


def first_not_smaller(val: int, lst: list[int]) -> int:
    for idx, cmp in enumerate(lst, 1):
        if cmp >= val:
            return idx
    return len(lst)


part_1 = part_2 = 0
for row, line in enumerate(lines):
    for col, tree in enumerate(line):
        tree_rows = [
            [line[x2] for x2 in range(col)][::-1],
            [line[x2] for x2 in range(col+1, len(line))],
            [lines[y2][col] for y2 in range(row)][::-1],
            [lines[y2][col] for y2 in range(row+1, len(lines))],
        ]
        score = reduce(int.__mul__, (first_not_smaller(tree, tree_row) for tree_row in tree_rows))
        part_2 = max(part_2, score)

        if row in {0, len(lines)-1} or col in {0, len(line)-1}:
            part_1 += 1
        else:
            part_1 += min(map(max, tree_rows)) < tree

time_print(part_1)
time_print(part_2)
