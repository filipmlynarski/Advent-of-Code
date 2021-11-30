import sys
sys.dont_write_bytecode = True
from utils import *
"""
Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words
Data structures:
Linked, UnionFind
dict: d.keys(), d.values(), d.items()
deque: q[0], q.append and q.popleft
List/Vector operations:
GRID_DELTA, OCT_DELTA
lget, lset, fst, snd
padd, pneg, psub, pmul, pdot, pdist1, pdist2sq, pdist2
Matrices:
matmat, matvec, matexp
binary_search(lambda x: x > 90000000000)  # -> 90000000001
"""

puzzle = open('puzzle/01.in').read()
all_ints = ints(puzzle)
lines = puzzle.splitlines()
lines_ints = lmap(ints, lines)

ans = None
for line in lines:
    print(ints(line))

print(ans)
